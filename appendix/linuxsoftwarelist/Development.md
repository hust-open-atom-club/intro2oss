# 程序开发

## 版本控制

### Git

- 介绍

Linus为管理Linux内核而开发的分布式版本管理工具

- 下载位置

[官方网站](https://git-scm.com/)

[下载位置](https://git-scm.com/download/linux)

- 安装方法

```
sudo apt-get install git
```

- 卸载方法

```
sudo apt-get purge git
```

### SVN

- 介绍

Apache开发的集中式版本管理工具

- 下载位置

[官方网站](https://subversion.apache.org/)

[下载位置](https://subversion.apache.org/packages.html)

- 安装方法

```
sudo apt-get install subversion
```

- 卸载方法

```
sudo apt-get install subversion
```

## 本文编辑器

### Sublime Text

- 介绍

A sophisticated text editor for code, markup and prose

- 下载位置

[官方网站](https://www.sublimetext.com/)

[下载位置](https://www.sublimetext.com/3)

- 安装方法

```
sudo apt-get install apt-transport-https
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

 Stable
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list

 Dev
echo "deb https://download.sublimetext.com/ apt/dev/" | sudo tee /etc/apt/sources.list.d/sublime-text.list

sudo apt-get update
sudo apt-get install sublime-text
```

- 卸载方法

```
sudo apt-get purge sublime-text
```

### Visual Studio Code

- 介绍

微软开发可以跨Linux，Windows，Mac OS的编辑器

- 下载位置

[官方网站](https://code.visualstudio.com/) [下载位置](https://code.visualstudio.com/Download)

- 安装方法

```
 1. Install from deb package
 Download deb package from https://code.visualstudio.com/
sudo gdebi code_*_amd64.deb

 2. Install from software repo
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install code
```

- 卸载方法

```
 1.
sudo dpkg -r code
 2.
sudo apt-get purge code
```

### gedit

- 介绍

GNOME桌面环境的默认文本编辑器

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/Gedit)

[下载位置](https://wiki.gnome.org/Apps/Gedit#Download)

- 安装方法

```
sudo apt-get install gedit
```

- 卸载方法

```
sudo apt-get purge gedit
```

### Atom

- 介绍

**A hackable text editor for the 21st Century**

- 下载位置

[官方网站](https://atom.io/) [Github仓库](https://github.com/atom/atom)

- 安装方法

```
 1. install from package
 Download deb package from https://atom.io/
sudo gdebi atom-amd64.deb

 2. install from source list
curl -sL https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'
sudo apt-get update
sudo apt-get install atom

 Or
sudo apt-get install atom-beta
```

- 卸载方法

```
 1.
sudo dpkg -r atom
 2.
sudo apt-get purge atom
```

### Vim

- 介绍

Unix/Linux平台下的高度可配置的文本编译器，可以说Linux下非常好的文本编译器，也是我默认使用的编译器。

- 下载位置

[下载位置](https://github.com/vim/vim.git)

- 安装方法

```
sudo apt-get install vim
```

- 卸载方法

```
sudo apt-get purge vim
```

### Emacs

- 介绍

An extensible, customizable, free/libre text editor — and more

- 下载位置

[下载位置](https://www.gnu.org/software/emacs/download.html)

- 安装方法

```
sudo apt-get install emacs
```

- 卸载方法

```
sudo apt-get purge emacs
```

### Nano

- 介绍

类Unix系统上基于命令行接口的文本编辑器

- 下载位置

[官方网站](https://www.nano-editor.org/)

- 安装方法

```
sudo apt-get install nano
```

- 卸载方法

```
sudo apt-get purge nano
```

## 集成开发环境

### Eclipse IDE

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

- 卸载方法

### JetBrains IDE

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

- 卸载方法

### Wireshark

- 介绍

世界第一以及使用最广泛的网络协议分析器

- 下载位置

[官方网站](https://www.wireshark.org/)

[下载位置](https://www.wireshark.org/download.html)

- 安装方法

```
sudo apt-get install wireshark
```

- 卸载方法

```
sudo apt-get purge wireshark
```

### Code Blocks

- 介绍

Codeblocks is a cross-platform IDE built around wxWidgets, designed to be extensible and configurable. 

- 下载位置

[官方网站](http://www.codeblocks.org/)

[下载位置](http://www.codeblocks.org/downloads)

- 安装方法

```
sudo apt-get install codeblocks
```

- 卸载方法

```
sudo apt-get purge codeblocks
```
