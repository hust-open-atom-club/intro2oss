# 📧 如何参与 QEMU 邮件列表讨论

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

以 qemu 为例，可以通过 `./scripts/get_maintainer.pl <patch-file>` 来获取发送对象和抄送对象，
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

## 补丁 Tag 规范与自动化工具

在开源社区协作中，补丁（patch）的 commit message 末尾通常会附带一组特殊的“标签”
（Trailers / Tags），用于记录补丁在审查、测试、合并过程中的参与者与状态变化。这些标签是社区
协作的“签名链”，对于追溯责任、维护补丁质量至关重要。

### 常见 Tag 规则

以下是 Linux Kernel、QEMU 等社区常用的补丁标签：

| Tag | 含义 | 使用场景 |
| --- | --- | --- |
| `Signed-off-by:` | 开发者源证书担保（Developer Certificate of Origin，简称 DCO），表示你有权提交此代码 | 必须由作者和每个转发者添加 |
| `Reviewed-by:` | 代码审查者认为该补丁正确 | 审查者 review 通过后在邮件中明确提供 |
| `Acked-by:` | 维护者/子系统负责人认可合并 | 由相关子系统 maintainer 在回复中提供 |
| `Tested-by:` | 测试者验证该补丁有效 | 他人测试通过后在邮件中明确提供 |
| `Reported-by:` | 问题最初的报告者 | 用于修复 Bug 时致谢报告者 |
| `Suggested-by:` | 方案建议者 | 若思路源自他人讨论 |
| `Co-developed-by:` | 共同开发者 | 必须与对应的 `Signed-off-by:` 配对出现 |
| `Fixes:` | 修复的旧补丁 commit | 格式 `Fixes: <sha12> ("subject")` |
| `Cc:` | 邮件抄送对象 | 希望其关注的人员 |
| `Link:` | 相关讨论链接 | 例如 lore.kernel.org 的讨论链接 |

这些标签放在 commit message 末尾的 trailer 区域，每个标签独占一行，标签之间不能有空行分隔。
例如：

```text
e1000e: Prevent crash from legacy interrupt firing after MSI-X enable

When MSI-X is enabled after legacy interrupt ...

Reported-by: Alice <alice@example.com>
Suggested-by: Bob <bob@example.com>
Signed-off-by: You <you@example.com>
Reviewed-by: Charlie <charlie@example.com>
Tested-by: Dave <dave@example.com>
```

!!! tip "顺序约定"

    一般约定 `Signed-off-by:` 按补丁流转顺序排列（作者在最前），其他 tag（如 `Reviewed-by`、
    `Tested-by`）放在对应 `Signed-off-by` 之后。`Fixes:` 通常放在正文说明之后、trailer 区域
    的开头。

### 手动添加标签

最直接的方式是使用 `git commit --amend` 或 `git rebase -i` 手动编辑 commit message，把
他人在邮件列表中回复的 tag 粘贴进去。但当一个补丁系列（patch series）有几十封邮件、几十个
`Reviewed-by` 时，手动整理非常繁琐且易出错。

### 自动化工具：b4

