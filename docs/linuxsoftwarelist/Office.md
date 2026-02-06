# 办公应用

## 输入法

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| ibus + pinyin/sunpinyin | 为Linux/Unix系统开发的全新输入法框架 | https://github.com/ibus/ibus/wiki | `sudo apt-get install ibus ibus-pinyin ibus-sunpinyin` | `sudo apt-get purge ibus ibus-pinyin ibus-sunpinyin` |
| fcitx + googlepinyin | 为Linux 提供的轻量的输入法框架 | https://fcitx-im.org/wiki/Fcitx | `sudo apt-get install fcitx fcitx-googlepinyin` | `sudo apt-get purge fcitx fcitx-googlepinyin` |
| fcitx + sogoupinyin | - | https://pinyin.sogou.com/ | `sudo gdebi sogoupinyin_*_amd64.deb` | `sudo dpkg -r sogoupinyin` |

## 文档阅读

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Evince | GNOME中默认的pdf阅读器 | https://wiki.gnome.org/Apps/Evince | `sudo apt-get install evince` | `sudo apt-get purge evince` |
| Okular | More than a reader | https://okular.kde.org/ | `sudo apt-get install okular` | `sudo apt-get purge okular` |
| Foxit Reader | The PDF Reader for the Connected World | https://www.foxitsoftware.com/pdf-reader/ | `tar zxvf FoxitReader.enu.setup.2.4.4.0911.x64.run.tar.gz`<br>`cd FoxitReader.enu.setup.2.4.4.0911.x64.run/`<br>`./FoxitReader.enu.setup.2.4.4.0911\(r057d814\).x64.run` | `rm -rf ~/opt/foxitsoftware/foxitreader` |

## 办公套件

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Libre Office | Ship by default | - | 系统默认安装 | - |
| WPS Office | Bringing **The World’s Best Office Experience** To Linux | https://linux.wps.cn/ | `sudo gdebi wps-office_*_amd64.deb` | `sudo dpkg -r wps-office` |

## 笔记记事

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Google Keep | Google 巨人开发的笔记服务 | https://keep.google.com/ | 使用网页版本 | - |
| WizNote | 为知笔记 | https://github.com/WizTeam/WizQTClient | - | - |
| NixNote | Evernote 开源版本 | https://sourceforge.net/projects/nevernote/ | - | - |