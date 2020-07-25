---
title: xshell 和 xming 联合使用图形界面软件
date: 2019-12-23 10:59:34
tags: xming
---

xmanger 是与xshell搭配的图形界面管理器，需要付费，作为替代，使用xming，只是运行没那么快。

<!--more-->
# 安装
[下载网址](https://sourceforge.net/projects/xming/)

# 配置

1. XMing的配置：打开XLaunch，记住Display Number，现在这里是0，后面配置及XShell中会用到。然后点击启动xming。
2. 首先打开Xming安装文件夹找到 X*.hosts 文件(*号为上面Display Number 数字），如本例就是找到X0.hosts文件，打开并在localhost下面一行，添加Linux服务器的IP地址。
3. 配置xshell,连接-》SSH -> 隧道-》
在x11 转移中设置xdisplay为localhost:0.0
4.  配置完成后，重新连接服务器，
  启动图形界面软件，如spyder,就可以在xming上启动了。

