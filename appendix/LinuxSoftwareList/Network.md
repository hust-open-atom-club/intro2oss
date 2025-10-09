# 网络应用

## 网络浏览器

### Chrome

- 介绍

Chrome 浏览器是一款专为现代互联网开发的网络浏览器，高速、简约而且安全。

- 下载位置

[Download](https://www.google.com/chrome/)

- 安装方法

```
 1. Install through deb package
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo gdebi google-chrome-stable_current_amd64.deb

 2. Install through software repo
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable

 Or 
sudo apt-get install google-chrome-beta
sudo apt-get install google-chrome-unstable
```

- 卸载方法

```
sudo apt-get purge google-chrome-stable

sudo apt-get purge google-chrome-beta

sudo apt-get purge google-chrome-unstable
sudo rm -rf /etc/apt/sources.list.d/google.list
```


### Firefox

- 介绍

自由、拓展性强大的浏览器

- 下载位置

[Download](http://www.firefox.com.cn/download/)

[PPA ubuntu-mozilla-daily](https://code.launchpad.net/~ubuntu-mozilla-daily/+archive/ubuntu/ppa)

- 安装方法

```
 1. Firefox
sudo apt-get install firefox firefox-locale-zh-hans

 2. Firefox PPA
sudo add-apt-repository ppa:ubuntu-mozilla-daily/ppa
sudo apt-get update
sudo apt-get install firefox-trunk
```

- 卸载方法

```
 1. Firefox
sudo apt-get purge firefox firefox-locale-zh-hans

 2. Firefox PPA
sudo apt-get purge firefox-trunk
sudo add-apt-repository -r ppa:ubuntu-mozilla-daily/ppa
sudo apt-get update
```


### Chromium

- 介绍

Google Chrome 浏览器的开源版本

- 下载位置

[Download](http://www.chromium.org/getting-involved/download-chromium)

[PPA chromium-daily](https://launchpad.net/~chromium-daily/+archive/ubuntu/stable)

- 安装方法

```
 1. Chromium
sudo apt-get install chromium

 2. Chromium PPA for Ubuntu/LinuxMint
sudo add-apt-repository  ppa:chromium-daily/stable
sudo apt-get update
sudo apt-get install chromium-browser
```

- 卸载方法

```
 1. Chromium
sudo apt-get purge chromium

 2. Chromium PPA
sudo apt-get purge chromium-browser
sudo add-apt-repository -r ppa:chromium-daily/stable
sudo apt-get update
```


### Opera

- 介绍

来自挪威的浏览器

- 下载位置

[Download](http://www.opera.com/computer/linux)

- 安装方法

```
 1. Add source in /etc/apt/sources.list
sudo add-apt-repository 'deb https://deb.opera.com/opera-stable/ stable non-free'
wget -qO- https://deb.opera.com/archive.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install opera-stable

 2. Add source in /etc/apt/sources.list.d/opera.list
sudo sh -c 'echo "deb https://deb.opera.com/opera-stable/ stable non-free" >> /etc/apt/sources.list.d/opera.list'
wget -qO- https://deb.opera.com/archive.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install opera-stable
```

- 卸载方法

```
 1. Add source in /etc/apt/sources.list
sudo apt-get purge opera-stable
sudo add-apt-repository -r 'deb https://deb.opera.com/opera-stable/ stable non-free'
sudo apt-get update

 2. Add source in /etc/apt/sources.list.d/opera.list
sudo apt-get purge opera-stable
sudo rm -rf /etc/apt/sources.list.d/opera.list
sudo apt-get update
```


### Vivaldi

### Maxthon

- 介绍

功能丰富、界面简洁的浏览器

- 下载位置

[Download](http://www.maxthon.cn/)

- 安装方法

```
sudo gdebi maxthon-browser-stable_XXX_amd64.deb
```

- 卸载方法

```
sudo dpkg -r maxthon-browser-stable
```


## 邮件客户端

### Thunderbird

- 介绍

专注于电子邮件管理的强大邮件客户端

- 下载位置

[Download](https://www.mozilla.org/zh-CN/thunderbird/)

- 安装方法

```
 1. Thunderbird
sudo apt-get install thunderbird

 2. Thunderbird PPA
sudo add-apt-repository ppa:ubuntu-mozilla-daily/ppa
sudo apt-get update
sudo apt-get install thunderbird-trunk
```

- 卸载方法

```
 1. Thunderbird
sudo apt-get purge thunderbird

 2. Thunderbird PPA
sudo add-apt-repository -r ppa:ubuntu-mozilla-daily/ppa
sudo apt-get update
```


### Evolution

- 介绍

提供邮件收发、日历和通讯录的个人信息解决方案

- 下载位置

[Download](https://wiki.gnome.org/Apps/Evolution)

- 安装方法

```
sudo apt-get install evolution
```

- 卸载方法

```
sudo apt-get purge evolution
```

### Geary

### Mutt

- 介绍

类 Unix 系统下基于文本的邮件客户端

- 下载位置

[Download](http://www.mutt.org/)

- 安装方法

```
sudo apt-get install mutt
```

- 卸载方法

```
sudo apt-get install mutt
```

## 即时聊天

### QQ

- 介绍

支持在线聊天、视频电话 (Linux 版暂不支持)、点对点断点续传文件的强大聊天软件

- 安装方法

1. 用浏览器打开[QQ](https://im.qq.com/linuxqq/index.shtml)；
2. 下载对应的架构和软件包格式安装即可。


### WeChat

- 介绍

微信，是一个生活方式

- 安装方法

1. UOS 用户可以使用 Wechat-UOS 版本，在[星火商店](https://www.spark-app.store/)自行安装即可。
2. Arch 用户可以使用如下命令安装：
```
yay -S wechat-beta-bwarp
```


### Skype

- 介绍

最清晰的免费网络电话，提供文字、声音和视频聊天

- 下载位置

[Download](https://www.skype.com/en/download-skype/skype-for-linux/)

- 安装方法

```
wget https://go.skype.com/skypeforlinux-64.deb
sudo gdebi skypeforlinux-64.deb
```

- 卸载方法

```
sudo dpkg -r skypeforlinux
```

- 备注

目前只支持 64 位版本的 `deb` 和 `rpm` 安装包。

### Skype WebPage

- 介绍

最清晰的免费网络电话，提供文字、声音和视频聊天

- 安装方法

使用 Skype 的[网页版本](https://web.skype.com)

### BearyChat

- 介绍

BearyChat, better communication service that brings your team on the same page

- 下载位置

[Download](https://bearychat.com/downloads)

- 安装方法

```
tar -xvf BearyChat-linux-x64.tar.gz
cd BearyChat-linux-x64/
./BearyChat
```

- 卸载方法

```
rm -rf BearyChat-linux-x64/ BearyChat-linux-x64.tar.gz
```

### Telegram Desktop

- 介绍

Fast and secure desktop app, perfectly synced with your mobile phone.

- 下载位置

[Download](https://desktop.telegram.org/)

- 安装方法

```
sudo apt-get install telegram-desktop
```

- 卸载方法

```
sudo apt-get purge telegram-desktop
```

### Empathy

- 介绍

支持多协议的强大聊天软件

- 下载位置

[Download](https://wiki.gnome.org/action/show/Apps/Empathy?action=show&redirect=Empathy)

[Github Empathy](https://github.com/GNOME/empathy)

- 安装方法

```
sudo apt-get install empathy
```

- 卸载方法

```
sudo apt-get purge empathy
```

### Pidgin

- 介绍

跨平台、支持多种协议的聊天软件

- 下载位置

[Download](https://pidgin.im/download/linux/)

- 安装方法

```
sudo apt-get install pidgin
```

- 卸载方法

```
sudo apt-get purge pidgin
```

### HexChat

- 介绍

跨平台的 IRC 聊天软件

- 下载位置

[Download](https://hexchat.github.io/downloads.html)

- 安装方法

```
sudo apt-get install hexchat
```

- 卸载方法

```
sudo apt-get purge hexchat
```

### Corebird

- 介绍

Native Gtk+ Twitter client for the Linux desktop

- 下载位置

[Download](https://github.com/baedert/corebird/releases)

- 安装方法

```
sudo apt-get install corebird
```

- 卸载方法

```
sudo apt-get purge corebird
```

## 文件传输

### FlareGet

- 介绍

支持多协议，多线程的下载软件

- 下载位置

[Download](https://flareget.com/download)

- 安装方法

```
sudo gdebi flareget_4.3-95_amd64.deb
```

- 卸载方法

```
sudo dpkg -r flareget
```

### UGet

- 介绍

轻量级的全能下载管理器

- 下载位置

[Download](http://ugetdm.com/downloads)

- 安装方法

```
sudo apt-get install uget
```

- 卸载方法

```
sudo apt-get purge uget
```

### Wget

- 介绍

运行在命令行下的多协议下载软件

- 下载位置

[Download](http://www.gnu.org/software/wget/)

- 安装方法

```
sudo apt-get install wget
```

- 卸载方法

```
sudo apt-get purge wget
```

### Transmission

- 介绍

一种 BitTorrent 客户端，特点是一个跨平台的后端和其上的简洁的用户界面

- 下载位置

[Download](http://www.transmissionbt.com/download/)

- 安装方法

```
sudo apt-get install transmission
```

- 卸载方法

```
sudo apt-get purge transmission
```

### qBittorrent

- 介绍

A BitTorrent client in Qt

- 下载位置

[Download](https://github.com/qbittorrent/qBittorrent)

- 安装方法

```
sudo apt-get install qbittorrent
```

- 卸载方法

```
sudo apt-get purge qbittorrent
```
### Aria2

- 介绍

运行在命令行下的轻量级下载软件

- 下载位置

[Download](http://sourceforge.net/projects/aria2/files/stable/aria2-1.15.2/)

- 安装方法

```
sudo apt-get install aria2
```

- 卸载方法

```
sudo apt-get purge aria2
```

### Filezilla

- 介绍

免费、开源的最强 FTP 客户端软件

- 下载位置

[Download](https://filezilla-project.org/)

- 安装方法

```
sudo apt-get install filezilla
```

- 卸载方法

```
sudo apt-get purge filezilla
```

## 云存储

### 坚果云

- 介绍

任何设备，随时随地实现文件共享

- 下载位置

[DEB 包](https://www.jianguoyun.com/static/exe/installer/debian/nautilus_nutstore_amd64.deb)

- 安装方法

```
sudo gdebi nautilus_nutstore_amd64.deb
```

- 卸载方法

```
sudo dpkg -r nautilus_nutstore
```

### Dropbox

- 介绍

我用的最好的的文件托管服务

- 下载位置

[Dropbox 安装](https://www.dropbox.com/install-linux)

- 安装方法

```
sudo apt install nautilus-dropbox
```

- 卸载方法

```
sudo apt purge nautilus-dropbox
```

### OwnCloud

- 介绍

The last cloud collaboration/file sharing/file syncing/data privacy platform you'll ever need.

- 下载位置

[下载](https://owncloud.org/download/#owncloud-desktop-client-linux)

- 安装方法

```
 Debian 10
su root
echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Debian_10/ /' > /etc/apt/sources.list.d/isv:ownCloud:desktop.list
wget -nv https://download.opensuse.org/repositories/isv:ownCloud:desktop/Debian_10/Release.key -O Release.key
apt-key add - < Release.key
apt-get update
apt-get install owncloud-client

 Debian 9
su root
echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Debian_9.0/ /' > /etc/apt/sources.list.d/isv:ownCloud:desktop.list
wget -nv https://download.opensuse.org/repositories/isv:ownCloud:desktop/Debian_9.0/Release.key -O Release.key
apt-key add - < Release.key
apt-get update
apt-get install owncloud-client
```

- 卸载方法

```
sudo apt-get remove owncloud-client
```

### Google Drive

- 介绍

Google 巨人开发的文件存储和同步服务

- 安装方法

使用 Google Drive 的[网页版本](https://drive.google.com)

### 百度网盘

- 介绍

记录每一份热爱，让美好永远陪伴。为你电脑/手机中的文件提供云备份、预览、分享等服务，帮你更便捷安全地管理数据。

- 下载位置

[安装包下载](https://pan.baidu.com/download#pan)

- 安装方法

```
sudo gdebi baidunetdisk_*.deb
```

- 卸载方法

```
sudo dpkg -r baidunetdisk
```


## 网络支付

### 支付宝

- 介绍

全球领先的独立第三方支付平台

- 下载位置
	- 首先进入[支付宝](https://www.alipay.com/)首页；
	- 点击登录按钮之后，下载支付宝控件；

- 安装方法

```
$ tar -xvf aliedit.tar.gz
aliedit.sh

$ ./aliedit.sh
Restart   firefox   to complete your changes
Successfully installed Alipay Security Control
Press any key to quit...
```

- 卸载方法

无
