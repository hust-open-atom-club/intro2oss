# Intro2OSS 项目指南

本文件面向需要维护或贡献 `intro2oss` 仓库的 AI 编码助手。项目所有核心文档、注释与沟通语言均为**中文**。

## 项目概述

`intro2oss` 是华中科技大学开放原子开源俱乐部（HUST Open Atom Club）维护的《开源软件通识课程》线上教材站点。项目遵循"以开源方式来建设开源课程"的方针，使用 **MkDocs + Material for MkDocs** 构建静态文档网站，部署在 GitHub Pages 上。

- 仓库地址：https://github.com/hust-open-atom-club/intro2oss
- 线上站点：https://oss.openatom.club/
- 许可证：MIT

## 技术栈与架构

### 核心工具链

| 工具 | 说明 |
|------|------|
| Python 3.13 | 运行时环境 |
| MkDocs | 静态站点生成器 |
| Material for MkDocs | 主题 |
| pymdown-extensions | Markdown 扩展 |
| mkdocs-audio | 音频嵌入插件 |
| mkdocs-md-preview | Markdown 源码/渲染对比插件 |
| autocorrect | 中文排版自动修正 |
| markdownlint-cli2 | Markdown 格式检查 |

### 关键配置文件

- `mkdocs.yml`：MkDocs 站点配置、导航、主题、插件与 Markdown 扩展。站点语言设为 `zh`，使用 `material` 主题并启用了搜索、评论、代码复制、导航索引等功能。
- `requirements.txt`：Python 依赖列表。
- `.markdownlint.json`：markdownlint 规则，关闭了 `MD046`、`MD013`、`MD033`。
- `.github/workflows/`：CI/CD 工作流定义。
- `.gitignore`：仅忽略 `.DS_Store` 与构建产物 `site/`。

### 项目结构

```text
intro2oss/
├── docs/                  # 文档源码
│   ├── index.md           # 站点首页
│   ├── course/            # 课程指南（大纲、真实贡献项目、成绩评定）
│   ├── ch0/               # 课程导入
│   ├── ch1/               # 开源简介
│   ├── ch2/               # 开源基础理论
│   │   ├── sec1/          # 名词、生态、许可证、许可证判断练习
│   │   ├── sec2/          # 开源文化
│   │   └── sec3/          # 项目运作、贡献回报、法律与合规
│   ├── ch3/               # 完成开源贡献
│   │   ├── writing/       # 第一节 Markdown
│   │   ├── git/           # 第二节 Git 与平台协作（platform/ 为平台实践，advanced/ 为拓展）
│   │   ├── linux/         # 第三节 Linux 命令行
│   │   ├── docker/        # 拓展 Docker
│   │   ├── qemu/          # 拓展 QEMU 与邮件列表
│   │   └── tools/         # 拓展效率工具
│   ├── ch4/               # 从一次贡献到持续参与
│   ├── ch99/              # 附录/关于
│   ├── assets/            # 图片与图标
│   ├── audios/            # 音频文件（MP3，不要提交未压缩的 WAV）
│   ├── overrides/         # Material 主题覆盖
│   │   └── partials/
│   │       └── comments.html   # Giscus 评论系统
│   ├── scripts/
│   │   └── mathjax.js     # MathJax 配置
│   └── stylesheets/
│       └── extra.css      # 自定义样式（主题色、图片配字、md-preview 样式）
├── reference/             # 课程参考 PPT/PDF（不参与站点构建）
├── mkdocs.yml
├── requirements.txt
├── README.md
├── CONTRIBUTING.md        # 贡献规范（必读）
├── Assignment.md          # 课程作业说明
└── .github/               # GitHub Actions 与 PR 模板
```

### 导航与内容组织

`mkdocs.yml` 的 `nav` 段显式声明了站点目录。**新增任何 `.md` 文件后必须同步更新 `nav`**，否则页面不会出现在站点导航中。可以用下面的命令自查：

```bash
# 列出未纳入 nav 的 Markdown 文件（应输出为空）
python3 - <<'EOF'
import re, pathlib
lines = open('mkdocs.yml').read().splitlines()
nav = '\n'.join(lines[lines.index('nav:')+1:]).split('extra_javascript')[0]
refs = set(re.findall(r':\s*([\w\-/.]+\\.md)', nav))
allmd = {str(p.relative_to('docs')) for p in pathlib.Path('docs').rglob('*.md')}
print(sorted(allmd - refs))
EOF
```

`pymdownx.snippets` 配置了 auto_append `includes/man.md` 与 `includes/authors.md`，但仓库中**没有** `docs/includes/` 目录（该插件在文件不存在时静默忽略，不产生警告）。若需要全站追加页脚署名，请创建该目录与文件；否则建议删除这两行配置以免误解。

## 本地开发

### 环境准备

```bash
# 建议使用虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# （可选）安装 Node 端 lint 工具
npm install
```

> 仓库没有 `package.json`，`npm install` 是否成功取决于当前目录下是否有相关包配置；CONTRIBUTING.md 中提及 markdownlint 等前端工具，请按实际情况确认。

### 常用命令

