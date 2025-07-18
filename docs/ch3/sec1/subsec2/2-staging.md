# Git 暂存区

## 目的

本节旨在帮助学生理解 Git 暂存区的作用，并掌握 `git add` 等基础命令

---

## 内容

### 1。Git 暂存区的作用

#### 什么是暂存区？

- **定义**：暂存区（Staging Area）是 Git 中一个临时存储区域，用于保存即将提交的更改。
- **作用**：允许开发者选择性地将修改的文件添加到暂存区，而不是一次性提交所有更改。

#### 工作流程

1. **工作目录**：开发者对项目文件进行修改。
2. **暂存区**：使用 `git add` 将修改的文件添加到暂存区。
3. **本地仓库**：使用 `git commit` 将暂存区的内容提交到本地仓库。

---

### 2。修改暂存区

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

### 3。撤销暂存区的修改

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
