---
title: bamdst使用
date: 2019-12-17 10:56:40
tags: 生信基础工具
---
bamdst:用于计算bam文件测序深度和覆盖度（Sequencing depth and coverage）,有个疑问，应该使用哪个bam呢？？使用bwa及samtools得到的bam测序深度很高。。
<!--more-->

### 安装
```bash
git clone https://github.com/shiquan/bamdst.git ~
cd bamdst/
make
```
#安装完后会在项目根目录生成一个bamdst程序
```
-rwxrwxr-x 1 liaorp liaorp 532816 Dec 17 11:02 bamdst
```
可以看到文件权限可执行,键入`./bamdst`即可运行，或者加入环境变量中。
```bash
echo -e '#添加bamdst\nexport PATH=~/software/bamdst:$PATH'>>~/.bashrc#记住是单引号
source ~/.bashrc#使环境生效
```
### 概念
**测序深度Depth**：测序得到的总碱基数与待测基因组大小的比值。如人的基因组为3Gb，测序获得90Gb数据量，平均测序深度为30X。
**覆盖率**：

### example
下载数据有个example文件夹，测试以下,使用-p,-o参数
```bash
cd example && mkdir test
bamdst -p MT-RNR1.bed -o ./test test.bsm
```
产生七个文件:
```
$ls
chromosomes.report  coverage.report  depth_distribution.plot  depth.tsv.gz  insertsize.plot  region.tsv.gz  uncover.bed
```
- chromosomes.report:该文件中存储的是从bam文件中获取的目标染色体深度、覆盖度信息
bed文件即是为了挑选目标区域，即感兴趣的位置。
- coverage.report：信息很多，只看这个文件即可
文件分成三部分[total],[Target],[Flank],其中文件中还有一个关键字rmdup
```bash
[Target] Average depth    0.26 
[Target] Average depth(rmdup)    0.06
[Target] Coverage (>0x)    5.66% #目标区域大于0X覆盖率，排除0X
[Target] Coverage (>=4x)    2.83%
[Target] Coverage (>=10x)    0.00%
[Target] Coverage (>=30x)    0.00%
[Target] Coverage (>=100x)    0.00%
```
目标区域平均测序深度，算一下呗,即LN/G，where L is the read length, N is the number of reads and G is the haploid genome length.[^1]
可以使用[中文pubmed](http://www.chinapubmed.net/)
```bash
$ awk '{a=$1*$2;sum+=a;b=sum/954}END{print b}' depth_distribution.plot
0.261006
```
目标区域覆盖率：为文件depth_distribution.plot的第五列，1-第三列
在R中输入`round(54/954,6)`得到0.056604
- insertsize.plot：由于example得到的文件为空，有待探究

- depth.tsv.gz：记录了每个位点的 Raw Depth       Rmdup depth     Cover depth，三个名词各自代表？列出前几列

```bash
#Chr    Pos     Raw Depth       Rmdup depth     Cover depth
chrM    650     8       6       8
chrM    651     8       6       8
chrM    652     8       6       8
chrM    653     9       6       9
chrM    654     9       6       9
chrM    655     9       6       9
chrM    656     9       6       9
chrM    657     9       6       9
chrM    658     9       6       9
```
- region.tsv.gz：记录bed文件每个区域的测序深度中位数覆盖率以及Coverage(FIX)？？，由于example的bed只有一个区域，所以可以直接去除以那个区域长度得到目标区域测序深度。

- depth_distribution.plot :深度分布图，可以结合R绘图,如下，测序深度为9的有6个位点
```bash
0       900     0.943396        54      0.056604
1       0       0.000000        54      0.056604
2       0       0.000000        54      0.056604
3       27      0.028302        27      0.028302
4       4       0.004193        23      0.024109
5       12      0.012579        11      0.011530
6       1       0.001048        10      0.010482
7       0       0.000000        10      0.010482
8       4       0.004193        6       0.006289
9       6       0.006289        0       0.000000
```
算下理解是否正确
```
$ awk '{sum+=$2}END{print sum}' depth_distribution.plot
954
$ expr 1603 - 649
954
```
- uncover.bed :没有捕获区域
```bash
$ cat example/MT-RNR1.bed
chrM    649     1603
$ cat uncover.bed
chrM    672     1603
```
### 可选参数
```bash
#方括号中为程序默认的参数值
   -f, --flank [200]   flank n bp of each region
   -q [20]             map quality cutoff value, greater or equal to the value will be count
   --maxdepth [0]      set the max depth to stat the cumu distribution.
   --cutoffdepth [0]   list the coverage of above depths
   --isize [2000]      stat the inferred insert size under this value
   --uncover [5]       region will included in uncover file if below it
   --bamout  BAMFILE   target reads will be exported to this bam file
   -1                  begin position of bed file is 1-based
   -h, --help          print this help info
```
[^1]: Sims, D., Sudbery, I., Ilott, N. et al. Sequencing depth and coverage: key considerations in genomic analyses. Nat Rev Genet 15, 121–132 (2014) doi:10.1038/nrg3642