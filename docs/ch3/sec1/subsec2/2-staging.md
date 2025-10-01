# Git 暂存区

## 目的

本节旨在帮助学生理解 Git 暂存区的作用，并掌握 `git add` 等基础命令

---

## 内容

### 1. Git 暂存区的作用

#### 什么是暂存区？

- **定义**：暂存区（Staging Area）是 Git 中一个临时存储区域，用于保存即将提交的更改。
- **作用**：允许开发者选择性地将修改的文件添加到暂存区，而不是一次性提交所有更改。

#### 工作流程

1. **工作目录**：开发者对项目文件进行修改。
2. **暂存区**：使用 `git add` 将修改的文件添加到暂存区。
3. **本地仓库**：使用 `git commit` 将暂存区的内容提交到本地仓库。

---

### 2. 修改暂存区

`git add` 是 Git 中用于将工作目录中的修改添加到暂存区的命令。以下是 `git add` 的常见用法：

#### 添加文件

  **命令**：

  ```bash
  git add <文件 1> <文件 2>
  ```

  **作用**：将文件（如 `file1.txt` 和 `file2.txt`）添加到暂存区。

#### 添加某个目录下的所有修改

  **命令**：

  ```bash
  git add <目录名>/
  ```

  **作用**：将指定目录（如 `src/`）下的所有修改添加到暂存区。

  如果你使用的是

  ```bash
  git add .
  ```
  
  那么将把当前所在目录的所有文件添加进暂存区

>可以把构建产物的文件路径加入 `.gitignore` 文件中，避免被错误加入暂存区

#### 交互式添加

  **命令**：

  ```bash
  git add -p
  ```

  **作用**：进入交互模式，逐块（hunk）选择要添加到暂存区的修改。Git 会显示每个修改块，并提示是否将其添加到暂存区。
  **使用场景**：当需要对修改进行精细控制时，可以使用交互式添加。

>`git rm`，`git mv` 的用法与 `git add` 差不多

---

### 3. 撤销暂存区的修改

如果误将某些修改添加到暂存区，可以使用以下命令将其撤销：

#### 撤销单个文件的暂存

  **命令**：

  ```bash
  git restore --staged <文件名>
  ```

  **示例**：

  ```bash
  git restore --staged README.md
  ```

  **作用**：将指定文件（如 `README.md`）从暂存区移回工作目录。

#### 撤销所有暂存的修改

  **命令**：

  ```bash
  git restore --staged .
  ```

  **作用**：将所有暂存的文件移回工作目录。

>`git restore` 是在 Git 2.23 引入的，在此之前，使用 `git checkout` 从某个提交恢复文件

## 总结

通过本节的学习，学生应掌握以下内容：

1. **暂存区的基础操作**

# Git 暂存区

## 4. Git Reset

前面我们提到了 `git restore`，与其不同，`git reset` 会移动头指针，并且可以选择性地修改暂存区和工作目录。

以下是 `git reset` 的常见用法：

### 撤销暂存区的修改（保留工作目录的更改）

  **命令**：

  ```bash
  git reset
  ```

  **作用**：将暂存区的内容重置为最后一次提交的状态，但保留工作目录中的修改。

### 撤销暂存区和工作目录的修改

  **命令**：

  ```bash
  git reset --hard
  ```

  **作用**：将暂存区和工作目录的内容都重置为最后一次提交的状态。**注意**：这将丢弃所有未提交的更改，使用时要小心。

### 回退到某个提交

  **命令**：

  ```bash
  git reset <commit-hash>
  ```

  **作用**：将当前分支的 HEAD 移动到指定的提交，并可以选择是否重置暂存区和工作目录。

- `git reset --soft <commit-hash>`：仅移动 HEAD，保留暂存区和工作目录的更改。
- `git reset --mixed <commit-hash>`：移动 HEAD 并重置暂存区，但保留工作目录的更改（默认行为）。
- `git reset --hard <commit-hash>`：移动 HEAD 并重置暂存区和工作目录，丢弃所有更改。
- **使用场景**: 比如，在你不小心把一些奇怪的文件交上去后，可以用这个撤销。

