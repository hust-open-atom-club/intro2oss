# 程序开发

## 版本控制

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Git | Linus为管理Linux内核而开发的分布式版本管理工具 | <https://git-scm.com/> | `sudo apt-get install git` | `sudo apt-get purge git` |
| SVN | Apache开发的集中式版本管理工具 | <https://subversion.apache.org/> | `sudo apt-get install subversion` | `sudo apt-get purge subversion` |

## 本文编辑器

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Sublime Text | A sophisticated text editor for code, markup and prose | <https://www.sublimetext.com/> | `sudo apt-get install apt-transport-https`<br>`wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg \| sudo apt-key add -`<br>`echo "deb https://download.sublimetext.com/ apt/stable/" \| sudo tee /etc/apt/sources.list.d/sublime-text.list`<br>`sudo apt-get update`<br>`sudo apt-get install sublime-text` | `sudo apt-get purge sublime-text` |
| Visual Studio Code | 微软开发可以跨Linux，Windows，Mac OS的编辑器 | <https://code.visualstudio.com/> | `sudo apt-get install apt-transport-https`<br>`curl https://packages.microsoft.com/keys/microsoft.asc \| gpg --dearmor > microsoft.gpg`<br>`sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/`<br>`sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'`<br>`sudo apt-get update`<br>`sudo apt-get install code` | `sudo apt-get purge code` |
| gedit | GNOME桌面环境的默认文本编辑器 | <https://wiki.gnome.org/Apps/Gedit> | `sudo apt-get install gedit` | `sudo apt-get purge gedit` |
| Atom | A hackable text editor for the 21st Century | <https://atom.io/> | `curl -sL https://packagecloud.io/AtomEditor/atom/gpgkey \| sudo apt-key add -`<br>`sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'`<br>`sudo apt-get update`<br>`sudo apt-get install atom` | `sudo apt-get purge atom` |
| Vim | Unix/Linux平台下的高度可配置的文本编译器 | <https://github.com/vim/vim.git> | `sudo apt-get install vim` | `sudo apt-get purge vim` |
| Emacs | An extensible, customizable, free/libre text editor — and more | <https://www.gnu.org/software/emacs/download.html> | `sudo apt-get install emacs` | `sudo apt-get purge emacs` |
| Nano | 类Unix系统上基于命令行接口的文本编辑器 | <https://www.nano-editor.org/> | `sudo apt-get install nano` | `sudo apt-get purge nano` |

## 集成开发环境

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Eclipse IDE | - | - | - | - |
| JetBrains IDE | - | - | - | - |
| Wireshark | 世界第一以及使用最广泛的网络协议分析器 | <https://www.wireshark.org/> | `sudo apt-get install wireshark` | `sudo apt-get purge wireshark` |
| Code Blocks | Codeblocks is a cross-platform IDE built around wxWidgets, designed to be extensible and configurable | <http://www.codeblocks.org/> | `sudo apt-get install codeblocks` | `sudo apt-get purge codeblocks` |
