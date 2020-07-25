---
title: python-docx笔记
mathjax: true
date: 2020-02-12 13:19:22
tags: python
categories: docx模块
---

> docx文件是office2007之后的版本使用的，docx格式的文件本质上是一个zip文件，主要内容是保存为XML格式的，因此可以通过修改Word背后的XML文件来设置自动更新域 。

<!--more-->

> python-docx是一个用于创建和更新Microsoft Word（.docx）文件的Python库 。

[中文教程，分享的cmd笔记]( https://www.zybuluo.com/belia/note/1303813 )

[官方文档]( https://python-docx.readthedocs.io/en/latest/index.html )

首先，谈谈一份word的组成部分，其基本是由标题，段落，表格，图片，分页，页眉页脚，目录，文本框，形状，章节，然后就是文字字体，字号等。【python-docx目前貌似还没有目录以及文本框的相关操作，所以对于涉及这两方面的暂时无法使用python-docx操作】

当你将一份word模板使用函数 Document() 打开，或者新建一份空白文档时，你就得到了一个文档对象，如：

```python
from docx import Document
document = Document()
```

对于对象`document`即word文档，其势必由上述所述的部分组成，其中最基本的即是段落，可以使用` add_paragraph `方法添加段落，而对于一个已存在的段落而言，如：

```python
paragraph = document.add_paragraph('Lorem ipsum dolor sit amet.')
paragraph.style = 'List Bullet'
```

在空白文档加入段落，或者获取模板第四个段落`paragraph = document.paragraphs[3]`，可以在其后面使用add_run方法添加文字获得一个run对象，添加的字符格式是默认的，这时你可以对这个run进行字体加粗，斜体，字体名等操作，如：

```python
run = paragraph.add_run('dolor')
run.bold = True
#英文字体名修改
run.font.name = '黑体'
#中文字体名修改
chinese = qn('w:eastAsia')
run._element.rPr.rFonts.set(chinese, u'黑体') #u为unicode编码
```

当然，你也可以修改段落的style,但是我在实践中遇到字体无法修改的情况，可以自行尝试。

标题添加就不说了，一般报告模板都会有的，但是记住，标题也是属于一个段落。

对于表格，你可在段落`paragraphs`处使用方法`add_table`添加，在整篇文档段落计算时，表格不属于段落，反倒是添加的表格由行列，单元格组成，而单元格之中又包含了段落，段落中又可以使用run对象进行操作。

说个例子，实际中我为了将自动化生成的表格文字单元格居中费了不少功夫。

首先我们需要找到官网的说明文档，找到cell即单元格这个对象，我们会发现，它有一些方法去修改这个单元格，

vertical_alignment这个方法，而对于居中，还是向上靠均存在WD_CELL_VERTICAL_ALIGNMENT这个预设好的对象里，而通过调用居中的方法即可实现单元格居中，如：

```python
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
```

具体学习看官方文档即可。

