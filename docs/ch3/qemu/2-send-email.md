# 如何参与 QEMU 邮件列表讨论

!!! note "主要作者"

    [@Zevorn(Chao Liu)](https://github.com/zevorn)

!!! warning "环境与时效说明"

    文中命令在 Ubuntu 22.04/24.04 上验证。邮件列表协作的具体要求以目标项目当前的贡献指南为准；本节的 smtp 配置示例仅用于本地验证，请勿在文档中记录真实密码或应用专用密码。

在参与开源项目开发的过程中，向社区提交代码补丁（Patch）是常见的协作方式。许多成熟的开源项目
（如 Linux Kernel、QEMU、Git 等）采用邮件列表（Mailing List）作为主要的代码审查与交流平台。
与 GitHub Pull Request 不同，这类社区通常要求开发者通过电子邮件发送补丁。

git send-email 是 Git 提供的一个强大工具，允许你将 Git 提交直接转换为符合邮件格式的补丁并
发送到指定的邮件列表。虽然配置过程稍显复杂，但一旦设置完成，即可高效、规范地参与主流开源社区的
协作。

本文将详细介绍如何在 Ubuntu 系统下安装、配置 git send-email，并使用它向 QEMU 上游提交补丁，
以及参加邮件讨论。

## 安装 Git Email

Ubuntu 默认不会安装完整版的 git（`git` 本身通常已随系统安装，但 `git-email` 需要单独安装），
因此还需要再装一次 `git-email`：

```bash
sudo apt update
sudo apt install git-email
```

如果 `apt update` 报 `Release file` 404，通常是当前发行版已经 EOL（例如 Ubuntu 23.10
`mantic`），仓库已被官方下线：请升级系统，或把镜像源换成仍在维护的版本，而不要继续使用
已下线的仓库。

??? note "典型的 apt 404 报错（已 EOL 的发行版）"

    ```text
    Err:9 https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports mantic-security Release
    404  Not Found [IP: 101.6.15.130 443]
    ...
    E: The repository 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports mantic Release' no longer has a Release file.
    N: Updating from such a repository can't be done securely, and is therefore disabled by default.
    E: The repository 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports mantic-updates Release' no longer has a Release file.
    ```

如果需要更新的 Git 版本，也可以手动添加 Git 官方的 PPA，再次安装：

```bash
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git-email
```

该 PPA 由 Git 社区维护，提供较新的稳定版 Git 及其扩展组件，推荐长期使用。

## 配置 Git Email

首先我们需要准备一个支持 SMTP 的邮箱。国内环境下推荐 **QQ 邮箱 / 163 邮箱 / 腾讯企业邮**：
它们在国内网络下连通性好，也都提供"授权码 / 应用专用密码"机制。

需要注意 Gmail：它在国内网络环境下不稳定，而且**已经不支持"低安全性应用密码"**（Less Secure
Apps）。如果确实要用 Gmail 发补丁，必须先在 Google 账号里开启两步验证，再生成一个
**应用专用密码（App Password）**，用它代替登录密码。

选定邮箱后，需要在邮箱网页端的设置里开启 SMTP 服务，并获取**应用专用密码 / 授权码**
（不是邮箱的登录密码）。各家的 SMTP 主机与端口如下，具体以服务商当前的帮助文档为准：

| 邮箱服务商 | SMTP 主机 | 端口与加密方式 | 备注 |
| --- | --- | --- | --- |
| QQ 邮箱 | `smtp.qq.com` | 465（`ssl`）/ 587（`tls`） | 需在设置中开启 SMTP 服务并获取授权码 |
| 163 邮箱 | `smtp.163.com` | 465（`ssl`） | 需开启 SMTP 服务并使用客户端授权码 |
| 腾讯企业邮 | `smtp.exmail.qq.com` | 465（`ssl`） | 使用客户端专用密码或登录密码 |
| Gmail | `smtp.gmail.com` | 465（`ssl`）/ 587（`tls`） | 需先开启两步验证并生成 App Password |

`sendemail.smtpEncryption` 只接受 `ssl`、`tls`、`none` 三个值（注意：写成 `stl` 是**拼写错误**，
Git 会直接报错拒绝）。端口与取值的对应关系如下：

| 端口 | 加密方式 | `sendemail.smtpEncryption` |
| --- | --- | --- |
| 465 | 隐式 SSL/TLS（SMTPS，连接建立即加密） | `ssl` |
| 587 | STARTTLS（先明文建连，再升级为 TLS，提交端口） | `tls` |
| 25 | STARTTLS（传统端口，服务商是否支持需确认） | `tls` |

配置 git email 绑定自己的邮箱，这里推荐使用命令行，而不是直接修改 `.gitconfig`，避免配置出错：

```bash
git config --global sendemail.smtpEncryption ssl
git config --global sendemail.smtpServer smtp.qq.com
git config --global sendemail.smtpServerPort 465
git config --global sendemail.smtpUser '<your email>'
git config --global sendemail.smtpPass '<应用专用密码>'
```

!!! tip "为什么密码要用单引号，且不能多写一个 `=`"

    密码 / 授权码里常含 `!`、`$`、`\` 等会被 shell 解释的字符，用**单引号**包住可以避免被
    shell 展开。另外 `git config` 的写法是 `key value`，中间**没有等号**：写成
    `git config --global sendemail.smtpPass = 'xxx'` 会把密码真的设成 `= xxx`，发送时认证必然失败。

上面的 `<>` 只是文档里的占位约定，实际执行时请替换成你的真实信息，并**去掉尖括号**（在 shell
里 `<`、`>` 是重定向符号，保留它们会被 shell 当成重定向而不是参数）。配置完毕以后，可以
`cat ~/.gitconfig` 检查一下：

```ini
[sendemail]
        smtpEncryption = ssl
        smtpServer = smtp.qq.com
        smtpServerPort = 465
        smtpUser = <your email>
        smtpPass = *****
```

!!! warning "不要把真实密码写进文档或仓库"

    `.gitconfig` 中明文存储密码存在安全风险，也**不要**把含密码的配置粘贴到 Issue、文档或
    聊天记录里。若担心泄露，可考虑使用凭据助手，或在每次发送时用 `--smtp-pass` 参数交互输入。

## 编辑补丁与发送

### 生成补丁

生成补丁系列时，把提交范围、版本号与输出目录一次性写清楚：

```bash
# 以 HEAD~3..HEAD 这 3 个提交生成 v2 补丁系列，输出到 outgoing/
git format-patch -v2 --cover-letter --thread --subject-prefix='PATCH' -o outgoing/ HEAD~3
```

参数说明：

- `-v2`：生成第二版补丁（Subject 前缀为 `[PATCH v2 ...]`）。初次提交时可以不写；
- `--subject-prefix='PATCH'`：为补丁插入统一的 Subject 前缀，常见取值还有 `RFC`（征求意见稿）
  或 `PATCH RFC` 这类组合，注意用引号包住；
- `--cover-letter`：额外生成序号为 `0000` 的封面信（cover letter），用于写整个补丁系列的背景、
  设计取舍与测试方法。它是**审查者读到的第一封邮件**，发送前请把模板里的占位内容替换成真实说明；
- `--thread`：让补丁系列以同一个邮件线程发送（用 `--in-reply-to` 串起来），方便审查者按顺序阅读；
- `-o outgoing/`：把生成的文件输出到 `outgoing/` 目录，避免污染工作区；

!!! warning "不要照抄 `HEAD~<number>`"

    `<` 和 `>` 在 shell 中是**重定向符号**，`git format-patch HEAD~<number>` 会被 shell 当成
    重定向而不是参数，命令直接失败。请写具体数字（如 `HEAD~3`），或使用 `main..HEAD` 这类范围
    表达式。同理，下面命令示例里所有 `<...>` 占位符都**必须用单引号包住**，否则 shell 会把尖括号
    当成重定向；唯一例外是 `--in-reply-to` 的 Message-Id——那里需要保留两侧尖括号（示例中已经用
    单引号包好）。

### 关于 DCO 与 Signed-off-by

`Signed-off-by:` 对应 **DCO（Developer Certificate of Origin，开发者源证书）**，表示你有权提交
这份代码，并且愿意以项目许可证分发它。它必须和你自己的署名一致，一般有三种落地方式：

- **提交时签名（推荐）**：`git commit -s`，Git 会自动在 commit message 末尾追加
  `Signed-off-by: 你的名字 <邮箱>`，把签名固化在提交里，后续每次 `format-patch` 都会带上；
- **让 format-patch 默认补签名**：`git config --global format.signoff true`，此后
  `git format-patch` 会自动加上该行；这是"忘记手动签名"的兜底；
- **单次补签名**：`git format-patch -s ...`。注意 `-s` 只对**当次**生成的补丁生效，如果你在多
  个版本之间来回切换、或者忘了写，很容易出现某一版缺少 `Signed-off-by:` 的情况——所以更推荐
  直接用 `git commit -s` 把签名固化在提交里。

如果补丁缺少 `Signed-off-by:`，`checkpatch.pl` 会报错，邮件列表也可能直接拒收。此时应回到提交
阶段用 `git commit --amend -s` 补签名，再重新生成补丁。

### 发送前自检三件套

邮件一旦发出就无法撤回，发送前请务必完成以下三步：

1. **`--dry-run` 预演**：只打印将要发送的邮件与收件人列表，不真正投递；
2. **`--annotate` 逐封检查**：在编辑器里逐封确认 Subject、收件人与正文，改好再放行；
3. **先发给自己**：把 `--to` 指向自己的邮箱完整跑一遍，确认能被正常收发和解析。

以 QEMU 为例，可以通过 `./scripts/get_maintainer.pl PATCH_FILE` 来获取发送对象和抄送对象，
具体发送邮件补丁的命令如下：

```bash
# 1. 预演：只显示将要发送的邮件，不实际投递
git send-email --dry-run \
    --to='<your own email>' \
    outgoing/*.patch

# 2. 逐封检查后正式发送
git send-email --annotate \
    --to='<maintainer email>' \
    --cc='<mailing list / reviewer email>' \
    outgoing/*.patch
```

发送成功以后，终端会输出：

```text
Result: 250
```

如果发送失败，可以在 git send-email 后面的参数选项里增加 `--smtp-debug 1` 排查失败原因。

!!! note "首次发送与列表审核"

    首次发送邮件，可以先发送给自己的邮箱，检查能否正常发送。有些开源社区邮件列表，第一次向其
    发邮件需要审核；如果没有立即在归档中看到自己的邮件，请耐心等待一下。

### 发 v2：新版本要另开线程

重发补丁系列时**不要**用 `--in-reply-to` 把它挂到上一版下面。[QEMU 官方提交指南](https://www.qemu.org/docs/master/devel/submitting-a-patch.html)的原文是：

> Patches are easier to find if they start a new top-level thread, rather than being buried
> in-reply-to another existing thread.
> （补丁如果开启**新的顶层线程**，会比埋在另一个已有线程里更容易被找到。）

版本的区分靠**标题里的版本号**和 cover letter 中的变更日志，而不是靠回信关系：

```bash
# 先用 format-patch 生成 v2：-v2 是 format-patch 的选项，
# 它把版本号写进标题（[PATCH v2 0/3] ...）与文件名
git format-patch -v2 --cover-letter -o outgoing/ <base>

# 再发送生成好的文件：版本号已经在文件里，发送命令不必再传 -v2
git send-email \
    --to='<maintainer email>' \
    --cc=qemu-devel@nongnu.org \
    outgoing/v2-*.patch
```

!!! tip "`-v2` 属于 `format-patch`，也可以直接交给 `send-email`"

    `git send-email` 的用法是 `git send-email [<options>] (<file>|<directory>)...` 或
    `git send-email [<options>] <format-patch-options>`——也就是说，**当参数是提交范围时，
    它可以接受 `git format-patch` 的选项**（例如直接 `git send-email -v2 <revision range>`
    让它内部调用 `format-patch`）。但本节这种"先把补丁生成到 `outgoing/`、再逐个发送文件"的
    用法中，版本号已经写进文件和标题，发送时再传 `-v2` 只是多余，容易被误读为"发送阶段才决定版本"。

要点：

- 每个版本都是**独立的顶层线程**。若把 v2 挂在 v1 下面，不同版本会混在同一线程里，Patchwork
  与审查者都难以判断哪一封才是当前版本；
- 变更日志（v1 → v2 改了什么）写在 cover letter 里，通常在 `---` 之后、diffstat 之前；
- `--in-reply-to` 的正确用途是**回复某封具体邮件**（例如回答审查意见、在某个补丁下追问），
  此时它的值取自被回复邮件的 `Message-Id`，建议连两侧尖括号一起给（形如
  `--in-reply-to='<20240101.123456.abc@host>'`）。

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
| `Fixes:` | 修复的旧补丁 commit | 格式 `Fixes: SHA12 ("subject")` |
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
# 【应用他人补丁】从 lore 拉取某个 message-id 对应的补丁系列，输出可供 git am 使用的 mbox
# 占位符必须用单引号包住：< > 在 shell 里是重定向符号，不加引号会在 b4 启动前就报语法错误
b4 am '<message-id-or-lore-url>'

# 【收录他人回复中的 tag】准备 v2 之前，切回该补丁对应的本地分支执行
b4 trailers -u

# 【准备并发送自己的补丁系列】按顺序执行下面五步
b4 prep -n '<branch-name>'   # 创建补丁系列工作分支（占位符同样要加引号）
b4 prep --edit-cover       # 编辑 cover letter，替换 EDITME 占位内容
b4 prep --auto-to-cc       # 自动填充 To/Cc 收件人
b4 prep --check            # 送检：checkpatch.pl 等检查
b4 send                    # 通过 git send-email 正式发送
```

!!! tip "如何获取 Message-Id"

    上面多条命令都依赖 `MESSAGE_ID`。Message-Id 是每封邮件在 email 头部的唯一标识，
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

    `b4 send` 之前必须依次完成 `--edit-cover`、`--auto-to-cc`、`--check`，否则会把带着
    `EDITME` 占位符和空收件人列表的补丁发出去。

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

在 QEMU、Linux Kernel 这类邮件列表社区里，回复邮件的格式要求非常明确：

- **一律采用 inline reply（引用在上、回复在下）**：先贴出被回复的那几行引用，紧跟其后写你的回复；这既不是"全部回复写在最前"的 top-post，也不是把回复堆在整封信末尾；
- **不要 top-post**（把自己要说的全部写在引用前面）——top-post 在这些社区明确不受欢迎，审查者
  需要反复上下滚动才能对上上下文；
- **不要发送 HTML 邮件**：邮件列表的过滤器通常会直接拒收，必须使用"纯文本"（plain text）格式；
- **不要重排引用层级**：保持 `>` 的层级原样，只裁剪掉与本次回复无关的部分，不要重写别人的引用。

一个合规的回复长这样：

```text
> This is a sample email.
> It changes a behavior of API x, ...
blabla ...
> API y has an issue that ...
blabla ...
```

### 方式一：直接用 lore 页面给出的命令（推荐）

以 Linux 内核官方的邮件列表存档服务 lore 为例。在 lore 页面上搜索你想要的邮件列表（比如键入
`qemu`），进入归档后搜索想回复的邮件标题，例如：

```text
e1000e: Prevent crash from legacy interrupt firing after MSI-X enable
```

打开某封邮件后，拉到页面底部，lore 会把回复所需的命令和收件人**直接列出来**：

```text
Reply instructions:

* Reply using the --to, --cc, and --in-reply-to
  switches of git-send-email(1):

  git send-email \
    --in-reply-to='CACGkMEsYDPjPBNmAd=AmZQ2AY46weFC_u8PK=+CSCuUD6W9zYg@mail.gmail.com' \
    --to=jasowang@redhat.com \
    --cc=dmitry.fleytman@gmail.com \
    --cc=qemu-devel@nongnu.org \
    /path/to/YOUR_REPLY

  https://kernel.org/pub/software/scm/git/docs/git-send-email.html

* If your mail client supports setting the In-Reply-To header
  via mailto: links, try the mailto: link
Be sure your reply has a Subject: header at the top and a blank line before the message body.
```

把 `/path/to/YOUR_REPLY` 换成你自己的回复正文文件，原样执行即可。其中 `--in-reply-to` 的值就是
被回复邮件的 `Message-Id`，**它保证你的回复挂进原线程，而不是新开一个孤立线程**。

发送成功后，终端会输出：

```text
OK. Log says:
Server: smtp.qq.com
...
Result: 250
```

这就表示邮件已经成功发出去了。

### 方式二：用 b4 回复

如果已经用 `b4` 管理补丁，可以让 b4 读取原邮件的 `Message-Id` 并直接生成回复：

```bash
# Message-Id 必须用单引号包住：去掉引号的话，shell 会把 < > 当成重定向符号直接报语法错误
b4 send --reply-to '<msgid-or-lore-url>'
```

### 方式三：用邮件客户端回复（Thunderbird）

不想订阅邮件列表、也不想手动拼 `git send-email` 命令时，可以借助邮件客户端的
**Reply to List（回复到邮件列表）** 功能。以 Thunderbird 为例：

1. lore 邮件页面底部提供 `mailto:` 链接（"If your mail client supports setting the
   In-Reply-To header via mailto: links" 那一行的 mailto 链接），点击它会唤起本地邮件客户端，
   并自动带上 `In-Reply-To` 头与原始收件人；
2. 在 Thunderbird 里也可以直接使用 `Reply to List`（回复到列表）按钮，按列表地址回复；
3. 无论走哪条路，发送前都必须把撰写格式切回**纯文本**。

对于中文版的 Thunderbird：

```text
工具 -> 账户设置 -> [账户名称] -> 通讯录 -> 取消勾选"以 HTML 格式编写消息"
```

对于英文版的 Thunderbird：

```text
Tools -> Account Settings -> [Account Name] -> Composition & Addressing -> 取消勾选 Compose messages in HTML format
```

当用纯文本格式发送邮件时取消勾选此项即可。判断正在撰写的邮件是否为纯文本格式很简单：
看【主题】下面是否出现 HTML 格式工具栏。

另外我们可以设置纯文本邮件的自动换行，方便网页端显示，以英文版为例：

```text
Settings -> General -> Config Editor -> 搜索 mailnews.wraplength，将其改为 80
```

!!! warning "再次强调：不要 top-post、不要发 HTML"

    邮件列表过滤器会拒收 HTML 邮件，top-post 在 QEMU / kernel 风格社区也不受欢迎；请始终使用
    纯文本 + inline reply。

??? note "应急方案：手动下载 raw 邮件再回复"

    只有在无法使用上述任何一种方式时，才考虑手动拼装回复。步骤：

    1. 在 lore 邮件页面点击 `raw`，保存得到纯文本格式的原始邮件；
    2. 删掉最上面一大段邮件头信息，但**保留 `Subject:` 那一行**，并在原标题前加上 `Re: `
       （`Subject: 原标题` -> `Subject: Re: 原标题`）；
    3. 用 `>` 标记引用原文，把自己的回复穿插在引用内容之间。批量加引用符号时可以用：

       ```bash
       # 只引用"头部之后"的正文：1,/^$/ 覆盖从第 1 行到第一个空行（含）的范围，
       # 因此 Subject 行与它后面那个分隔空行都保持原样，只有正文被加上 >
       sed -i -e '1,/^$/!s/^/> /' /path/to/the-patch-email
       ```

    4. 回到 lore 的邮件页面，向下滚动，页面底部会列出用 `git send-email` 回复这封邮件的完整
       命令（含 `--in-reply-to`），把 `/path/to/YOUR_REPLY` 替换为你整理好的正文文件后执行。

    手动回复方法虽然麻烦，但不要求使用者订阅邮件列表。另外注意：`mailto:` 是给邮件客户端用的
    URI scheme，不要把它写进 `git send-email` 的 `--to=` 参数里。

## 参考资料

1. [正确使用邮件列表参与开源社区的协作](https://tinylab.org/mailing-list-intro/)

2. [Linux 内核中文文档翻译规范（补丁发送相关）](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/translations/zh_CN/how-to.rst)

3. [thunderbird 发送纯文本邮件](https://www.cnblogs.com/darkmatter/p/3606819.html)

4. [b4 官方文档](https://b4.docs.kernel.org/)

5. [patman 官方文档](https://docs.u-boot.org/en/latest/develop/patman.html)

6. [Linux Kernel Submitting Patches（trailer 约定）](https://www.kernel.org/doc/html/latest/process/submitting-patches.html#using-reported-by-tested-by-reviewed-by-suggested-by-and-fixes)
