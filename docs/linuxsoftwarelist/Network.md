# 网络应用

## 网络浏览器

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Chrome | Chrome 浏览器是一款专为现代互联网开发的网络浏览器，高速、简约而且安全 | https://www.google.com/chrome/ | `wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub \| sudo apt-key add -`<br>`sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'`<br>`sudo apt-get update`<br>`sudo apt-get install google-chrome-stable` | `sudo apt-get purge google-chrome-stable`<br>`sudo rm -rf /etc/apt/sources.list.d/google.list` |
| Firefox | 自由、拓展性强大的浏览器 | http://www.firefox.com.cn/download/ | `sudo apt-get install firefox firefox-locale-zh-hans` | `sudo apt-get purge firefox firefox-locale-zh-hans` |
| Chromium | Google Chrome浏览器的开源版本 | http://www.chromium.org/getting-involved/download-chromium | `sudo apt-get install chromium` | `sudo apt-get purge chromium` |
| Opera | 来自挪威的浏览器 | http://www.opera.com/computer/linux | `sudo add-apt-repository 'deb https://deb.opera.com/opera-stable/ stable non-free'`<br>`wget -qO- https://deb.opera.com/archive.key \| sudo apt-key add -`<br>`sudo apt-get update`<br>`sudo apt-get install opera-stable` | `sudo apt-get purge opera-stable`<br>`sudo rm -rf /etc/apt/sources.list.d/opera.list` |
| Vivaldi | - | - | - | - |
| Maxthon | 功能丰富、界面简洁的浏览器 | http://www.maxthon.cn/ | `sudo gdebi maxthon-browser-stable_XXX_amd64.deb` | `sudo dpkg -r maxthon-browser-stable` |

## 邮件客户端

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Thunderbird | 专注于电子邮件管理的强大邮件客户端 | https://www.mozilla.org/zh-CN/thunderbird/ | `sudo apt-get install thunderbird` | `sudo apt-get purge thunderbird` |
| Evolution | 提供邮件收发、日历和通讯录的个人信息解决方案 | https://wiki.gnome.org/Apps/Evolution | `sudo apt-get install evolution` | `sudo apt-get purge evolution` |
| Geary | - | - | - | - |
| Mutt | 类Unix系统下基于文本的邮件客户端 | http://www.mutt.org/ | `sudo apt-get install mutt` | `sudo apt-get purge mutt` |

## 即时聊天

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| QQ | 支持在线聊天、视频电话(Linux版暂不支持)、点对点断点续传文件的强大聊天软件 | https://im.qq.com/linuxqq/index.shtml | 下载对应的架构和软件包格式安装 | - |
| WeChat | 微信，是一个生活方式 | - | UOS用户在星火商店安装，Arch用户使用：`yay -S wechat-beta-bwarp` | - |
| Skype | 最清晰的免费网络电话，提供文字、声音和视频聊天 | https://www.skype.com/en/download-skype/skype-for-linux/ | `wget https://go.skype.com/skypeforlinux-64.deb`<br>`sudo gdebi skypeforlinux-64.deb` | `sudo dpkg -r skypeforlinux` |
| Skype WebPage | 最清晰的免费网络电话，提供文字、声音和视频聊天 | https://web.skype.com | 使用网页版本 | - |
| BearyChat | BearyChat, better communication service that brings your team on the same page | https://bearychat.com/downloads | `tar -xvf BearyChat-linux-x64.tar.gz`<br>`cd BearyChat-linux-x64/`<br>`./BearyChat` | `rm -rf BearyChat-linux-x64/ BearyChat-linux-x64.tar.gz` |
| Telegram Desktop | Fast and secure desktop app, perfectly synced with your mobile phone | https://desktop.telegram.org/ | `sudo apt-get install telegram-desktop` | `sudo apt-get purge telegram-desktop` |
| Empathy | 支持多协议的强大聊天软件 | https://wiki.gnome.org/action/show/Apps/Empathy?action=show&redirect=Empathy | `sudo apt-get install empathy` | `sudo apt-get purge empathy` |
| Pidgin | 跨平台、支持多种协议的聊天软件 | https://pidgin.im/download/linux/ | `sudo apt-get install pidgin` | `sudo apt-get purge pidgin` |
| HexChat | 跨平台的 IRC 聊天软件 | https://hexchat.github.io/downloads.html | `sudo apt-get install hexchat` | `sudo apt-get purge hexchat` |
| Corebird | Native Gtk+ Twitter client for the Linux desktop | https://github.com/baedert/corebird/releases | `sudo apt-get install corebird` | `sudo apt-get purge corebird` |

## 文件传输

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| FlareGet | 支持多协议，多线程的下载软件 | https://flareget.com/download | `sudo gdebi flareget_4.3-95_amd64.deb` | `sudo dpkg -r flareget` |
| UGet | 轻量级的全能下载管理器 | http://ugetdm.com/downloads | `sudo apt-get install uget` | `sudo apt-get purge uget` |
| Wget | 运行在命令行下的多协议下载软件 | http://www.gnu.org/software/wget/ | `sudo apt-get install wget` | `sudo apt-get purge wget` |
| Transmission | 一种BitTorrent客户端，特点是一个跨平台的后端和其上的简洁的用户界面 | http://www.transmissionbt.com/download/ | `sudo apt-get install transmission` | `sudo apt-get purge transmission` |
| qBittorrent | A BitTorrent client in Qt | https://github.com/qbittorrent/qBittorrent | `sudo apt-get install qbittorrent` | `sudo apt-get purge qbittorrent` |
| Aria2 | 运行在命令行下的轻量级下载软件 | http://sourceforge.net/projects/aria2/files/stable/aria2-1.15.2/ | `sudo apt-get install aria2` | `sudo apt-get purge aria2` |
| Filezilla | 免费、开源的最强FTP客户端软件 | https://filezilla-project.org/ | `sudo apt-get install filezilla` | `sudo apt-get purge filezilla` |

## 云存储

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| 坚果云 | 任何设备，随时随地实现文件共享 | https://www.jianguoyun.com/static/exe/installer/debian/nautilus_nutstore_amd64.deb | `sudo gdebi nautilus_nutstore_amd64.deb` | `sudo dpkg -r nautilus_nutstore` |
| Dropbox | 我用的最好的的文件托管服务 | https://www.dropbox.com/install-linux | `sudo apt install nautilus-dropbox` | `sudo apt purge nautilus-dropbox` |
| OwnCloud | The last cloud collaboration/file sharing/file syncing/data privacy platform you'll ever need | https://owncloud.org/download/#owncloud-desktop-client-linux | `sudo apt-get install owncloud-client` | `sudo apt-get remove owncloud-client` |
| Google Drive | Google巨人开发的文件存储和同步服务 | https://drive.google.com | 使用网页版本 | - |
| 百度网盘 | 记录每一份热爱，让美好永远陪伴。为你电脑/手机中的文件提供云备份、预览、分享等服务，帮你更便捷安全地管理数据 | https://pan.baidu.com/download#pan | `sudo gdebi baidunetdisk_*.deb` | `sudo dpkg -r baidunetdisk` |

## 网络支付

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| 支付宝 | 全球领先的独立第三方支付平台 | https://www.alipay.com/ | `tar -xvf aliedit.tar.gz`<br>`./aliedit.sh` | 无 |