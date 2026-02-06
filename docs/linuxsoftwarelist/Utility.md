# 系统工具

## 硬件查询

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| CPU-G | - | - | `sudo add-apt-repository ppa:atareao/atareao`<br>`sudo apt-get update`<br>`sudo apt-get install cpu-g` | `sudo apt-get purge cpu-g` |
| Hardinfo | - | - | `sudo apt-get install hardinfo` | `sudo apt-get purge hardinfo` |
| I-Nex | - | - | `sudo apt-get install cpu-g` | `sudo apt-get purge cpu-g` |
| Psensor | - | - | `sudo apt-get install psensor` | `sudo apt-get purge psensor` |

## 系统监视

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| System Monitor | - | - | `sudo apt-get install gnome-system-monitor` | `sudo apt-get purge gnome-system-monitor` |
| Htop | Htop is an ncursed-based process viewer similar to top, but it allows one to scroll the list vertically and horizontally to see all processes and their full command lines | https://hisham.hm/htop/ | `sudo apt-get install htop` | `sudo apt-get purge htop` |

## 远程控制

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| TeamViewer | - | https://www.teamviewer.cn/cn/ | `wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb -O teamviewer_amd64.deb`<br>`sudo dpkg -i teamviewer_amd64.deb` | `sudo dpkg -r teamviewer` |
| Remmina | 通过 Linux 来随时随地访问任何操作系统 | https://remmina.org/ | `sudo apt-get install remmina` | `sudo apt-get purge remmina` |
| AnyDesk | 随时随地 AnyDesk | https://anydesk.com/en | `wget https://download.anydesk.com/linux/anydesk_5.1.2-1_amd64.deb -O anydesk_amd64.deb`<br>`sudo gdebi anydesk_amd64.deb` | `sudo dpkg -r anydesk` |
| Putty | - | https://www.putty.org/ | `sudo apt-get install putty` | `sudo apt-get purge putty` |

## 终端模拟器

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Gnome Terminal | Gnome Terminal 是 Gnome 桌面环境中的终端模拟软件 | https://help.gnome.org/users/gnome-terminal/stable/index.html.en | `sudo apt-get install gnome-terminal` | `sudo apt-get purge gnome-terminal` |
| Terminator | Terminator 是一个程序，它可让用户自由地排布多个 GNOME 终端，而不用通过窗口管理器来实现，比较适合需要同时打开多个终端的用户 | http://gnometerminator.blogspot.com/p/introduction.html | `sudo apt-get install terminator` | `sudo apt-get purge terminator` |
| tmux | GNU screen 类似的程序，可作为 screen 的替代品使用 | http://sourceforge.net/projects/tmux/ | `sudo apt-get install tmux` | `sudo apt-get purge tmux` |

## Shell

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Zsh | - | - | `sudo apt-get install zsh` | `sudo apt-get purge zsh` |

## 启动盘制作工具

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| UNetbootin | - | - | - | - |

## 包管理器

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Gdebi | 用于安装你自己手动下载的包的GUI程序 | https://packages.debian.org/stretch/gdebi | `sudo apt-get install gdebi` | `sudo apt-get purge gdebi` |
| Synaptic | apt系的图形化安装软件 | https://www.nongnu.org/synaptic/ | `sudo apt-get install synaptic` | `sudo apt-get purge synaptic` |

## 电源管理

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Caffeine | Caffeine prevents the desktop from becoming idle when an application is running full-screen | https://packages.debian.org/buster/caffeine | `sudo apt-get install caffeine` | `sudo apt-get purge caffeine` |

## SSH Server/Client

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Openssh Server | Secure Shell 的开源实现，目前已经成为 SSH Server 的首选 | http://www.openssh.com/ | `sudo apt-get install openssh-server` | `sudo apt-get purge openssh-server` |
| Openssh Client | Secure Shell 的开源实现，目前已经成为 SSH Server 的首选 | http://www.openssh.com/ | `sudo apt-get install openssh-client` | `sudo apt-get purge openssh-client` |