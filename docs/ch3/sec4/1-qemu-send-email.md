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

```bash
Err:9 https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports mantic-security Release
404  Not Found [IP: 101.6.15.130 443]
Hit:10 https://ppa.launchpadcontent.net/obsproject/obs-studio/ubuntu mantic InRelease
Hit:11 https://repo.waydro.id mantic InRelease
Reading package lists... Done

E: The repository 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports mantic Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
E: The repository 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports mantic-updates Release' no longer has a Release file.
...
```
可以手动添加 Git 官方的 PPA，再次安装：

```bash
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git-email
```

该 PPA 由 Git 社区维护，提供最新稳定版 Git 及其扩展组件，推荐长期使用。

## 配置 Git Email

首先我们需要准备一个邮箱，笔者使用的是 yeah.net 邮箱，另外 qq/foxmail 邮箱、网易邮箱、腾讯
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

!!! note

    首次发送邮件，可以先发送给自己的邮箱，检查能否正常发送。有些开源社区邮件列表，第一次向其发
    邮件，社区需要审核，如果没有在邮件列表中看到自己的邮件，请耐心等待一下。

## 回复邮件

**手动回复邮件**

手动回复邮件，也可以使用 git send-email 进行操作。且邮件格式须为“纯文本”格式。回复别人的邮件
时，需要引用。一般使用符号 > 作为标记。

在 QEMU 社区回复别人邮件，可以选择回复内容在顶部，下面放引用内容。即所谓“Top-Post”的方式。

但现在更习惯，先贴引用内容，然后在下面写回复。

两种方式都可以，但更推荐第二种，我们以此为例，进行展示：

```
> This is a sample email.
> It changes a behavior of API x, ...
blabla ...
> API y has an issue that ...
blabla ...
```

我们可以使用 Linux 内核官方的邮件列表存档服务 lore 为例，进行说明。

首先在 lore 页面上搜索你想要的邮件列表，比如在搜索框键入 qemu，点击返回的 链接 进入，然后搜素
自己想回的邮件标题，比如搜索：

```
e1000e: Prevent crash from legacy interrupt firing after MSI-X enable
```
会返回几个结果，定位到自己想回的某封邮件，点击进去以后，搜索 raw 并点击保存得到纯文本格式的原始邮件。

接下来是编辑保存的文件：

1. 删掉最上面的一大片的邮件头信息

2. 保留邮件标题所在的行，并在原标题前面加上 Re: 即可

    ``` “Subject: 原标题” -> "Subject: Re: 原标题" ```

3. 用符号标记 > 引用原文，自己回复的内容穿插于引用的内容之间，可以批量替换：

    ``` sed -i -e 's/^/> /g' /path/to/the-patch-email ```

    注意：不要替换 Subject 所在邮件标题行

最后我们回到 lore 的邮件页面，向下滚动，页面底部列出了用 git send-email 命令来回复这封邮件的命令：

```
  git send-email \
    --in-reply-to='CACGkMEsYDPjPBNmAd=AmZQ2AY46weFC_u8PK=+CSCuUD6W9zYg@mail.gmail.com' \
    --to=jasowang@redhat.com \
    --cc=dmitry.fleytman@gmail.com \
    --cc=lvivier@redhat.com \
    --cc=michael.roth@amd.com \
    --cc=odaki@rsg.ci.i.u-tokyo.ac.jp \
    --cc=philmd@linaro.org \
    --cc=qemu-devel@nongnu.org \
    --cc=stefanha@redhat.com \
    --cc=thuth@redhat.com \
    /path/to/YOUR_REPLY
```
发送成功后，见到

```
OK. Log says:
Server: smtp.gmail.com
...
Result: 250
```

就表示邮件已经成功地发送出去了。

手动回复方法虽然麻烦，但不要求使用者订阅邮件列表。

**邮箱客户端回复邮件**

邮前多数使用 UI 邮件客户端的默认格式都已经是 HTML 了，因此从客户端撰写邮件的时候需要注意切换成
文本格式。我们以 Thunderbird 为例，修改邮件格式（plain text 或者 html 格式）。

对于中文版的 Thunderbird：

```
[工具 -> 账户设置 -> [账户名称] -> 通讯录] -> “以 HTML 格式编写消息”
```
对于英文版的 Thunderbird：

```
Tools -> Account Settings -> [Account Name] -> Composition & Addressing -> Compose messages in HTML format
```

当用纯文本格式发送邮件时取消勾选此项即可，判断正在撰写的邮件是否为纯文本格式很简单，
看【主题】下面是否有 HTML 格式工具栏即可。

另外我们可以设置邮件列表的自动换行，方便网页端显示，我们以英文版本为例：

```
Settings -> Gernal -> Config Editor -> 搜索：mailnews.wraplength，将其改为 80
```

大部分邮件列表，都支持 maito:link 操作，这样可以直接唤起本地邮箱客户端，进行邮件的快捷回复。

我们以 lore.kernel.org 为例，下面是一封示例邮件，一般拉到邮件的末尾，会有一个 reply 选项：

```
...
     prev parent reply(首先点击这个)	other threads:[~2025-08-18  2:09 UTC|newest]
---

Thread overview: 3+ messages / expand[flat|nested]  mbox.gz  Atom feed  top
2025-08-07 11:08 [PATCH v2] e1000e: Prevent crash from legacy interrupt firing after MSI-X enable Laurent 
...
Reply instructions:

...

* Reply using the --to, --cc, and --in-reply-to
  switches of git-send-email(1):

  git send-email \
    --in-reply-to='CACGkMEsYDPjPBNmAd=AmZQ2AY46weFC_u8PK=+CSCuUD6W9zYg@mail.gmail.com' \
    --to=jasowang@redhat.com \
    --cc=dmitry.fleytman@gmail.com \
    ...
    /path/to/YOUR_REPLY

  https://kernel.org/pub/software/scm/git/docs/git-send-email.html

* If your mail client supports setting the In-Reply-To header
  via mailto: links, try the mailto: link （然后点击这个）
Be sure your reply has a Subject: header at the top and a blank line before the message body.
```

最后找到 `mailto: link` 点击它会自动使用本地邮箱客户端，比如使用 Thunderbird 回复邮件。

## 参考资料

[[1]: 正确使用邮件列表参与开源社区的协作](https://tinylab.org/mailing-list-intro/)

[[2]: Linux 内核中文文档翻译规范（补丁发送相关）](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/translations/zh_CN/how-to.rst)

[[3]: thunderbird 发送纯文本邮件](https://www.cnblogs.com/darkmatter/p/3606819.html)
