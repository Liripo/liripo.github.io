---
title: fastp+gencore使用
mathjax: true
date: 2020-01-07 23:05:42
tags: UMI
categories: 生信软件
password: Liripo
---

> 使用以上两个软件+vardict/varscan/outLyzer构建UMI分析流程

<!--more-->

# fastp

## 安装
```bash
conda install -c bioconda fastp
```
## fastp处理UMI功能
>**结果路径**：253：/data3/liaorp/umi/NL190929/fastp+genecore/umi_process

默认情况下fastp启动质量过滤，-q参数来指定合格的 phred 质量值,-u参数来指定最多可以有多少百分比的质量不合格碱基,使用-Q禁用[^1]
默认启动长度过滤，可以使用-L禁用，--length_required默认15（即低于15的舍弃），--length_limit限制长度
默认情况下，适配器修整是启用的，可以通过-A或--disable_adapter_trimming禁用
-w, --thread参数可使用多线程

```bash
mkdir umi_process && cd umi_process
fastp -i ../NL190929-1C.R1.fastq.gz -o R1.fastq.gz -I ../NL190929-1C.R2.fastq.gz -O R2.fastq.gz \
        -U --umi_loc=per_read --umi_len=3 --umi_skip=4 --umi_prefix=UMI \
        -Q -L -A
```
产生的fastq的query names形如，这是gencore接受的query names。
```
@ST-E00252:685:H5CLNCCX2:1:1101:27884:2680:UMI_CAG_AGA 1:N:0:TTCGTTGG+TACACACG
```
# 生成bam文件

>传入的fasta参考文件以及bed文件只是计算相应区域覆盖率。

## 使用bwa+samtools生成比对的bam文件
脚本：
```bash
bwa mem -t 10 /data3/liaorp/hg/hg19.fa R1.fastq.gz R2.fastq.gz > bwa.sam
#samtools将sam转bam并排序
samtools view -Sb bwa.sam |samtools sort -n -o sortquery.bam
#samtools index sortquery.bam 
```
samtools貌似只能对pos位置排序（即默认排序）建立索引，上面选用-n参数进行query排序导致失败了。

在后面使用gencore时提示我仍旧没有sort

尝试改用picard进行sort，使用输入文件samtools转bam的输出文件

```bash
java -jar /data3/liaorp/software/picard.jar SortSam I=sam.bam O=picardsort.bam SO=queryname
```
还是提示未排序
**使用samtools默认排序即可**

```
samtools sort -@ 10 -o sortpos.bam sam.bam
```

# gencore

>具有处理UMIs和报告信息性结果的功能,可以对重复序列进行删除以及降低背景噪音。[^2]

## 安装

```bash
cd ~/gitclone && wget [http://opengene.org/gencore/gencore](http://opengene.org/gencore/gencore)
chmod a+x ./gencore
#~/.soft已在环境变量中，将程序软连接过去，省去配置环境变量的麻烦
cd ~/.soft && ln -s ~/gitclone/gencore ./
```
## 运行
脚本
```bash
mkdir gencore && cd gencore
gencore -i ../umi_process/sortpos.bam -o gencore.unsort.bam -r /data3/liaorp/hg/hg19.fa \
        -b ../snp.probe.bed -u UMI -s 1 --high_qual 30
```
结果目录：253：/data3/liaorp/umi/NL190929/fastp+genecore/gencore

对结果按碱基排序
```bash
samtools sort -@ 20 -o sortgencore.bam gencore.unsort.bam
```
> 需要建立索引后进行vardictjava变异检测！！！

```bash
samtools index sortgencore.bam
```

# vardictjava变体识别

脚本
```bash
java -jar /data3/liaorp/software/VarDictJava-master/build/libs/VarDict-1.7.0.jar \
        -G /data3/liaorp/hg/hg19.fa -N NL19332 -f 0.01 \
        -b sortgencore.bam \
        -z -c 1 -S 2 -E 3 -g 4  \
        ../snp.probe.bed \
        | /data3/liaorp/software/VarDictJava-master/dist/VarDict-1.7.0/bin/teststrandbias.R \
    | /data3/liaorp/software/VarDictJava-master/dist/VarDict-1.7.0/bin/var2vcf_valid.pl -N NL19332 -E -f 0.01 \
        |awk '{if ($1 ~ /^#/) print; else if ($4 != $5) print }' \
        > tmp.vcf

java -Xmx32g -jar /data3/liaorp/software/picard.jar SortVcf \
        I=tmp.vcf O=NL19332.vcf SD=/data3/liaorp/hg/picard_CreateSequenceDictionary/hg19.dict
```

参考文献：

[^1]: Chen S, Zhou Y, Chen Y, Gu J. Fastp: an ultra-fast all-in-one FASTQ preprocessor. Bioinformatics. 2018;34:884–90.
[^2]: Chen, S., Zhou, Y., Chen, Y. *et al.* Gencore: an efficient tool to generate consensus reads for error suppressing and duplicate removing of NGS data. *BMC Bioinformatics* **20,** 606 (2019) doi:10.1186/s12859-019-3280-9