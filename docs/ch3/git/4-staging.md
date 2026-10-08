# Git 暂存区与提交

## 学习目标

完成本节后，你应当能够：

1. 区分工作区、暂存区和当前提交；
2. 查看修改并选择本次提交包含的内容；
3. 撤销误暂存的文件而不丢失工作区修改；
4. 创建一项范围聚焦、可以解释的提交。

## 三个区域

```mermaid
graph LR
    A[工作区] -->|git add| B[暂存区]
    B -->|git commit| C[本地仓库]
    B -->|git restore --staged| A
```

- **工作区**：当前正在编辑的文件。
- **暂存区**：准备放入下一次提交的文件内容。
- **本地仓库**：已经形成的提交历史。

暂存区允许你从多项本地修改中选择一部分，避免把无关内容混入同一个提交。

## 查看当前状态

先使用以下命令确认分支、已暂存修改和未暂存修改：

```bash
git status
```

查看工作区与暂存区的内容差异：

```bash
git diff
```

查看暂存区与当前提交的内容差异：

```bash
git diff --staged
```

只看每个文件改了多少行、不展示具体内容：

```bash
git diff --stat
```

`git status` 回答“哪些文件处于什么状态”，`git diff` 回答“具体改了什么”，`git diff --stat` 回答“这次改动大致有多大”。

## 选择要提交的修改

暂存指定文件：

```bash
git add docs/example.md
```

暂存指定目录：

```bash
git add docs/ch1/
```

逐块选择同一文件中的修改：

```bash
git add -p
```

进入交互后，Git 会逐个“块（hunk）”询问你的决定，常用按键如下：

| 按键 | 含义 | 使用建议 |
| ---- | ---- | -------- |
| `y` | 暂存这个块 | 确认与本次提交相关 |
| `n` | 不暂存这个块 | 无关修改或调试代码 |
| `s` | 把当前块拆成更小的块 | 一个块里混了相关和无关改动时 |
| `e` | 手动编辑当前块 | 需要逐行挑选，要求理解 diff 格式 |
| `q` | 退出，已做的选择保留 | 中途放弃，不再处理后续块 |
| `?` | 查看全部按键帮助 | 忘记按键时 |

`git add .` 会暂存当前目录下的全部修改。使用前应先检查 `git status`，确认其中不包含构建产物、密钥或与当前任务无关的文件。

## 撤销误暂存

将指定文件移出暂存区，同时保留工作区中的修改：

```bash
git restore --staged docs/example.md
```

撤销全部暂存内容：

```bash
git restore --staged .
```

这两条命令不会删除工作区修改。执行后再次运行 `git status` 和 `git diff` 确认结果。

## 创建提交

提交前完成三项检查：

```bash
git status
git diff --staged
git diff --check
```

确认差异聚焦且没有明显空白错误后创建提交：

```bash
git commit
```

提交时可以在编辑器里同时看到已暂存差异，帮助自己复核：

```bash
git commit -v
```

`git commit -v` 把暂存区的 diff 作为注释附在提交信息模板下方，写信息时能直接对照改动，**不会**把注释写进最终提交。推荐在写较长的提交信息时使用。

如果需要快速提交所有**已跟踪**文件的修改，可以跳过显式 `git add`：

```bash
git commit -a
```

- **取舍**：`-a` 省事，适合“我确认这次所有已跟踪修改都属于同一个逻辑变更”的场景。
- **风险**：它会一次性吞掉所有已跟踪文件的修改，容易把调试代码、临时注释或密钥一起提交；它**不会**包含新建的未跟踪文件，容易出现“以为提交了其实没有”的错觉。本课程建议先用 `git status` 和 `git add -p` 明确选择，再 `git commit`。

提交信息应说明这项修改做了什么以及为什么需要修改。项目若规定了提交格式、签名或 DCO，应遵循项目自己的贡献指南。

## 修改最后一次提交

如果最后一次提交尚未共享，并且只需要修正提交信息或补入遗漏内容，可以使用：

