# 如何参与 QEMU 邮件列表讨论

!!! note "主要作者"

    [@Zevorn(Chao Liu)](https://github.com/zevorn)

在参与开源项目开发的过程中，向社区提交代码补丁（Patch）是常见的协作方式。许多成熟的开源项目
（如 Linux Kernel、QEMU、Git 等）采用邮件列表（Mailing List）作为主要的代码审查与交流平台。
与 GitHub Pull Request 不同，这类社区通常要求开发者通过电子邮件发送补丁。

git send-email 是 Git 提供的一个强大工具，允许你将 Git 提交直接转换为符合邮件格式的补丁并
发送到指定的邮件列表。虽然配置过程稍显复杂，但一旦设置完成，即可高效、规范地参与主流开源社区的
协作。

本文将详细介绍如何在 Ubuntu 系统下安装、配置 git send-email，并使用它向 QEMU 上游提交补丁，
以及参加邮件讨论。

## 安装 Git Email

ubuntu 默认不会安装完全版的 git，因此需要我们在安装 git 以后（ulan 默认安装了 git），
再安装 git-email :

```bash
sudo apt update
sudo apt install git-email
```

如果安装失败，比如遇到下面的问题：

![](https://www.nanocode.cn/wiki/uploads/youlan/images/m_23df7dcad0d38d698c99288a1e7e375e_r.jpeg)

可以手动添加 Git 官方的 PPA，再次安装：

```bash
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git-email
```

该 PPA 由 Git 社区维护，提供最新稳定版 Git 及其扩展组件，推荐长期使用。

## 配置 Git Email

首先我们需要准备一个邮箱，笔者使用的是 yeah.net 邮箱，另外 qq /foxmail 邮箱、网易邮箱、腾讯
企业邮箱等等也是可以的。

> PS: 如果是国内环境，不推荐使用 google 邮箱，需要翻墙。

需要开启邮箱的 smtp 服务，这个可以 google 找一下教程。注意事项如下：

	- 有一些邮箱会为第三方客户端设置独立的密码，这个需要先 copy 下来，后面需要用;
	- 需要关注邮箱支持的 smtp 加密协议是 stl 还是 ssl,或者都支持，这个后续配置的时候要用到。

配置 git email 绑定自己的邮箱，这里推荐使用命令行，而不是直接修改 .gitconfig，避免配置出错：

```bash
git config --global sendemail.smtpEncryption <ssl or stl>
git config --global sendemail.smtpServer <your smtp address>
git config --global sendemail.smtpServerPort 587
git config --global sendemail.smtpUser <your email>
git config --global sendemail.smtpPass = <your pass or smtp pass>
```

上述命令中的 `<>` 内部的部分，需要你按照自己的实际邮箱信息来填写。

配置完毕以后，可以 `cat ~/.gitconfig` 检查一下：

```bash
[sendemail]
        smtpEncryption = <ssl or stl>
        smtpServer = <your smtp address>
        smtpServerPort = 587
        smtpUser = <your email>
        smtpPass = *****
```

!!! tip "安全提示"

    `.gitconfig` 中明文存储密码存在安全风险。若担心泄露，可考虑使用凭据助手或在每次发送时手
    动输入密码（添加 --smtp-pass 参数交互输入）。

## 编辑补丁与发送

常用的补丁生成命令：

```bash
git format-patch HEAD~<number>     \
    --subject-prefix="your prefix" \
    --thread                       \
    --cover-letter                 \
    -s
```

- `--subject-prefix=`，可以为补丁插入统一的 prefix，一般写 PATCH or RFC 或者组合;
- `--cover-letter` 生成一个序号为 0 的抬头文件，可以编辑它，增加一些补丁说明；
- `-s` 为补丁插入邮箱签名

发送邮件到邮件列表的命令如下：

以 qemu 为例，可以通过 `./script/get_maintainer.pl <patch-file>` 来获取发送对象和抄送对象，
具体发送邮件补丁的命令如下：

```bash
git send-email   \
    --to=<email> \
    --cc=<email> \
    <your-patch>
```

邮件发送成功以后，终端会输出：

```
Result: 250
```

如果发送失败，可以在 git send-email 后面的参数选项里增加 `--smtp-debug 1` 排查失败原因。

> PS: 首次发送邮件，可以先发送给自己的邮箱，检查能否正常发送。有些开源社区邮件列表，第一次向其
发邮件，社区需要审核，如果没有在邮件列表中看到自己的邮件，请耐心等待一下。

回复邮件，可以参考这篇文章：[正确使用邮件列表参与开源社区的协作][2]。

[1]: https://www.nanocode.cn/wiki/docs/youlan/youlan-1g2mb8qr3al59
[2]: https://tinylab.org/mailing-list-intro/
