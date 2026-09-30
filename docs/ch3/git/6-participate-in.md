# 参与开源项目

!!! note "本节目标"

    把 Markdown、Git 和代码托管平台串联起来，完成从发现问题到响应评审的真实贡献流程。

## 找到合适的任务

首次贡献不要“随机刷仓库”。先用检索式把范围缩到能做完的粒度，再判断项目是否仍然活跃。

### 用 GitHub 检索式筛选 Issue

在仓库的 Issues 页面或 GitHub 搜索框里使用：

```text
is:issue is:open label:"good first issue" no:assignee sort:updated-desc
```

各字段的含义：

| 字段 | 作用 |
| ---- | ---- |
| `is:issue` | 只要 Issue，排除 Pull Request |
| `is:open` | 只要未关闭的 |
| `label:"good first issue"` | 带有新人友好标签 |
| `no:assignee` | 还没有被指派给某人，可能仍可认领 |
| `sort:updated-desc` | 按最近更新倒序，优先看仍有人讨论的条目 |

在检索式前面加上 `repo:所有者/仓库名` 可以限定到具体仓库；把 `is:open` 换成 `is:closed`，可以看到同类问题过去是怎么被解决的——这往往比通读文档更快地了解维护者的偏好。

### 常见聚合入口

- GitHub 的 [Explore](https://github.com/explore) 页面与 `good first issue` 话题；
- 开源之夏（OSPP）、Google Summer of Code、LFX Mentorship 等带导师的长期项目；
- [Up For Grabs](https://up-for-grabs.net/) 等按标签聚合新人任务的站点；
- 本课程项目池由教师发布并标注先修知识的任务（见[真实贡献项目](../../course/project.md)）。

### 判断项目是否活跃

选中一个候选任务前，至少确认四件事：

1. 仓库最近一次提交或合并是否发生在近几个月；
2. 目标 Issue 下的最新评论是否在近几周内，避免追问三个月无人应答；
3. PR 的合并与关闭节奏如何，维护者是否回应新人；
4. `CONTRIBUTING`、Issue 模板、CI 配置是否齐全——它们决定了你的贡献能否被顺畅评审。

## 选择合适的项目和任务

首次贡献应优先选择范围清晰、能够独立验证、符合自己当前能力的任务。开始前检查：

- 项目最近仍有维护活动；
- 仓库提供许可证和贡献指南；
- Issue 或讨论区允许新人公开沟通；
- 任务没有被他人认领或已经解决；
- 自己能够在课程周期内完成修改和验证。

`good first issue`、`help wanted` 等标签可以帮助筛选任务，但标签不是质量保证。最终仍要阅读 Issue 内容、相关代码和项目规则。

## 阅读项目入口文件

| 文件或入口 | 需要确认的内容 |
|------------|----------------|
| `README` | 项目用途、安装方式和基本架构 |
| `LICENSE` | 使用、修改和分发的权利与义务 |
| `CONTRIBUTING` | 开发环境、分支、提交、测试和评审要求 |
| `CODE_OF_CONDUCT` | 社区交流和行为边界 |
| `SECURITY` | 安全问题的非公开报告方式 |
| Issue 与 PR | 是否已有相同问题、维护者偏好的解决方式 |

目标项目的规范始终优先于本课程提供的通用示例。

## Fork 场景下的上游同步

Fork 之后，你的仓库与原项目各自独立。上游继续合并新提交时，你的 `main` 不会自动更新。**在过期分支上开发是最常见的返工原因**：等 PR 打开时基准分支出了一堆改动，冲突和 CI 失败都会一起出现。

### 一次性配置 upstream

```bash
git remote -v                       # 确认 origin 指向你自己的 fork
git remote add upstream https://github.com/原项目所有者/仓库名.git
git remote -v                       # 现在应该同时有 origin 和 upstream
```

### 每次开发前同步

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main   # 只允许快进：本地 main 被改过会立即报错
git push origin main                # 把同步后的 main 推回自己的 fork（可选，推荐）
```

`--ff-only` 是一个安全阀。如果你曾把提交直接做在本地 `main` 上，它会拒绝合并并提示分叉，而不是悄悄制造一个合并提交。此时应先把那些提交移到功能分支：

```bash
git switch -c fix/brief-description   # 在当前提交上创建分支，先把提交保住
git switch main
git reset --hard upstream/main        # 让本地 main 重新指向 upstream/main
git merge --ff-only upstream/main     # 再确认一次可以快进
```

!!! danger "`git reset --hard` 会丢弃未提交的修改"

    这里的 `--hard` 是必要的：`git switch -c` 只是**新建**一个分支，它不会移动 `main`，
    因此本地 `main` 仍然指向那个误提交，单靠 `--ff-only` 永远无法快进。
    执行前请确认：① 误提交已经在上一步的分支上保住了（`git log fix/brief-description` 能看到它）；
    ② 工作区没有未提交的改动（先 `git status` / `git stash push -u`）。
    如果不希望用 `--hard`，可以改用 `git branch -f`——但要注意**它不能作用于已检出的分支**：
    此时 `main` 正在被当前工作区使用，直接执行会报
    `fatal: cannot force update the branch 'main' used by worktree`。正确顺序是先切回刚才的功能分支：

    ```bash
    git switch fix/brief-description   # 先离开 main
    git branch -f main upstream/main   # 现在可以移动 main 了
    ```

### GitHub 网页上的“Sync fork”

Fork 仓库页面上方的 **Sync fork → Update branch** 等价于前几条命令。它很方便，但有三个限制：

- 只有在 `main` 与上游不冲突时才能使用；
- 它只同步默认分支，**不会**更新你正在开发的功能分支；
- 功能分支仍需要自己跟上上游的最新 `main`。

功能分支同步上游的常用做法：

```bash
git switch fix/brief-description
git fetch upstream
git rebase upstream/main            # 分支只有自己使用时推荐
# 有冲突时：解决冲突 → git add FILE → git rebase --continue
git push --force-with-lease         # 已推送过的个人分支需要强制更新
```

!!! warning "只有自己能改的分支才能改写历史"

    `rebase` 会重写提交哈希，因此上面的 `--force-with-lease` 仅限**你一个人的 fork 分支**。如果别人也在该分支上工作，改用 `git merge upstream/main`，或先与维护者确认整理流程。

## 提交贡献

### 1. 确认问题

先搜索已有 Issue 和 Pull Request。任务较大或方案存在多种选择时，在动手前说明：

- 实际问题和复现方式；
- 预期结果；
- 准备修改的范围；
- 计划使用的验证方法。

### 2. 准备个人分支

从最新默认分支创建聚焦当前任务的分支：

```bash
git status
git switch main
git pull --ff-only
git switch -c fix/brief-description
```

默认分支名称以目标项目为准，不一定都是 `main`。

### 3. 修改并检查差异

开发过程中频繁确认仓库状态：

```bash
git status
git diff
```

只暂存与当前任务有关的修改，并在提交前检查暂存区：

```bash
git add path/to/file
git diff --staged
```

### 4. 形成可解释的提交

提交应当聚焦一个逻辑变化。标题简洁说明做了什么，正文解释为什么修改以及需要注意的影响。

```bash
git commit
```

是否采用 Conventional Commits、子系统前缀或 `Signed-off-by`，以目标项目贡献指南为准。

### 5. 按项目要求验证

运行项目明确要求的构建、测试、格式或文档检查，并记录实际命令和结果。不要复制与项目无关的通用检查，也不要在未阅读内容时直接运行来自网络的脚本。

### 6. 创建 Pull Request 或发送补丁

贡献说明至少回答四个问题：

1. 当前存在什么问题？
2. 这项修改采用了什么方案？
3. 哪些内容不在本次修改范围内？
4. 如何验证修改有效？

需要关联 Issue 时，使用目标平台支持的语法，例如 `Fixes #123`。不要为了自动关闭 Issue 而错误关联不完整的修改。

## 读懂自动检查结果

PR 页面底部的 **Checks** 区列出了所有自动检查。点击具体条目右侧的 **Details** 会跳到 **Actions** 的运行页面，展开失败的 step 就能看到完整日志。

### 从日志定位失败原因

先看被标红的 step 名称和日志最后几行，再往前翻到第一个错误。常见失败大致有五类：

| 类型 | 典型日志特征 | 本地复现方式 |
| ---- | ------------ | ------------ |
| 代码或测试错误 | 断言失败、异常堆栈、`FAILED` | 按项目文档运行同一测试命令 |
| 格式检查不通过 | `would reformat`、lint 报出行号、markdownlint 错误 | 本地运行项目的格式化或 lint 命令后提交修正 |
| 许可证头缺失 | 新文件被提示缺少 SPDX / License header | 按项目既有文件补上文件头 |
| DCO 缺失 | `Expected "Signed-off-by"`、DCO 检查红叉 | 仅在自己使用的个人分支中，把 `BASE` 替换为本次贡献的基准提交，用 `git rebase --signoff BASE` 补签；再按前文的历史改写警告用 `git push --force-with-lease` 更新 |
| 偶发失败（flaky） | 与本 PR 无关的模块超时，重跑一次通过 | 本地重复运行确认；确认无关就在 PR 中说明 |

### 本地复现的基本步骤

1. 复制失败 step 中执行的原始命令，在本地尽可能相同的环境下运行；
2. 以 `CONTRIBUTING` 中给出的构建、测试、格式命令为准，不要自己发明命令；
3. 只改与本任务相关的文件，不要为了“让 CI 变绿”而顺手重构。

!!! warning "慎用 Re-run"

    **Re-run failed jobs** 适合已经确认过的偶发失败。如果失败原因是你的代码或格式，重跑只会重复失败，还会消耗项目有限的 CI 时长。重跑前先在本地复现一次；对同一个失败连续重跑而不做任何修改，会被维护者视为没有认真读日志。

## PR 描述范例

标题应能独立读懂，并与仓库既有风格一致。本仓库的约定是动词开头、可用英文类型前缀，例如：

```text
Fix: correct outdated clone command in Git configuration chapter
Docs: add Personal Access Token section
```

描述正文与本仓库 `.github/pull_request_template.md` 的字段一一对应。一份完整范例如下：

```markdown
## 关联章节/文件

- 文档路径：`docs/ch3/git/3-basic-configuration.md`

## 修改类型

- [x] 内容补充
- [x] 错别字/语句修正
- [ ] 格式调整
- [ ] 图片/附件更新
- [ ] 代码示例修改
- [ ] 其他 (请说明):

## 修改描述

- **问题**：`3-basic-configuration.md` 仍写着 HTTPS 克隆“需要每次输入密码”，但 GitHub 自 2021 年 8 月起已禁用密码认证，按文档操作会失败。
- **方案**：改写为“HTTPS 需要 Personal Access Token，SSH 需要密钥”，并新增 `### 使用 Personal Access Token（PAT）` 小节，说明最小权限创建、凭据助手保存方式，以及不要把令牌提交进仓库的警告。
- **不在本次范围内**：不改动 SSH 端口与代理配置那一节；平台对比表的调整另开 PR。
- **如何验证**：在本地执行 `mkdocs serve`，确认新增小节的提示框、表格与代码块渲染正常，页面内链接可跳转。

## 本地验证

- [x] 已通过 `autocorrect --lint .` 检查
- [x] 已执行 `mkdocs serve` 并在本地预览，确认页面渲染正常、链接有效

## 附加说明 (可选)

内容依据 GitHub 官方认证方式的变更，未引入新的外部依赖。
```

!!! tip "PR 描述不等于复述 diff"

    diff 说明“改了什么”，描述要回答“为什么改、边界在哪里、别人怎么验证”。评审者读不懂动机时，最常见的结果是请求补充而非直接合并。

## 响应 Code Review

提交后继续向同一分支推送，Pull Request 会自动更新。收到反馈时：

1. 逐条确认评审意见的含义。
2. 修改代码或文档，并重新运行相关检查。
3. 推送到原分支，不要关闭后重复创建 Pull Request。
4. 回复修改位置和验证结果；不同意时说明事实和技术依据。

!!! warning "谨慎改写远程历史"

    不要对共享分支使用强制推送。若项目要求整理个人分支提交，确认只有自己使用该分支后，再使用 `git push --force-with-lease`，并遵循维护者给出的流程。

## 作为评审者

评审他人的 Pull Request 是本课程的一部分，也是理解维护者视角最快的途径。

### 一次有效评审的顺序

1. **先跑起来**：按 PR 描述的验证步骤在本地复现。“我按描述跑不起来”本身就是最有价值的一条评审意见。
2. **再看范围**：修改是否只做了一件事？有没有夹带无关改动、构建产物或密钥？
3. **再看细节**：命名是否贴切，注释是否解释了“为什么”，边界条件、文档和测试是否同步更新。
4. **区分阻塞与建议**：会导致错误、破坏兼容或缺少必要测试的问题明确标为必须修改；个人风格偏好写成“建议/可以考虑”，不要把两类混在一起。
5. **提问代替断言**：把“这里应该改成 X”换成“这里改成 X 是出于什么考虑？如果出现 Y 场景会怎样？”，既表达观点又给对方解释空间。
6. **24 小时内首次回应**：哪怕只是一句“我今天稍晚细看”，也能让对方确认 PR 没有被忽略。

### 不同意时的措辞模板

- **事实分歧**：“我按 README 的步骤执行到第 3 步时报错，日志见下。请问是我的环境问题，还是文档需要补充前置条件？”
- **方案分歧**：“我理解这样能解决问题。不过它会让 A 场景多一次网络请求，是否可以用 B 方案避免？如果维护者更倾向现有实现，我可以补充对应的测试。”
- **范围分歧**：“这部分改动看起来有价值，但和本 Issue 的目标不同。能否拆成单独的 PR？这样本 PR 会更容易被合并。”

### 用 GitHub 的 suggestion 直接给修改

在 PR 的 **Files changed** 页面，把鼠标移到目标行上点击 `+`，选择 **Add a suggestion**，写入推荐的替换内容。作者可以直接点 **Commit suggestion** 应用。它适合改错别字或改一行命令，不适合大段重写。

### 被要求整理提交时

维护者要求 squash 时，用交互式变基把多条提交并成一条（或少数几条有意义的提交）：

```bash
git rebase -i BASE       # 把后续的 pick 改成 squash 或 fixup
git push --force-with-lease
```

具体按键和效果见 [Rebase 与 Merge](advanced/1-rebase-merge.md)。

## DCO 与 CLA：怎么判断、怎么补救

不少项目要求贡献者声明“我有权按项目许可证提交这段代码”。常见机制有两种，**先读目标项目的 `CONTRIBUTING`，以项目要求为准**。

| 机制 | 是什么 | 表现形式 | 覆盖面 |
| ---- | ------ | -------- | ------ |
| DCO（Developer Certificate of Origin） | 你声明对每个提交拥有提交权，同意按项目许可证分发 | 每个提交脚注里有一行 `Signed-off-by: 姓名 <邮箱>` | 逐提交 |
| CLA（Contributor License Agreement） | 你与项目或基金会签署一份法律协议，通常还包含版权或专利授权 | 首次 PR 时机器人给出链接，点击或邮件签署 | 一次性，覆盖之后的贡献 |

### 怎么判断项目要哪一类

- PR 出现 `DCO` 检查，或机器人提示 `Expected "Signed-off-by"`，走的是 DCO；
- 出现 `cla-assistant`、`EasyCLA` 之类的机器人，或贡献指南里写着“Sign our CLA”，走的是 CLA；
- Linux 内核、QEMU 等邮件列表流程同样要求 `Signed-off-by`；
- 两者都要求、或都不要求，都是正常情况。

### DCO 缺失怎么补救

提交时加上 `-s`，Git 会自动写入签名行：

```bash
git commit -s
```

如果已经推送到 PR 才发现漏签，用 `--signoff` 给分支上的提交补签：

```bash
git rebase --signoff BASE          # BASE 是 PR 的基准，例如 upstream/main
git push --force-with-lease          # 仅限只有自己使用的分支
```

!!! warning "签名不是可以随便补的"

    `Signed-off-by` 使用你配置的 `user.name` 与 `user.email`，必须真实可联系。不要替他人添加 `Signed-off-by`、`Reviewed-by` 或 `Tested-by`，这属于伪造他人声明。若你所在机构对贡献有额外要求，先与教师和维护者沟通。

## 常见问题

??? question "维护者没有回复怎么办？"

    先检查项目说明的响应周期。经过合理等待后，可以在原讨论中礼貌补充一次信息。不要重复创建 Issue、频繁点名维护者或转向私人渠道施压。课程评分不以维护者是否及时回复为依据。

??? question "PR 没有被接受，贡献是否失败？"

    不一定。方案被拒绝可能来自范围、兼容性、维护成本或项目方向。保存公开反馈，说明自己如何理解和调整，这同样是有价值的开源学习成果。

??? question "发现安全漏洞怎么办？"

    不要创建公开 Issue 或公开披露复现细节。阅读 `SECURITY` 文件，使用项目指定的私密报告渠道，并及时联系教师。

## 完成标准

完成本节后，你应当能够提供：

- 可访问的 Issue、Pull Request 或补丁链接；
- 聚焦且可解释的修改，以及基于最新上游分支的提交记录；
- 与贡献类型匹配的验证结果，包括自动检查状态或失败原因说明；
- 规范、尊重且可追踪的社区交流，至少一次对他人贡献的评审回应；
- 对反馈、结果和下一步的简短复盘。

课程项目的完整里程碑和异常情况处理见[真实贡献项目](../../course/project.md)。
