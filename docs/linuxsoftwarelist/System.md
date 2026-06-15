# 系统管理

## 文件管理

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| Nautilus | GNOME桌面的简单文件管理器 | <https://wiki.gnome.org/Apps/Nautilus> | `sudo apt-get install nautilus` | `sudo apt-get purge nautilus` |

## 压缩打包

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| FileRoller | GNOME桌面使用的解压工具 | <https://wiki.gnome.org/Apps/FileRoller> | `sudo apt-get install file-roller` | `sudo apt-get purge file-roller` |
| UnZip | UnZip is an extraction utility for archives compressed in .zip format | <https://packages.debian.org/buster/unzip> | `sudo apt-get install unzip` | `sudo apt-get purge unzip` |
| Unrar | WinRAR的Linux版本 | <https://www.rarlab.com/> | `sudo apt-get install unrar` | `sudo apt-get purge unrar` |

## 虚拟机

| 软件名称 | 简介 | 官网 | 安装方式 | 卸载方式 |
| -------- | ---- | ---- | ---- | -------- |
| VMware Workstation | VMware Workstation Pro is the industry standard for running multiple operating systems as virtual machines (VMs) on a single Linux or Windows PC. IT professionals, developers and businesses who build, test or demo software for any device, platform or cloud rely on Workstation Pro. | <https://www.vmware.com/products/workstation-pro.html> | `chmod +x VMware-Workstation-Full-*.x86_64.bundle`<br>`sudo ./VMware-Workstation-Full-*.x86_64.bundle` | `sudo vmware-installer -u vmware-workstation` |
| VirtualBox | Sun公司开发的完全开源的x86模拟器 | <https://www.virtualbox.org/> | `sudo apt-get install virtualbox-6.0` | `sudo apt-get purge virtualbox-6.0` |
| Vagrant | Vagrant 提供了一个易于配置，可重复使用，兼容的环境，通过一个单一的工作流程来控制，帮助你和团队最大化生产力和灵活性 | <https://www.vagrantup.com/> | `sudo apt install vagrant` | `sudo apt-get purge vagrant` |
| Docker | Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口 | <https://www.docker.com/> | `sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common`<br>`curl -fsSL https://download.docker.com/linux/debian/gpg \| sudo apt-key add -`<br>`sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"`<br>`sudo apt-get update`<br>`sudo apt-get install docker-ce` | `sudo apt-get purge docker-ce` |
| Boxes | A simple GNOME application to view, access, and manage remote and virtual systems | <https://wiki.gnome.org/Apps/Boxes> | `sudo apt-get install gnome-boxes` | `sudo apt-get purge gnome-boxes` |
| QEMU & QEMU-KVM | The **FAST!** processor emulator | <https://www.qemu.org/download/> | `sudo apt-get install qemu qemu-kvm` | `sudo apt-get purge qemu qemu-kvm` |
