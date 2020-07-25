---
title: R包shiny
mathjax: true
date: 2020-01-15 23:11:25
tags: Rpackage
categories: R
---

R包shiny 可以构建交互式Web应用程序 。

<!--more-->

# Rstudio中初步使用shiny

```R
library(shiny)
runExample()
```
可以看到shiny包含11个示例app.R
```R
Valid examples are "01_hello", "02_text", "03_reactivity", "04_mpg", "05_sliders", "06_tabsets", "07_widgets", "08_html", "09_upload", "10_download", "11_timer"
```

通过查看示例的app.R代码，shiny由三个部分组成

- 用户界面（`ui`）对象控制应用程序的布局和外观。前端，用户界面对象。

-  `server`功能包含计算机构建应用程序所需的说明 。后端，服务器功能。

-  `shinyApp`函数创建对象。

shiny包含在一个名为app.R的脚本,位于一个目录中（例如newdir/），该应用可以通过runApp("newdir")运行,建议每个应用程序都位于其自己的唯一目录中。

app.R基本如下
```R
library(shiny)
ui <- ...
server <- ...
shinyApp(ui = ui, server = server)
```
# shinyapps.io分享你的程序

>在这里尝试web部署，这种东西当然是共享才有意义，试试在shinyapp.io上运行。

[shinyapp.io](http://www.shinyapps.io/)注册一个账户，配置rsconnect，在R中`install.packages('rsconnect')`导入这个包，输入你的账户信息，`rsconnect::setAccountInfo(name="<ACCOUNT>", token="<TOKEN>", secret="<SECRET>")`这些直接在你的shinyapp.io账户中找到。

Rstudio中即可点击public上传，或者R代码上传
```R
library(rsconnect)
deployApp("shiny app文件夹的路径",account = "你的用户名（如果你一台电脑上只有一个用户配置过，这个可以省略的）")
```
# ui布局

shiny的最基本配置如下,运行可以看到一个空白用户界面的应用程序。
```R
library(shiny)
ui <- fluidPage()
server <- function(input, output) {}
shinyApp(ui = ui, server = server)
```
从空白界面开始，

# R shiny服务器部署

[教程](https://rstudio.github.io/shiny-server/os/latest/)

首先，shiny需要安装R，并且需要包shiny,rmarkdown,digest

ubuntu安装R可以直接apt-get安装，不过不是最新版，需修改镜像源，十分推荐这种方法。

> 我使用conda安装，并将R程序软连接到/usr/bin目录下，这样做是为了让shiny能找到你的R，如果只是单纯配置root环境变量，运行shiny-server会找不到R的。

还有一个需要注意的，digest使用以下R命令安装

```R
install.packages('digest', repos='http://cran.us.r-project.org')
```

之后按照教程安装shiny-server即可。软件安装在/opt/shiny-server中。

由于我使用linux子系统，没有systemd，而是直接`sudo shiny-server`启动。

遇到错误就看文件log，在`/var/log/shiny-server`。

配置文件为：`/etc/shiny-server/shiny-server.conf`

## 添加当前用户运行shiny-server

暂时未解决。

# shiny相关资料

