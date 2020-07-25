---
title: bioawk使用
date: 2019-12-20 23:22:55
tags: bioawk
---

> awk是我很喜欢的处理文本文件的工具，称他为一种语言也不过分了。但是在处理生信文件时还是不方便。另一种选择就是使用bioawk。唯一的短板就是无法使用awk内置变量，无法同时操作多个文件。

<!--more-->
# 安装
- conda 安装，方便，conda install 可以加-p参数指定安装路径
- 源码编译安装
```bash
git clone git://github.com/lh3/bioawk.git
cd bioawk && make
echo "export PATH=${path}/bioawk/:$PATH" >> ~/.bashrc
soyrce ~/.bashrc
```
# 语法
```bash
$ bioawk
usage: bioawk [-F fs] [-v var=value] [-c fmt] [-tH] [-f progfile | 'prog'] [file ...]
-F： 输入记录列和列之间的分隔符，和awk相同
-c： 支持的格式，前面讲过
-t： 以制表符分割各列，效果等同于bioawk -F't' -v OFS="t"
-f：官方文档没有介绍，这个参数和awk的参数意义一样，从文件读取source命令
-H：处理sam文件时，是否包含header
```
-c 支持输入文件格式，查看帮助：
```bash
$  bioawk -c -h
###bed:
1:chrom 2:start 3:end 4:name 5:score 6:strand 7:thickstart 8:thickend 9:rgb 10:blockcount 11:blocksizes 12:blockstarts
###sam:
1:qname 2:flag 3:rname 4:pos 5:mapq 6:cigar 7:rnext 8:pnext 9:tlen 10:seq 11:qual
###vcf:
1:chrom 2:pos 3:id 4:ref 5:alt 6:qual 7:filter 8:info
###gff:
1:seqname 2:source 3:feature 4:start 5:end 6:score 7:filter 8:strand 9:group 10:attribute
###fastx:fastx为序列格式,包括fasta和fastq
1:name 2:seq 3:qual 4:comment
```
bioawk依赖于 zlib，以便使用gzip文件。

# 使用
1.提取没有标题未映射读取
```bash
bioawk -c sam 'and($flag,4)' example.sam
```
2.提取标题映射读取
```bash
bioawk -Hc sam '!and($flag,4)' example.bam
```
3.反向互补fasta,revcomp函数
```bash
bioawk -c fastx '{print">"$name;print revcomp($seq)}' seq.fa
```
4.从SAM创建 FASTA ( 如果标志16，则使用 revcomp )
```bash
samtools view example.bam | bioawk -c sam '{s=$seq; if(and($flag, 16)) {s=revcomp($seq)} print">"$qname"n"s}'
```
5.从VCF打印样本 foo 和 bar的基因型
```bash
grep -v ^## in.vcf | bioawk -tc hdr '{print $foo,$bar}'
#hdr或者 header 根据输入中的第一行来命名每个列。 第一个字符中的特殊字符将转换为下划线
#用R习惯了，很容易上手
```
6.将fa打印成表格形式，以“Tab”分隔
```bash
bioawk -t -c fastx '{print $name,$seq}' input.fa
```
7.还有gc函数统计GC含量
```bash
bioawk -c fastx '{print $name, gc($seq)}' input.fa
```
8.fq转fa
```bash
bioawk -c fastx '{print ">"$name; print $seq}' input.fastq
```
还有各种函数meanqual--计算Phred平均值，length，trimq(30,0,5)剪掉质量值低于30，碱基位置从0-5的片段；

