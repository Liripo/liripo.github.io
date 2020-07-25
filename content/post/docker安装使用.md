---
title: docker安装使用
date: "2020-03-28"
tags: docker
summary: "linux dockor."
---

[docker从入门到实践](https://vuepress.mirror.docker-practice.com/install/ubuntu.html)

# 安装docker

linux ubuntu

1.安装依赖

```shell
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```

2.为了确认所下载软件包的合法性，需要添加软件源的 `GPG` 密钥。

```shell
$ curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

# 官方源
# $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

3.然后，我们需要向 `source.list` 中添加 Docker 软件源

```she
$ sudo add-apt-repository \
    "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
    $(lsb_release -cs) \
    stable"


# 官方源
# $ sudo add-apt-repository \
#    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#    $(lsb_release -cs) \
#    stable"
```

4.安装

```shell
sudo apt-get install docker-ce
```

## 另一种方式，使用脚本安装

```shell
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun
```

## 使用

```shell
sudo service docker start #运行
sudo docker --help
```

## 建立docker用户组，将当前用户加入

```shell
sudo groupadd docker
sudo usermod -aG docker $USER
```

退出重连即可无需sudo。

## 如果网络不行，添加镜像源

```shell
sudo mkdir /etc/docker
sudo vim /etc/docker/daemon.json
#添加如下信息
{
  "registry-mirrors": [
    "https://dockerhub.azk8s.cn",
    "https://hub-mirror.c.163.com"
  ]
}
```

重启即可`sudo service docker restart`

