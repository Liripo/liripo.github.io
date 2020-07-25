---
title: 翻墙？自搭！
mathjax: true
date: 2020-01-06 23:39:54
tags: ssh
categories: 
---

购买海外服务器，选用 [virmach]( https://virmach.com/)，或者Vultr、Linode、DigitalOcean。

xshell进入服务器后创建用户，非必须。

```bash
adduser liripo && passwd liripo
#添加sudo权限
$ vim /etc/sudoers
#在root    ALL=(ALL)       ALL下面添加
liripo   ALL=(ALL)      ALL
```

<!--more-->

# 使用ShadowsocksR

```bash
sudo su
wget -N --no-check-certificate https://makeai.cn/bash/ssrmu.sh && chmod +x ssrmu.sh
bash ssrmu.sh
```

 输入 **1** ，开始安装ShadowsocksR服务端。

之后会提示输入Shadowsocks的 **端口/密码/加密方式/ 协议/混淆（混淆和协议是通过输入数字选择的）** 等参数来添加第一个用户 。

之后按着提示走呗。端口号尽量选高点，比如6888，25是不行的。

得到相关信息如下：

```bash
===================================================
 用户 [liripo] 的配置信息：
 I  P	    : 45.76.209.91
 端口	    : 6888
 密码	    : ******
 加密	    : aes-256-ctr
 协议	    : auth_sha1_v4_compatible
 混淆	    : tls1.2_ticket_auth_compatible
 设备数限制 : 5
 单线程限速 : 0 KB/S
 用户总限速 : 0 KB/S
 禁止的端口 : 无限制 

 已使用流量 : 上传: 0 B + 下载: 0 B = 0 B
 剩余的流量 : 819.21 TB 
 用户总流量 : 819.21 TB 
 SS    链接 : ss://YWVzLTI1Ni1jdHI6cnAzMTgwMjA4NTYzQDQ1Ljc2LjIwOS45MToyNQ 
 SS  二维码 : https://makeai.cn/qr/?m=2&e=H&p=3&url=ss://YWVzLTI1Ni1jdHI6cnAzMTgwMjA4NTYzQDQ1Ljc2LjIwOS45MToyNQ
 SSR   链接 : ssr://NDUuNzYuMjA5LjkxOjI1OmF1dGhfc2hhMV92NDphZXMtMjU2LWN0cjp0bHMxLjJfdGlja2V0X2F1dGg6Y25Bek1UZ3dNakE0TlRZeg 
 SSR 二维码 : https://makeai.cn/qr/?m=2&e=H&p=3&url=ssr://NDUuNzYuMjA5LjkxOjI1OmF1dGhfc2hhMV92NDphZXMtMjU2LWN0cjp0bHMxLjJfdGlja2V0X2F1dGg6Y25Bek1UZ3dNakE0TlRZeg 
 
提示: 
在浏览器中，打开二维码链接，就可以看到二维码图片。
协议和混淆后面的[ _compatible ]，指的是 兼容原版协议/混淆。
===================================================
```



由于二维码自动生成功能连接不上，自己安装ShadowsocksR的安卓或者windows版本

# 安装windows或android客户端

配置相关信息即可使用。

安卓apk可在[Githubshadowsocksr-android]( https://github.com/shadowsocksr-backup/shadowsocksr-android/releases )下载

由于百度网盘分享不了，windowns版本可在我的[腾讯云下载](https://liripo-1300901505.cos.ap-guangzhou.myqcloud.com/%E8%BD%AF%E4%BB%B6/ShadowsocksR-4.7.0.zip)

倘若电脑端网速太慢，可右键点击程序的那个小飞机，选择代理规则：绕过局域网和大陆。

