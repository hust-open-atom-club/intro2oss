# 图像影音

## 音乐播放

### Spotify

- 介绍

Spotify: Music for everyone

- 下载位置

[下载](https://www.spotify.com/us/download/linux/)

- 安装方法

```
curl -sS https://download.spotify.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb http://repository.spotify.com stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list
sudo apt-get update && sudo apt-get install spotify-client
```

- 卸载方法

```
sudo apt-get purge spotify-client
```

### FeelUOwn

- 介绍

网易云音乐的linux客户端

- 下载位置

[FeelUOwn源码](https://github.com/cosven/FeelUOwn)

- 安装方法

[安装方法](https://github.com/cosven/FeelUOwn#安装方法)

### 网易云音乐官方客户端

### Banshee

- 介绍

高度自定义的音乐播放器

- 下载位置

[安装包下载](http://banshee.fm/download/)

- 安装方法

```
sudo apt-get install banshee
```

- 卸载方法

```
sudo apt-get purge banshee
```

### Rhythmbox

- 介绍

Gnome桌面中默认带的音乐播放器，提供音乐管理与播放的强大播放器

- 下载位置

[下载位置](https://wiki.gnome.org/Apps/Rhythmbox)

- 安装方法

```
sudo apt-get install rhythmbox
```

- 卸载方法

```
sudo apt-get purge rhythmbox
```

## 视频播放

### SMPlayer

- 介绍

一个基于mplayer2的视频播放器，可能是Linux下最方便的视频播放器

- 下载位置

[Download](http://smplayer.sourceforge.net/)

- 安装方法

```
sudo apt-get install smplayer
```

- 卸载方法

```
sudo apt-get purge smplayer
```

### VLC

- 介绍

全平台的自由多媒体解决方案

- 下载位置

[下载位置](http://www.videolan.org/)

- 安装方法

```
sudo apt-get install vlc
```

- 卸载方法

```
sudo apt-get purge vlc
```

### mpv

- 介绍

专注与视频播放质量和体验。GUI？我们不需要，配置文件更高效。

- 下载位置

[Official website](https://mpv.io/)

[GitHub](https://github.com/mpv-player/mpv)

- 安装方法

```
sudo apt-get install mpv
```

- 卸载方法

```
sudo apt-get purge mpv
```

### KODI(原XBMC)

- 介绍

全平台的媒体库解决方案，插件丰富是它的最大特点

- 下载位置

[Download](http://kodi.tv/download/)  

- 安装方法

```
sudo add-apt-repository ppa:team-xbmc/ppa
sudo apt-get update
sudo apt-get install kodi
```

- 卸载方法

```
sudo apt-get purge kodi
```

注: 中文插件 [xbmc-addons-chinese](https://github.com/taxigps/xbmc-addons-chinese)


## 屏幕录制

### SimpleScreenRecorder

- 介绍

基于QT的Linux原生屏幕录制软件

- 下载位置

[Download](https://www.maartenbaert.be/simplescreenrecorder/#download)  

- 安装方法

```
sudo apt-get install simplescreenrecorder
```

- 卸载方法

```
sudo apt-get purge simplescreenrecorder
```


## 音频编辑

### Audacity

- 介绍

简单易用的跨平台多轨音频编辑器

- 下载位置

[官方网站](https://www.audacityteam.org/)

- 安装方法

```
sudo apt-get install audacity
```

- 卸载方法

```
sudo apt-get purge audacity
```


## 图像浏览

### Eye of GNOME(EOG)

- 介绍

Gnome桌面中默认的图片查看器

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/EyeOfGnome)

- 安装方法

```
sudo apt-get install eog
```

- 卸载方法

```
sudo apt-get purge eog
```

### gThumb

- 介绍

Gnome桌面中的图片查看器及浏览器

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/gthumb)

- 安装方法

```
sudo apt-get install gthumb
```

- 卸载方法

```
sudo apt-get purge gthumb
```


## 图像编辑

### GIMP

- 介绍

支持多种操作系统（Linux，Windows，MacOS等）的跨平台的图片编辑软件

- 下载位置

[官方网站](https://www.gimp.org/)

- 安装方法

```
sudo apt-get install gimp
```

- 卸载方法

```
sudo apt-get purge gimp
```

### Inkscape

- 介绍

支持多种操作系统（Linux，Windows，MacOS）的矢量图片编辑软件

- 下载位置

[官方网站](https://inkscape.org/)

- 安装方法

```
sudo apt-get install inkscape
```

- 卸载方法

```
sudo apt-get purge inkscape
```


## 截图工具

### shutter

- 介绍

Shutter is a feature-rich screenshot program for Linux based operating systems.

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/gthumb)

- 安装方法

```
sudo apt-get install shutter
```

- 卸载方法

```
sudo apt-get purge shutter
```

### Gnome Screenshot

- 介绍

GNOME Screenshot is a small utility that takes a screenshot of the whole desktop; the currently focused window; or an area of the screen.

- 下载位置

[官方网站](https://github.com/GNOME/gnome-screenshot)

- 安装方法

```
sudo apt-get install gnome-screenshot
```

- 卸载方法

```
sudo apt-get purge gnome-screenshot
```


## 画图工具

### Dia

- 介绍

GNOME桌面环境中的画图软件

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/Dia)

- 安装方法

```
sudo apt-get install dia
```

- 卸载方法

```
sudo apt-get purge dia
```
