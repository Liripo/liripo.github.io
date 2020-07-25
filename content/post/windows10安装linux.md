---
title: windows10安装linux
mathjax: true
date: 2020-03-21 14:27:47
tags: linux
summary: "windows10安装ubuntu，以及源码安装python到指定目录，及更多相关配置。温馨提示：目前已有wsl2,推荐安装wsl2。"
---
windows10安装ubuntu，以及源码安装python到指定目录，及更多相关配置。

温馨提示：目前已有wsl2,推荐安装wsl2。

<!--more-->

### 安装ubuntu
1.windows10选择【开始】->【设置】-> 【安全和更新】->【开发者选项】，选择【开发人员模式】
2.打开控制面板------>程序与功能---->启用或关闭windows功能------>勾选 [适用于linux的windows子系统] 选项
3.打开Microsoft Store,搜索wsl
下载ubuntu或者Centos

打开ubuntu软件

添加root的passwd,初次使用。

```shell
sudo passwd
[sudo] password for jd:输入当前用户的密码
Enter new UNIX password:设置root用户的密码
Retype new UNIX password:再次输入设置root用户的密码
passwd: password updated successfully
```

- 修改ubuntu的apt源：
```shell
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vim /etc/apt/sources.list
```
添加清华源
```shell
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
 
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
 
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
 
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
 
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
 
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
 
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
 
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
 
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
 
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
```
更新
```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
```

### 添加ssh服务，xshell连接ubuntu

1. 卸载 ssh server

```shell
sudo apt-get remove openssh-server
```
2. 安装 ssh server
```shell
sudo apt-get install openssh-server
```
3. 修改 ssh server 配置
```shell
sudo vim /etc/ssh/sshd_config
```
```shell
Port 2222  #默认的是22，但是windows有自己的ssh服务，也是监听的22端口，所以这里要改一下
UsePrivilegeSeparation no
PasswordAuthentication yes
```
启动ssh server

```shell
sudo service ssh start
#设置开机启动
#由于wsl比较特殊，systemctl不是rc.0级运行，无法使用
#sudo systemctl enable ssh
#sudo vim /etc/rc.local
#service ssh start
#以上均不能解决开机自启问题，因为linux子系统还不算真正的linux
```

### xshell连接linux子系统

### 设置xming和ubuntu开机自动启动

开始菜单搜索运行-->键入shell：startup，将需要开机自动启动软件快捷方式复制到当前文件夹。

### 源码安装python到指定目录

```shell
#安装ssl
sudo apt-get install openssl
sudo apt-get install libssl-dev
wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
tar -zxvf Python-3.8.0.tgz
#vim Modules/Setup
#修改结果如下：
# Socket module helper for socket(2)
_socket socketmodule.c timemodule.c

# Socket module helper for SSL support; you must comment out the other
# socket line above, and possibly edit the SSL variable:
#SSL=/usr/local/ssl
_ssl _ssl.c \
-DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
-L$(SSL)/lib -lssl -lcrypto
```

### 安装make和zlib*

```shell
sudo apt-get install make && sudo apt-get install zlib*
```

### 编译安装

```shell
./configure --enable-optimizations --prefix=/mnt/d/linux/softwore/python
make
sudo -H make install #记得加-H
```

### 配置`~/.bashrc`和`~/.vimrc`

`~/.bashrc`

```shell
export PS1="\[\e[37;1m\][\[\e[33;1m\]\u\[\e[37;1m\]@\h:\[\e[34;1m\]\w\[\e[37;1m\]]\$\[\e[0m\]"
alias lt='ll -th'
alias le='less -SN'
# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi
#####添加软件路径
export PATH=/mnt/d/linux/softwore/python/bin:$PATH
```

`~/.vimrc`

