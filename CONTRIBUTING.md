# 贡献指南 (CONTRIBUTING.md)

欢迎您参与 `intro2oss` 项目的贡献！为了确保项目的文档质量和风格一致性，我们制定了以下贡献规范。请您在开始贡献前仔细阅读。

本文档参考了 [`Linux201` 项目规范](https://201.ustclug.org/spec/writing/)，并结合了 `intro2oss` 项目的实际需求。

## 目录

- [贡献指南 (CONTRIBUTING.md)](#贡献指南-contributingmd)
  - [目录](#目录)
  - [我们欢迎什么样的贡献](#我们欢迎什么样的贡献)
  - [开始之前：本地环境配置](#开始之前本地环境配置)
  - [贡献流程](#贡献流程)
  - [书写规范](#书写规范)
    - [1. 从一级标题开始书写](#1-从一级标题开始书写)
    - [2. 主要作者署名](#2-主要作者署名)
    - [3. 为图片添加配字](#3-为图片添加配字)
    - [4. 使用提示框 (Admonition)](#4-使用提示框-admonition)
    - [5. 图片与附件文件](#5-图片与附件文件)
  - [Commit 提交规范](#commit-提交规范)
  - [Pull Request (PR) 规范](#pull-request-pr-规范)
  - [风格指南参考](#风格指南参考)
  - [反馈与建议](#反馈与建议)

## 我们欢迎什么样的贡献

我们欢迎并感谢大家的贡献，以帮助 `intro2oss` 项目变得更好。以下是我们接受的主要贡献类型及建议流程：

1. **修正错误 (Typos, Bugs)**
    - **内容**：修正文档中的错别字、语句不通、格式错误，或修复失效的链接。
    - **技术**：报告或修复构建问题（如 `mkdocs` 配置错误）、脚本失效等。
    - **流程**：对于这类明确的、无争议的修改，您可以直接创建 Pull Request。不过，我们更推荐您**先创建一个 Issue** 来描述问题，然后再提交关联该 Issue 的 PR。这有助于我们更好地追踪每一个修复。

2. **内容补充与功能建议 (New Content, Features)**
    - **内容**：如果您希望增加新的章节、撰写大段新内容、或对现有内容进行大幅重构。
    - **流程**：**请务必先创建一个 Issue** 来发起讨论！请在 Issue 中详细描述您的想法、要解决的问题以及您的建议方案。这可以帮助我们达成共识，避免您在错误的方向上投入过多精力。在社区讨论并确认方案后，再开始编写并提交 PR。

**总结：** 对于小修小补，可以直接 PR；对于大的改动，请务必先发 Issue 讨论。

## 开始之前：本地环境配置

为了能够顺利地贡献内容并验证您的修改，请先完成以下准备工作：

1. **克隆仓库并配置上游 (remote upstream)**

   ```bash
   # Fork 本仓库到您的 GitHub 账户后执行
   git clone https://github.com/<你的 GitHub 用户名>/intro2oss.git
   cd intro2oss

   # 添加上游仓库以便后续同步更新
   git remote add upstream https://github.com/<原始仓库用户名>/intro2oss.git
   ```

2. **安装依赖**

   ```bash
   # 安装 Python 依赖
   pip install -r requirements.txt

   # 安装前端工具（如 markdownlint 等）
   npm install
   ```

3. **`autocorrect`：中文排版/格式检查**
   项目地址：<https://github.com/huacnlee/autocorrect/>
   请参考项目文档进行安装和使用。

4. **`markdownlint-cli2`：Markdown 格式检查**
   项目地址：<https://github.com/DavidAnson/markdownlint-cli2>
   请参考项目文档进行安装和使用。

5. **本地预览文档**

   ```bash
   mkdocs serve
   ```

   然后在浏览器中打开 `http://127.0.0.1:8000` 进行预览。

6. **常用 Git 命令备忘**

   ```bash
   # 查看当前状态
   git status

   # 基于 main 创建工作分支
   git checkout -b feature/your-feature-name

   # 拉取上游最新代码（在 main 分支）
   git checkout main
   git pull upstream main
   ```

## 贡献流程

我们欢迎各种形式的贡献，包括但不限于：

- 修正错别字或语句不通顺的地方
- 补充缺失的内容或更新过时的信息
- 改进示例代码或添加新的示例
- 提出宝贵的建议

贡献流程如下：

1. **Fork** 本项目到您的 GitHub 仓库
2. 将您 Fork 的仓库 **Clone** 到本地
3. 基于 `main` 分支创建一个新的 **Feature Branch** (例如 `git checkout -b feature/my-new-feature` 或 `fix/typo-in-chapter-one`)
4. 在新的分支上进行修改和创作
5. 确保您的修改符合本文档中的书写规范和格式要求
6. 提交您的更改 (Commit)。请遵循 [Commit 提交规范](#commit-提交规范)
7. 将您的分支推送到您 Fork 的远程仓库 (Push)
8. 在 `intro2oss` 原始仓库创建一个 **Pull Request (PR)**，目标分支为 `main`。请遵循 [Pull Request (PR) 规范](#pull-request-pr-规范)
9. 等待维护者 Review 您的 PR。如果需要修改，请及时更新
10. PR 合并后，您的贡献就成功啦！

## 书写规范

### 1. 从一级标题开始书写

在编写 Markdown 文档时，为了保持文档结构的一致性和可读性，所有单个 `.md` 文件应以 **一级标题 (`#`)** 作为开头。

示例：

```markdown
# 这是一个文档的标题
```

### 2. 主要作者署名

如果您编写了某个章节的主要内容，请在章节的开头添加主要作者提示框。

格式如下，不同作者名字之间用中文全角顿号（「、」）分隔：

```markdown
!!! note "主要作者"

    [@example][github.com/example]、[@new-contributor][github.com/new-contributor]
```

### 3. 为图片添加配字

所有图片都应在图片下方添加配字说明，并在配字的下一行写上 `{: .caption }` 以应用特定样式。

格式如下：

```markdown
![图片替代文本](images/example-image.png)

图 1. 这是一张示例图片的配字说明
{: .caption }
```

请确保配字简洁明了，并对图片内容进行必要的解释。图号建议按章节顺序编号（如图 1.1, 图 1.2, 图 2.1 等）或按文档顺序编号。

### 4. 使用提示框 (Admonition)

提示框（Admonition）是 `mkdocs-material` 主题的特色功能，能够有效突出显示特定信息。建议根据内容性质选用以下类型的提示框：

- `note`：普通提示，用于补充说明或引人注意的信息

   ```markdown
   !!! note "请注意"

       这是一条普通提示信息。
   ```

- `warning`：警告信息，需要读者特别注意，否则可能出现非预期行为

   ```markdown
   !!! warning "警告"

       进行此操作前请务必备份数据。
   ```

- `danger`：危险操作提示，可能导致严重后果（如数据丢失、系统损坏等）

   ```markdown
   !!! danger "危险操作"

       以下命令将删除所有数据，请谨慎操作！
   ```

- `tip`：小技巧或建议，帮助读者更高效地学习或操作

   ```markdown
   !!! tip "小技巧"

       您可以使用快捷键 `Ctrl + S` 保存文件。
   ```

- `example`：用于展示示例代码、配置或操作步骤

   ```markdown
   !!! example "示例：Python 'Hello World'"

       ```python
       print("Hello, World!")
       ```
   ```

- `question`：提出问题，引导读者思考

   ```markdown
   !!! question "思考题"

       为什么我们需要使用版本控制系统？
   ```

**可折叠的提示框：**

您可以创建可折叠的提示框。

- **默认折叠**：使用三个问号 `???`。用户需要点击标题才能展开内容

   ```markdown
   ??? note "这是一个默认折叠的提示框 (点击展开)"

       这里是折叠的内容。
   ```

- **默认展开**：使用三个问号加一个加号 `???+`。内容默认是可见的，但用户可以点击标题将其折叠

   ```markdown
   ???+ tip "这是一个默认展开的可折叠提示框 (点击折叠)"

       这里是默认展开的内容。
   ```

这种方式可以帮助您更好地组织较长的补充信息或示例，保持文档的整洁性，同时允许读者按需查看详细内容。

### 5. 图片与附件文件

所有图片都应在图片下方添加配字说明，并在配字的下一行写上 `{: .caption }` 以应用特定样式。

格式如下：

```markdown
![图片替代文本](images/example-image.png)

图 1. 这是一张示例图片的配字说明
{: .caption }
```

请确保配字简洁明了，并对图片内容进行必要的解释。图号建议按章节顺序编号（如图 1.1, 图 1.2, 图 2.1 等）或按文档顺序编号。

## Commit 提交规范

为了保持 Commit 历史的清晰和可追溯性，请遵循以下规范：

1. **Commit Message 格式**：
   - 尽量使用英文撰写 Commit Message，以便更广泛的开发者理解。如果觉得困难，简洁的中文亦可，但避免中英文混杂
   - 第一行：简要概括本次提交的目的，动词开头，例如 `Fix: correct a typo in installation guide` 或 `Feat: add new section on licenses`
   - 后续行（可选）：详细描述修改内容、原因和影响
2. **原子性提交**：尽量保证每个 Commit 的原子性，即一个 Commit 只做一件事情
3. **合并 Commit**：对于一系列微小修改或为了修复 CI/CD 问题而产生的多个 Commit，请在发起 PR 前或 Review 过程中，考虑使用 `git rebase -i` 将它们合并成一个或少数几个有意义的 Commit
4. **Linting 问题**：如果在 `git commit` 后，CI/CD 流程（GitHub Actions）报告了 Markdown 格式问题，请注意：
   - 在对应的 Action Run 详情页底部，通常会有一个名为 "artifact" 的压缩包。下载并解压它可以查看详细的 linting 日志和 `autocorrect` 自动修复后的文件
   - 根据日志和修复建议，在本地修改代码，然后使用 `git commit --amend` 修改上一个提交，或创建一个新的修复提交

## Pull Request (PR) 规范

在创建 Pull Request 时，请确保遵循以下步骤并填写提供的 PR 模板：

1. **PR 标题**：清晰概括 PR 的主要内容，例如 `Fix: Typo in Chapter 1 Introduction` 或 `Docs: Add new section on OSS licenses`
2. **PR 内容**：我们提供了 PR 模板，请认真对照内容进行填写

**PR 模板示例**：

```markdown
## 关联章节/文件
<!-- 请填写您修改的文档路径或代码文件路径，例如： -->
- 文档路径：`docs/1-install/2-partition.md`

## 修改类型
<!-- 请选择一项或多项，并用 [x] 标记 -->
- [ ] 内容补充
- [ ] 错别字/语句修正
- [ ] 格式调整
- [ ] 图片/附件更新
- [ ] 代码示例修改
- [ ] 其他 (请说明):

## 修改描述
<!-- 请简要描述您本次修改的主要内容和原因 -->
-
-

## 本地验证
<!-- 请确保您已在本地完成以下检查 -->
- [ ] 已通过 `autocorrect .` (或 `autocorrect --lint .` 检查并通过)
- [ ] 已执行 `mkdocs serve` 并在本地预览，确认页面渲染正常、链接有效、排版美观

## 附加说明 (可选)
<!-- 如有其他需要说明的事项，请在此填写 -->
-
```

## 风格指南参考

- `Linux201`项目写作规范：<https://201.ustclug.org/spec/writing/>

## 反馈与建议

本贡献指南旨在帮助大家更好地参与项目，我们欢迎任何关于本指南的反馈和建议。您可以通过 Issue 或在相关的 PR 中提出您的看法。

感谢您的贡献！
