---
title: Markdown与Typora,Rmarkdown
date: 2019-12-17 23:42:15
tags: markdown
---

>[在线教程](http://www.markdown.cn/)
<!--more-->
Markdown的特点就不赘述了。
### 编辑器
推荐[Tpyora](https://typora.io/)--熟悉这个软件大部分的写作可以解决。
Tpyora支持导出PDF，html，word--需安装[pandoc](https://pandoc.org/installing.html)等。
### 写作方式
我喜欢在源代码模式进行写作，Tpyora`CTRL+/`即可来回切换视图模式。新建表格可以在非源码视图使用`CTRL+T`。字体大小颜色可以使用html语法进行修改，很少用。`:smile:`即可输出笑脸，虽然我不怎么用，记录下呗。一般我不会添加[toc]在文章开头处生成目录。高亮也很少用，源码模式使用`==hightlight==`,引用句首加`>`。图片的话虽然可以Tpyora可以直接本地复制粘贴，但是依赖于本地，其他人无法查看，所以我习惯使用腾讯云cos功能，或者Github构建的图床，出图不稳定，尤其0点到10点无法显示，少用。由于Markdown的表格功能无法快速的复制粘贴，对于大的数据表格一行行复制太麻烦了，使用软件[exceltk](https://files.cnblogs.com/files/math/exceltk.0.1.3.zip)将excel转.md文件,命令`./exceltk.exe -t md -xls xxx.xls`,可以知道sheet,`./exceltk.exe -t md -xls xx.xls -sheet sheetname`,指定小数数字精度`./exceltk.exe -t md -p 2 -xls xxx.xls`

> 在Tpyora中可以在视图模式直接复制整个表格

>Markdown的哲学就是 Less is more， 专注于自己的思维流，特定的时间段内大量输出。

所以不必追求过多花里胡哨的，除非报告之类的。接下来就试试Rmarkdown呗。
### Rmarkdown
使用前安装rmarkdown包--`devtools:install_github("rmarkdown", "rstudio")`
注：直接创建新文件会自动下载
#### 导出html
直接点击knit to html即可。
#### 导出PDF
需要安装[tinytex](https://yihui.org/tinytex/cn/)
```R
#以下任选即可
tinytex::install_tinytex()#这个我没成功过
devtools::install_github('yihui/tinytex')#github下载多好
```
记录个问题，花了我很长时间，tinytex需要调用DOS命令DOSKEY,由于我的公司电脑没有配置好环境变量路径：c:\windows\System32，所以一直无法设置别名。当然，如果没有问题的话，安装好tinytex直接导出pdf时会自动下载。
下载完后下载[miktex](https://miktex.org/download)--这是windows的
之后设置Rstudio,打开tools,点击global option，如下所示，
![Rstudio-pdf](https://liripo-1300901505.cos.ap-guangzhou.myqcloud.com/home20191223202204.png)

打开Rmarkdown文件，点击设置，进去output options,点击Advanced
![](https://liripo-1300901505.cos.ap-guangzhou.myqcloud.com/home20191223202635.png)![](https://liripo-1300901505.cos.ap-guangzhou.myqcloud.com/home20191223202827.png)

>以xeLaTeX+ xeCJK 来处理终于能用Rmarkdown编译pdf文档

##### 解决中文pdf不支持问题
下载rticles`install.packages("rticles")` 这个包中有Ctex相关功能，所以可以实现中文的输出 
之后在写Rmarkdown时使用rticles的cetx模板即可。
![](https://liripo-1300901505.cos.ap-guangzhou.myqcloud.com/home20191223205725.png)

弄到这，干嘛不直接下个[ceTX](http://www.ctex.org/CTeXDownload)就好，不过还要编辑header.tex文件，想想还是模板吧。

直接修改这个包的.RMD文件不就好了。。

#### 导出word

安装pandoc即可。

#### 试试ppt呗
[中文帮助](https://slides.yihui.org/xaringan/zh-CN.html#26)
[Github](https://github.com/yihui/xaringan)
有空再搞吧，好累
#### bookdown
用R写书。
[Github](https://github.com/rstudio/bookdown)

试试增强般及简化版 [bookdownplus]( bookdownplus ) 

### LaTeX的使用


#### 数学公式
