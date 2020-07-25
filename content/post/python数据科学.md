---
title: conda
date: 2019-11-25 20:35:16
tags: software
---

<!--more-->

#### spyder3
[spyder github网址](https://github.com/spyder-ide/spyder),其提供的安装方法有多种，官方强推[anaconda](https://www.anaconda.com/distribution/),确实我本人也喜欢使用，anaconda同时还创建了虚拟环境，使得我在linux使用各种软件如R、python等不需要过多的权限。miniconda是缩过之后的anaconda，没有那么多额外的软件，但也是可以使用虚拟环境的。
windows下简单使用`pip install spyder`安装即可，打开方式为在命令行中键入：`spyder3`
汉化spyder3
[SpyderSimplifiedChinese-master]( https://github.com/kingmo888/Spyder\_Simplified\_Chinese )下载解压后，到根目录使用shift键点击鼠标右键打开命令行窗口或者powershell;运行python main.py 或者python .\main.py;
重启Spyder,选择Tools---Preferences---General---Advanced Settings---language-----简体中文；
#### anaconda
anaconda有必要同时说下。
Anaconda可以便捷获取包且对包能够进行管理，同时对环境可以统一管理的发行版本。Anaconda包含了conda、Python在内的超过180个科学包及其依赖项。**推荐**
不需要那么多可以使用[Miniconda](https://docs.conda.io/en/latest/miniconda.html)。


|  Anaconda  | 其包含的科学包包括：conda, numpy, scipy, ipython notebook等。 |
| :--------: | ------------------------------------------------------------ |
|   conda    | 包及其依赖项和环境的管理工具,适用于Python, R, Ruby, Lua, Scala, Java, JavaScript, C/C++, FORTRAN |
|    pip     | pip是用于安装和管理软件包的包管理器                     |
| virtualenv | 用于创建一个**独立的**Python环境的工具。                |



[conda](https://conda.io/docs/):仅需要几条命令，你可以创建一个完全独立的环境来运行不同的Python或者其他语言的版本。
安装过程中，会有将conda加入环境变量的提示，当然，忘记加入时可以手动添加。conda的位置windows版本是在安装根目录下的scripts目录下。
**conda命令**
`conda list`会显示已经安装的包名和版本号。
`anaconda-navigator`启动anaconda图形界面。
`conda update conda`更新conda
创建新环境

```
conda creante -n <env_name> <you==版本>
```
`<env_name>`即创建的环境名。建议以英文命名，且不加空格。名称两边不加尖括号“<>”。
`<you==版本>`即安装在环境中的包名或者语言的版本。名称两边不加尖括号“<>”。
例如：`conda creante -n liaorp python==3.7`
`conda info --e`查看所含有的环境，环境前的\*表明当前身处的环境。或者`conda info --envs``conda env list`
**切换环境**
linux下`conda activate env_name`，gitbash下`source activate env_name`,windows`activate env_name`
`conda deactivate`退出环境；
**查找及安装包，模块，语言**
`conda search r`或者`conda search pysam`搜索conda中含有的包或者语言版本
`conda install r=3.6.1`即下载
```bash
#精准查找
conda search --full-name <package_full_name>
#指定环境下载
conda install --name <env_name> <package_name>
#复制环境
conda create --name <new_env_name> --clone <copied_env_name>
#删除环境
conda remove --name <env_name> --all
```
**换清华镜像源**
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
# 设置搜索时显示通道地址
conda config --set show_channel_urls yes
```
linux下，可less ~/.condarc
