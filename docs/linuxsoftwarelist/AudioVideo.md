# 影音

## 音乐播放

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Spotify | Music for everyone | <https://www.spotify.com/us/download/linux/> | `curl -sS https://download.spotify.com/debian/pubkey.gpg \| sudo apt-key add -`<br>`echo "deb http://repository.spotify.com stable non-free" \| sudo tee /etc/apt/sources.list.d/spotify.list`<br>`sudo apt-get update && sudo apt-get install spotify-client` | `sudo apt-get purge spotify-client` |
| FeelUOwn | 网易云音乐的linux客户端 | <https://github.com/cosven/FeelUOwn> | 参考官网安装 | 参考官网卸载 |
| 网易云音乐官方客户端 | 网易云音乐官方Linux客户端 | <https://music.163.com/> | 参考官网安装 | 参考官网卸载 |
| Banshee | 高度自定义的音乐播放器 | <http://banshee.fm/download/> | `sudo apt-get install banshee` | `sudo apt-get purge banshee` |
| Rhythmbox | Gnome桌面默认音乐播放器 | <https://wiki.gnome.org/Apps/Rhythmbox> | `sudo apt-get install rhythmbox` | `sudo apt-get purge rhythmbox` |

## 视频播放

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| SMPlayer | 基于mplayer2的视频播放器 | <http://smplayer.sourceforge.net/> | `sudo apt-get install smplayer` | `sudo apt-get purge smplayer` |
| VLC | 全平台的自由多媒体解决方案 | <http://www.videolan.org/> | `sudo apt-get install vlc` | `sudo apt-get purge vlc` |
| mpv | 专注视频播放质量和体验 | <https://mpv.io/> | `sudo apt-get install mpv` | `sudo apt-get purge mpv` |
| KODI(原XBMC) | 全平台的媒体库解决方案 | <http://kodi.tv/download/> | `sudo add-apt-repository ppa:team-xbmc/ppa`<br>`sudo apt-get update`<br>`sudo apt-get install kodi` | `sudo apt-get purge kodi` |

注: 中文插件 [xbmc-addons-chinese](https://github.com/taxigps/xbmc-addons-chinese)

## 屏幕录制

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| SimpleScreenRecorder | 基于QT的Linux原生屏幕录制软件 | <https://www.maartenbaert.be/simplescreenrecorder/#download> | `sudo apt-get install simplescreenrecorder` | `sudo apt-get purge simplescreenrecorder` |

## 音频编辑

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Audacity | 简单易用的跨平台多轨音频编辑器 | <https://www.audacityteam.org/> | `sudo apt-get install audacity` | `sudo apt-get purge audacity` |