| 命令 | 作用 |
|------|------|
| `mkdocs serve` | 本地预览，默认 http://127.0.0.1:8000 |
| `mkdocs build` | 构建站点，输出到 `site/` |
| `mkdocs -v build` | 详细输出构建日志（CI 使用） |
| `autocorrect --fix .` | 自动修正中文排版 |
| `autocorrect --lint .` | 仅检查不修改 |
| `markdownlint-cli2 "**/*.md"` | Markdown 格式检查 |

## CI/CD 与部署

仓库使用 GitHub Actions，工作流位于 `.github/workflows/`：

- `build.yml`：所有 Pull Request 触发，使用 Python 3.13 安装依赖并执行 `mkdocs -v build`，用于验证文档能否正确构建。
- `deploy_ghpage.yml`：`main` 分支推送时触发，构建后将 `site/` 目录上传并部署到 GitHub Pages。
- `lint.yml`：推送或 PR 中的 Markdown 文件变更时触发，执行 `autocorrect --fix`。修复后的文件会打包上传为 `autocorrect-fixes` artifact；**仅当 PR 来自本仓库分支时**才自动回推（`git add -u` + 回推同一分支）。fork PR 无法自动回推也无法留言——fork 触发的 `pull_request` 事件拿到的 `GITHUB_TOKEN` 恒为只读——因此改为在运行摘要（Job Summary）中说明如何用 artifact 或本地 `autocorrect --fix .` 应用修复。安装脚本下载到 `$RUNNER_TEMP`，不得放进工作区（否则会被变更检测与 `git add` 误提交）。
- `lint-all.yml`：手动触发，下载并检查安装脚本后执行 `autocorrect`（不使用 `curl | sh`）。

部署目标分支为 `main`，站点产物目录为 `./site`。

## 代码与文档风格

详细规范见 `CONTRIBUTING.md`。核心要求如下：

### 文档书写

1. **一级标题开头**：每个 `.md` 文件应以 `# 标题` 开头。
2. **主要作者署名**：章节开头使用 `!!! note "主要作者"` 提示框，多名作者用中文顿号 `、` 分隔。
3. **图片配字**：图片下方写配字，并在下一行加 `{: .caption }`。
4. **提示框**：优先使用 `note`、`warning`、`danger`、`tip`、`example`、`question`，可折叠提示框使用 `???` 或 `???+`。
5. **文件命名**：保持与 `mkdocs.yml` 中 `nav` 路径一致；新增文件后必须同步更新 `nav`。

### Commit 与 PR

- Commit message 尽量使用英文，动词开头，例如 `Fix: correct a typo` / `Feat: add new section on licenses`。
- 保持提交的原子性；PR 前可使用 `git rebase -i` 合并同类提交。
- 大的内容改动需先创建 Issue 讨论；小修小补可直接 PR。
- PR 必须填写提供的 PR 模板，并勾选本地验证项（autocorrect + `mkdocs serve` 预览）。

## 测试策略

本项目没有传统单元测试，质量保障依赖：

1. `mkdocs build`：验证站点能否成功构建、链接是否有效。
2. `autocorrect`：中文排版与格式自动修正。
3. `markdownlint-cli2`：Markdown 格式检查（`.markdownlint.json` 已关闭部分规则）。
4. 人工 Review：PR 需维护者审核。

修改文档后，应在本地执行 `mkdocs serve` 确认页面渲染、链接、图片与提示框样式正常。

提交前建议至少运行：

```bash
mkdocs build --strict   # 严格模式，把警告视为错误
autocorrect --lint .
```

## 已知问题与注意事项

- **署名框尚未补齐**：`!!! note "主要作者"` 目前覆盖部分文件。其余文件无法从 git 历史可靠推断主要作者（多数文件由 5 位以上贡献者各提交 1 次），需要由章节负责人自行声明，不要凭"提交次数最多"自动填写。
- **数据必须有来源**：教材要求"对事实、数据和案例标注来源与时间"。定量表述一律给"来源 + 年份 + 链接"；无法取证的量化表述应删除，改为定性结论。请勿用"据估计""有研究显示"给无来源数字背书。
- **技术示例必须可执行**：命令应在作者环境中实际运行过；破坏性命令（`reset --hard`、强制推送、删除数据卷等）必须配 `!!! danger` 或 `!!! warning` 提示。
- **许可证事实需谨慎**：许可证的效力范围、专利条款与兼容性结论必须以 [SPDX License List](https://spdx.org/licenses/) 和许可证原文为准；`GPL-2.0-only` 与 `GPL-2.0-or-later` 必须区分。
- 新增章节或页面时，请同时更新 `mkdocs.yml` 的 `nav` 与 `README.md` 中的课程大纲（如适用）。
- 教材评审报告与待办清单见根目录 `COURSE-AUDIT.md`（不参与站点构建）。

## 安全与合规

- 内容应遵守 MIT 许可证；引用第三方图片、代码或文字时需注明来源并确认授权。
- 评论系统通过 Giscus 加载，配置在 `docs/overrides/partials/comments.html`，涉及 `data-repo-id` 与 `data-category-id` 等固定标识，非必要请勿修改。
- 不要在文档中写入个人敏感信息、账号密码或内部未公开链接。
