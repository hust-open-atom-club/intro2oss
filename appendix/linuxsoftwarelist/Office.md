# 办公应用

## 输入法

### ibus + pinyin/sunpinyin

- 介绍

为 Linux/Unix 系统开发的全新输入法框架

- 下载位置

[官方网站](https://github.com/ibus/ibus/wiki)

- 安装方法

```
sudo apt-get install ibus ibus-pinyin ibus-sunpinyin
```

- 卸载方法

```
sudo apt-get purge ibus ibus-pinyin ibus-sunpinyin
```


### fcitx + googlepinyin

- 介绍

为 Linux 提供的轻量的输入法框架

- 下载位置

[官方网站](https://fcitx-im.org/wiki/Fcitx)

- 安装方法

```
sudo apt-get install fcitx fcitx-googlepinyin
```

- 卸载方法

```
sudo apt-get purge fcitx fcitx-googlepinyin
```


### fcitx + sogoupinyin

- 介绍

- 下载位置

[官方网站](https://pinyin.sogou.com/)

[下载位置](https://pinyin.sogou.com/linux/?r=pinyin)

- 安装方法

```
sudo gdebi sogoupinyin_*_amd64.deb
```

- 卸载方法

```
sudo dpkg -r sogoupinyin
```

## 文档阅读

### Evince

- 介绍

GNOME 中默认的 pdf 阅读器

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/Evince)

- 安装方法

```
sudo apt-get install evince
```

- 卸载方法

```
sudo apt-get purge evince
```

### Okular

- 介绍

More than a reader

- 下载位置

[官方网站](https://okular.kde.org/)

- 安装方法

```
sudo apt-get install okular
```

- 卸载方法

```
sudo apt-get purge okular
```

### Foxit Reader

- 介绍

The PDF Reader for the Connected World

- 下载位置

[下载位置](https://www.foxitsoftware.com/pdf-reader/)

- 安装方法

```
tar zxvf FoxitReader.enu.setup.2.4.4.0911.x64.run.tar.gz
cd FoxitReader.enu.setup.2.4.4.0911.x64.run/
./FoxitReader.enu.setup.2.4.4.0911\(r057d814\).x64.run
```

- 卸载方法

```
rm -rf ~/opt/foxitsoftware/foxitreader
```

## 办公套件

### Libre Office

Ship by default

### WPS Office

- 介绍

Bringing **The World’s Best Office Experience** To Linux

- 下载位置

[下载位置](https://linux.wps.cn/)，点击对应的架构与包格式（如 X64）下载对应的安装包

- 安装方法

```
sudo gdebi wps-office_*_amd64.deb
```

- 卸载方法

```
sudo dpkg -r wps-office
```

## 笔记记事

### Google Keep

- 介绍

Google 巨人开发的笔记服务

- 下载位置

[网页](https://keep.google.com/)

### WizNote

为知笔记 [linux 版源代码](https://github.com/WizTeam/WizQTClient)

### NixNote

[Evernote 开源版本](https://sourceforge.net/projects/nevernote/)
