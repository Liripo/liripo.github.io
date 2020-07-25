---
title: R包开发
mathjax: true
date: "2020-03-28"
tags: "R"
summary: "一些R包使用问题。"
toc: TRUE
---

**[R包开发书籍](https://r-pkgs.org/)**

**[Writing R Extensions](https://cran.r-project.org/doc/manuals/r-release/R-exts.html)**

[https://qianjiye.de/2015/04/r-packages](https://qianjiye.de/2015/04/r-packages)

# R包开发

使用devtools+Rtools进行R包开发，而Linux可以使用dockor+Rstudio开发版本。

### create_package()

```R
library(devtools)
create_package("./liripo.R")
```

### use_r()

使用`use_r("scales")`在R文件夹下生成一个scales.R文件。

下面举个我写的例子，参考函数`scales::show_col`

```R
#' @title show your colors by ggplot2
#'
#' @param colors colors
#' @param ncol ncol
#' @importFrom ggplot2 ggplot geom_tile aes aes_
#' @importFrom ggplot2 geom_text scale_fill_manual theme_void
#' @export
show_color <- function(colors,ncol = NULL){
  n <- length(colors)
  ncol <- ncol %||% ceiling(sqrt(length(colors)))
  nrow <- ceiling(n/ncol)
  tbl <- data.frame(cols = rep(1:ncol,times = nrow),
    rows = rep(nrow:1,each = ncol),
    colors = c(colors,rep(NA,ncol*nrow-length(colors)))
  )
  tbl <- na.omit(tbl)
  p <- ggplot(tbl,aes_(~cols,y =~rows))+
    geom_tile(aes_(fill = ~colors),color = "black",show.legend = F) +
    geom_text(aes_(label = ~colors)) +
    scale_fill_manual(values = tbl$colors,breaks = tbl$colors) +
    theme_void()
  class <- attributes(p)$class
  attr(p,"class") <- c(class,"show_color")
  p
}
#' @rdname print
#' @export
#' @method print show_color
print.show_color <- function(x,...){
  print(x,...)
}
```

里面ggplot2写R包时应使用aes_替代aes函数，具体可以`?aes\_`,当你想在R包中使用dplyr时，你可以运行R代码`vignette("programming")`看看dplyr的编程文档。

举个例子：

```R
#' @title ---
#' @importFrom dplyr filter 
#' @importFrom rlang .data
print_99 <- function(){
    table <- expand.grid(a = 1:9,b = 1:9) %>%
    filter(.data$a <= .data$b)
}
```

# document

`devtools::document()`会自动根据上面的rocelt调用Roxygen2生成man/*.Rd文件和Description文件。

具体可见`vignette("rd")`

# use_package

这个函数会在**DESCRIPTION**下引入R包依赖的其他R包,如：

```R
Imports: 
    ggplot2,
    stats
```

### load_all()

`load_all()`默认载入当前路径的包，类似`library()`，然后你可以试试写的代码。

```r
>exists("show_color", where = ".GlobalEnv", inherits = FALSE)
[1] FLASE
#可以看到当前全局环境没有这个函数，确实是以包的函数载入
>search()#看到载入的包
```

### check()

使用`check()`检查R包，可以看到是否有报错。



### use_mit_licence

`use_mit_licence("Liripo")`可以生成MIT许可证，具体生成什么许可证可以`?use_mit_license()`

# 快捷插入skeleon代码

Rstudio可以点击code-->Inseart roxygen skeleton快速插入，当然函数不规范的话，无法使用这个操作。

```R
> document()
Updating liripo.R documentation
Loading liripo.R
Writing NAMESPACE
Writing NAMESPACE
Writing scale.Rd
```

# R包中文

目前来说，不要使用中文。必须使用的可以看看函数`?stringi::stri_escape_unicode()`使用生成的unicode替代。ps:不过我使用后还是提示我使用ASCII字符编码。

# install()

install()将包载入到`.libpath()`路径。看下是否安装上了：

```R
> stringr::str_detect(.packages(all.available = TRUE),"liripo.R",)
[1] TRUE
```

### check_built()和build()

`check_built()`检查tar.gz包。

`build()`生成tar.gz包，便于分享。

# R包加入数据集

`use_data()`函数可以对R对象生成/data/*.rda文件，之后使用`use_r("R包名-package")`，在这个新生成的文件加入skeleon，例子：

```R
#' @name Rliripo
#' @docType package
#' @importFrom grDevices colorRampPalette
#' @importFrom stats na.omit
NULL
#'It's the color data of rmb
#'
#'used to this package
#'@docType data
#'@name rmb
NULL

#'It's the Codon table
#'
#'used to this package
#'@docType data
#'@name dna_pro_table
NULL
#'It's the seqence data of 2003 SARS
#'
#'used to this package
#'@docType data
#'@name SARS
NULL
globalVariables(c("rmb","dna_pro_table"))
```

`globalVariables`使得能在编写的R包中直接使用这些数据集。

