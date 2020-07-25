---
title: Github及Git使用
date: 2019-12-13 10:31:55
tags: Git
---

[Github在线教程](http://iissnan.com/progit/)【第一版】
[Github在线教程](https://git-scm.com/book/zh/v2)【第二版】
以下为我自己的总结
<!--more-->

在[Github](https://github.com/)网址上如何申请账号，建立仓库以及Git的下载就不赘述了，我的hexo搭建博客有。

### 配置用户信息
初次使用Git请配置好用户信息，详细可看[初次运行 Git 前的配置](http://iissnan.com/progit/html/zh/ch1_5.html)
```bash
git config --global user.name "Liripo"
git config --global user.email liripo@qq.com
#--global参数是在用户主目录下生成.config文件，如果某个仓库想用其他用户信息，可去掉--global，在项目根目录下生成.git/config文件[一般我想用不到吧]
```
```bash
git config --list
#查看配置信息
```
### 配置SSH密匙
https 和 SSH 的区别：
- https可以随意克隆github上的项目，而不管是谁的；而SSH则是你必须是你要克隆的项目的拥有者或管理员，且需要先添加 SSH key ，否则无法克隆。
- https url 在push的时候是需要验证用户名和密码的；而 SSH 在push的时候，是不需要输入用户名的，如果配置SSH key的时候设置了密码，则需要输入密码的，否则直接是不需要输入密码的。
详细教程可看my blog的Hexo搭建
创建命令
```
ssh-keygen -t rsa -C "your_email@example.com"
```
### Github项目
#### 单人作业
单人的代码管理，理解一下几个命令就足够了
```bash
git clone <path/to/repository> # 版本库的地址
git add <filename> # 将文件改动保存到缓存区
git commit -m "代码提交信息"
git push origin master # 将改动推送到版本库,Github默认分支master
```
#### 多人协作
```bash
git checkout -b <branchname> # 新建一个分支，分支没有merge 成功前只有自己可见
git push origin <brachname> # 将项目改动提交到分支
git checkout master # 切换到主分支,即master
git checkout -d <branchname> # 删除分支
git merge <branchname> # 合并分支
git branch -a #查看所有分支
```
```bash
git pull # 更新本地仓库至最新改动
```
#### 版本控制
查看提交历史
```bash
git log
git reflog
```
以我博客为例
**git reflog**
```bash
0098662 (HEAD -> master, github/master) HEAD@{0}: commit: Backup blog
102f7cf HEAD@{1}: commit: Backup blog
372f0ed HEAD@{2}: commit: Backup blog
4949fbb HEAD@{3}: commit: Backup blog
950b0de HEAD@{4}: commit: Backup blog
49fa595 HEAD@{5}: commit: Backup blog
c766121 HEAD@{6}: commit: Backup blog
8c5d216 HEAD@{7}: commit (initial): First commit
```
版本回退至**commit id**--上面如：0098662即为我最新提交版本的MD5值前几位
```bash
git reset --hard <commit_id>
#回退上个版本
git reset --hard HEAD^
#回退到上上个版本只需把HEAD^ 改成 HEAD^^ 以此类推
#或者git reset –hard HEAD~<回归次数>
```
本地版本回归，强制推送，*==**谨慎使用**==*
```bash
git push -f origin master
#origin远程仓库名
```
制用本地的代码去覆盖掉远程仓库的代码,用它是为了便捷。。。

### Git命令速查表

**本地仓库操作**

| 命令                                     | 功能                                                     |
| :--------------------------------------- | :------------------------------------------------------- |
| git config –global user.email your_email | 设置git email (必须设置)                                 |
| git config –global user.name your_name   | 设置git name (必须设置)                                  |
| git init                                 | 将目录变为仓库                                           |
| git add FILE                             | 将文件或目录加到缓存区                                   |
| git commit –m "Description"              | 提交更改 并注释做了什么更改                              |
| git status                               | 可以查看当前仓库的状态，是否有变化等                     |
| git diff                                 | 查看文件的不同                                           |
| git diff HEAD~n -- file                  | 查看和版本库中的同一个文件有什么不同                     |
| git reset --hard commit_id               | 将工作区恢复到commit_id指定的版本库内的版本              |
| git log                                  | 可以查看提交历史，以便确定要回退到哪个版本               |
| git reflog                               | 查看命令历史，以便确定要回到未来的哪个版本。             |
| git add                                  | 添加到缓存区                                             |
| git commit                               | 提交变更到版本库                                         |
| git checkout -- file                     | 可以丢弃工作区的修改（没有-- 就是创建一个分支）          |
| git reset HEAD file                      | 放弃缓存区的更改                                         |
| git rm                                   | 然后git commit 删除版本库内的相关文件                    |
| git checkout -b 分支名                   | 创建并转到新分支上                                       |
| git merge 分支名                         | 合并分支                                                 |
| git branch -d 分支名                     | 删除分支                                                 |
| git log --graph                          | 查看合并图                                               |
| git stash                                | 可以把当前工作现场“储藏”起来，等以后恢复现场后继续工作： |
| git stash list                           | 查看被存起来的工作                                       |
| git stash pop                            | 恢复并删除stash藏起来的工作                              |
| git tag name                             | 用于新建一个标签，默认为HEAD，也可以指定一个commit id    |
| git tag -a tagname -m "blablabla..."     | 可以指定标签信息；                                       |
| git tag -s tagname -m "blablabla..."     | 可以用PGP签名标签；                                      |
| git tag                                  | 可以查看所有标签。                                       |
| git tag -d                               | 删除一个标签                                             |
| git rebase HEAD~2                        | 合并两个commit                                           |

远程仓库操作

| 命令                                    | 功能                      |
| :-------------------------------------- | :------------------------ |
| git add remote origin git@host:repo.git | 建立和远程仓库的连接      |
| git push -u origin master               | 完成远程仓库的创建        |
| git push origin master                  | 用来推送最新修改          |
| git clone                               | 从远程克隆至本机          |
| git remote -v                           | 查看远程库信息            |
| git push --set-upstream gitname develop | 设置向远程推送的分支      |
| git push origin tagname                 | 在远程产生一个release版本 |
| git push origin :refs/tags/v0.9         | 远程删除标签              |

**GIT FLOW操作(标准化软件开发流程)**

| 命令                                                         | 功能                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| cd /git/cloned_repo                                          | 进入克隆仓库                                                 |
| git checkout -b develop origin/develop                       | 初始化版本流程控制（得到远程服务器develop）                  |
| git flow init                                                | 初始化工作目录(一直回车即可)                                 |
| git flow feature start editimage                             | 开始创建新的需求分支,目的修改image; 这时项目会自动切换feature/editimage分支 |
| git flow feature finish editimage                            | 更改部分代码后                                               |
| git commit -a -m "修改完了"(-a 参数表示提交所有更改了的文件，但是不适用于新创建的文件) | 完成开发分支合并develop(自动)                                |
| git push origin develop                                      | 发布到远程开发分支                                           |
| git flow release start v0.7.0                                | 开始进行发布版本的准备工作（develop -> master分支）          |
| git flow release finish v0.7.0                               | 进行Merge以及打tag                                           |
| git push origin master                                       | 将发布版本推送至远程                                         |

**Git flow 紧急BUG流程**

| 命令                                      | 功能            |
| :---------------------------------------- | :-------------- |
| git pull origin release/v1.0              | 拉回release版本 |
| git checkout release/v1.0                 | 切换分支        |
| git push origin release/v1.0              | 修改BUG         |
| git commit -a -m "修改完BUG,BUG文件+行数" | 修改完后提交    |