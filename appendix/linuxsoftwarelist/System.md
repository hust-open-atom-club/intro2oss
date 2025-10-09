# 系统管理

## 文件管理

### Nautilus

- 介绍

GNOME桌面的简单文件管理器

- 下载位置

[Files](https://wiki.gnome.org/Apps/Nautilus)

- 安装方法

```
sudo apt-get install nautilus
```

- 卸载方法

```
sudo apt-get purge nautilus
```


## 压缩打包

### FileRoller

- 介绍

GNOME桌面使用的解压工具

- 下载位置

[FileRoller](https://wiki.gnome.org/Apps/FileRoller)

- 安装方法

```
sudo apt-get install file-roller
```

- 卸载方法

```
sudo apt-get purge file-roller
```

### UnZip

- 介绍

UnZip is an extraction utility for archives compressed in .zip format

- 下载位置

[Unzip](https://packages.debian.org/buster/unzip)

- 安装方法

```
sudo apt-get install unzip
```

- 卸载方法

```
sudo apt-get purge unzip
```

### Unrar

- 介绍

WinRAR的Linux版本

- 下载位置

[官方网站](https://www.rarlab.com/)

- 安装方法

```
sudo apt-get install unrar
```

- 卸载方法

```
sudo apt-get purge unrar
```


## 虚拟机

### VMware Workstation

- 介绍

VMware Workstation Pro is the industry standard for running multiple operating systems as virtual machines (VMs) on a single Linux or Windows PC. IT professionals, developers and businesses who build, test or demo software for any device, platform or cloud rely on Workstation Pro.

- 下载位置

[官方网站](https://www.vmware.com/products/workstation-pro.html)

[下载位置](https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html)

- 安装方法

```
chmod +x VMware-Workstation-Full-*.x86_64.bundle
sudo ./VMware-Workstation-Full-*.x86_64.bundle
```

- 卸载方法

```
sudo vmware-installer -u vmware-workstation
```

### VirtualBox

- 介绍

Sun公司开发的完全开源的x86模拟器

- 下载位置

[官方网站](https://www.virtualbox.org/) [下载位置](https://www.virtualbox.org/wiki/Linux_Downloads)

- 安装方法

```
 1. Install from deb package
 Ubuntu 18.04 / 18.10 / 19.04 / Debian 10
wget https://download.virtualbox.org/virtualbox/6.0.8/virtualbox-6.0_6.0.8-130520~Ubuntu~bionic_amd64.deb -O virtualbox.deb
 Debian 9
https://download.virtualbox.org/virtualbox/6.0.8/virtualbox-6.0_6.0.8-130520~Debian~stretch_amd64.deb -O virtualbox.deb
sudo gdebi virtualbox.deb

 2. Install through software repo
sudo sh -c 'echo "deb https://download.virtualbox.org/virtualbox/debian stretch contrib" > /etc/apt/sources.list.d/virtualbox.list'
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
sudo apt-get update
sudo apt-get install virtualbox-6.0
```

- 卸载方法

```
sudo apt-get purge virtualbox-6.0
```

### Vagrant

- 介绍

Vagrant 提供了一个易于配置，可重复使用，兼容的环境，通过一个单一的工作流程来控制，帮助你和团队最大化生产力和灵活性。

- 下载位置

[官方网站](https://www.vagrantup.com/)

[下载位置](https://www.vagrantup.com/downloads.html)

- 安装方法

```
 1. install from downloaded package
wget https://releases.hashicorp.com/vagrant/2.2.2/vagrant_2.2.2_x86_64.deb
sudo gdebi vagrant_2.2.2_x86_64.deb

 2. install from apt-get
sudo apt install vagrant
```

- 卸载方法

```
 1. uninstall from downloaded package
sudo dpkg -r vagrant

 2. uninstall from apt-get
sudo apt-get purge vagrant
```

### Docker

- 介绍

Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口。

- 下载位置

[官方网站](https://www.docker.com/)

[下载位置](https://docs.docker.com/install/linux/docker-ce/debian/)

- 安装方法

```
sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
```

- 卸载方法

```
sudo apt-get purge docker-ce
```

### Boxes

- 介绍

A simple GNOME application to view, access, and manage remote and virtual systems.

- 下载位置

[官方网站](https://wiki.gnome.org/Apps/Boxes)

- 安装方法

```
sudo apt-get install gnome-boxes
```

- 卸载方法

```
sudo apt-get purge gnome-boxes
```

### QEMU & QEMU-KVM

- 介绍

The **FAST!** processor emulator


- 下载位置

[下载位置](https://www.qemu.org/download/)

- 安装方法

```
sudo apt-get install qemu qemu-kvm
```
- 卸载方法

```
sudo apt-get purge qemu qemu-kvm
```
