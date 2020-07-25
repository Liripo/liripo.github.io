---
title: samtools使用
date: 2019-12-17 21:19:12
tags: 生信基础工具
---
> samtools是一个用于操作sam和bam文件的工具合集。sam为bam文件的十进制文件；bam为二进制文件。

<!--more-->

# View

作用：bam与sam互转，查看bam文件，对bam进行排序和提取的操作。
- sam与bam互转:-S指定输入文件格式为sam，不加则为bam,-b指定输出格式(默认输出sam)
```bash
samtools view -Sb SRR3589956.sam >SRR3589956.bam #重定向符也可以换成-o参数
samtools view -h SRR3589956.bam > SRR3589956.sam #-h置输出sam时带上头注释信息
```
- 过滤功能-F：后接flag数字，常用有4（表示序列没比对上）、8（配对的另一条序列，即mate序列没比对上）以及12（两条序列都没比对上）。加上-F就表示过滤掉这些情况
```bash
#提取一条reads比对到参考序列上的序列结果
samtools view -bF4 abc.bam>abc.F4.bam
#提取两条reads都比对到参考序列上的序列结果
samtools view -bF12 abc.bam>abc.F12.bam
```
反之-f，就是提取指定flag的序列.当然还有其它参数，详情请--help

# sort
作用：对bam进行排序，一些软件需要使用排序后的bam，拿到bam先按照比对位置的顺序排一下，百利无一害。
Usage: samtools sort [-n] [-m <maxMem>] <in.bam> <out.prefix> 
-m 参数默认下是 500,000,000 即500M。每个线程运行内存大小。
-n 设定排序方式按short reads的ID排序。默认下是按序列在fasta文件中的顺序（即header）和序列从左往右的位点排序。
-@：设置排序和压缩的线程数，默认单线程
`samtools sort -@ 10 -o abc.sorted.bam abc.bam`
# merge
作用：将两个及以上的sort过的bam文件融合成一个bam文件,融合后的文件不需要则是已经sort过了的。
Usage:   samtools merge [-nr] [-h inh.sam] <out.bam> <in1.bam> <in2.bam>[...]
# index
作用：对bam文件构建索引，产生.bai文件，方便以后的快速处理；bam文件进行排序sort后，才能进行index，否则报错；要显示比对结果时，比如用IGV导入bam，就需要有.bai的存在
```bash
samtools index abc.bam
```
**当有多个bam文件时，一般思路就是对每一个bam进行sort、index后，再merge成一个整体merged.bam，然后对merged.bam再进行sort、index，才算能用了，得到最终结果应该是是sorted.merge.bam**
# faidx
作用：对fasta文件建立提取索引，索引文件后缀是.fai。利用索引文件可以快速提取fasta文件中的某些序列
```bash
samtools faidx hg19.fasta
```
# tview
作用：直观显示reads比对到基因组的情况，与IGV类似需要先sort和index
```bash
samtools tview abc.sorted.bam hg19.fasta
```
# flagstat
作用：统计bam文件的比对结果
```bash
samtools flagstat abc.sorted.bam > abc.sorted.flagstat.txt
```
# depth
作用：统计每个碱基位点的测序深度;需要使用重定向定义输出文件；要使用构建过索引的bam
Usage: bam2depth [-r reg] [-q baseQthres] [-Q mapQthres] [-b in.bed] <in1.bam> [...]
-r：（region）加染色体号；
-q：要求测序碱基质量最低值；
-Q：要求比对的质量最低值
```bash
samtools depth abc.sorted.bam >abc.depth
```
# mpileup
作用：用于生成bcf文件，或者说是pileup文件，之后结合bcftools进行SNP与InDel的分析，安装samtools时，包含了bcftools。【非常重要】
Usage: samtools mpileup [-EBug] [-C capQcoef] [-r reg] [-f in.fa] [-l list] [-M capMapQ] [-Q minBaseQ] [-q minMapQ] in.bam [in2.bam [...]]
-f：输入有索引的参考基因组fasta；
-g：输出到二进制的bcf格式【不使用-g，就不生成bcf格式，而是一个文本文件，统计了参考序列中每个碱基位点的比对情况；每一行代表参考序列中某一个碱基位点的比对结果】
-u：类似于-g，但是其主要用在管道操作，因为其输出是未压缩的bcf文件。

```bash
samtools mpileup -f hg19.fa abc.sorted.bam >abc.mpileup.txt
```
结果包含6列：参考序列名、匹配位置、参考碱基、比对上的reads数、比对的情况、比对的碱基质量
```
在第5列比对具体情况中:
. 表示与参考序列正链匹配；
, 表示与参考序列负链匹配；
ATCGN 表示在正链不匹配；
atcgn 表示在负链不匹配；
* 模糊碱基；
^ 匹配的碱基是一个read的开始，后面的ASCII码-33表示比对质量，再向后修饰的(.,ATCGNatcgn) 表示该read的第一个碱基；
$ 表示一个read结束，修饰前面碱基;
正则表达式+[0-9][ATCGNatcgn] 表示在该位点后面插入的碱基；
正则表达式-[0-9][ATCGNatcgn] 表示该位点后面缺失的碱基
```
# bam转fastq
作用：方便提取出一段比对到参考序列的reads进行分析
利用软件：http://www.hudsonalpha.org/gsl/information/software/bam2fastq
# rmdup
作用：将测序数据中由于PCR duplicate得到的reads去掉，只保留比对质量最高的reads
# idxstats
作用：输出一个表格，包含“序列名、序列长度、比对上的reads数、没有比对上的reads数”；其中第四列指PE reads中的一条read能匹配到参考基因组的染色体A，另一条read不能匹配到A上
# reheader
作用：替换bam文件的头文件

# bcftools
bcftools用于处理vcf(variant call format)文件和bcf(binary call format)文件。前者为文本文件，后者为其二进制文件。

bcftools集成了