---

## 5. Git Diff

`git diff` 用于比较工作目录、暂存区和仓库之间的差异。以下是 `git diff` 的常见用法：

### 比较工作目录和暂存区

  **命令**：

  ```bash
  git diff
  ```

  **作用**：显示工作目录中尚未添加到暂存区的更改。

  **输出示例**：

  ```diff
  diff --git a/file.txt b/file.txt
  index 1234567..89abcde 100644
  --- a/file.txt
  +++ b/file.txt
  @@ -1,3 +1,4 @@
   Hello, World!
  -This is the old content.
  +This is the new content.
  +Added a new line.
  ```

- `---` 表示旧文件（暂存区中的文件）。
- `+++` 表示新文件（工作目录中的文件）。
- `-` 表示删除的行。
- `+` 表示新增的行。

- **使用场景**：在将修改添加到暂存区之前，检查工作目录中的更改。

---

### 比较暂存区和最后一次提交

  **命令**：

  ```bash
  git diff --cached
  ```

  >或者是`git diff --staged`

  **作用**：显示暂存区中尚未提交的更改。

### 比较工作目录和最后一次提交

  **命令**：

  ```bash
  git diff HEAD
  ```

  **作用**：显示工作目录和最后一次提交之间的所有差异（包括暂存区和工作目录的更改）。

### 比较两个提交之间的差异

  **命令**：

  ```bash
  git diff <commit-hash-1> <commit-hash-2>
  ```

  **作用**：显示两个提交之间的差异。
  >类似的，可以使用`git diff <branch-1> <branch-2>` 来比较两个分支的最新提交之间的差异。

### diff 的其他用法

  **命令与输出**:

  ```bash
  #统计
  git diff --stat
  docs/ch3/sec1/subsec2/3-reset-diff-and-commit.md | 25 +++++++++++++++++++++++--
  1 file changed, 23 insertions(+), 2 deletions(-)
  ```

  使用`git diff`查看某个文件在几个 commit 之间的差异

  命令：`git diff  a6274 293c5  docs/ch3/sec1/subsec1/2-code-hosting-platforms.md`

  ```diff

  diff --git a/docs/ch3/sec1/subsec1/2-code-hosting-platforms.md b/docs/ch3/sec1/subsec1/2-code-hosting-platforms.md
  index 0a257d5..4b2f348 100644
  --- a/docs/ch3/sec1/subsec1/2-code-hosting-platforms.md
  +++ b/docs/ch3/sec1/subsec1/2-code-hosting-platforms.md
  @@ -97,7 +97,7 @@
   - **是什么**：自动化测试、构建和部署的工具，就像你在 Steam 上设置了自动更新游戏，每次有新版本都会自动下载安装。
   - **为什么重要**：提升开发效率，确保代码质量，就像你设置了自动回复，不用每次手动处理重复的事情。
   - **使用场景**：自动化测试、持续集成/持续交付，比如每次提交代码后，自动运行测试并发布新版本。
  -
  +- **案例**:[开源操作系统训练营的自动化测评](https://github.com/LearningOS/template-2024a-rcore/blob/ch8/.github/workflows/build.yml)，[本教程](https://github.com/hust-open-atom-club/intro2oss/actions)
   ---
 
   ## 常用代码托管平台
  ```

---

## 6. Git Commit

`git commit` 用于将暂存区的内容提交到本地仓库。以下是 `git commit` 的常见用法：

### 提交暂存区的更改

  **命令**：

  ```bash
  git commit -m "提交信息"
  ```

  **作用**：将暂存区的内容提交到本地仓库，并附带提交信息。

### 提交时跳过暂存区

  **命令**：

  ```bash
  git commit -a -m "提交信息"
  ```

  **作用**：将所有已跟踪文件的修改直接提交到本地仓库。**注意**：未跟踪的文件不会被提交。

### 修改最后一次提交

  **命令**：

  ```bash
  git commit --amend
  ```

  **作用**：修改最后一次提交的内容或提交信息。

> 对 commit 进行签名 [参考链接](https://docs.github.com/zh/authentication/managing-commit-signature-verification)