```shell
set number
set vb t_vb=   "关警告声
set  nohlsearch
hi Comment ctermfg =blue
hi String ctermfg =darkyellow
set showmatch  "自动匹配相应括号
hi Number ctermfg = green
hi MatchParen ctermbg=darkyellow guibg= white
highlight Function cterm=bold
hi Type ctermfg =blue
set tabstop =4
hi Special ctermfg  = red
hi Identifier cterm = bold "变量标识符名称。
hi Statement cterm = bold
""编程语言的声明，一般是像“if”或“while”这样的关键字。
hi PreProc ctermfg = grey cterm=bold  "预处理颜色,一般像R的library
set paste
set wildmenu
""""""""插件管理
call plug#begin('~/.vim/plugged')
call plug#end()
filetype plugin indent on
""""""""""""""""""""""""""
"pep8
au BufNewFile,BufRead *.py
    \ set tabstop=4 |
    \ set softtabstop=4 |
    \ set shiftwidth=4 |
    \ set textwidth=79 |
    \ set expandtab |
    \ set autoindent |
    \ set fileformat=unix
set encoding=utf-8
"一键运行代码
map <F5> :call CompileRunGcc()<CR>
    func! CompileRunGcc()
        exec "w"
if &filetype == 'c'
            exec "!g++ % -o %<"
            exec "!time ./%<"
elseif &filetype == 'cpp'
            exec "!g++ % -o %<"
            exec "!time ./%<"
elseif &filetype == 'java'
            exec "!javac %"
            exec "!time java %<"
elseif &filetype == 'sh'
            :!time bash %
elseif &filetype == 'python'
            exec "!time python %"
elseif &filetype == 'html'
            exec "!firefox % &"
elseif &filetype == 'go'
    "        exec "!go build %<"
            exec "!time go run %"
elseif &filetype == 'mkd'
            exec "!~/.vim/markdown.pl % > %.html &"
            exec "!firefox %.html &"
elseif &filetype == 'R'
            exec "!time Rscript %"
endif
    endfunc
"高亮显示当前行
#set cursorline
#hi CursorLine   cterm=underline
```

### WSL开机自启动ssh

1.win+R搜索运行，输入`shell:startup`，进入开始菜单启动程序目录(C:\Users\用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup)

2.编辑脚本文件保存到上述目录，文件名`startWSL.vbs`

startWSL.vbs

```shell
Set ws = WScript.CreateObject("WScript.Shell")
cmd = "C:\Windows\System32\bash.exe -c ""bash /init.sh"""
'运行命令不显示cmd窗口
ws.Run cmd, 0, false
Set ws = Nothing
WScript.quit
```

3.编辑init.sh文件到linux系统根目录，`/init.sh`如下

```shell
#!/bin/bash
pn=$(ps aux|grep -v grep|grep sshd|wc -l)
[ -d /var/run/sshd ] || mkdir /var/run/sshd
chmod 744 /var/run/sshd
if [ "${pn}" != "0" ]; then
    pid=$(ps aux|grep -v grep|grep /usr/sbin/sshd|awk '{print $2}')
    kill $pid
fi
/usr/sbin/sshd -D
```

4.ubuntu需要默认root运行

```shell
#在cmd 下：
wslconfig /list # 查看wsl版本 
#ubuntu 16.04
ubuntu1604 config --default-user root
#Ubuntu 18.04
ubuntu1804 config --default-user root
```

### WSL开启chmod功能
>由于我在使用hexo d -g时遇到了些问题，出现Operation not permitted的问题，虽然文件看着是777的权限，但是报错让人很无奈。

Linux 挂载需要开启一些特性，解决办法是更改 wsl.conf 文件。
```shell
sudo vim /etc/wsl.conf
```
添加挂载磁盘的一些默认设置。
```shell
[automount]
enabled = true
options = "metadata,umask=22,fmask=11"
mountFsTab = false
```
以管理员权限运行cmd,重启linux子系统。
```shell
net.exe stop LxssManager
```
之后在所需要使用文件夹，运行
```shell
sudo chmod -R 777 software
```
便可以自由操纵那个文件夹了。

### 源码编译最新的vim
> 备注：不知道为什么一直失败

```shell
git clone https://github.com/vim/vim.git
```

`cd vim/src`

```shell
./configure --with-features=huge --enable-multibyte --enable-rubyinterp --enable-pythoninterp --enable-python3interp --enable-luainterp --enable-cscope --enable-gui=gtk3 --enable-perlinterp --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/ --with-python3-config-dir=/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu/ --prefix=/usr/local/vim
```

```shell
--with-features=huge：支持最大特性 
--enable-rubyinterp：打开对 ruby 编写的插件的支持 
--enable-pythoninterp：打开对 python 编写的插件的支持 
--enable-python3interp：打开对 python3 编写的插件的支持 
--enable-luainterp：打开对 lua 编写的插件的支持 
--enable-perlinterp：打开对 perl 编写的插件的支持 
--enable-multibyte：打开多字节支持，可以在 Vim 中输入中文 
--enable-cscope：打开对cscope的支持 -
-enable-gui=gtk3 表示生成采用 GNOME3 风格的 gvim 
--with-python3-config-dir=/usr/lib/python3.6/config-3.6m-x86_64-linux-gnu/ 指定 python3路径,已经弃用
--prefix=/usr/local/vim：指定将要安装到的路径
```

记住，--with-python3-config-dir为python3的配置路径，不是执行路径。

- 源码编译失败，使用apt更新

```shell
sudo apt remove vim
sudo apt-get install vim
```
