---
title: vcf文件注释
mathjax: true
date: 2020-01-20 23:58:40
tags: annovar
categories: 
---



> 原始测序文件fq.gz经genome比对，变异检测得到vcf文件，亦即变异位点文件， 只是通过看vcf文件我们是不知道些变异位点到底是位于基因的exon、intron、UTR等的哪些区域的 ，所以需要注释， 常用的vcf注释软件有annovar和snpEff 。

<!--more-->

###  ANNOVAR 

[annovar官网](http://annovar.openbioinformatics.org/en/latest/)

#### 安装

官网注册下载即可，程序为perl脚本，

#### ANNOVAR结构

```bash
ANNOVAR  
│  annotate_variation.pl #主程序，功能包括下载数据库，三种不同的注释
│  coding_change.pl #可用来推断蛋白质序列
│  convert2annovar.pl #将多种格式转为.avinput的程序
│  retrieve_seq_from_fasta.pl #用于自行建立其他物种的转录本
│  table_annovar.pl #注释程序，可一次性完成三种类型的注释
│  variants_reduction.pl #可用来更灵活地定制过滤注释流程
│
├─example #存放示例文件
│
└─humandb #人类注释数据库
```

#### ANNOVAR下载数据库

```bash
Perl annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene humandb/
#可用-downdb avdblist参数查看可供下载数据库列表
# -buildver 表示version
# -downdb 下载数据库的指令
# -webfrom annovar 从annovar提供的镜像下载，不加此参数将寻找数据库本身的源
# humandb/ 存放于humandb/目录下
# 默认使用gene-based注释类型以及refGene数据库，即基于基因的注释
```
基于区域的注释(Region-based Annotation):揭示variant与不同基因组特定段的关系，例如：它是否落在已知的保守基因组区域。基于区域的注释的数据库一般由UCSC提供;在一个数据库中，它不在乎位置的精确匹配，它不在乎核苷酸的识别。
```bash
annotate_variation.pl -regionanno -build hg19 -out ex1 -dbtype phastConsElements46way example/ex1.avinput humandb/
# -regionanno 表示使用基于区域的注释
# -dbtype phastConsElements46way 表示使用"phastConsElements46way"数据库，注意需要使用Region-based的数据库
```
Filter-based Annotation（基于过滤的注释）:filter-based和region-based主要的区别是，filter-based针对mutation（核苷酸的变化）而region-based针对染色体上的位置。例如region-based比对chr1:1000-1000而filter-based比对chr1:1000-1000上的A->G\
```bash
nnotate_variation.pl -filter -dbtype 1000g2012apr_eur -buildver hg19 -out ex1 example/ex1.avinput humandb/
# -filter 使用基于过滤的注释
# -dbtype 1000g2012apr_eur 使用"1000g2012apr_eur"数据库
#运行命令后，已知的变异会被写入一个*dropped结尾的文件，而没有在数据库中找到的变异将会被写入*filtered结尾的文件，*dropped文件是我们所需要的结果
```

#### vcf转.avinput
ANNOVAR使用.avinput格式，最重要为前5列
- 染色体(Chromosome)
- 起始位置(Start)
- 结束位置(End)
- 参考等位基因(Reference Allele)
- 替代等位基因(Alternative Allele)
- 剩下为注释部分（可选）
```bash
convert2annovar.pl -format vcf4 NL190929.vcf >out.avinput
#根据前五列去重
awk '!a[$1,$2,$3,$4,$5]++{print $0}' out.avinput >uniq.avinput
```
#### ANNOVAR注释功能
用table_annovar.pl进行注释
```bash
table_annovar.pl uniq.avinput ~/software/annovar/humandb -buildver hg19 -out annoresult -remove -protocol refGene,avsnp150,1000g2015aug_all,1000g2015aug_eas,1000g2015aug_sas,1000g2015aug_amr,1000g2015aug_afr,1000g2015aug_eur,gnomad_exome_20190125,dbnsfp30a,intervar_20170202,clinvar_20190305 -operation g,f,f,f,f,f,f,f,f,f,f,f 2>annovar.log &wait
# -buildver hg19 表示使用hg19版本
# -out annoresult 表示输出文件的前缀为annoresult
# -remove 表示删除注释过程中的临时文件，试了下不加，多产生27个文件，其中annoresult.hg19_multianno.txt文件为后续分析使用
# -protocol 表示注释使用的数据库，用逗号隔开，且要注意顺序
# -operation 表示对应顺序的数据库的类型（g代表gene-based、r代表region-based、f代表filter-based），用逗号隔开，注意顺序
# -nastring . 表示用点号替代缺省的值
# -csvout 表示最后输出.csv文件
#2>annovar.log 将标准错误输出到文件中
#wait等待所有线程的程序运行完执行下一步操作
```
#### InterVar
[InterVar](https://github.com/WGLab/InterVar)
这个软件是同个作者写的，是增加Intervar注释的软件。
```bash
#按照参考的配置文件配好相关路径
cp ~/config.ini ./ 
python2 ~/InterVar-master/Intervar.py -c ./config.ini 2>Intervar.log
#从其运行来看，是对数据库Intervar再次运行脚本annotate_variation.pl生成annocar数据库，convert2annovar.pl ,table_annovar.pl产生三个文件，其中
intervar_result.hg19_multianno.txt.intervar为后续分析使用，
##去重
awk '!a[$1,$2,$3,$4,$5]++{print $0}' intervar_result.hg19_multianno.txt.intervar >intervar_result_uniq
```
