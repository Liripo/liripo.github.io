---
title: ggplot2绘制图收录
mathjax: true
date: 2020-03-08 19:10:29
tags: R
categories: ggplot2
---

文章包含一些我绘制过的ggplot2图一些美化方法。

<!--more-->

### ggplot2修改绘图字体

使用extrafont包,
```R
library(extrafont)
loadfonts(device = "win")
```
这样你就能使用`windowsFonts()`函数看到的字体
对于英文字体，我一直选用family = "serif"，完全能应对大部分图形字体。
当然，extrafont包支持把所有字体导入到extrafontdb包中。
```R
font_import() #导入字体库
fonts() #查看导入的字体向量
```
ggplot2的theme函数能用来修改字体family、face、size等text标签参数，或者说是字体属性。

下图是我绘制散点图的一个函数，可以重点关注theme。
```R
plotfun <- function(df,x,y){
    #x,y为列名字符串,df参数为tibble
    p <- ggplot(df,aes(get(x),get(y))) + geom_point(size = 1) +
        labs(title = "Point Plot",x=x,y=y)+
        theme(text=element_text(family="serif"),
              axis.title=element_text(size=14,hjust = 0.5,face = "bold"),
              plot.title = element_text(hjust = 0.5,size = 20 , face = "bold"),
              legend.text = element_text(hjust = 0.5,size = 12 , face = "bold"),
              legend.text.align = 0 ,
              legend.title = element_text(hjust = 0.5,size = 12 , face = "bold"),
              axis.line = element_line(linetype = 1),
              panel.grid.major = element_blank())
    p1 <- p + geom_smooth(method="lm",se=F) #添加lm线性回归直线
    return(p1)
}
```

### 拼接图形

使用包patchwork
```R
library(patchwork)
```
对于上面那个函数，可以使用mapply循环绘制ggplot2对象列表，但是函数需要修改下，似乎不接受作为参数传入,把函数数据框参数去掉，往函数添加形似mtcars的数据框。
```R
plist <- mapply(plotfun,x = colnames(mtcars)[3],y = colnames(mtcars)[4:7],SIMPLIFY = F)
#对列表拼接
patch <- wrap_plots(plist,nrow = 2,guides = "collect")
```

### 拼图也可以绘制为分面图

使用gather函数对形式mtcars数据变形。这里就不放入真实数据了，虽说使用mtcars运行我的代码图毫无意义。

比如去mtcas的mpg列与其他列绘制散点图

```R
ga <- mtcars %>% gather(name1,value1,-mpg) %>%
	gather(name2,value2,mpg)%>%
	ggplot(aes(value1,value2)) + geom_point(size = 1) +
    labs(title = "Point Plot",x="name2",y="")+
    facet_wrap(~name1,strip.position = "left")
```

### 保存高清的png

我喜欢使用png去保存图片，当然更清晰的是tiff等
```R
png(file="xx.png",width = 10000,height = 4500,res = 600)
p
dev.off()
```
这是我经常使用的保存图片方式。

### plotly包

这个包可以绘制交互式点图，但是对于上述拼接的图不能支持，所以我才会去绘制分面图，方便看数据。

这个图使用很简单，使用`ggplotly(p)`即可在Rstudio导出一个网页图,p为ggplot绘制。

当然，这个包有其他函数，只是基本没用过。

### 2000*2000的corr相关性图

使用ggcor包

```R
library(tidyverse)
library(ggcor)
x <- matrix(rnorm(100*2000),nrow = 100)
#cor相关性值还未计算
#直接绘制相关性图,由于2000个过多
plot <- quickcor(x) +geom_raster + remove_axis()
#或者计算好后传入ggcor
cortbl <- cor(x)%>%cor_tbl(type = "upper")
#corr值颜色
cortbl$a <- ifelse(cortbl$r>0,"red",ifelse(cortbl$r < 0 ,
"green","white"))
#绘制及保存
p <- ggcor(cortbl, mapping = aes_string(x = ".col.id", y = ".row.id")) +
geom_tile(mapping = aes(fill = a))+
scale_fill_manual(name = "color",values = levels(factor(cortbl$a)),
labels = c("green:corr<0",
"red:corr>0",
"white:corr =0")) + remove_axis()
pdf("ggcor.pdf")
print(p)
dev.off()
```