[b4](https://b4.docs.kernel.org/) 是 Linux Kernel 社区官方推荐的补丁管理工具。它可以从
lore.kernel.org 等公开存档中抓取补丁系列与讨论线程，并围绕“准备补丁 — 汇总 tag — 发送补丁”
的工作流，提供多条便捷命令。

安装：

```bash
pip install b4
# 或在较新的发行版上：
sudo apt install b4
```

常用命令：

```bash
# 【应用他人补丁】从 lore 拉取某个 message-id 对应的补丁系列，生成可供 git am 使用的 mbox。
# 邮件线程中他人回复的 Reviewed-by / Tested-by 等 tag 会被汇总写入 mbox 的 commit message，
# 但并不会修改你当前分支已有的 commit。典型用于 maintainer 把投递上来的补丁应用到自己分支。
b4 am <message-id-or-lore-url>

# 【更新本地补丁的 tag】作为贡献者投递了一版补丁后，收到 Reviewed-by / Tested-by 等回复时，
# 准备 v2 前切回该补丁对应的本地分支运行下列命令。b4 会抓取 lore 上的回复，把新增的 trailer
# 追加到本地对应的 commit message 中，从而避免手工整理，也避免遗漏：
b4 trailers -u

# 【准备并发送自己的补丁系列】完整的贡献者发送流程，推荐按顺序执行：
# 1) 基于当前分支创建补丁系列工作分支（后续命令默认作用于该分支）
b4 prep -n <branch-name>
# 2) 编辑 cover letter，替换其中的 EDITME 占位内容
b4 prep --edit-cover
# 3) 自动填充 To/Cc 收件人（内部会调用 get_maintainer.pl 等工具）
b4 prep --auto-to-cc
# 4) 送检：对补丁本身执行 checkpatch.pl 等检查，及时修正格式问题
b4 prep --check
# 5) 正式通过 git send-email 发送补丁系列
b4 send
```

!!! tip "如何获取 Message-Id"

    上面多条命令都依赖 `<message-id>`。Message-Id 是每封邮件在 email 头部的唯一标识，
    形如 `20240101.123456.abc@host`（以下几种获取方式中，使用时一般去掉两侧的 `<>`）。
    常见的获取方式：

    - **从 lore 页面 URL 中截取**：例如
      `https://lore.kernel.org/qemu-devel/20240101.123456.abc@host/`，其中
      `qemu-devel/` 之后、结尾斜杠之前的部分即为 Message-Id。`b4` 也支持直接把整个
      lore URL 传给它（如 `b4 am https://lore.kernel.org/qemu-devel/.../`），效果等价。
    - **从邮件原文头部读取**：在 lore 页面点击 `raw` 查看纯文本邮件，或者在邮件客户端里
      选择“查看源码 / Show source”，在头部字段中找到 `Message-Id:`，尖括号中的内容就是
      该邮件的 Message-Id。

!!! note "两种使用场景区分"

    - `b4 am` 作用于 **mbox 输出**，适合 maintainer 把他人投递的补丁应用到自己的分支，它
      **不会**修改你当前分支上已有的 commit；
    - 作为 **贡献者**准备下一版补丁（如 v2）时，应使用 `b4 trailers -u` 把他人回复中的 tag
      合并到 **本地已有的** commit 上，而不是重新 `b4 am`。

!!! warning "发送前务必完成预检"

    直接 `b4 prep -n` 后 `b4 send` 会带着**未填写的 cover letter**（含 `EDITME` 占位符）
    和**空的收件人列表**把补丁发出去，常常导致邮件被社区忽略或被邮件列表拒收。请确保在
    `b4 send` 之前依次完成 `--edit-cover`、`--auto-to-cc`、`--check` 三步。

### 自动化工具：patman

[patman](https://docs.u-boot.org/en/latest/develop/patman.html) 源自 U-Boot 社区，也被
其他项目采用。它从 commit message 中解析特殊标记（如 `Series-to:`、`Cc:` 等），自动生成
补丁、cover letter，并调用 `git send-email` 发送。

常用命令：

```bash
# 预览（-n 表示 dry-run，不实际发送）
patman send -n

# 实际发送
patman send
```

patman 还能抓取之前版本补丁收到的 review tag 自动延续到新版本补丁中，减少重复劳动。

!!! warning "重要礼仪：不要替他人添加 tag"

    `Reviewed-by:`、`Tested-by:`、`Acked-by:` 等 tag **必须**由本人在邮件列表中明确回复
    （即对方亲自写出 `Reviewed-by: Name <email>` 这一行）之后，作者才能将其加入 commit
    message。

    未经同意替别人加 tag，在社区属于严重失礼，甚至可能被视为伪造背书。正确做法是等对方在邮件
    中明确签名，再收录到下一版补丁。使用 `b4` / `patman` 这类工具的好处之一，就是它们**只会**
    识别真实邮件里出现过的 tag，既避免遗漏、也避免“代签”。

    例外：`Signed-off-by:` 是唯一可以（且必须）由你自己为自己添加的 tag，代表你对所提交代码
    的 DCO（Developer Certificate of Origin）声明。

### 小结

- 对于 Linux Kernel、QEMU 等使用 lore 存档的社区，优先推荐 `b4`；
- 对于 U-Boot 及其他项目，`patman` 是成熟选择；
- 对于少量补丁，手动维护 trailer 亦可，但务必保证格式正确、顺序合理，**且绝不替他人加 tag**。

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

[[4]: b4 官方文档](https://b4.docs.kernel.org/)

[[5]: patman 官方文档](https://docs.u-boot.org/en/latest/develop/patman.html)

[[6]: Linux Kernel Submitting Patches（trailer 约定）](https://www.kernel.org/doc/html/latest/process/submitting-patches.html#using-reported-by-tested-by-reviewed-by-suggested-by-and-fixes)