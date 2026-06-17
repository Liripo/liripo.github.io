#!/usr/bin/env python3
"""
fastq_bc.py —— 基于 cutadapt 并行框架的 FASTQ Barcode 校正工具

利用 cutadapt 内置的 SingleEndPipeline / make_runner / OutputFiles 等模块，
实现多进程并行读取、处理和写回 FASTQ，无需自己管理进程池或数据分发。

用法:
    python fastq_bc.py input.fastq.gz -w whitelist.txt -o output.fastq.gz
    python fastq_bc.py input.fastq.gz -w whitelist.txt -o output.fastq.gz -c 4

需要安装:
    pip install cutadapt dnaio typer levenshtein
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, Dict, List, Tuple

import typer
from typing_extensions import Annotated

from dnaio import SequenceRecord

from cutadapt.modifiers import SingleEndModifier
from cutadapt.steps import SingleEndStep, SingleEndSink
from cutadapt.pipeline import SingleEndPipeline
from cutadapt.runners import make_runner
from cutadapt.files import InputPaths, OutputFiles, FileOpener
from cutadapt.utils import available_cpu_count, DummyProgress
from cutadapt.info import ModificationInfo

import Levenshtein

app = typer.Typer(
    name="fastq-bc",
    help="并行 FASTQ barcode 校正工具 (基于 cutadapt 框架)",
    no_args_is_help=True,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Barcode 校正核心：k-mer 索引 + Hamming 距离（参考 PISA/sim_search.c）
# ---------------------------------------------------------------------------

class BarcodeCorrector:
    """
    基于 k-mer 索引的 barcode 校正器。

    构建阶段：对白名单中每条 barcode 提取 k-mer，建立 k-mer -> barcode 集合的反向索引。
    查询阶段：从 query barcode 提取 k-mer，召回候选 barcode，逐一计算 Hamming 距离，
             仅接受唯一命中且距离 <= max_dist 的结果（多命中返回 NULL，避免歧义校正）。

    参考：PISA (https://github.com/shienex/PISA) src/sim_search.c
    """

    def __init__(self, whitelist: List[str], k: int = 5, max_dist: int = 1):
        self.k = k
        self.max_dist = max_dist
        self.whitelist = set(whitelist)
        # k-mer -> set of barcode indices
        self.index: Dict[str, set] = defaultdict(set)
        self._build_index()

    def _build_index(self):
        for i, barcode in enumerate(self.whitelist):
            for j in range(len(barcode) - self.k + 1):
                kmer = barcode[j : j + self.k]
                self.index[kmer].add(i)

    def correct(self, query: str) -> Optional[str]:
        """
        校正 query barcode。返回校正后的 barcode 或 None（歧义/无命中）。
        """
        # 先检查精确匹配
        if query in self.whitelist:
            return query

        if len(query) < self.k:
            return None

        # 通过 k-mer 召回候选
        candidates: set = set()
        for j in range(len(query) - self.k + 1):
            kmer = query[j : j + self.k]
            if kmer in self.index:
                candidates.update(self.index[kmer])

        if not candidates:
            return None

        # 计算 Hamming 距离，取唯一命中
        whitelist_list = list(self.whitelist)
        best_dist = self.max_dist + 1
        best_barcode: Optional[str] = None
        for idx in candidates:
            barcode = whitelist_list[idx]
            dist = Levenshtein.hamming(query, barcode)
            if dist < best_dist:
                best_dist = dist
                best_barcode = barcode
            elif dist == best_dist:
                # 多个候选距离相同，歧义校正
                best_barcode = None

        return best_barcode


# ---------------------------------------------------------------------------
# cutadapt Modifier：将 barcode 校正逻辑封装为 SingleEndModifier
# ---------------------------------------------------------------------------

class BarcodeCorrectorModifier(SingleEndModifier):
    """
    SingleEndModifier：在 pipeline 中对每条 read 执行 barcode 校正。

    校正发生在 read 的前 N 个碱基（N = barcode 长度）。
    校正成功则替换前 N 个碱基，失败则保留原序列。
    在 read name 上附加 CR:Z（原始 barcode）和 CB:Z（校正后 barcode）标签，
    格式参考 PISA（||| 分隔）。无校正时 CB 为空。
    """

    def __init__(self, corrector: BarcodeCorrector, barcode_length: int):
        self.corrector = corrector
        self.barcode_length = barcode_length
        self.corrected = 0
        self.total = 0

    def __repr__(self):
        return (
            f"BarcodeCorrectorModifier("
            f"barcode_length={self.barcode_length}, "
            f"max_dist={self.corrector.max_dist})"
        )

    def __call__(self, read: SequenceRecord, info: ModificationInfo) -> SequenceRecord:
        self.total += 1
        bl = self.barcode_length
        barcode = read.sequence[:bl]

        corrected = self.corrector.correct(barcode)
        if corrected is not None and corrected != barcode:
            self.corrected += 1
            new_seq = corrected + read.sequence[bl:]
            read = SequenceRecord(read.name, new_seq, read.qualities)

        corr_tag = corrected if (corrected is not None and corrected != barcode) else ""
        read = SequenceRecord(
            f"{read.name}|||CR:Z:{barcode}|||CB:Z:{corr_tag}",
            read.sequence, read.qualities,
        )
        return read


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@app.command()
def main(
    input_files: Annotated[
        list[Path],
        typer.Argument(help="输入 FASTQ 文件路径（支持 .gz）"),
    ],
    whitelist: Annotated[
        Path,
        typer.Option("-w", "--whitelist", help="barcode 白名单文件，每行一条"),
    ],
    output: Annotated[
        Optional[Path],
        typer.Option("-o", "--output", help="输出 FASTQ 文件路径"),
    ] = None,
    cores: Annotated[
        int,
        typer.Option("-c", "--cores", help="并行进程数（默认使用全部 CPU 核心）"),
    ] = 0,
    barcode_length: Annotated[
        int,
        typer.Option("-l", "--barcode-length", help="barcode 长度（默认自动检测）"),
    ] = 0,
    max_dist: Annotated[
        int,
        typer.Option("-d", "--max-dist", help="最大允许 Hamming 距离（默认 1）"),
    ] = 1,
    kmer_size: Annotated[
        int,
        typer.Option("-k", "--kmer-size", help="k-mer 索引的 k 值（默认 5）"),
    ] = 5,
    compression_level: Annotated[
        int,
        typer.Option("--compression-level", help="gzip 压缩等级 1-9（默认 1，最快）"),
    ] = 1,
    verbose: Annotated[
        bool,
        typer.Option("-v", "--verbose", help="打印详细日志"),
    ] = False,
):
    """
    并行 FASTQ barcode 校正。

    使用 cutadapt 的多进程框架 (SingleEndPipeline + make_runner) 实现高效并行处理，
    基于 k-mer 索引的 barcode 校正算法快速纠正测序错误。
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    # ---- 读取白名单 ----
    if not whitelist.exists():
        logger.error(f"白名单文件不存在: {whitelist}")
        raise typer.Exit(1)

    with open(whitelist, "r", encoding="utf-8") as f:
        barcodes = [line.strip() for line in f if line.strip()]

    if not barcodes:
        logger.error("白名单为空")
        raise typer.Exit(1)

    # 自动检测 barcode 长度
    if barcode_length == 0:
        barcode_length = len(barcodes[0])
        logger.info(f"自动检测 barcode 长度: {barcode_length}")
    else:
        logger.info(f"barcode 长度: {barcode_length}")

    # 验证白名单 barcode 长度一致
    lengths = set(len(b) for b in barcodes)
    if len(lengths) != 1:
        logger.error(f"白名单中 barcode 长度不一致: {lengths}")
        raise typer.Exit(1)
    if list(lengths)[0] != barcode_length:
        logger.error(f"白名单 barcode 长度 ({list(lengths)[0]}) 与指定长度 ({barcode_length}) 不一致")
        raise typer.Exit(1)

    # ---- 构建校正器 ----
    corrector = BarcodeCorrector(barcodes, k=kmer_size, max_dist=max_dist)
    logger.info(
        f"白名单: {len(barcodes)} 条 barcode, "
        f"k-mer={kmer_size}, max_dist={max_dist}"
    )

    # ---- 设置并行参数 ----
    if cores == 0:
        cores = available_cpu_count()
    if cores < 1:
        cores = 1
    logger.info(f"使用 {cores} 个进程")

    # ---- 构建 cutadapt pipeline ----
    file_opener = FileOpener(
        compression_level=compression_level,
        threads=max(1, cores // 2),
    )

    # 输入路径
    input_paths = InputPaths(*[str(p) for p in input_files], interleaved=False)

    # 输出路径
    if output is None:
        output_path = "-"
    else:
        output_path = str(output)

    with make_runner(input_paths, cores) as runner:
        # OutputFiles: proxied=True 在多进程模式下使用 ProxyRecordWriter
        outfiles = OutputFiles(
            proxied=cores > 1,
            qualities=runner.input_file_format().has_qualities(),
            file_opener=file_opener,
            interleaved=False,
        )

        # 获取 record writer
        if output_path == "-":
            writer = outfiles.open_stdout_record_writer(interleaved=False)
        else:
            writer = outfiles.open_record_writer(output_path, force_fasta=False)

        # modifier: barcode 校正
        bc_modifier = BarcodeCorrectorModifier(corrector, barcode_length)

        # sink: 写入输出
        sink = SingleEndSink(writer)

        # 组装 pipeline: modifier -> sink
        pipeline = SingleEndPipeline(modifiers=[bc_modifier], steps=[sink])

        # 运行
        progress = DummyProgress()
        stats = runner.run(pipeline, progress, outfiles)

    # ---- 输出统计 ----
    total_reads = bc_modifier.total
    corrected_reads = bc_modifier.corrected
    if total_reads > 0:
        rate = corrected_reads / total_reads * 100
        logger.info(
            f"处理完成: {total_reads} 条 reads, "
            f"校正 {corrected_reads} 条 ({rate:.2f}%)"
        )
    else:
        logger.info("处理完成，无 reads")


if __name__ == "__main__":
    app()
