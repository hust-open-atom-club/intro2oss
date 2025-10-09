# 系统工具

## 硬件查询

### CPU-G

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

```
sudo add-apt-repository ppa:atareao/atareao
sudo apt-get update
sudo apt-get install cpu-g
```

- 卸载方法

```
sudo apt-get purge cpu-g
```

### Hardinfo

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

```
sudo apt-get install hardinfo
```

- 卸载方法

```
sudo apt-get purge hardinfo
```

### I-Nex

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

```
sudo apt-get install cpu-g
```

- 卸载方法

```
sudo apt-get install cpu-g
```

### Psensor

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

```
sudo apt-get install psensor
```

- 卸载方法

```
sudo apt-get purge psensor
```

## 系统监视

### System Monitor

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

```
sudo apt-get install gnome-system-monitor
```
- 卸载方法

```
sudo apt-get purge gnome-system-monitor
```

### Htop

- 介绍

Htop is an ncursed-based process viewer similar to top, but it allows one to scroll the list vertically and horizontally to see  all processes and their full command lines.

- 下载位置

[官方网站](https://hisham.hm/htop/)

- 安装方法

```
sudo apt-get install htop
```

- 卸载方法

```
sudo apt-get purge htop
```

## 远程控制

### TeamViewer

- 介绍

- 下载位置

[官方网站](https://www.teamviewer.cn/cn/)

[下载位置](https://download.teamviewer.com/download/linux/teamviewer_amd64.deb)

- 安装方法

```
wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb -O teamviewer_amd64.deb
sudo dpkg -i teamviewer_amd64.deb
```

- 卸载方法

```
sudo dpkg -r teamviewer
```

### Remmina

- 介绍

通过 Linux 来随时随地访问任何操作系统

- 下载位置

[官方网站](https://remmina.org/)

[下载位置](https://remmina.org/how-to-install-remmina/)

- 安装方法

```
sudo apt-get install remmina
```

- 卸载方法

```
sudo apt-get purge remmina
```

### AnyDesk

- 介绍

随时随地 AnyDesk

- 下载位置

[官方网站](https://anydesk.com/en)

[下载位置](https://anydesk.com/en/downloads/linux)

- 安装方法

```
wget https://download.anydesk.com/linux/anydesk_5.1.2-1_amd64.deb -O anydesk_amd64.deb
sudo gdebi anydesk_amd64.deb
```

- 卸载方法

```
sudo dpkg -r anydesk
```

### Putty

- 介绍

- 下载位置

[官方网站](https://www.putty.org/)

[下载位置](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

- 安装方法

```
sudo apt-get install putty
```

- 卸载方法

```
sudo apt-get purge putty
```


## 终端模拟器

### Gnome Terminal
 
- 介绍

Gnome Terminal 是 Gnome 桌面环境中的终端模拟软件

- 下载位置

[Official Website](https://help.gnome.org/users/gnome-terminal/stable/index.html.en)

[GitHub](https://github.com/GNOME/gnome-terminal)

- 安装方法

```
sudo apt-get install gnome-terminal
```

- 卸载方法

```
sudo apt-get purge gnome-terminal
```

### Terminator

- 介绍

Terminator 是一个程序，它可让用户自由地排布多个 GNOME 终端，而不用通过窗口管理器来实现，比较适合需要同时打开多个终端的用户

- 下载位置

[Official Website](http://gnometerminator.blogspot.com/p/introduction.html)

- 安装方法

```
sudo apt-get install terminator
```

- 卸载方法

```
sudo apt-get purge terminator
```

### tmux

- 介绍

GNU screen 类似的程序，可作为 screen 的替代品使用

- 下载位置

[Official Website](http://sourceforge.net/projects/tmux/)

- 安装方法

```
sudo apt-get install tmux
```

- 卸载方法

```
sudo apt-get purge tmux
```

## Shell

### Zsh

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

```
sudo apt-get install zsh
```

- 卸载方法

```
sudo apt-get purge zsh
```

## 启动盘制作工具

### UNetbootin

- 介绍

- 下载位置

[官方网站]()

[下载位置]()

- 安装方法

- 卸载方法

## 包管理器

### Gdebi

- 介绍

用于安装你自己手动下载的包的GUI程序

- 下载位置

[Official Website](https://packages.debian.org/stretch/gdebi)

- 安装方法

```
sudo apt-get install gdebi
```

- 卸载方法

```
sudo apt-get purge gdebi
```

### Synaptic

- 介绍

apt系的图形化安装软件

- 下载位置

[Official Website](https://www.nongnu.org/synaptic/)

- 安装方法

```
sudo apt-get install synaptic
```

- 卸载方法

```
sudo apt-get purge synaptic
```

## 电源管理

### Caffeine

- 介绍

Caffeine prevents the desktop from becoming idle when an application is running full-screen.

- 下载位置

[Debian Package](https://packages.debian.org/buster/caffeine)

- 安装方法

```
sudo apt-get install caffeine
```

- 卸载方法

```
sudo apt-get purge caffeine
```


## SSH Server/Client

### Openssh Server

- 介绍

Secure Shell 的开源实现，目前已经成为 SSH Server 的首选

- 下载位置

[Official Website](http://www.openssh.com/)

- 安装方法

```
sudo apt-get install openssh-server
```

- 卸载方法

```
sudo apt-get purge openssh-server
```

### Openssh Client

- 介绍

Secure Shell 的开源实现，目前已经成为 SSH Server 的首选

- 下载位置

[Official Website](http://www.openssh.com/)

- 安装方法

```
sudo apt-get install openssh-client
```

- 卸载方法

```
sudo apt-get purge openssh-client
```
