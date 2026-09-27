# Git 基础配置

## 学习目标

完成本节后，你应当能够：

1. 配置 Git 的用户名、邮箱和默认分支名，并用 `git config` 查看当前配置；
2. 用 SSH 密钥或 Personal Access Token（PAT）安全地访问远程仓库；
3. 初始化、克隆仓库并用 `git status` 判断仓库当前状态。

---

## 1. 配置 Git

在使用 Git 之前，首先需要进行一些基本的配置，包括设置用户名和邮箱。这些信息会与每次提交（Commit）关联，用于标识代码的贡献者。

### 打开终端（Terminal）

如果你使用的是 Windows：

- 推荐安装 [Git for Windows](https://git-scm.com/download/win)，安装后你会获得一个名为 **Git Bash** 的终端工具，点击即可使用。

如果你使用的是 macOS 或 Linux：

- 打开自带的 **Terminal** 应用程序即可。

安装完成后，就可以输入下面步骤的命令进行 Git 的基础配置

### 配置用户名和邮箱

- **命令**：

  ```bash
  git config --global user.name "你的用户名"
  git config --global user.email "你的邮箱"
  ```

  ```bash
  # 正确示例
  git config --global user.name "John Doe"
  git config --global user.email "john.doe@example.com"
  # 错误示例（用户名中有空格时必须加引号）
  git config --global user.name John Doe  # 错误！
  ```

  上面那条错误命令报错或写入错误的值，真正的原因是 **shell 会先按空格把参数拆开**：`John` 和 `Doe` 变成了两个彼此独立的参数，`git config` 只把 `John` 当作 `user.name` 的值，再把 `Doe` 当成一个无法识别的多余参数。加引号是为了阻止 shell 拆分，而不是 Git 本身要求“引号”这种语法。

- **作用**：
  - `user.name`：设置提交代码时显示的作者名称。
  - `user.email`：设置提交代码时显示的作者邮箱。
  - `--global`：表示全局配置，适用于当前用户的所有仓库。如果只想为某个仓库单独配置，可以去掉 `--global` 参数。

- **提示**
  - 如果你不希望暴露自己的真实邮箱，可以使用 GitHub 提供的隐私邮箱（形如 `用户名@users.noreply.github.com`）
  - 查看方法：登录 GitHub，进入 **Settings -> Emails**，可以找到你的隐私邮箱地址。

### 设置默认分支名

- **命令**（需要 Git 2.28 及以上版本）：

  ```bash
  git config --global init.defaultBranch main
  ```

- **作用**：让 `git init` 新建的仓库默认使用 `main` 作为初始分支名，避免每次都被提示 `master` 与 `main` 不一致。
- **注意**：分支名只是约定。老项目仍可能叫 `master`，参与已有项目时以目标仓库的实际分支名为准，可以用 `git branch -a` 或平台页面确认。

### 查看配置信息

- **命令**：

  ```bash
  git config --list
  ```

- **作用**：查看当前 Git 的所有配置信息，包括用户名、邮箱等。

### 查看帮助

- **比如我想看看 merge 是个什么玩意**：

  ```bash
  git help merge 
  git merge --help
  man git-merge
  ```

---

## 2. 连接远程仓库：SSH 与 Personal Access Token（PAT）

SSH（Secure Shell）是一种加密的网络协议，用于安全地访问远程服务器。通过 SSH 连接 Git 远程仓库，可以避免每次操作时输入用户名和密码，同时提高数据传输的安全性。

### 生成 SSH 密钥

#### 什么是 SSH 密钥？

SSH 密钥是一个由“私钥 + 公钥”组成的安全认证方式，类似于“锁和钥匙”。你将公钥添加到 GitHub 账户后，GitHub 就知道“这个钥匙是你自己的”，从而允许你访问代码仓库，无需每次都输入用户名密码。

```mermaid
graph LR
    A[你的电脑] -->|生成密钥对| B[私钥 id_ed25519]
    A -->|生成密钥对| C[公钥 id_ed25519.pub]
    C -->|添加到| D[GitHub 账户]
    A -->|使用私钥认证| E[GitHub 服务器]
    E -->|验证公钥匹配| D
```

1. **检查是否已有 SSH 密钥**：
  
    打开终端，输入以下命令：

    ```bash
    ls ~/.ssh/
    ```

    如果看到 id_ed25519 和 id_ed25519.pub 文件，说明已有密钥

    在文件管理器中查看路径：C:/Users/你的用户名/.ssh/ (Windows) 或 /home/你的用户名/.ssh/ (macOS/Linux)

2. **生成新的 SSH 密钥**：

    如果不存在 SSH 密钥，可以使用以下命令生成：

     ```bash
     ssh-keygen -t ed25519 -C "你的邮箱"
     ```

    按提示选择保存路径和设置密码（可选）。

    生成成功后，会在 `~/.ssh/` 目录下生成两个文件：

    - `id_ed25519`：私钥，切勿泄露。

    - `id_ed25519.pub`：公钥，用于添加到远程仓库。

3. **添加到 ssh-agent**：

     ```bash
     eval "$(ssh-agent -s)"
     ssh-add ~/.ssh/id_ed25519
     ```

### 添加 SSH 密钥到远程仓库

1. **复制公钥**：

    使用以下命令复制公钥内容：

    ```bash
     cat ~/.ssh/id_ed25519.pub
    ```

    复制输出的全部内容。

2. **添加到 GitHub**：

    1.登录 GitHub，进入 **Settings** -> **SSH and GPG keys**

    2.点击 **New SSH key**

    3.在 Title 中输入设备名称（如 "My Laptop"）

    4.在 Key 字段粘贴公钥内容

    5.点击 **Add SSH key**

### 测试 SSH 连接

- 使用以下命令测试 SSH 连接是否成功：

  ```bash
  ssh -T git@github.com
  ```

  - 如果显示 `Hi 用户名! You've successfully authenticated ...`，说明 SSH 配置成功。

```mermaid
flowchart TD
    A[执行 ssh -T git@github.com] --> B{连接成功?}
    B -->|是| C[显示欢迎消息]
    B -->|否| D[检查密钥是否添加]
    D --> E[检查ssh-agent是否运行]
    E --> F[尝试不同端口]
    F --> G[检查网络/代理设置]
    G --> H[查看详细日志 ssh -vT]
```

#### 如果测试失败怎么办？

- 确保你生成了 SSH 密钥并添加到了 GitHub。
- 检查是否执行了 `ssh-add ~/.ssh/id_ed25519`。
- 有时 Git Bash 或 WSL 可能未自动启动 ssh-agent，可以先执行：

  ```bash
  eval "$(ssh-agent -s)"
  ```

- 如果还是失败，可以在终端中运行以下命令查看调试信息：

  ```bash
  ssh -vT git@github.com
  ```

### 使用 SSH 克隆仓库

- 使用 SSH 地址克隆远程仓库：

  ```bash
  git clone git@github.com:用户名/仓库名.git
  ```

- **两种克隆方式对比**：

  ```bash
  # HTTPS 方式（GitHub 自 2021 年 8 月起禁用密码认证，需要 Personal Access Token）
  git clone https://github.com/用户名/仓库名.git

  # SSH 方式（配置密钥后无需每次输入口令）
  git clone git@github.com:用户名/仓库名.git
  ```

  两种方式都能用：HTTPS 需要 Personal Access Token（PAT）作为密码；SSH 需要先配置密钥对。SSH 配置一次即可长期使用，日常开发更省事；HTTPS 在受限网络或临时环境中更方便。

### 将现有仓库切换为 SSH 连接

- 如果已经使用 HTTPS 克隆了仓库，可以通过以下命令切换为 SSH：

  ```bash
  git remote set-url origin git@github.com:用户名/仓库名.git
  ```

- 使用 `git remote -v` 查看远程仓库地址，确认是否切换成功。

### 使用 Personal Access Token（PAT）

GitHub 自 2021 年 8 月起**不再接受账户密码**进行 Git 的 HTTPS 认证，改用 Personal Access Token（PAT，个人访问令牌）。其他平台（GitLab、Gitee 等）也普遍采用令牌或应用密码。

#### 什么时候需要 PAT

- 用 HTTPS 地址 `git clone` / `git push` 一个私有或需要写入权限的仓库；
- 在没有配置 SSH 密钥的机器（如公共机房、临时容器）上临时操作；
- 调用平台的 API 或 CI 中的脚本。

#### 如何创建（最小权限）

1. 打开平台的令牌设置页，例如 GitHub 的 **Settings → Developer settings → Personal access tokens**；
2. 选择过期时间，尽量设置较短的有效期；
3. 只勾选本次任务真正需要的权限范围（scope），例如只读公开仓库就不需要 `repo` 的写入权限；
4. 生成后**立刻复制**，令牌只显示一次。

#### 如何使用

- 最简单的方式：执行 `git clone https://github.com/用户名/仓库名.git` 时，用户名填 GitHub 用户名，密码位置粘贴 PAT。
- 建议交给凭据助手保存，避免每次手输：

  ```bash
  # macOS：使用系统钥匙串
  git config --global credential.helper osxkeychain

  # Windows：使用 Git Credential Manager
  git config --global credential.helper manager

  # Linux：使用 libsecret（需要先安装）
  git config --global credential.helper libsecret
  ```

  ```bash
  # 内存缓存 15 分钟（各平台通用，但重启后失效）
  git config --global credential.helper "cache --timeout=900"
  ```

!!! danger "不要把令牌写进仓库或 `.git/config`"

    - 不要把 PAT 写进源码、README、脚本或配置文件后提交——一旦推送，令牌就等于公开泄露，即使事后删除，历史里仍然存在。发现泄露应立即到平台**吊销**该令牌。
    - `git config credential.helper store`（以及 `git config --global credential.helper store`）会把凭据以**明文**写入 `~/.git-credentials`。只有在完全可控的个人机器上、并且理解风险时才使用；更推荐上面的钥匙串或缓存方案。
    - 不要用 `git remote set-url` 把令牌直接嵌进远程地址（形如 `https://user:TOKEN@github.com/...`）：它会明文保存在 `.git/config` 中，还可能出现在命令历史和日志里。

### SSH 端口绕行与代理配置

如果你的网络环境比较特殊（不能访问 GitHub，或 22 端口被屏蔽），需要按情况选择下面**两种方案之一**，不要同时使用。先打开（或创建）`~/.ssh/config`：

```bash
nano ~/.ssh/config
```

**方案一：走 443 端口绕行（无需代理）**

如果 22 端口被防火墙屏蔽，但可以正常访问 HTTPS，就用这条：

```bash
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
```

**方案二：通过本地 HTTP/SOCKS 代理访问**

只有当你确实需要走代理时才用这条。`ProxyCommand` 里的地址和端口是**本机代理的监听地址**，请按自身环境替换（常见端口有 7890、1080、10808 等，因软件而异）。

```bash
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
    # 端口按本机代理软件的实际监听端口替换
    ProxyCommand nc -X connect -x 127.0.0.1:7890 %h %p
```

!!! warning "可移植性提示"

    不同系统的 netcat 实现参数不同：`-x` 是 BSD/macOS 与部分发行版 netcat 的写法，`-X connect` 用于指定 HTTP CONNECT 方式，而 GNU netcat 等实现可能不支持。若报错，可以改用 `ncat --proxy 127.0.0.1:7890 --proxy-type http %h %p`，或改用 SSH 自带的 `-o ProxyCommand` / `ssh -o ProxyJump` 方式。配置完成后先执行 `ssh -T git@github.com` 验证，失败时用 `ssh -vT git@github.com` 查看实际连接过程。

保存 `~/.ssh/config` 后再次测试 SSH 连接。

---

## 3. Git 最为基础的命令

以下是 Git 中最基础且常用的命令，掌握这些命令是使用 Git 进行版本控制的第一步。

### 初始化仓库（`git init`）

- **命令**：

  ```bash
  git init
  ```

- **作用**：在当前目录中创建一个新的 Git 仓库。执行该命令后，Git 会在当前目录下生成一个隐藏的 `.git` 文件夹，用于存储版本控制所需的元数据和对象。
- **使用场景**：当你需要从头开始创建一个新项目时，可以使用 `git init` 初始化仓库。

### 克隆远程仓库（`git clone`）

- **命令**：

  ```bash
  git clone 远程仓库地址
  ```

- **作用**：从远程服务器（如 GitHub、Gitee 等）克隆一个已有的仓库到本地。克隆操作会将远程仓库的所有文件、分支和历史记录复制到本地。
- **示例**：

  ```bash
  git clone https://github.com/example/project.git
  ```

- **使用场景**：当你需要参与一个已有的项目时，可以使用 `git clone` 将项目代码下载到本地。

### 查看仓库状态（`git status`）

- **命令**：

  ```bash
  git status
  ```

- **作用**：查看当前仓库的状态，包括哪些文件被修改、哪些文件已暂存（Staged）、哪些文件未跟踪（Untracked）等。
- **输出示例**：

  ```plaintext
  On branch main
  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
      modified:   README.md

  Untracked files:
    (use "git add <file>..." to include in what will be committed)
      new-file.txt

  no changes added to commit (use "git add" and/or "git commit -a")
  ```

- **使用场景**：在提交代码之前，使用 `git status` 检查当前工作目录的状态，确保没有遗漏或误操作。

### 拉取远程更新（`git pull`）

`git pull` 等价于 `git fetch` 之后再做一次合并。合并方式由配置决定，**不要在不清楚策略时直接 `git pull`**，否则容易产生意料之外的合并提交或分叉。

- **命令**：

  ```bash
  git pull
  ```

- **两种常见策略**：

  ```bash
  # 拉取后用变基方式把你的本地提交放到远程更新之上（个人分支推荐）
  git pull --rebase

  # 只允许快进：本地与远程分叉时直接报错，不产生合并提交（最安全，便于发现问题）
  git pull --ff-only
  ```

- **持久化配置**（Git 2.27 起，分叉的拉取会给出提示）：

  ```bash
  # 全局默认使用变基拉取
  git config --global pull.rebase true

  # 或者全局只允许快进拉取
  git config --global pull.ff only
  ```

- **取舍**：
  - `pull.rebase` 保持线性历史，适合个人分支；但会改写你本地提交的哈希，共享分支上仍需谨慎。
  - `pull.ff only` 不允许自动合并，遇到分叉会报错并要求你手动决定，是最不容易“悄悄出错”的选择，和后续[参与开源项目](6-participate-in.md)中用到的 `git pull --ff-only` 保持一致。
  - 默认的 `pull.rebase false`（合并式拉取）会生成合并提交，在多人协作的共享分支上是合理选择。

---

## Git 工作流程概览图

```mermaid
flowchart TD
    A[配置用户信息] --> B[生成SSH密钥]
    B --> C[添加密钥到GitHub]
    C --> D[克隆仓库]
    D --> E[修改文件]
    E --> F[查看状态]
    
    subgraph 本地操作
    E
    F
    end
    
    subgraph 远程连接
    C
    D
    end
```

---

## 总结

1. 如何配置 Git 的用户名、邮箱和默认分支名，以便正确标识代码贡献者。
2. 如何生成 SSH 密钥、把公钥添加到平台，并通过 `ssh -T git@github.com` 验证连接；网络受限时如何选择 443 端口绕行或代理方案。
3. 什么是 Personal Access Token（PAT），如何以最小权限创建它，以及为什么不能把令牌提交到仓库或交给 `credential.helper store` 明文保存。
4. 如何使用 `git init` 初始化一个新的 Git 仓库。
5. 如何使用 `git clone` 克隆远程仓库到本地（HTTPS 需 PAT，SSH 需密钥）。
6. 如何使用 `git status` 查看仓库的当前状态，以及如何用 `git pull --rebase` / `--ff-only` 控制拉取行为。

## 实践任务

1. 配置用户名和邮箱

   ```bash
   git config --global user.name "你的名字"
   git config --global user.email "你的邮箱"
   git config --global init.defaultBranch main
   git config --list | grep user  # 检查配置是否正确
   ```

2. 创建并添加 SSH 密钥

   ```bash
   ssh-keygen -t ed25519 -C "你的邮箱"  # 一路回车即不设口令
   cat ~/.ssh/id_ed25519.pub  # 复制输出的所有内容
   # 添加到 GitHub 后测试：
   ssh -T git@github.com
   ```

   **关于 passphrase**：一路回车表示**不设置口令**，适合教学环境和个人虚拟机，代价是私钥文件一旦被复制就能直接使用。生产环境或经常在多台机器上工作的同学建议设置口令，并配合 `ssh-agent`（`eval "$(ssh-agent -s)"` 加 `ssh-add ~/.ssh/id_ed25519`）避免频繁输入。

3. 在 GitHub 上找到一个开源仓库（如 [https://github.com/octocat/Hello-World](https://github.com/octocat/Hello-World)），用 SSH 方式克隆它到本地：

   ```bash
   git clone git@github.com:octocat/Hello-World.git
   ```

4. 进入该项目文件夹，执行以下命令：

   ```bash
   cd Hello-World
   git status
   # 应该看到："nothing to commit, working tree clean"
   ```

如果你成功完成以上步骤，恭喜你！已经具备基本的 Git 配置与使用能力。
