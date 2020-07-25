---
title: bioconductor的学习与使用
date: 2019-12-22 22:27:21
tags: bioconductor
---

> 在生物信息学领域 , bioPerl和bioPython 是使用和研究生物信息学的开发者提供的在线资源库，那么bioR应当就是bioconductor。


<!--more-->
[官网](https://bioconductor.org/)
[2018年bioconductor教程](https://bioconductor.github.io/BiocWorkshops/)

# R包安装
```R
#官网安装
if (!require("BiocManager"))
    install.packages("BiocManager")
BiocManager::install("your-package")
```
倘若下载速度慢，则更换镜像源
```R
# 先安装BiocManager，它位于CRAN 
if(length(getOption("CRAN"))==0) options(CRAN="https://mirrors.tuna.tsinghua.edu.cn/CRAN/")
if(!require("BiocManager")) install.packages("BiocManager",update = F,ask = F)
# 然后添加BioC的国内源，可以选清华或者中科大
if(length(getOption("BioC_mirror"))==0) options(BioC_mirror="https://mirrors.ustc.edu.cn/bioc/")
```
快速查找包的文档,如`browseVignettes("clusterProfiler")`
