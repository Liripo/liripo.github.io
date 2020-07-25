---
title: gitbash配置文件
date: 2019-11-08 22:37:49
tags: bash
---
**gitbash的好处是能在windows下使用bash命令以及自带vim编辑器。**
<!--more-->

~/.vimrc配置文件代码
```
set number
set vb t_vb=   "关警告声
set  nohlsearch
hi Comment ctermfg =blue
hi String ctermfg =darkyellow
set showmatch  "自动匹配相应括号
hi Number ctermfg = green
"hi MatchParen ctermbg=darkyellow guibg= white
"自动缩进不好用 set autoindent
highlight Function cterm=bold
hi Type ctermfg =blue
set tabstop =4
hi Special ctermfg  = red
hi Identifier cterm = bold " 变量标识符名称。
hi Statement cterm = bold
""编程语言的声明，一般是像“if”或“while”这样的关键字。
hi PreProc ctermfg = grey cterm=bold "预处理颜色,一般像R的library
set paste #消除gitbash粘贴出现空格及自动缩进的情况
```
~/.bashrc配置
```
export PATH=/d/R-3.6.1/bin/x64:$PATH
alias python='winpty python.exe' #windows下打开python别名
export PS1="\\liripo@windows:\w\$(__git_ps1 '(%s)')\$ " #使用PS1
alias lt='ll -th'
alias le='less -N'
```

