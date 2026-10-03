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

下面以 Ubuntu 22.04/24.04 为例，介绍如何安装 QEMU 开发环境。

### 前置依赖

无论选择下面哪条安装路径，都建议先把这些包一次性装好：

```bash
sudo apt update

# RISC-V 全系统仿真所需的 QEMU、固件与 U-Boot
sudo apt install opensbi qemu-system-misc u-boot-qemu
```

!!! note "为什么安装 qemu-system-misc"

    `qemu-system-riscv64` 由 `qemu-system-misc` 这个包提供，Ubuntu 上不需要（也不应该）再单独
    安装一个 `qemu-system-riscv64` 包。其中 `opensbi` 提供 OpenSBI 固件，`u-boot-qemu` 提供可在
    QEMU 上运行的 U-Boot。

### 安装路径一：直接用发行版软件包

??? note "点击展开：使用发行版软件包安装"

    上面的前置依赖装完即可使用。验证安装是否成功：

    ```bash
    qemu-system-riscv64 --version
    ```

    优点：几分钟就能跑起来。缺点：发行版仓库里的 QEMU 版本通常落后于上游，不适合跟进 QEMU
    本身的新特性，也不便于调试。

### 安装路径二：从源码编译安装

??? note "点击展开：从源码编译安装"

    ```bash
    # 1) 启用 deb-src 源码仓库，然后安装构建依赖
    #
    # Ubuntu 24.04 及以后使用 deb822 格式，仓库配置在
    # /etc/apt/sources.list.d/ubuntu.sources，/etc/apt/sources.list 里通常
    # 只有一段迁移说明。需要把该文件里的 "Types: deb" 改成
    # "Types: deb deb-src"（改之前先备份）。
    sudo cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.bak
    sudo sed -i 's/^Types: deb$/Types: deb deb-src/' /etc/apt/sources.list.d/ubuntu.sources

    # Ubuntu 22.04 及更早版本使用传统 sources.list：
    #   sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
    #   sudo sed -i '/^# deb-src /s/^# //' /etc/apt/sources.list

    sudo apt update
    sudo apt build-dep qemu

    # 2) 拉取 QEMU 代码
    git clone https://gitlab.com/qemu-project/qemu.git

    cd qemu

    # 这里以配置 RISC-V 架构的全系统仿真为例
    ./configure --target-list=riscv64-softmmu

    # 只编译 riscv64 目标，比全量编译快得多
    ninja -C build qemu-system-riscv64
    ```

    !!! note "为什么 `apt build-dep` 会找不到源码"

        `apt build-dep` 需要**源码仓库**（`deb-src` / `Types: deb-src`）。Ubuntu 24.04 的
        `/etc/apt/sources.list` 里通常只剩迁移说明，真正生效的仓库在
        `/etc/apt/sources.list.d/ubuntu.sources`，所以对旧文件执行 `sed` 不会添加任何源码仓库，
        `apt build-dep qemu` 会直接失败。修改 `Types` 行后可用下面的命令确认源码仓库已生效：

        ```bash
        apt-cache showsrc qemu | head -5
        ```

        若没有任何输出，说明源码仓库仍未启用；检查 `Types` 行并重新执行 `sudo apt update`。

    !!! tip "git clone 的几种写法"

        上面使用 HTTPS 地址，无需额外配置即可匿名拉取。如果确实要用 SSH，请先配置好 SSH key
        再使用 `git clone git@gitlab.com:qemu-project/qemu.git`；也可以使用 GitHub 上的镜像
        `https://github.com/qemu/qemu.git`。

    验证是否编译成功：

    ```bash
    ./build/qemu-system-riscv64 --version
    ```

    如果需要用 GDB 调试 QEMU 自身，可以在 configure 阶段打开调试开关：

    ```bash
    ./configure --target-list=riscv64-softmmu --enable-debug --enable-debug-tcg
    ninja -C build qemu-system-riscv64
    ```

    说明：

    - **QEMU 自 5.2 起采用 Meson/Ninja 构建系统**（[QEMU 5.2.0 官方发布公告](https://www.qemu.org/2020/12/08/qemu-5-2-0/)，2020-12-08）。
      `./configure` 负责环境检查并调用 Meson 生成构建规则，随后由 Ninja 执行构建。
      QEMU 的 Makefile 包装了 Ninja 及固件、测试等其他构建步骤，详见[官方构建系统文档](https://www.qemu.org/docs/master/devel/build-system.html)。
      本文只构建 RISC-V 模拟器，可直接使用上面的 `ninja -C build qemu-system-riscv64` 命令。
    - `--enable-debug` 保留调试符号并关闭优化，`--enable-debug-tcg` 额外为 TCG 打开断言检查，
      二者配合 GDB 调试 QEMU 源码时很有用（代价是运行明显变慢）。
    - 只做 RISC-V 相关开发时，用 `--target-list=riscv64-softmmu` 限制目标架构可以显著缩短编译时间。

## QEMU 使用

我们以模拟 RISC-V 架构的全系统仿真为例，展示如何使用 QEMU。

基本思路是采用 QEMU 软件模拟一个 RISCV SoC（virt Machine），在上面运行 Ubuntu 发行版。

### 基本环境准备

宿主机（x86-64）为 Ubuntu 操作系统环境时，软件包依赖已经在上一节的「前置依赖」里装好
（`opensbi`、`qemu-system-misc`、`u-boot-qemu`），这里不再重复安装。

接下来需要准备一个 RISC-V 版本的 Ubuntu 镜像，用于模拟 RISC-V 硬件虚拟化的使用环境。

直接在 [Ubuntu 官网](https://ubuntu.com/download/risc-v) 下载即可（请自己尝试 STFW 获取），
这里推荐使用 preinstalled 版本，不需要自己手动安装操作系统。**本文全篇统一使用 Ubuntu 24.04
LTS 的 RISC-V preinstalled 镜像** `ubuntu-24.04.2-preinstalled-server-riscv64.img.xz`；
如果你下载到的文件名与本文不同，请把下文所有命令里的文件名一起替换为你自己的文件名。

镜像下载好以后，需要解压和扩容：

```bash
# 解压下载好的镜像：xz -dk 会保留原压缩包，并输出去掉 .xz 后缀的 .img 文件
xz -dk ubuntu-24.04.2-preinstalled-server-riscv64.img.xz

# 镜像扩容：对上面解压出来的 .img 文件操作，在原有大小基础上再加 5G
qemu-img resize -f raw ubuntu-24.04.2-preinstalled-server-riscv64.img +5G
```

!!! note "关于这两个文件名"

    `xz -dk` 的输入是 `.img.xz`，输出是同名的 `.img`（去掉 `.xz` 后缀），所以下一步
    `qemu-img resize` 以及后面 `-drive file=...` 用的都应该是 `.img` 文件，而不是 `.img.xz`。
    如果误把 `.img.xz` 交给 `qemu-img` 或 QEMU，会因为「不是 raw 镜像」而报错。

使用如下命令启动 RISC-V Ubuntu 镜像：

```bash
qemu-system-riscv64 \
    -machine virt -nographic -m 4096 -smp 4 \
    -kernel /usr/lib/u-boot/qemu-riscv64_smode/uboot.elf \
    -device virtio-net-device,netdev=eth0 \
    -netdev user,id=eth0,hostfwd=tcp::2222-:22 \
    -device virtio-rng-pci \
    -drive file=ubuntu-24.04.2-preinstalled-server-riscv64.img,format=raw,if=virtio
```

下面对每个配置项进行详解：

* `-machine virt` 这里我们配置了 virt Machine 来运行客户机操作系统（virt 默认开启了对 H 扩展的支持）。

* `-nographic` 不需要图形界面，通过命令行终端打印客户机串口输出，并允许人机交互 (先按下 ctrl + a, 再按下 c 进入)。

* `-m 4096 -smp 4` 分配 4G 内存、4 个核心。这个数值请按宿主机资源调整：一般 2–4 核、2–4G 就足够启动 Server 版并完成日常练习；宿主机内存有限时给太大反而会拖慢整机。

* `-kernel /.../uboot.elf` 我们通过 U-Boot 来引导 kernel。

* `-device virtio-net-device,netdev=eth0` 高性能半虚拟化网卡（基于 VirtIO 标准），绑定到名为 eth0 的后端网络设备。

* `-netdev user,id=eth0,hostfwd=tcp::2222-:22` 使用 QEMU 内置的用户模式网络栈（无需主机网桥），并把客户机的 22 端口映射到宿主机的 2222 端口，以便通过 ssh 等远程连接工具访问虚拟机。

* `-device virtio-rng-pci` 基于 PCI 的虚拟随机数生成器（RNG），Linux 内核需加载 virtio_rng 驱动

* `-drive file=ubuntu-24.04.2-preinstalled-server-riscv64.img,format=raw,if=virtio` 加载磁盘镜像

以上命令不必强制记忆，可以通过 qemu 的 help 命令查询。一般在生产环境，我们会使用脚本或者交互更友好的中间件或者上层软件来操作，比如 libvirt。

### 配置 RISC-V Ubuntu

成功启动 Ubuntu 以后，将会看到以下打印信息，我们使用默认的用户名 ubuntu 来登录，并修改初始密码 ubuntu 为你需要的密码，操作如下：

```text
...
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Reached target getty.target - Login Prompts.
Ubuntu 24.04.2 LTS ubuntu ttyS0
ubuntu login: ubuntu  # 输入用户名
Password: ubuntu      # 输入密码，之后会提示你修改初始密码
...
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux ... riscv64)
```

!!! note "登录提示"

    这里我们使用默认的用户名 ubuntu 来登录，密码也为 ubuntu。你可以根据需要修改用户名和密码。

这样，我们就可以正常在 QEMU 中使用这个系统了。

## 启动链详解：OpenSBI → U-Boot → GRUB → Linux 内核

在 RISC-V 的 virt 机器上，一次完整的启动通常会经过 **OpenSBI → U-Boot → GRUB → Linux 内核**
几个阶段：OpenSBI 是运行在 M 模式（Machine Mode）的固件，负责最底层的中断、时钟与 SBI 调用；
它跳转到 S 模式（Supervisor Mode）的 U-Boot 之后，U-Boot 读取磁盘分区里的 GRUB，再由 GRUB
加载 Linux 内核与 initramfs。

在 QEMU 里，你可以决定"从哪一级开始交棒"，对应的就是下面三个参数：

- **`-bios <文件>`：显式指定固件（OpenSBI 或 U-Boot 的 ELF）**。适合固件版本需要与 QEMU 版本
  精确匹配、或要换成自己编译的 OpenSBI/U-Boot 的场景。注意 `virt` 机器默认就自带一份 OpenSBI
  固件，**不写 `-bios` 时 QEMU 会自动加载它**，这是当前 QEMU 的正常行为；也就是说，只有当你
  想用「别的固件」替换默认 OpenSBI 时，才需要显式写 `-bios`。
- **`-kernel <文件>`：直接把内核或 U-Boot 的 ELF/镜像交给 QEMU 加载**。最常用于两种情况：一是
  跳过固件与引导器直接启动 Linux 内核（配合 `-append` 传内核命令行，启动最快，适合内核开发）；
  二是像本文这样把 U-Boot 交给 QEMU 加载，再由 U-Boot 去引导磁盘上的发行版。
- **`-drive file=...`：纯磁盘引导**。把整块磁盘（含分区表、引导器、内核）交给固件与 U-Boot，
  最接近真实硬件的行为，也是运行发行版镜像的常规用法；此时不需要 `-kernel`。

简单记：**调试固件用 `-bios`，调试内核/引导器用 `-kernel`，验证真实发行版启动流程用 `-drive`。**

## 想给 QEMU 提补丁，从这里开始

QEMU 项目完全基于邮件列表协作（流程与 Linux 内核类似），没有 GitHub Pull Request 通道。
第一次贡献时，按下面的顺序读一遍即可：

1. **官方流程文档**：[`docs/devel/submit-a-patch-process.rst`](https://gitlab.com/qemu-project/qemu/-/blob/master/docs/devel/submit-a-patch-process.rst)
   规定了补丁格式、收件人获取方式与 Review 流程；
2. **提交前自检**：在源码树里运行 `./scripts/checkpatch.pl YOUR_PATCH`，把报告出来的格式
   问题改掉再发送；
3. **确定收件人**：运行 `./scripts/get_maintainer.pl YOUR_PATCH`，它会根据你修改的文件给出
   对应的 maintainer 与邮件列表，把结果填进 `--to` / `--cc`；
4. **发送与讨论**：本目录的 [如何参与 QEMU 邮件列表讨论](2-send-email.md) 详细介绍了
   `git send-email` 的配置、`b4` 工具链与回复邮件的礼仪。

## 参考资料

1. [QEMU 官方文档](https://www.qemu.org/docs/master/system/index.html)

2. [模拟 RISCV 虚拟化](https://gevico.github.io/learning-qemu-docs/ch2/sec7/emulate-rvh/)
