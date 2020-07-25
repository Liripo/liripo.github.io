---
title: awk使用
date: 2019-11-11 19:41:23
tags: awk
categories: linux三剑客
---
awk逐行读入文件，以空格为默认分隔符将每行切片，切开的部分再进行各种分析处理。
[awk书籍github](https://github.com/wuzhouhui/awk)

<!--more-->

读取fa文件碱基数
```
cat ref.fa|awk '/^>/&&NR>1{print "";}{ printf "%s",/^>/ ? $0" ":$0 }'|awk '{print $1"\t"length($3)}'
```
# awk简单入门

运行一个awk 程序有多种方式. 可以键入下面这种形式的命令
```bash
awk 'program' input files
```
awk帮助信息的example,计算第一列的和
```bash
 gawk '{ sum += $1 }; END { print sum }' file
```
程序内容多时，将程序写入文件progfile，选择-f参数键入
```bash
awk -f progfile optional list of files
```
awk报错信息，错误的地方会被>>> <<< 标记。
# 内建变量

**$0**	当前记录（这个变量中存放着整个行的内容）
**$1-$n** 当前记录的第n个字段，字段间由FS分隔
**NF**：awk 计算当前输入行的字段数量, 并将它存储在一个内建的变量中, 这个变量叫作NF。即为最后一列。或者说是字段。
**NR**：表示的是已经处理过的总记录数目，或者说行号(不一定是一个文件，可能是多个)
**FNR** 当前输入文件的记录数目
**FS**  用来设置每一记录的字段分隔符号
**OFS**: 输出字段分隔符变量
**RS** 定义了一行记录。读取文件时，默认将一行作为一条记录。
**ORS** 条记录在输出时候会用分隔符隔开，默认换行符
**FILENAME** 表示当前正在输入的文件的名字。
**ARGIND**        当前文件在ARGV中的位置
**ARGC**         当前命令行参数个数
**ARGV**         包含命令行参数的数组
**ENVIRON**      当前shell环境变量及其值组成的关联数组
**RLENGTH**       由match函数所匹配的子字符串的长度
**RSTART**        由match函数所匹配的子字符串的起始位置

# 内建函数

1.算术函数
>字符串函数

**length()**  获得字符串长度,例如：`length($0)`
**split()**  将字符串按分隔符分隔，并保存至数组,如：`split($0,arr,/:/)`
**getline** 从输入(可以是管道、另一个文件或当前文件的下一行)中获得记录，赋值给变量或重置某些环境变量。-------很强大的命令
**next** 作用和getline类似，也是读取下一行并覆盖`$0`，区别是next执行后，其后的命令不再执行，而是读取下一行从头再执行
**sub(regex,substr,string)**   替换字符串string(省略时为`$0`)中首个出现匹配正则regex的子串substr
**gsub(regex,substr,string)**  与sub()类似，但不止替换第一个，而是全局替换。
**substr(str,n,m)**   切割字符串str，从第n个字符开始，切割m个长度字符。如果m省略，则到结尾。
**tolower(str)和toupper(str)**  大小写转换
**system(cmd)**  执行shell命令cmd，返回执行结果，执行成功为0，失败为非0
**match(str,regex)**  返回字符串str中匹配正则regex的位置
**index(string, substring)**  函数返回子字符串第一次被匹配的位置，偏移量从位置1开始。如：awk '{ print index("test", "mytest") }' testfile 结果为3

# awk --help
-f 可以传入脚本文件，但是无法与命令行程序一起使用
-F fs 指定分隔符
-v var=val 传入shell变量

# awk一行式实战

1.去重  `awk '!a[$0]++{print $0}' input.file`
判定`!a[$0]++`是未定义的，以`$0`为数据下标，建立数组a，且其值为空字符串“”或者0----此处执行`++`后数组被定义为int型，初始值就为0；遇到重复的行是，数组的下标相同，此时数组的value为0，执行`++`后，数组值为1，经取反后数组为0，action不执行【即不打印】；没有遇到重复的行，即`a[$0]`执行++后为0，而!0=1,1为真。
那么`a[$0]`还同时记录着重复数-1
2.awk 合并两个文件----假设文件只有两个字段，而判定条件均为第一个字段

```bash
awk 'NR==FNR{a[$1]=$2;next}NR>FNR{print $0,a[$1]}' b.txt a.txt
```
>这里NR\==FNR即判断第一个文件，因为读取第一个文件总行数等于当前文件记录行数，而`a[$1]=$2`,即是把当前文件的第一个字段作为数组下标，第二个字段作为数组的值value
当NR>FNR读取第二个文件，输出第二个文件所有字段，以第二个文件第一个字段为索引，取得相应的值。当然可以使用ARGIND\==number判定读取的文件

3. awk提取两个fastq.gz文件的UMI序列

```bash
#提取R1，R2文件使用bioawk,可惜bioawk -c无法使用awk内置变量
bioawk -c fastx '{umi=substr($seq,1,3);seq_8 = substr($seq,8,length($seq));qual_8=substr($qual,8,length($qual))}{print "@"$name"_"umi"\n"seq_8"\n+\n"qual_8}' NL190929-1C.R1.fastq.gz >R1.fastq
bioawk -c fastx '{umi=substr($seq,1,3);seq_8 = substr($seq,8,length($seq));qual_8=substr($qual,8,length($qual))}{print "@"$name"_"umi"\n"seq_8"\n+\n"qual_8}' NL190929-1C.R2.fastq.gz >R2.fastq
#将R2中UMI提取到R1，以"_"为分隔符
awk '(ARGIND==1 && NR%4==1){split($0,a,"_");b[i]=a[2];i++}(NR!=FNR && FNR%4==1){print $0""b[j];j++}(ARGIND==2 && NR%4!=1){print $0}' R2.fastq R1.fastq >umi_R1.fastq
awk 'ARGIND==1 && NR%4==1{name[i]=$0;i++}ARGIND==2 && FNR%4==1{split($0,a,"_");print name[j]""a[2];j++}ARGIND==2 && FNR%4!=1{print}' R1.fastq R2.fastq >umi_R2.fastq
```

4.
