# QEMU 基础

!!! note "主要作者"

    [@Zevorn(Chao Liu)](https://github.com/zevorn)

## QEMU 介绍

QEMU（Quick Emulator）是一个开源的通用机器模拟器和虚拟化工具，最初由 Fabrice Bellard 开发。它主要通过动态二进制翻译（使用 TCG - Tiny Code Generator）来模拟多种 CPU 架构（如 x86、ARM、RISC-V 等），使客户程序或操作系统能在不同硬件平台上运行。

QEMU 支持两种主要模式：用户模式仿真（User Mode Emulation）允许在宿主机上直接运行跨架构的二进制程序；全系统仿真（Full System Emulation）则模拟完整的硬件环境（包括 CPU、内存和外设），以启动客户操作系统。

此外，QEMU 可结合硬件加速器（如 KVM、Xen）提升性能，实现近原生速度的虚拟化。

QEMU 具备高度可配置性，能模拟丰富的外设（如磁盘、网络卡、UART 等），并支持灵活的内存管理、快照和迁移功能。它广泛应用于云计算、嵌入式开发、软件测试、芯片功能验证和教育等领域，目前已成为虚拟化领域的标准工具之一。官网为 https://www.qemu.org/ 。

!!! note "QEMU 开源协作"

    QEMU 项目采用基于邮件列表的开源协作流程（类似 kernel），所有的开发、讨论和补丁提交都通过邮件列表进行。

    你可以在 [QEMU 邮件列表](https://lists.nongnu.org/archive/html/qemu-devel/) 上订阅并参与讨论。

## QEMU 安装

下面以 Ubuntu 22.04 为例，介绍如何安装 QEMU 开发环境。

### 从软件包安装 QEMU

```bash
sudo apt update
sudo apt install qemu-system-misc
```

可以使用如下命令验证是否安装成功：

```bash
qemu-system-riscv64 --version
```

### 从源码编译安装 QEMU

```bash
# 备份 sources.list 文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 启用 deb-src 源（将所有 deb 源对应的 deb-src 源解锁）
sudo sed -i '/^# deb-src /s/^# //' /etc/apt/sources.list
sudo apt-get update
sudo apt update && sudo apt build-dep qemu

# 拉取 QEMU 代码（可以从 github、gitlab、gitee 等平台拉取，也可以直接从 QEMU 官方下载源码）
git clone git@gitlab.com:qemu-project/qemu.git

cd qemu

# 这里以配置 RISC-V 架构的全系统仿真为例
./configure --target-list=riscv64-softmmu

# 编译 QEMU
make -j$(nproc)
```

可以使用如下命令验证是否编译成功：

```bash
./qemu/build/qemu-system-riscv64 --version
```

## QEMU 使用

我们以模拟 RISC-V 架构的全系统仿真为例，展示如何使用 QEMU。

基本思路是采用 QEMU 软件模拟一个 RISCV SoC（virt Machine），在上面运行 Ubuntu 发行版。

### 基本环境准备

以宿主机（x86-64）为 Ubuntu 操作系统环境为例，需要安装以下几款软件包：

```bash
sudo apt update
sudo apt install opensbi qemu-system-misc u-boot-qemu
```

另外我们还需要准备一个 RISC-V 版本的 Ubuntu 镜像，用于模拟 RISC-V 硬件虚拟化的使用环境。

直接在 [Ubuntu 官网](https://ubuntu.com/download/risc-v) 下载即可（请自己尝试 STFW 获取），这里推荐使用 preinstalled 版本，不需要自己手动安装操作系统。

镜像下载好以后，需要解压和扩容：

```bash
# 解压下载好的镜像
xz -dk ubuntu-24.04.2-preinstalled-server-riscv64.img.xz

# 镜像扩容
qemu-img resize -f raw ubuntu-24.04-preinstalled-server-riscv64.img +5G
```

使用如下命令启动 RISC-V Ubuntu 镜像：

```bash
qemu-system-riscv64 \
    -machine virt -nographic -m 4096 -smp 32 \
    -kernel /usr/lib/u-boot/qemu-riscv64_smode/uboot.elf \
    -device virtio-net-device,netdev=eth0 \
    -netdev user,id=eth0,hostfwd=tcp::2222-:22 \
    -device virtio-rng-pci \
    -drive file=ubuntu-25.04-preinstalled-server-riscv64.img,format=raw,if=virtio
```

下面对每个配置项进行详解：

* `-machine virt` 这里我们配置了 virt Machine 来运行客户机操作系统（virt 默认开启了对 H 扩展的支持）。

* `-nographic` 不需要图形界面，通过命令行终端打印客户机串口输出，并允许人机交互 (先按下 ctrl + a, 再按下 c 进入)。

* `-m 4096 -smp 32` 分配 4G 内存，32 个核心（u-boot 最大支持数量）。

* `-kernel /.../uboot.elf` 我们通过 U-Boot 来引导 kernel。

* `-device virtio-net-device,netdev=eth0` 高性能半虚拟化网卡（基于 VirtIO 标准），绑定到名为 eth0 的后端网络设备。

* `-netdev user,id=eth0,hostfwd=tcp::2222-:22` 使用 QEMU 内置的用户模式网络栈（无需主机网桥），并把客户机的 22 端口映射到宿主机的 2222 端口，以便通过 ssh 等远程连接工具访问虚拟机。

* `-device virtio-rng-pci` 基于 PCI 的虚拟随机数生成器（RNG），Linux 内核需加载 virtio_rng 驱动

* `-drive file=ubuntu-riscv64.img,format=raw,if=virtio` 加载磁盘镜像

!!! note "启动提示"

    QEMU 启动 RISC-V 的第一阶段 boot 是 OpenSBI，在 7.0 版本以前需要通过 -bios 选项指定，后续高版本，QEMU 默认自动加载，无需手动指定。第二阶段，才是 U-Boot。

以上命令不必强制记忆，可以通过 qemu 的 help 命令查询。一般在生产环境，我们会使用脚本或者交互更友好的中间件或者上层软件来操作，比如 libvirt。

### 配置 RISC-V Ubuntu

成功启动 Ubuntu 以后，将会看到以下打印信息，我们使用默认的用户名 ubuntu 来登录，并修改初始密码 ubuntu 为你需要的密码，操作如下：

```bash
...
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Reached target getty.target - Login Prompts.
Ubuntu 25.04 ubuntu ttyS0
ubuntu login: ubuntu # 输入用户名
Password: ubuntu # 输入密码，之后会提示你修改初始密码
...
Welcome to Ubuntu 25.04 (GNU/Linux 6.14.0-13-generic riscv64)
```

!!! note "登录提示"

    这里我们使用默认的用户名 ubuntu 来登录，密码也为 ubuntu。你可以根据需要修改用户名和密码。

这样，我们就可以正常在 QEMU 中使用这个系统了。

## 参考资料

[[1]: QEMU 官方文档](https://www.qemu.org/docs/master/system/index.html)

[[2]: 模拟 RISCV 虚拟化](https://gevico.github.io/learning-qemu-docs/ch2/sec7/emulate-rvh/)