```bash
git commit --amend
```

这会创建一个新的提交对象。已经推送并供他人使用的提交不应随意改写。

### 用 `--fixup` 与 `rebase -i --autosquash` 整理提交

如果错误出在**更早**的提交上（例如第 2 个提交漏了一个文件，而后面又提交了三次），不必手工记忆每个哈希。`--fixup` 和 `--autosquash` 是配套的三件套：

下面的 `SHA` 需要替换为要修补的提交哈希，`SHA^` 表示它的父提交；本例假设要修补的不是仓库的首次提交。

```bash
# 1. 照常修改文件并暂存
git add path/to/file

# 2. 把它标记为“对 SHA 的修补”
git commit --fixup SHA

# 3. 交互式变基时自动把 fixup 排到对应提交之后并标记为 fixup
git rebase -i --autosquash SHA^
```

在打开的编辑器中，`fixup!` 开头的行会被自动放到目标提交之后并标记为 `fixup`，保存退出后 Git 会把它们合并进原提交，历史看起来就像一次写对。

> `--autosquash` 也可以配成默认行为：`git config --global rebase.autoSquash true`。

!!! warning "改写历史的前提"

    这一套操作会重写提交哈希，只应在**尚未推送**、或**只有你自己使用**的个人分支上做。分支已经推送时，整理后用 `git push --force-with-lease` 更新，不能对共享分支强制推送。详见 [Rebase 与 Merge](advanced/1-rebase-merge.md)。

## 常见失败场景

### 误把构建产物或密钥 `add` 进来

如果错误内容还没提交，先用 `git restore --staged` 把它移出暂存区；如果它已经被提交过一次，就需要同时把它从版本库中移除、但保留本地文件：

```bash
# 仅从 Git 跟踪中移除，本地文件保留；随后把它写进 .gitignore
git rm --cached build/output.bin
git commit -m "chore: stop tracking build artifacts"
```

!!! danger "密钥已经提交并被推送"

    `git rm --cached` 只是让后续提交不再包含它，**历史里仍然存在**。正确顺序是：立即在服务端**吊销/轮换**该凭据，再按项目要求处理历史（例如 `git filter-repo` 或平台提供的清理流程），并通知维护者。不要以为删掉文件就安全了。

### 把无关修改混进了提交

```bash
# 撤销最近一次提交，把内容退回暂存区，再重新拆分
git reset --soft HEAD~1
```

这条命令只移动分支指针，不丢弃内容；随后用 `git restore --staged` 和 `git add -p` 重新组织成两个聚焦的提交。相比之下 `git reset --hard` 会直接丢弃工作区修改，除非你确定不要这些内容，否则不要使用。

!!! danger "谨慎使用 reset --hard"

    `git reset --hard` 会移动当前分支并丢弃工作区和暂存区中的修改。本课程的常规贡献流程不需要使用它。需要恢复文件或撤销暂存时，优先使用作用范围更明确的 `git restore`。

## 实践任务

1. 在练习仓库中修改两个文件，并让其中一个文件包含两处独立修改。
2. 使用 `git add -p` 只暂存一处修改。
3. 用 `git diff` 和 `git diff --staged` 解释剩余修改分别位于哪个区域。
4. 创建一次聚焦提交，再用 `git show --stat` 和 `git show` 检查结果。
5. 记下第 4 步提交的哈希，用它替换下面的 `SHA`。再做一个小的修补并暂存，用 `git commit --fixup SHA` 创建修补提交。若前面还保留了其他未提交改动，先用 `git stash push -u` 保存。然后用 `git rebase -i --autosquash SHA^` 把修补合并回原提交，若使用了 stash，再用 `git stash pop` 取回改动。最后用 `git log --oneline` 和 `git show` 确认修补已合入，且没有独立的 `fixup!` 提交。

完成后，你应当能够准确说明“下一次提交将包含什么”，而不是依赖试错来操作 Git。
