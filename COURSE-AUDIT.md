# 《开源软件通识》教材评审报告与丰满方案

> 评审日期：2026-09-27
> 评审对象：`docs/` 下 45 个 Markdown 文件（约 9.2 万中文字，含代码约 45 万字符）
> 核查方式：逐文件通读 + 程序化体例检查 + `mkdocs build` 实际构建 + 与 `docs/course/` 课程设计逐条对照
> 说明：本报告是**待讨论的评审意见**，不是已生效的教材内容。文件位于仓库根目录，不参与站点构建，可随时删除或转为 Issue 清单。

---

## 摘要：五条最重要的判断

1. **课程设计（`docs/course/`）质量高，教材正文没跟上。** 大纲、项目制、评分办法已经是一套完整、可落地的 16 课时课程设计；但正文大部分仍是"课堂讲座稿 + 资料汇编"，没有按 8 次课重组，也没有提供三次关键"当次成果"（项目画像、许可证判断练习、贡献提案）所需的支撑材料。
2. **第一章第二节存在系统性内容可信度风险，这是当前最紧急的问题。** `docs/ch1/sec2/history-of-oss.md` 含 **47 处百分比断言、0 条超链接、0 条脚注**，其中包含"微软收购 git""GitHub 引入 zk-SNARK 身份验证""2025 年 OpenHarmony 10% 设备被 AI 投毒、召回成本 3 亿美元"等无法证实或明确错误的内容。课程自定的"对事实、数据和案例标注来源与时间"原则在这一节被整体违反。
3. **有一批"照抄即失败"的技术示例。** `git config --global sendemail.smtpEncryption stl`（正确值为 `ssl`/`tls`）、`git config --global sendemail.smtpPass = <密码>`（多了一个 `=`）、QEMU 镜像版本号在同一篇里出现四个不同值、Docker 的 Jupyter 示例教用户关闭认证并禁用 XSRF。这些会直接造成学生操作失败或形成错误安全习惯。
4. **结构与导航有真实的编号错位和职责混淆。** 目录名 `sec0/sec1/sec2` 与导航"第一节/第二节/第三节"不对应；`docs/ch3/sec1/subsec3/` 把必修内容（参与开源项目）和课外拓展（rebase、Git 底层原理）放在同一个目录；`docs/ch3/sec1/subsec1/2-code-hosting-platforms.md` 一个文件里有 **4 个一级标题**（4 篇文档被拼在一起）。
5. **体例合规率很低，而且多是无成本的机械修复（"快赢"）。** 全站 25 张图片没有一处**正确**使用图注语法——有 6 处写了图注却全用了全角符号（`{： 。caption}`），导致 `extra.css` 的 `.caption` 样式完全失效；45 个文件中只有 9 个有"主要作者"署名框；有 3 处 `!!! tips`、2 处 `???+ node`、1 处 `??? answer` 这类**渲染不出来的提示框拼写错误**；`docs/includes/` 目录不存在但 `mkdocs.yml` 仍在 auto_append；仓库里还有一个 **16 MB 的 WAV 文件**（占站点 26 MB 的六成）。

---

## 执行记录：本次已完成的三条线（2026-09-27）

> 本节记录实际落地的改动。**报告中所有"文件：行号"引用的是改造前的旧路径**，改造后的路径见 §8.1 与下表。

### B 结构与体例（全部完成）

| 项目 | 改造前 | 改造后 |
|------|--------|--------|
| `docs/ch3/` 目录编号错位 | `sec0`(叫第一节) / `sec1`(第二节) / `sec2`(第三节) / `sec3`(Docker) / `sec4`(QEMU) / `sec5`(工具) | `writing/` / `git/` / `linux/` / `docker/` / `qemu/` / `tools/`，24 个文件迁移，`mkdocs.yml` 与全部站内链接同步 |
| 必修与拓展混放 | `git/subsec3/` 同时放必修的"参与开源项目"和拓展的 Git 底层 | 必修 → `git/6-participate-in.md`；拓展 → `git/advanced/` |
| 单文件 4 个一级标题 | `2-code-hosting-platforms.md`（564 行，4 个 H1） | 拆为 `git/platform/` 下 4 页（index / practice-register / practice-repository / practice-fork），内容逐行比对无损 |
| 无效提示框 | `!!! tips`×3、`???+ node`×2、`??? answer`×1 | 全部修正；全库无效提示框为 0 |
| 图注语法 | `{： 。caption}`×2、`{： .caption}`×4 → 样式完全失效 | 13 处图注全部使用半角 `{: .caption }`；真实图片 13/13 已配图注 |
| 署名框 | 9 / 45 | **23 / 50**（新增 14 处，其中 5 处把正文里的"本节作者：…"提升为规范署名框） |
| 标题 emoji | 8 个文件标题含 emoji | 全部移除 |
| 文件名与 nav 不一致 | `semeste`（缺 r）、`2-Control-Process.md`、H1 与 nav 名称不一 | `2-missing-semester.md`、`2-control-process.md`、H1 与 nav 全部对齐 |
| 残留历史编号 | `# 4.1.3.2 …`、`### 3.3 架构图`、全角序号 `1。` | 全部清除 |

### A P0 止血（已完成）

- **内容可信度**：`docs/ch1/sec2/history-of-oss.md` 的百分比断言 **38 → 0**，全库 71 → 21（剩余 21 处全部是合法用途：博弈算术、`docker stats` 输出、`git clone` 输出、评分权重）。删除或改写的内容包括"微软收购 git"、GitHub 使用 zk-SNARK、2025 年 AI 投毒与 3 亿美元召回、"Log4j 97%"、MindSpore 30.26%、以及整节《GB/T 44272-2024》对比（该标准号公开渠道无法证实）。Copilot X 营销式整节替换为定性讨论；供应链一节改用可确证的 CVE-2021-44228 与 CVE-2024-3094。
- **许可证事实**：Apache-2.0 表述为宽松 + 专利条款（不再称"弱传染"）、GPLv3 专利授权、OpenSSL 从 LGPL 示例中移除、Redis 改为"曾为 BSD-3-Clause，现为 AGPLv3"、Linux 内核明确为 `GPL-2.0-only`、SSPL 改为"基于 AGPLv3 第 13 条改写"、FSF 1985、GPLv1 1989、Sun/Oracle 收购 MySQL 时间线。
- **技术性错误**：`sendemail.smtpEncryption stl`→`ssl/tls`（含端口对照表）、`smtpPass =` 多余等号、QEMU 镜像版本四处不一致统一为 24.04.2、`-smp 32`→`4`、SSH clone 改 HTTPS、Docker Jupyter 示例删除关闭认证与 XSRF 并只绑回环、Compose 删除废弃的 `version` 字段并改名 `compose.yaml`、镜像 tag 全面更新、`git checkout --`→`git restore`、`reset --hard` 补 danger、`xtm4z`→`z/x/m`、`p7zip`→`7z`、`yum`→`dnf`、SHA-1"加密"表述修正、新增 PAT 小节（此前全库 0 次）。
- **命令占位符**：`docker stop <container_id>` 这类写法在 bash 中会触发重定向，约 50 行改为 `CONTAINER_ID` 形式（HTML 标签、邮箱、`#include` 与"讲解该隐患"的原文均保留）。
- **仓库工程**：16 MB WAV → 2.7 MB MP3（−83%，引用同步更新）；`actions/setup-python` v4→v5；CI 中 `curl | sh` 改为"下载 → 打印 → 执行"（与课程自身的安全口径一致）；修复 fork PR 无法回推导致的静默失败（改为同仓库才回推，fork 走自动修复 PR）并上传修复产物为 artifact；`AGENTS.md` 按当前结构重写。
- **口径统一**：全库唯一残留的 `curl | sh` 只剩两处"反面示例"说明文字。

### C 第 3 次课许可证内容（已完成）

- **重建** `docs/ch2/sec1/2-open_source_licenses.md`（1.7 KB → 约 14 KB）：学习目标、义务何时触发（使用/修改/分发/网络服务四类行为）、许可证家族全景（宽松/弱 copyleft/强 copyleft/source-available/内容数据硬件/AI 模型）、GPL v1-v2-v3 差异表、兼容性矩阵与"链接不等于组合"、10 条常见误判、选择决策树、SPDX 标识符规范、自测题。
- **新增** `docs/ch2/sec1/3-license-practice.md`：这是第 3 次课的**当次成果**。含 5 组练习（SPDX 识别 10 题、义务判断 10 题、兼容性 5 题、固件综合场景、找错题），**每题附参考答案与理由**，并给出教师用评分标准。已加入 nav。
- **扩写** `docs/ch2/sec3/3-legal-and-compliance.md`（5.8 KB → 16 KB）：修正 CLA/DCO 嵌套提示框、用真实判例（Jacobsen v. Katzer、Artifex v. Hancom、BusyBox、数字天堂案、"不乱买"案）替换"何同学"热点案例、新增合规基础设施（SPDX / SBOM 的 SPDX 与 CycloneDX / ScanCode、FOSSA、ORT、reuse / OpenChain ISO-IEC 5230 / 欧盟 CRA 时间表）、企业合规五步流程、中国开源法律实践（含 MulanPSL-2.0 与开放原子基金会）、讨论题附参考要点。
- 另外补齐了课程主线缺口：`docs/ch1/sec4/how-to-oss.md` 新增"第一次贡献的操作清单"（8 步，与 `course/project.md` 对齐）；`docs/ch2/sec1/1-open_source_ecosystem.md` 新增生态角色全景与角色分析工作表；`docs/ch2/sec2/culture.md` 新增行为准则读法、沟通礼仪、社区健康度；`docs/ch2/sec1/terminology.md` 升级为 24 条术语表；`docs/ch2/sec3/rules.md` 新增项目入口档案与提案写作；`docs/ch3/git/6-participate-in.md` 补充任务检索、CI 排障、PR 范例、评审者视角、upstream 同步、DCO/CLA 六节。

### 验证结果

```text
mkdocs build                ✅ 成功，无警告
nav 覆盖                    50 / 50，无未纳入、无死链
站内链接检查                 失效 0
一级标题唯一                 0 个文件违反
代码围栏配对                 全部通过
无效提示框 / 全角 caption     0
标题 emoji                   0
中文字数                     91,953 → 120,865（+31%）
```

### 评审后续修正（Codex review）

PR 提交后，仓库配置的 Codex 评审先后进行了 7 轮，共提出 **31 条意见**（2 条 P1 + 29 条 P2），已全部处理并逐条回复。按类别归纳：

| 类别 | 主要问题 | 处理 |
|------|----------|------|
| CI（4 条） | fork PR 的 token 恒为只读，却承诺自动修复 PR；安装脚本被 `git add -A` 误提交；`push` 事件下判断条件恒真 | 安装脚本改到 `$RUNNER_TEMP` 并加 `.gitignore` 兜底；fork PR 改为运行摘要 + 只打包修改文件的 artifact；权限收敛为 `contents: write`；显式区分 `push` / `pull_request` |
| 许可证事实（14 条） | Apache-2.0 被当成 copyleft；Apache-2.0 与 GPLv3 被误判为不兼容；Llama 被写成 Apache-2.0；Nginx 被写成 `BSD-3-Clause`；Git 与 Nextcloud 的 `only`/`or-later` 写反；MPL 的源码范围与次级许可证条件两次写错；AGPL 第 13 条被"内部分发"错误豁免；ODbL 义务不全 | 逐条按许可证原文修正（§1.12/§3.2/§3.3/§4.4、GPLv3 第 11 条、AGPL 第 13 条），并把兼容性矩阵统一为完整 SPDX 标识符 |
| Docker / QEMU（8 条） | `command: >-` 折叠换行导致 heredoc 失效；Compose 变量插值破坏配置与前端；只读根文件系统与 `--user`、capabilities 三个示例起不来；`WORKDIR` 属主导致 Jupyter 无法保存；Docker Desktop 的 host networking 被写成"不生效"；QEMU 源码仓库未按 24.04 的 deb822 格式启用 | 改为真实构建上下文（新增 `nginx/`、`frontend/` 的 Dockerfile 与文件）；补齐可写目录与 capabilities；改用官方非 root 变体；按 `Types: deb deb-src` 改写；host networking 补版本与开关 |
| Git / Linux（4 条） | 误提交到 `main` 的恢复流程缺"重置 main"这一步；`git merge` 被声称一定产生合并提交；`7z` 混用了包装器语法；静态链接结论缺分发前提 | 补 `git reset --hard upstream/main`（含风险提示）；说明 `--ff` 快进与 `--no-ff`；改为 `7z x`/`7z a`；题设与答案补上"对外分发"前提 |

所有修正均已通过 `mkdocs build`（零告警）、`autocorrect --lint`（无问题）与站内链接检查，CI 的 `build`、`markdown-lint` 均为 success。

**容器级实测（Docker 29.8.1 / Docker Desktop，本机执行）**：本节所有 Docker 示例都已实际运行验证，修正前后的对比结果如下。

| 文档中的示例 | 修正前 | 修正后 |
|--------------|--------|--------|
| 只读根文件系统（`1-foundation.md`、`3-storage.md`） | ❌ `mkdir() "/var/cache/nginx/client_temp" failed (30: Read-only file system)` | ✅ 容器正常运行 |
| capabilities（`1-foundation.md`） | ❌ `chown("/var/cache/nginx/client_temp", 101) failed (1: Operation not permitted)` | ✅ 需 `NET_BIND_SERVICE + SETGID + SETUID + CHOWN`（实测这四项齐备才启动） |
| 官方镜像直接 `--user`（`1-foundation.md`） | ❌ `mkdir() ... failed (13: Permission denied)` | ✅ 改用 `nginxinc/nginx-unprivileged`，`--cap-drop=ALL` 零能力亦可运行，HTTP 200 |
| Compose Todo 项目（`5-compose.md`） | ❌ 内联 heredoc 因换行折叠与变量插值无法启动 | ✅ 4 个容器全部就绪（backend/mongodb healthy）；页面 200、`/api/todos` 完整 CRUD（201/200/200/204）、`down` 后重新 `up` 数据仍在（命名卷持久化） |
| Jupyter 非 root 工作目录（`2-dockerfile.md`） | ❌ `touch: cannot touch '/notebooks/new.ipynb': Permission denied` | ✅ `WRITE_OK`，`/notebooks` 属主为 `jupyter:jupyter` |
| MySQL 口令与持久化（`3-storage.md`） | ❌ 变量未定义 + 登录用硬编码口令 | ✅ 同一变量登录成功；删容器后复用同一卷，`SELECT * FROM users` 仍返回原数据 |
| host 网络（`4-network.md`） | 笼统写"在 macOS 上不生效" | ✅ 实测：两个 `host` 网络容器争用 80 端口复现 `bind() ... Address already in use`；`HostNetworkingEnabled = false` 时容器访问宿主机 `127.0.0.1:18099` 失败。文档已按这一差异改写 |

> 注：本机 Docker 的 buildx 状态目录默认在 `~/.docker/buildx`，在受限沙箱下需要设置 `BUILDX_CONFIG` 才能构建；这是执行环境的限制，不影响文档内容。


### 仍需你决策的事项

1. **27 个文件仍无署名框**。git 历史无法可靠推断：多数文件由 5 位以上贡献者各提交 1 次，最长者也只有 2 次提交。**我不建议按"提交次数最多"自动填写**，请由章节负责人自述。已有的 23 处中，5 处来自文件内已有的"本节作者"声明，9 处来自单一作者独占全部提交的文件（其中 `yxw`、`yinchunyuan`、`CAICAII` 等来自 git 作者名，若与 GitHub 账号不一致请更正）。
2. **许可证事实需联网复核**：欧盟 CRA 的分阶段生效日期、SPDX 兼容性矩阵中的边界情形（MPL-2.0 与 GPL 的双向性、EPL-2.0 的次级许可证条款）、MulanPSL-2.0 获 OSI 批准的年份。
3. ~~**站点 URL 已变化**~~：已于本轮解决。`docs/ch3/` 下的路径重组后，引入 `mkdocs-redirects` 并在 `mkdocs.yml` 中配置 24 条 `redirect_maps`，覆盖旧树的全部页面（如 `/ch3/sec1/subsec1/1-git-introduction/` → `/ch3/git/1-introduction/`）；`requirements.txt` 已加入该依赖。构建后逐个核对：24 个旧路径页面均生成且指向新地址。
4. **`neofetch` 的维护状态**：据报告上游已停止维护，但本环境无法联网确证，故未替换。
5. **提交拆分**：当前暂存区**混合了会话前你已有的未提交重构**（`docs/course/`、`README.md`、`Assignment.md`、`mkdocs.yml`、`ch3/index.md`、`ch4/index.md`、`docs/index.md`、`ch99/abouts.md` 等）与本次改造。建议按下列分组拆分提交，或先 `git reset` 自行整理：
   - 你的课程设计层：`docs/course/*`、`README.md`、`Assignment.md`、`docs/index.md`、`ch99/abouts.md`
   - 结构重构：目录迁移 + `mkdocs.yml` nav
   - 事实与技术错误修正：`ch1/*`、`ch2/sec1/1-*`、`ch2/sec2/*`、`ch3/*`
   - 许可证章节与练习：`ch2/sec1/2-*`、`ch2/sec1/3-*`、`ch2/sec3/3-*`
   - 体例与工程：署名框、图注、CI、音频、`AGENTS.md`
   - 评审报告：`COURSE-AUDIT.md`
6. **本次未做的剩余项**（见 §8.3、§9 阶段 4–5）：`ch3/tools/1-useful-oss.md` 仍是 606 行的"通读材料"，建议改写为速查手册并拆分；Docker 六篇可精简为三篇；`ch3/linux/1-commands.md` 仍偏长；§8.3 列出的新增专题（开源与 AI、供应链安全、中国开源生态、职业路径）只做了局部补充，尚未独立成节；教师手册、案例库、练习库等教学基础设施尚未建立。

---

## 一、现状盘点

### 1.1 体量分布

| 模块 | 中文字数 | 约合阅读时长 | 对应课时 | 判断 |
|------|---------:|-------------:|----------|------|
| ch0 课程导入 | 1,682 | 4 min | 第 1 次课开场 | 偏少，且风格与全书不一致 |
| ch1 开源简介 | 25,496 | 64 min | 第 1、2 次课 | 单节严重超量，含高风险内容 |
| ch2 基础理论 | 22,043 | 55 min | 第 2、3、4 次课 | 内容与课时错配（许可证过薄、治理尚可） |
| ch3 必修（Markdown/Git/平台/Linux） | 19,340 | 48 min | 第 5、6、7 次课 | 骨架正确，缺流程化与练习 |
| ch3 拓展（Git 进阶/Docker/QEMU/工具） | 20,208 | 51 min | 课外 | 篇幅与必修相当，定位与形态不匹配 |
| ch4 持续参与 | 668 | 2 min | 第 8 次课（整次） | **严重不足** |
| course 课程指南 | 2,516 | 6 min | — | 质量最高 |
| **合计** | **91,953** | **约 230 min** | 720 min | 总量不算多，问题在分布与教学法 |

> 总阅读量只占课堂时长的三分之一，说明**教材不缺字数，缺的是"课堂怎么用"**：学习目标、活动、练习、产出物、自测。

### 1.2 "新层"与"旧层"

仓库正处于一次未提交的重构中间状态（`git status` 显示 16 个文件已修改、`docs/course/` 未跟踪）。可以清楚区分两层：

**新层（目标形态，质量好，应作为全站样板）**

- `docs/course/{index,project,assessment}.md`：课程大纲、项目制、评分办法
- `docs/index.md`、`README.md`、`Assignment.md`、`docs/ch99/abouts.md`
- `docs/ch3/index.md`、`docs/ch4/index.md`
- `docs/ch3/sec1/index.md`、`docs/ch2/sec1/terminology.md`、`docs/ch2/sec3/rules.md`（三个导览）
- `docs/ch3/sec1/subsec2/2-staging.md`、`docs/ch3/sec1/subsec3/5-participate-in.md`

新层的共同特征：面向"你"、有明确学习目标、有安全习惯提示、有"完成标准/实践任务"、结论可执行。

**旧层（未迁移）**

- `docs/ch0/index.md`（口吻夸张、大量感叹号，与全书不一致）
- `docs/ch1/{index,sec1,sec2,sec3,sec4}`（讲座稿体，无学习目标、无练习、无来源）
- `docs/ch2/sec1/*`、`docs/ch2/sec2/culture.md`、`docs/ch2/sec3/*`（资料汇编体，emoji 与标题编号不统一）
- `docs/ch3/sec0/*`、`docs/ch3/sec1/subsec1|subsec2|subsec3/*`、`docs/ch3/sec2/*`、`docs/ch3/sec3..5/*`

**结论：本轮工作的性质不是"再写一本教材"，而是"把旧层按新层标准迁移，并补齐课程设计承诺的成果材料"。**

---

## 二、P0：内容可信度问题（必须先处理）

### 2.1 数量特征

| 文件 | 百分比断言 | 脚注/引用 | 超链接 |
|------|-----------:|----------:|-------:|
| `docs/ch1/sec2/history-of-oss.md` | **47** | 0 | **0** |
| `docs/ch1/sec3/why-oss.md` | 15 | 0 | 0 |
| `docs/ch2/sec2/culture.md` | 4 | 0 | 16 |
| 其余章节 | 0–4 | 0 | — |

第一章第二节是唯一一个"高密度定量断言 + 零来源"并存的文件。这不是排版问题，而是教材的学术诚信问题——课程本身在 `docs/course/assessment.md` 里要求学生"引用第三方文字、图片、代码或数据时，应保留来源"，教材应该先做到。

### 2.2 明确的事实错误（建议直接改）

| # | 位置 | 原文 | 问题 | 建议 |
|---|------|------|------|------|
| 1 | `ch1/sec2:296` | `##### **微软收购 git 的争议与影响**` | 主体错误。微软 2018 年收购的是 **GitHub**（75 亿美元）；Git 由 Linus 于 2005 年创建，从未被收购 | 改为"微软收购 GitHub"，并补一句"Git 不属于任何公司" |
| 2 | `ch1/sec2:248` | "2004 年 Oracle 收购 MySQL" | 年份与主体双错。2008 年 Sun 收购 MySQL AB，2010 年 Oracle 收购 Sun 才间接获得 MySQL | 改写为正确链路 |
| 3 | `ch1/sec2:89` | "Linux 内核采用 GPLv2（后升级至 GPLv3）" | 内核至今为 **GPL-2.0-only**，Torvalds 明确反对 GPLv3 | 改为"自 1992 年 0.12 版起 GPLv2，并明确停留在 v2" |
| 4 | `ch1/sec2:70` | "MongoDB 采用 SSPL（GPLv2 变种）" | SSPL 基于 **AGPLv3** 第 13 条改写 | 改为"基于 AGPLv3" |
| 5 | `ch1/sec2:452` | "1983 年 Stallman 创立 FSF" | FSF 成立于 **1985 年**；1983 年是 GNU 宣言与 GNU 计划 | 改为 1985 年 |
| 6 | `ch2/culture.md:71` | "OSI 制定开源定义…该理念催生 GPLv2（1991）、GPLv3（2007）" | 时序与归属双错：GPLv2 早于 OSI（1998），GPLv3 由 FSF 主导 | 拆成"自由软件运动 → GPLv2/v3"与"1998 年 OSI 提出开源定义"两条线 |
| 7 | `ch1/sec1:99` | Apache HTTP Server 是"世界上最早的开源 Web 服务器" | CERN httpd（1990）、NCSA HTTPd（1993）更早 | 改为"最流行的开源 Web 服务器之一" |
| 8 | `ch2/sec1/2-open_source_licenses.md:18` | "Apache 弱传染" | **Apache-2.0 不是 copyleft，没有传染性**；义务是保留声明、附许可证、NOTICE、标注变更、专利报复终止 | 删去"弱传染"，单列"宽松 + 明确专利授权" |
| 9 | 同上 `:16` | "GPL：专利条款 ❌" | GPLv3 第 11 条是明确专利授权；GPLv2 被 FSF 解释为含隐含许可 | 改为"v2 隐含 / v3 明确" |
| 10 | 同上 `:20` | "LGPL 典型用户：GTK, **OpenSSL**" | OpenSSL 3.0 起为 Apache-2.0，历史许可是 OpenSSL/SSLeay 双许可，从来不是 LGPL | 换为 glibc（LGPLv2.1+）、Qt（LGPLv3 双授权） |
| 11 | 同上 `:19` | "BSD 典型用户：Nginx, **Redis**" | Redis 2018 年转 RSALv2/SSPLv1，2024 年 SSPLv1，2025 年 Redis 8 回归 AGPLv3 | 直接改写为"曾为 BSD-3-Clause，现为 AGPLv3"——这本身就是最好的教学案例 |
| 12 | `ch2/culture.md:90` | "Code Review 需 2+ 维护者批准…工具 Crucible, Phabricator" | "2 名批准"不是通行规则；Phabricator 2021 年 EOL，Atlassian Crucible 已停止支持 | 改为"以项目 CONTRIBUTING 为准"，工具换 GitHub PR / GitLab MR / Gerrit |
| 13 | `ch2/sec1/1-open_source_ecosystem.md:170` | 把 "Eclipse SDV" 列为 Linux 基金会项目 | Eclipse SDV 属 **Eclipse Foundation** | 修正，并借此区分两大基金会 |
| 14 | 同上 `:172` | "特斯拉将 Autopilot 专利开源…捐赠给 Linux 基金会管理" | Tesla 2014 年只是承诺对善意使用者不起诉，**未向 LF 捐赠专利** | 删除捐赠说法 |
| 15 | 同上 `:184` | 把 "Vault" 当 CNCF 托管项目 | Vault 属 HashiCorp，2023-08 起 BUSL-1.1；分叉 OpenBao 才进入基金会 | 改写为"许可证变更引发分叉"案例 |
| 16 | `ch1/sec2:596` | 用"地平线征程 6""平头哥倚天 710"举例 RISC-V | 两者均为 **ARM** 架构 | 换为玄铁 C910/C930、赛昉 VisionFive、曳影 1520 |
| 17 | `ch1/sec2:534` | "推动 OpenHarmony 进入 Android 兼容性测试框架" | OpenHarmony 是不含 AOSP 的独立系统；CTS 是 Google 的 | 删除 |
| 18 | `ch1/sec2:177` | "华为鸿蒙、**阿里云 OpenSearch**" | OpenSearch 是 AWS 项目 | 改为"华为 OpenHarmony/openEuler、阿里 OpenAnolis（龙蜥）" |
| 19 | `ch1/sec2:709` | "GitHub 引入 ZKP（zk-SNARK）验证开发者身份"；"OpenHarmony 要求所有 PR 使用 ZKP 签名" | 不成立的技术断言。GitHub 用 2FA/passkey/SSO，代码签名用 GPG/SSH | 删除；改写为 SBOM + Sigstore/SLSA + 代码签名 |
| 20 | `ch1/sec2:691` | "2025 年 AI 攻击案例…10% 的 OpenHarmony 设备异常…召回成本超 3 亿美元" | 查无此事件，把假设写成事实并赋予精确数字 | 明确标注为"情形推演"，或换成 xz-utils CVE-2024-3094 等真实复盘 |
| 21 | `ch1/sec2:347-427` | 整节 "GitHub Copilot X" | 品牌已并入 GitHub Copilot；节内"覆盖率提升 40%""文档时间减少 70%""每日节省 2.5 小时"等均无来源 | 压缩为 1 段"AI 编程助手对开源协作的影响"，保留许可与归属争议 |
| 22 | `ch1/sec2:432-441, 630-633, 646` | 整节围绕"《GB/T 44272-2024》"展开，称其"强制兼容性验证""国防军工双认证" | 该标准号在公开渠道无法证实；且把国家标准描述为可"成为 ISO 标准"体例上也不成立 | **与标准起草方核实前整段撤下**；改讲 OpenChain ISO/IEC 5230、OpenSSF、信通院开源白皮书 |
| 23 | `ch2/culture.md:45-47` | 引号内"软件的自由关乎用户控制自身计算的权利，而非价格问题"称引自《GNU 宣言》 | 属**伪引**，并非宣言原文 | 替换为原文并给链接，或改为转述 |
| 24 | `ch1/sec3:67` | 表格"50 人 (50%)｜选红 100 块｜50×**120** + 50×80 = **10，000**" | 表内算术与全角逗号错误；同节 :31-35 的博弈论表述（"纳什均衡""帕累托最优"）缺乏推导 | 重做收益表与均衡推导；删掉 :55"其他的钱去哪了？我也不知道" |
| 25 | `ch2/sec1/1-open_source_ecosystem.md:64-71` | 商业模式表把 Elastic 列为"开放核心" | Elastic 2024 年已重新以 AGPLv3 授权（保留 ELv2/SSPL 选项） | 建议给该表加"当前许可证"一列，把"开源核心"与"许可证切换"绑定讲解 |
| 26 | `ch2/sec1/1-open_source_ecosystem.md:89,91` | "关键漏洞平均修复时间曾低至 2.4 小时"、"华尔街历史上第八大首日涨幅" | 无来源 | 删除或补来源 |
| 27 | `ch2/sec2/culture.md:206,225,231` | "OpenStreetMap 全球 200+ 万注册编辑者"、"Wikipedia 287 个语言版本"、"ClueBot NG 准确率 99.7%" | OSM 实际为千万量级；Wikipedia 语言版本已 300+；准确率无来源 | 改为定性表述或补来源与日期 |
| 28 | `ch2/sec3/2-contributions-rewards.md` 全文 | "技能 Buff 加满""江湖名号""爽感""当红炸子鸡""用爱发电" | 口语化与网络用语，与全书体例不符；且 72 行承载 4,433 字，单段常超 400 字 | 去口语化、拆段，各条回报配 1 个可核查案例 |
| 29 | `ch2/sec3/3-legal-and-compliance.md:80-87` | 用"何同学"作为合规案例 | 网络热点、无事例链接、时效性强，与开源无直接关系 | 换成真实判例：Artifex v. Hancom（2017）、Jacobsen v. Katzer、BusyBox、VMware vmklinux |
| 30 | `ch2/sec3/3-legal-and-compliance.md:89-98` | "与开源发展较早的国家相比，我们…可能还有一段路要走" | 判断偏消极且缺事实支撑 | 补可核查事实：《著作权法》2020 年修订、数字天堂案（2019）与"不乱买"案（2021）对 GPL 的司法认可、木兰 MulanPSL-2.0 获 OSI 批准、开放原子基金会 2020-06 成立 |
| 31 | `ch2/culture.md:158-160,192` | "Apache 要求至少 3 个 +1 且无 -1"、"自动化测试覆盖率通常要求 >80%"、"出口管制自动合规检测" | 前两条被写成通行规则（应限定于具体项目/场景）；第三条无对应实践 | 标注适用范围或删除 |
| 32 | `ch1/sec4:58,59` | "GSoC 2025 支持 800+ 项目"、"Hacktoberfest 2024 吸引 500 万开发者" | 数量级与官方公布明显不符（GSoC 参与组织约 180 个） | 更正或删除；Hacktoberfest 还应提"垃圾 PR 刷量"争议及其规则调整 |

### 2.3 需要标注来源或删除的"精确数字"（抽样）

- MindSpore "2025 年市场份额达 **30.26%**"；TensorFlow "42%"、PyTorch "CVPR 引用占比 68%"
- "微软注资 GitHub 后，开发者薪资平均提升 **18%**，中小企业采用率增长 **40%**"（因果不成立）
- "Apache Log4j 被全球 **97%** 的 Java 应用使用"（与 Sonatype 公开口径不符）
- "全球 1.2 万家企业投入超 **50 亿美元**修复（Gartner）"、"中国金融行业修复成本 **5 亿美元**"
- "OpenEuler 设立 **500 万美元**漏洞悬赏基金，2024 年漏洞数增长 40%"
- "Codeberg 用户量 5 万→15 万"、"GitHub Sponsors 中微软系项目占比 12%→25%"
- "GSoC 2025 支持 **800+ 项目**"（实际参与组织约 180 个）、"Hacktoberfest 2024 吸引 **500 万开发者**"
- "OpenStreetMap 全球 **200+ 万**注册编辑者"（现实为千万量级）
- "Linux 内核 4000 万行、每月增加 20w+ 行、每年 8-9w 次提交"（口径不明，应注明版本与报告来源）
- "Docker 开源：刚开始只有很少人参与（**7%**）"
- "拉丁美洲政府采用开源节省 **90%** 软件成本"

### 2.4 建议的处理原则

1. 为全书建立统一的数据注记规范：**"数据 → 来源机构 + 年份 + 链接"**，无来源的数字一律删除或改为定性表述。`mkdocs.yml` 已启用 `footnotes`，可直接使用。
2. 在每章末增加"**数据与来源**"小节，并标注"**最后核对日期**"（教材长期在线，必须让读者知道数字的保质期）。
3. 对无法取证的历史叙事（Copilot X、2025 AI 投毒、ZKP 身份验证、GB/T 44272）采取**"撤下优先"**策略：宁可少讲，不可讲错。
4. 把第一章第二节从"编年史"重构为"**时间轴 + 3 个深度案例**"，把不产出于当次成果的内容移出（见 §8.2）。

---

## 三、P0：技术性错误（学生照抄即失败）

### 3.1 邮件列表协作（`docs/ch3/sec4/2-qemu-send-email.md`）

| 位置 | 问题 | 改法 |
|------|------|------|
| `:68`（另见 `:63`、`:81`） | `sendemail.smtpEncryption <ssl or **stl**>` — 枚举值写错，`stl` 会直接报错 | 全文改 `ssl`/`tls`，并补端口对照：465→ssl，587→tls |
| `:72` | `git config --global sendemail.smtpPass **=** <your pass>` — 多了一个 `=`，会把值设成 `= xxx` | 删掉 `=`，用单引号包裹 |
| `:55-58` | 建议"国内不推荐 Gmail"但同时 `:353` 示例输出是 `smtp.gmail.com`；未说明 Gmail 已不支持低安全性应用密码 | 给各家 SMTP 主机/端口对照表，说明 Gmail 需两步验证 + App Password |
| `:98-103` | `git format-patch HEAD~<number>` — `<` `>` 在 shell 中是重定向符；未提 `-v2` 版本号（而全文在讲 v2 流程） | 改为 `git format-patch -v2 --cover-letter --thread -o outgoing/ HEAD~3` |
| `:292-299` | "回复在顶部或底部两种都可以，更推荐第二种" — 对 kernel 风格社区 **top-post 明确不受欢迎** | 改为"一律 inline reply，HTML 邮件会被过滤器拒收" |
| `:387`、`:384`、`:20`、`:364` | `maito:`→`mailto:`、`Gernal`→`General`、`ulan`→`Ubuntu`、`邮前`→`目前` | 直接更正 |

> 该篇的 **tag 规范、`b4 trailers -u` 防代签、`b4 am` 与 `b4 trailers` 的区别** 是全教材最接近真实上游协作的内容，建议保留并作为"旗舰篇"打磨。

### 3.2 QEMU（`docs/ch3/sec4/1-qemu-foundation.md`）

- **镜像版本号四处不一致**（`:92` ubuntu-24.04.2 / `:107` ubuntu-24.04 / `:142` ubuntu-25.04 / `:146` 横幅 25.04）→ 统一为同一 LTS 版本。
- `:102` `-smp 32` 远超普通笔记本（正文还误称"u-boot 最大支持数量"）→ 改 `-smp 4 -m 2048`。
- `:52` `git clone git@gitlab.com:...` 要求预先配置 SSH key → 改 HTTPS。
- `:57-66` 未说明 QEMU ≥ 9 已转为 meson/ninja 构建 → 补 `ninja -C build` 与构建目录说明。
- 缺"启动链详解"（OpenSBI → U-Boot → GRUB → kernel）——这正是读者对 `-bios`/`-kernel`/`-drive` 困惑的根源。

### 3.3 Docker（`docs/ch3/sec3/*`）

- `2_dockerfile.md:125` 的 `CMD ["jupyter","lab","--allow-root","--NotebookApp.token=''","--NotebookApp.disable_check_xsrf=True"]` **教用户关闭认证与 XSRF 防护**，且 `-p 8888:8888` 绑定所有网卡 → 必须删除并改写。
- `5_compose.md:79` 保留 `version: "3.9"`（Compose Spec 已废弃该字段，会打印 deprecation 警告）→ 删除，只留 `name:`。
- 文件名沿用 `docker-compose.yml`，而命令已是 v2 的 `docker compose` → 统一为 `compose.yaml` 并加 v1 已 EOL 提示。
- 过时镜像：`node:18-alpine`（已 EOL）→ `node:22`；`python:3.10-slim` → `python:3.13-slim`；`alpine:latest` → 固定版本；`mysql:8.0` → `mysql:8.4`。
- `2_dockerfile.md` 作为唯一系统讲 Dockerfile 的章节只有 `FROM`/`RUN` 两条指令，**完全没有多阶段构建、`.dockerignore`、层缓存顺序、非 root 用户、HEALTHCHECK**。
- `5_compose.md:188-233` 把后端源码用 heredoc 内联进 YAML，没有 `healthcheck`、裸用 `depends_on`，是反模式。
- 全栏目未提 **Docker Desktop 商业许可门槛**（>250 人或年收入 >1000 万美元的组织需付费），而这是学生毕业后最容易踩的合规坑。
- `1_foundation.md` 演示了"下载脚本 → 阅读 → 执行"的正确做法（很好），但 `sec5/1-useful-oss.md:180`、`:297` 又出现 `curl | sh`，全课程口径自相矛盾。

### 3.4 Git 与平台协作（`docs/ch3/sec1/*`）

| 位置 | 问题 | 改法 |
|------|------|------|
| `subsec2/1-basic-configuration.md:197` | **"HTTPS 方式（需要每次输入密码）"** — GitHub 自 2021-08 起已禁用密码认证，HTTPS 必须使用 PAT；配置凭据助手后也不需要每次输入 | 改写为"HTTPS 需要 Personal Access Token（PAT）；SSH 需要密钥"，并新增 PAT 的创建、权限范围与安全存放说明 |
| 全站 | **"PAT / 个人访问令牌 / token" 0 次出现**（已全库检索） | 第 6 次课必须补：为什么需要、如何创建与最小授权、如何避免把 token 写进仓库 |
| `subsec2/1-basic-configuration.md:229` | `ProxyCommand nc -v -x 127.0.0.1:10808 %h %p` — 端口是作者本机代理端口；且与上一行 `Hostname ssh.github.com` + `Port 443` 的"免代理绕行"方案自相矛盾；`nc -x` 在多数 Linux 的 netcat 上不支持 | 拆成两个独立方案（443 端口绕行 / 代理），并标注"端口按自身环境替换" |
| `subsec2/1-basic-configuration.md:36-37` | "错误示例（缺少引号会导致问题）"的解释不准确：真正原因是 shell 把 `John Doe` 拆成两个参数，git 报参数数量错误 | 改为准确解释，并演示 `git config --global user.name "John Doe"` |
| `subsec2/1-basic-configuration.md:340` | "按三次回车"= 不设 passphrase，未提示安全代价 | 补一句"教学环境可不设；生产环境建议设置并配合 ssh-agent" |
| `subsec2/1-basic-configuration.md` | 未提 `git config --global init.defaultBranch main`；未提 `.gitignore` 与"不要提交密钥" | 补进"最小安全习惯"，与 `ch3/sec1/index.md` 呼应 |
| `subsec2/1-basic-configuration.md:3` | 首行是 `> 让学生掌握 Git 的基本配置与命令。`——**教师视角的教学目标写在学生教材里** | 改为学生视角的"学习目标"，并补署名框 |
| `subsec3/4-help-open.md:163`、`2-Control-Process.md:175` | `git reset --hard HEAD~1` 无警告（`2-staging.md` 已有 `!!! danger`，全书口径不一） | 统一补危险提示 |
| `subsec3/*`、`2-Control-Process.md` | 大量 `git checkout` 用法，未提 Git 2.23+ 推荐的 `git switch`/`git restore` | 至少在一处说明新旧命令对应关系 |
| `subsec1/2-code-hosting-platforms.md` | 4 个一级标题拼接；含大量过时的 GitHub 网页界面描述（截图无法覆盖 UI 改版）；实践步骤依赖具体菜单路径 | 拆成 4 页；把"点哪个菜单"改为"完成什么目标 + 截图版本说明"，并补 Gitee/AtomGit/GitLab 的差异说明 |
| 第 6 次课整体 | 缺 **CI 失败如何排查**、**PR 描述模板**、**如何响应 review 的具体操作**（`5-participate-in.md` 已有原则，缺可粘贴模板） | 补齐，并与 `course/project.md` 的证据包要求对齐 |

补充说明：未覆盖的知识点还有 `.gitignore` 与密钥泄露防护、DCO/`Signed-off-by` 与 CLA 的区别（`3-commit-message.md` 与 `2-qemu-send-email.md` 各讲了一半）、Conventional Commits 与目标项目规范的优先级、Gitee/AtomGit 的实名与认证差异。

### 3.5 Git 概念与 Linux 命令的准确性

| 位置 | 问题 | 改法 |
|------|------|------|
| `subsec1/1-git-introduction.md` | "SHA-1 哈希**加密**确保历史不可篡改" — 哈希不是加密；SHA-1 的选择前缀碰撞已于 2017 年被公开演示 | 改为"内容寻址使历史难以被无声改写；SHA-1 碰撞已被公开演示，Git 正在向 SHA-256 迁移（Git 2.29+ 支持 SHA-256 仓库）" |
| 同上 | "40 位的十六进制指纹（如 `2fd4e1c67a2d28fced849ee1`）"——示例只有 24 个字符，自相矛盾 | 补全示例或注明"实际显示时常缩写" |
| 同上 vs `subsec3/3-advanced-theory.md` | "十天写出 Git" vs "两周完成初步开发"，同章矛盾 | 统一表述 |
| 同上 | hotfix 分支生命周期写作"修复后 24 小时"，属杜撰 | 改为真实惯例或以具体项目为例 |
| `subsec3/3-advanced-theory.md` | 三处概念错误待核："树是表示有向无环图的一种数据结构"、"blob 即 binary large object"、对象头格式示例；另有截断句"而 commit 的哈希发生了变化，"与拼写 `contene` | 逐处修正；补"本节对实际贡献有什么用"的动机段 |
| `sec2/4-other-commands.md` | "启动 `top` 后输入命令 `xtm4z` 获得友好界面"——`top` 只接受单键，不存在该命令 | 改为"依次按 `z`、`x`、`m`" |
| 同上 | kill 一节粘贴了 htop 的操作说明（"用方向键或鼠标点击，按 `F9`"） | 删句，改讲 `kill -l`、`-15`/`-9` |
| 同上 | "关于管道的使用和定义，请参考本章的上一篇目"——上一节是 Git，全章从未讲管道与重定向 | 新增"输入输出与管道"小节 |
| 同上 | 练习要求用 `ss -tunlp`，但正文从未介绍 `ss`，且 `-p` 需要 root | 先在正文补 `ss` 说明与提权提示 |
| 同上 | `p7zip [options]`——可执行文件是 `7z`（`p7zip` 只是包名）；"默认删除输入文件"与 7-Zip 实际行为不符（默认保留，`-sdel` 才删） | 统一为 `7z`，改写删除行为 |
| 同上 | `sudo yum install htop`（CentOS/RHEL）；RHEL 8+ 以 `dnf` 为准，CentOS 7 已 EOL | 改 `dnf` |
| 同上 | `curl -u user:password https://...` 会让密码进入 shell 历史与 `ps` 输出；`--no-check-certificate` 未提安全代价 | 改 `curl -u user` 或 `--netrc-file`；为 `--no-check-certificate` 加 warning |
| `subsec3/4-help-open.md` | `git checkout -- file.txt` / `git checkout -- .`（标注"不可逆操作"）未给安全替代 | 改 `git restore`，补"先 `git stash push -u` 再决定丢弃"，并说明 `restore` 不覆盖未跟踪文件 |
| `subsec3/1-rebase-merge.md` | 把"已推送"等同"共享"，得出"共享分支必须用 Merge"，与 `5-participate-in.md`、`course/project.md` 的 `--force-with-lease` 指引矛盾 | 判定条件改为"是否有他人提交"；区分"个人 fork 可 rebase + `--force-with-lease`""主干禁止改写" |
| 同上 | "趣味小练习"在同一仓库里先演示 merge 再演示 rebase，方案 A 已合并，方案 B 会得到 "Already up to date" | 改为两个独立仓库，并给出期望的历史图 |
| `subsec3/2-Control-Process.md` | "rebase 将目标分支的修改按时间顺序添加到当前分支"——方向说反 | 引用 `1-rebase-merge.md` 中正确的表述 |
| 多个文件 | 30 处 `git checkout`，未提 `git switch`/`git restore`；`git checkout -- .` 仍在推荐列表 | 统一为新命令，保留一句新旧对照 |
| 多处 | `git pull` 未讨论 `pull.rebase`/`pull.ff only`（Git 2.27+ 对分叉拉取有告警） | 与 `5-participate-in.md` 使用的 `git pull --ff-only` 对齐 |
| 全站 | `git rebase -i` 在 Git 章节内出现 **0 次**（仅 `ch3/sec4/2-qemu-send-email.md` 提过一次）、`--fixup` **0 次**，而 `CONTRIBUTING.md:265` 自己要求"发起 PR 前考虑用 `git rebase -i` 合并提交" | 补 `--amend` / `--fixup` + `--autosquash` / `rebase -i` 三件套 |
| 全站 | `upstream` 在 `docs/ch3/sec1/` 内 **0 命中**（只有 `ch1/sec4` 的流程图里出现过 `git pull upstream`）——fork 后如何同步上游完全没有讲，学生会在过期分支上开发 | 补 `git remote add upstream` / `fetch upstream` / GitHub "Sync fork" 三条路径 |
| 全站 | `CODEOWNERS` **0 命中**、`personal access`（PAT）**0 命中**，而仓库自己有 `.github/pull_request_template.md` | 补"仓库级配置文件"表（ISSUE_TEMPLATE、pull_request_template、CODEOWNERS、SECURITY）与 PAT 说明 |
| `subsec1/2-code-hosting-platforms.md` | 同页自相矛盾：平台对比表写"GitHub 私有仓库有限"，后文又写"GitHub 现在提供无限免费私人仓库" | 该列改为"免费额度"，写具体维度（协作者数、Actions 分钟） |
| 同上 | "Q：一定要用 Git 命令吗？A：**不需要！**入门可不学命令" | 与第 5/6 次课及结课成果直接冲突，改为"网页界面可作补充，可评审的贡献必须通过分支与提交完成" |
| `subsec2/3-commit-message.md` | "2019 年由 Angular 团队提出，现已成为 GitHub **80% 以上**开源项目的选择"——规范由 B. Coe 等维护、v1.0.0 于 2019 发布，"80%"无来源 | 改为"受 Angular 提交约定影响"，删除百分比 |
| 同上 | 长度规范自相矛盾（"标题 50 / 正文 72" vs "每行不超过 100 字符"）；类型字典在两处不一致 | 统一为 50/72，把项目自定义部分标为项目约定 |
| 同上 | 拼写 `<suject>`；`<type>(<scope>)!:` 的说明句法含混 | 修正，并给出 `!` 与 `BREAKING CHANGE:` 两种等价写法 |
| `sec0/2-advanced.md` 等多处 | `Github`/`github`/`BitBucket`/`markdown` 大小写不规范；`1。`/`2。` 全角序号与 `1.` 混用 | 统一为 `GitHub`、`Bitbucket`、`Markdown`、半角序号 |

### 3.6 许可证内容（第 3 次课核心，需重建）

`docs/ch2/sec1/2-open_source_licenses.md` 仅 **1,758 字符（约 4 分钟）**，却要承担第 3 次课"许可证与合规"的一半主线。除 §2.2 的表格错误外，缺口：

- 缺 **MPL-2.0**（文件级 copyleft）、**AGPL 网络分发条款**、**LGPL 链接边界**；
- 缺 **source-available** 与开源的区分（SSPL、BUSL 1.1、Elastic License 2.0）；
- 缺 **CC 家族**（CC BY/BY-SA/CC0）及"CC 不宜用于软件"；
- 缺 **数据与硬件许可**（ODbL、CERN-OHL）；
- 缺 **AI 模型许可**（Llama Community License、OpenRAIL、Gemma）与 OSI 的 **OSAID 1.0**；
- 缺 **SPDX 标识符与 License List**、**义务矩阵**（使用/修改/分发/SaaS 何时触发义务）、**兼容性矩阵**；
- 缺 **合规工具链**（ScanCode、FOSSA、ORT、reuse）、**SBOM**（SPDX/CycloneDX）、**OpenChain ISO/IEC 5230**、**欧盟 CRA 时间表**；
- 缺将许可证变为教学案例的经典事件：HashiCorp→BUSL→OpenTofu、Redis→SSPL→Valkey、Elastic 改回 AGPLv3。

---

## 四、结构与导航问题

| # | 问题 | 具体表现 | 建议 |
|---|------|----------|------|
| 1 | **目录编号与导航编号错位** | `docs/ch3/sec0/` 在导航里叫"第一节 协作写作"，`docs/ch3/sec1/` 叫"第二节"，`docs/ch3/sec2/` 叫"第三节" | 目录重命名为 `sec1-writing` / `sec2-git-platform` / `sec3-linux`，编号与导航一致 |
| 2 | **必修与拓展混在同一目录** | `docs/ch3/sec1/subsec3/` 同时放着必修的 `5-participate-in.md` 和拓展的 `1-rebase-merge.md`、`2-Control-Process.md`、`3-advanced-theory.md`、`4-help-open.md` | 把 `5-participate-in.md` 提升到 `docs/ch3/sec2-git/` 下，其余移入 `docs/ch3/advanced-git/` |
| 3 | **单文件多一级标题** | `docs/ch3/sec1/subsec1/2-code-hosting-platforms.md` 有 4 个 `#`（代码托管平台简介 / 实践：注册… / 创建并管理仓库 / GitHub Fork 简明解析） | 拆成 4 个页面；否则侧边栏 TOC 与锚点结构混乱 |
| 4 | **文件名拼写错误** | `2-the-missing-semeste-of-your-CS-education.md`（缺 `r`），`mkdocs.yml` 与正文同步了这个错名 | 重命名为 `...-semester-...` 并同步 nav |
| 5 | **残留旧编号** | `# 4.1.3.2 Git 分布式版本控制工作原理`、`# 4.1.3.2 Git 辅助本地项目开发`、`### 3.3 架构图` | 去掉遗留编号 |
| 6 | **导览与正文比例失衡** | `terminology.md`（276 字）、`rules.md`（213 字）要承担"本节导览"，而正文约 2.1 万字；`ch2/index.md` 本身是正文缩写版，且留下"各协议类型比较""核心职能""案例与思考"三处空标题 | 导览升级为"学习目标 + 内容地图 + 课时切分 + 自测"；`ch2/index.md` 改为映射表 |
| 7 | **章节编号体系不一** | 第零/一/二/三/四章，但内部有"拓展 Git 进阶""拓展 Docker"等游离节点 | 统一为"章 - 节 - 目"三级，拓展内容集中到附录或独立栏目 |
| 8 | **`docs/includes/` 不存在** | `mkdocs.yml:76-79` auto_append `includes/man.md`、`includes/authors.md`，实际无此目录（`pymdownx.snippets` 默认静默忽略） | 要么创建这两个文件，要么删除配置 |
| 9 | **同一概念三处名称不一** | `# 一些常用的 Linux 工具`（正文）vs `常用命令与工具`（nav）vs `常用 Linux 工具`（`ch3/index.md`）；`Git 进阶理论` vs nav `Git 底层理论`；`Git 暂存区与提交` vs nav `暂存区操作` | 统一标题与 nav |
| 10 | **文件命名风格不一** | `2-Control-Process.md` 为 Title-Case，同目录其余为 kebab-case（`1-rebase-merge.md`、`4-help-open.md`） | 用 `git mv` 统一为 `2-control-process.md`（注意大小写不敏感文件系统） |
| 11 | **章节内交叉引用错误** | `sec0/1-basic.md` 写"请参考本章第二节 - Markdown 进阶语法"，但 `2-advanced.md` 与它同属第一节 | 改为"本节" |
| 12 | **`ch3/index.md` 拓展条目无链接** | "拓展学习"四条只有文字，学生无法点击进入 | 补链接与"预计学时" |

> 备注：`mkdocs build` 现在**零警告、构建成功**（已在本地验证）；`nav` 已覆盖全部 45 个文件，无死链、无重复。AGENTS.md 中"部分文件未纳入 nav"的说明已过时，需要更新。

---

## 五、体例合规问题

| 检查项 | 现状 | 规范要求 |
|--------|------|----------|
| "主要作者"署名框 | **9 / 45** 文件有（ch2 三篇、Markdown 两篇、Linux 工具、QEMU 两篇、开源工具）。另有 4 个文件把作者写成"本节作者：[@xxx]"塞在"本节概览"框内，格式不符 | `CONTRIBUTING.md`：章节开头加 `!!! note "主要作者"` |
| 图片配字 `{: .caption }` | **0 / 25 张图片正确使用了该语法**——有 6 处写了图注但语法全错：`{： 。caption}`（全角冒号 + 全角句号，`2-code-hosting-platforms.md:236,249`）、`{： .caption}`（全角冒号，`3-advanced-theory.md:60,261,335,389`）；图注文字本身写作"图 1**。**Dashboard" | 正确写法是**半角** `{: .caption }`，图号用半角 `.`；目前 `extra.css` 的 `.caption` 样式完全失效 |
| 一级标题唯一 | 1 个文件违反（4 个 H1） | 每个 md 以单个 `#` 开头 |
| 代码围栏语言标记 | 基本合规；`2-qemu-send-email.md` 有 9 处无标记；`3-advanced-theory.md` 有 4 处 Ruby 代码标成 `bash` | 补齐并改正 |
| 围栏语言一致性 | Docker 栏目 `shell` 与 `bash` 混用；部分写成 ` ``` shell`（栅栏后带空格） | 统一为 `bash`/`shell` 之一 |
| 提示框类型 | 实际使用 **13 种**：`note`(21) / `tip`(18) / `warning`(11) / `example`(11) / `success`(9) / `question`(7) / `summary`(4) / `info`(2) / `quote`(2) / `error`(2) / `danger`(1) / `bug`(1)，另有 `!!! tips`（×3，**拼写错误，不会渲染成提示框**）与 `??? answer`（非 Material 类型） | 规范只列 `note/warning/danger/tip/example/question`。至少要把 `tips`→`tip`、`bug`→`danger`/`note` 改掉，并决定是否把 `success/summary/info` 正式纳入规范 |
| 提示框排版 | `!!! summary` 后缺空行直接跟列表；`!!! tip` 顶格出现在缩进列表中间；4 空格缩进的提示框内用 2 空格嵌套列表（会被判为块外） | 统一缩进与空行 |
| 可折叠提示框类型 | `???+ node "Dashboard 的介绍"`（`2-code-hosting-platforms.md:238,251`，`node` 是 `note` 的拼写错误）、`??? answer "参考"`（`3-advanced-theory.md:396`，Material 无该类型，且与上面的 `!!! question` 未配对） | 改为 `???+ note` / `??? note` |
| 标题内加粗 | 常见 `#### **总结与思考**` | 建议标题内不加 `**` |
| Emoji | `ch2/index.md` 三处标题带 🚀📚🌍；`ch2/sec1/2-open_source_licenses.md` 用 ✔️/❌/★ 表达专利条款；`sec2/4-other-commands.md`、`2-staging.md` 标题带 🧪 | 建议：标题去 emoji；事实判断用文字（emoji 表达"有无专利条款"会同时损害准确性与可访问性） |
| 人称与口吻 | 两极分化：`ch3` 新层克制、`ch2/index` 用"您"、`ch0` 通篇感叹号、`1-git-introduction.md` 玄幻体（"魔法杖""量子分身术""邓布利多军通过 Git 分支对抗伏地魔"）、`1-rebase-merge.md` 段子化（"乾坤大挪移""merge 虽乱心不乱"）、`ch2/sec3/2` 网络流行语（"技能 Buff 加满""当红炸子鸡"） | 统一为面向"你"的教材口吻；比喻可保留，结论句中性化，段子与 emoji 降级为提示框 |
| 术语 | "开源协议" vs "许可证"（license）；"开发者们们"；"Linux + GNU"应为"GNU + Linux"；"索引"与"暂存区"混用；`Github`/`github`/`BitBucket`/`markdown` 大小写；全角序号 `1。`/`2。` 与 `1.` 混用 | 全站统一"许可证（license）"、专名大小写与半角序号，建立术语表 |

---

## 六、工程与 CI 问题

| # | 问题 | 证据 | 建议 |
|---|------|------|------|
| 1 | **16 MB 未压缩音频** | `docs/audios/open-source.wav` = 16 MB，站点 26 MB | 转为 MP3/OGG（约 1–2 MB），或迁移到外部托管 |
| 2 | `actions/setup-python@v4` 过旧 | `build.yml:14`、`deploy_ghpage.yml:22` | 升到 `@v5`+ |
| 3 | **`huacnlee/autocorrect-action@main` 未固定版本** | `lint-all.yml:14` | 固定到 tag/commit SHA |
| 4 | **CI 里 `curl -fsSL .../install \| sh`** | `lint.yml:37` | 与课程"供应链安全"主题直接矛盾；改为固定版本的安装方式 |
| 5 | lint 自动向贡献者分支推送修复 commit | `lint.yml:56-62` | 对 fork PR 无效（`continue-on-error` 掩盖失败）；且对教"PR 规范"的课程而言是坏的示范；建议改为"仅检查 + 评论提示" |
| 6 | 缺少链接检查与 markdownlint CI | 仓库文档提到 markdownlint，CI 未运行 | 增加 `lychee-action`（链接）与 `markdownlint-cli2` 步骤 |
| 7 | `docs/includes/` 配置指向不存在的文件 | `mkdocs.yml:76-79` | 见 §4.8 |
| 8 | `AGENTS.md` 与实际不符 | 其中"未纳入 nav 的文件""构建会产生警告"等描述已过时 | 更新 AGENTS.md |
| 9 | 中文搜索 | `search_index.json` 的 `lang` 为 `['en']`；`separator` 已含中文标点 `、。，．？！；`，未启用中文分词 | 属可优化项：实测关键词命中率后再决定是否调整（本地试配 `search: lang: zh` 可构建通过，但生成的 worker 与 `en` 完全一致，说明未带来分词改善） |

---

## 七、与 8 次课的对齐缺口（核心表）

对照 `docs/course/index.md` 的"当次成果"，逐次课评估教材支撑度：

| 次 | 主题 | 当次成果 | 教材现有支撑 | 缺口 | 判定 |
|----|------|----------|--------------|------|------|
| 1 | 认识开源与项目启动 | **一个开源项目画像** | `ch0`、`ch1/sec1` | **项目画像工作纸完全没有**：无模板、无示例、无"如何查许可证/判断维护状态/找贡献入口"的方法 | ❌ 无法达成 |
| 2 | 历史与生态 | **项目生态角色分析** | `ch1/sec2`、`ch2/sec1/1` | `ch1/sec2` 是编年史而非角色结构；无生态角色分析框架（个人/高校/标准组织/发行版/集成商/用户企业），无项目健康度信号（Bus factor、贡献者集中度、发布节奏） | ❌ 无法达成 |
| 3 | 许可证与合规 | **许可证判断练习** | `ch2/sec1/2`（1.7k 字）、`ch2/sec3/3` | 许可证正文过薄且表格有 5 处错误；**无练习题、无答案、无义务矩阵/兼容性矩阵** | ❌ 无法达成 |
| 4 | 社区文化与治理 | **贡献选题与实施提案** | `ch2/sec1/1`、`ch2/sec2`、`ch2/sec3/1`、`ch2/sec3/2` | 治理部分尚可；**缺 CoC 读法与举报路径、Issue 礼仪、六要素提案模板、选题渠道（good first issue/OSPP/GSoC/LFX）** | ❌ 无法达成 |
| 5 | 最小贡献工具链 | **本地 Git 实验** | Markdown 两篇、Git 前 5 篇 | 骨架正确，`2-staging.md` 已是好样板；缺 Markdown 与课程的结合（本课程文档即是最好的练习仓库）、缺 `git switch/restore` 现代用法 | ⚠️ 基本可达成 |
| 6 | 平台协作流程 | **可评审的贡献草稿** | `ch3/sec1/subsec1/2`、`5-participate-in.md` | `5-participate-in.md` 质量高；但 `2-code-hosting-platforms.md` 是 4 篇拼接、含过时 UI 截图描述；缺 CI 失败排查、PR 描述模板 | ⚠️ 基本可达成 |
| 7 | 真实贡献工作坊 | **向真实项目提交贡献** | `course/project.md` | 流程定义清楚，缺"卡住了怎么办"的排障手册 | ⚠️ 基本可达成 |
| 8 | 反馈响应与持续参与 | **贡献证据包与复盘报告** | `ch4/index.md`（668 字） | **缺评审响应的命令级流程、缺证据包模板、缺复盘报告结构、缺展示脚本、缺"如何评审他人"的清单** | ❌ 无法达成 |

**一句话总结：8 次课里有 4 次课的"当次成果"在教材中找不到支撑材料。这是"丰满"最该优先解决的部分，比补知识点更重要。**

### 7.1 教学法与课时预算

**课时超支**：第三章课堂必修内容（Markdown + Git + 平台 + Linux）按现有篇幅估算约 **5.2 课时**，而大纲只给第 5–7 次课共 **4.5 课时**，超支约 15%。第一章四节内容估算约 8–10 课时，但只对应第 1、2 次课共 4 课时，超支一倍以上。**教材需要一次显式的"课时预算重分配"**，而不是继续加内容。

**练习分布极不均**：有实验/练习的只有 `sec0/1-basic.md`、`1-basic-configuration.md`、`2-staging.md`、`1-rebase-merge.md`、`4-other-commands.md`；而最重的 `2-code-hosting-platforms.md`（564 行）只有 6 个复选框、`3-commit-message.md`（310 行）0 练习、`5-participate-in.md`（结课核心）0 练习。

**验收标准缺失**：全书只有 `2-staging.md` 的"应当能够准确说明'下一次提交将包含什么'"与 `5-participate-in.md` 的"完成标准"5 条。建议必修统一为"**实验步骤 → 期望输出 → 自检清单**"三段式。

**故障排查不成体系**：只有 `2-code-hosting-platforms.md` 的"遇到问题怎么办"（4 条，其中认证那条是错的）与 `1-basic-configuration.md` 的一个 SSH 失败流程图。建议抽出章级"故障排查手册"（认证 / 22 端口与代理 / CRLF / 权限 / 大文件误提交）。

**存在有 bug 的练习**：`1-rebase-merge.md` 的"趣味小练习"在同一仓库里先演示 merge 再演示 rebase，方案 A 合并后方案 B 只会得到 "Already up to date"，学生看不到任何差异。

**练习与课程仓库脱节**：全书没有一个"跟着本课程仓库走一遍"的端到端实验（fork → 改文档 → `mkdocs build` → PR → 等 CI），而 `course/project.md` 的 A 类项目池做的正是这件事。

---

## 八、丰满方案

### 8.1 建议的目标结构

```
课程指南
├── 课程大纲 / 真实贡献项目 / 成绩评定          （已有，保持）
├── 教师手册（新增）：课时教案、活动脚本、评分量规、常见问题
└── 学生速查（新增）：术语表、命令速查、工具链清单、模板下载

第零章 课程导入（扩写）
第 1 次课 认识开源与项目启动
├── 什么是开源（含三套话语：自由软件/开源/FOSS）
├── 开源项目画像工作纸（新增，核心）
└── 身边的开源案例（新增：校园/国内项目）
第 2 次课 历史与生态
├── 开源简史 = 时间轴 + 3 个深度案例（重构）
├── 开源生态的角色结构（新增框架）
├── 项目健康度怎么判断（新增）
└── 中国开源生态（新增独立小节）
第 3 次课 许可证与合规（重建）
├── 权利、义务与条件
├── 许可证家族全景
├── GPL 三代差异与兼容性
├── 义务何时触发：使用/修改/分发/SaaS
├── 合规工具链与 SBOM、OpenChain、欧盟 CRA
├── 中国开源法律实践与木兰许可证（新增）
└── 许可证判断练习（含答案与解析）
第 4 次课 社区、文化与治理
├── 开源文化的两次分裂
├── 行为准则怎么读、怎么用（新增）
├── 治理模式与决策机制（保留 ch2/sec3/1）
├── 沟通与 Issue 礼仪（新增）
├── 贡献提案六要素模板（新增，核心）
└── 贡献与回报（保留，去口语化）
第 5 次课 最小贡献工具链
├── Markdown（保留，补"用本课程仓库练习"）
├── Git 工作区/暂存区/提交（保留）
└── 提交信息规范（保留）
第 6 次课 平台协作流程
├── 代码托管平台（拆分为 4 页）
├── Fork/Issue/PR/Review 流程
├── CI 与自动检查（新增：如何看失败日志）
└── 可评审的 PR 描述模板（新增）
第 7 次课 真实贡献工作坊
├── 参与开源项目（已有，保持）
├── 按需使用 Linux（保留为手册）
└── 排障手册（新增：常见卡点）
第 8 次课 反馈响应与持续参与（大幅扩写）
├── 评审意见分类与回应模板
├── 修改与推送（命令级）
├── 如何评审他人的贡献（新增）
├── 贡献证据包模板（新增）
├── 复盘报告模板与范文（新增）
├── 成果展示脚本（新增）
└── 贡献之后的 30 天（新增）

附录
├── 术语表（新增，全站复用）
├── 拓展 Git 进阶（迁移到附录）
├── 拓展 Docker（精简为 3 篇）
├── 拓展 QEMU 与邮件列表（保留，旗舰篇）
├── 拓展效率工具（改为按需速查手册）
└── 数据与来源、致谢、许可证
```

### 8.2 逐次课的丰满清单（可直接作为写作任务）

**第 1 次课**

- `项目画像工作纸`：5 行模板（用途 / 许可证与类型 / 维护状态指标（最近提交、Issue 响应中位数、Release 频率）/ 贡献入口三件套 / 一个待查问题）+ 1 个完整示例。
- `开源的三套话语`：FSF/free software（1985）与 OSI/open source（1998）的分野、OSD 十条原文与链接——这同时是 `ch1/sec2` 辩论题的前提。
- `身边的开源案例`：补国内基础软件（openEuler、OpenHarmony、Anolis、龙蜥）与中国高校参与路径。

**第 2 次课**

- `时间轴`：1969–2026 一行一年，表格形式；重点补 **SourceForge（1999）→ Google Code（2006）→ GitHub（2008）** 平台迁移脉络（`ch1/index.md` 承诺了但正文缺失）与 **Mozilla 1998 / IBM 10 亿美元 Linux 计划 / IBM 收购 Red Hat 2019 / 微软收购 GitHub 2018** 的企业接纳线。
- `生态角色结构`：个人开发者、高校、标准组织、发行版、集成商、用户企业、基金会；配 `项目生态角色分析` 工作表。
- `项目健康度信号`：贡献者集中度、Bus factor、Issue/PR 响应时延、发布节奏、治理文档完备度。
- `中国开源生态`：开放原子基金会（2020-06）、木兰 MulanPSL-2.0（首个获 OSI 批准的中国基金会主导许可证）、OpenHarmony/openEuler/Anolis、Gitee/AtomGit、开源之夏 OSPP。
- `许可证变更与社区分叉`：HashiCorp→BUSL→OpenTofu、Redis→SSPL→Valkey、Elastic 回归 AGPLv3、MongoDB→SSPL——这是"生态角色分析"最好的素材。

**第 3 次课**（重建，最重要）

- `义务矩阵`：使用 / 修改 / 分发 / SaaS 四场景 × 各许可证义务。
- `许可证家族全景`：permissive / 弱 copyleft / 强 copyleft / source-available / 内容与数据 / 硬件 / AI 模型。
- `GPL v1/v2/v3 差异`：反 Tivoization、安装信息、专利报复、DRM、与 Apache-2.0 的兼容、only/or-later。
- `兼容性`：GPLv2-only + Apache-2.0（不兼容）、GPLv3 + Apache-2.0（兼容）、AGPL 与 SaaS。
- `合规工具链`：SPDX 标识符与 License List、ScanCode/FOSSA/ORT、SBOM（SPDX/CycloneDX）、OpenChain ISO/IEC 5230、欧盟 CRA 时间表（2026-09-11 报告义务、2027-12-11 全面适用）。
- `判断练习`：8 道仓库判 SPDX 与"可否闭源商用/是否必须开源/是否需提供源码" + 3 道兼容性题 + 1 道固件综合题，**附答案与解析**。

**第 4 次课**

- `行为准则怎么读`：Contributor Covenant 的结构、举报渠道、与导师的关系。
- `Issue 礼仪与最小可复现示例`：模板 + 正反例。
- `贡献提案六要素模板`：问题、价值、范围、实施方案、验证方法、潜在风险——逐项给写作指导和一段范文。
- `选题渠道`：good first issue / help wanted / roadmap / OSPP / GSoC / LFX Mentorship，配"如何判断三周内能完成"。
- `治理文档读法`：GOVERNANCE/charter/投票记录；Apache 孵化流程、CNCF 三阶段。

**第 5、6 次课**

- **把"分支"补成必修**：大纲第 5 次课明确写了"提交与**分支**"，但 `ch3/index.md` 的必修 6 步只到提交信息，分支只在一处术语表里出现。补"分支：并行工作与命名"（`git switch -c`、`git branch -vv`、上游跟踪、命名规范）。
- **把本课程仓库（`intro2oss`）作为 Markdown + Git + PR 的统一起点练习靶场**：fork → 改一处文档 → 本地 `mkdocs build` → PR → 响应 CI 与 review。这既是第 5/6 次课的实验，也是 A 类项目池的真实任务。
- **补四处时效缺口**（都落在必修路径上）：`git config --global init.defaultBranch main`、PAT（替代已禁用的密码认证）、`git switch`/`git restore`（替代 30 处 `git checkout`）、`--fixup` + `rebase -i --autosquash`（`CONTRIBUTING.md` 自己要求但教材没教）。
- **补 fork 场景的 upstream 同步**：`git remote add upstream` / `fetch upstream` / GitHub "Sync fork"——否则学生会在过期分支上开发。
- **新增 `找到合适的任务`**：GitHub 搜索语法 `is:issue is:open label:"good first issue" no:assignee sort:updated-desc`、聚合站点、项目活跃度判断步骤。
- **新增 `读懂自动检查结果`**：Checks → Actions 日志、五类常见失败（代码错误 / 格式 / 许可证头 / DCO 缺失 / flaky）、本地复现方法、慎用 Re-run。
- **新增 `PR 描述模板`**：问题 / 方案 / 不在范围内 / 如何验证，并给一份与本仓库 `.github/pull_request_template.md` 对应的完整范例。
- **新增 `作为评审者`**：先跑起来、区分阻塞与建议、用提问代替断言、24 小时内首次回应；附"不同意时怎么措辞"模板。
- **补"仓库级配置文件"表**：ISSUE_TEMPLATE、pull_request_template、CODEOWNERS、SECURITY。
- **给 Linux 部分补基础命令**：现有内容直接从 `ps/top/df` 起步，缺 `ls/cd/cp/mv/rm/mkdir/find/head/wc/sort/uniq/which/history/alias`、权限与 `sudo`、输入输出与管道——对第一次接触命令行的本科生门槛过高。
- **修正 Linux 部分的错误**：`xtm4z`（`top` 不存在该命令）、kill 一节混入 htop 的操作说明、`p7zip`→`7z`、`yum`→`dnf`、`curl -u user:password` 的密码泄露风险、`--no-check-certificate` 缺安全提示。

**第 8 次课**（从 668 字扩到 200–300 行）

- `评审意见分类与回应模板`：功能分歧 / 风格意见 / 范围扩张 / 无法复现，各给"维护者说 X → 建议回复 Y"。
- `修改与推送`：同分支更新、`--amend` vs 新增 commit、`--force-with-lease` 的前提、CI 失败就地修复。
- `如何评审他人的贡献`：检查清单、提问式评论、`Reviewed-by:`/`Tested-by:` 的有效形式（与 `2-qemu-send-email.md` 的"不替他人加 tag"互链）。
- `证据包模板`：与 `course/project.md` 的 5 项证据一一对应。
- `复盘报告模板 + 脱敏范文`、`8 分钟展示脚本`、`贡献之后的 30 天`。

### 8.3 新增专题（当前全站缺失，可按课时取舍）

| 专题 | 现状 | 建议 |
|------|------|------|
| 开源与 AI | 只有 Copilot X 营销式内容；"模型权重"0 次出现 | 独立小节：AI 生成代码的版权与许可证归属、训练数据合规、模型许可（Llama/OpenRAIL/OSAID 1.0）、AI 辅助贡献的披露规范 |
| 供应链安全 | SBOM 仅 4 次提及，OpenSSF / CHAOSS / Scorecard / Log4Shell 0 次 | 独立小节：SBOM、可信构建（SLSA/Sigstore）、依赖治理、真实事件复盘（Log4Shell、xz-utils CVE-2024-3094） |
| 社区治理与 CoC | "行为准则"仅零星出现，无独立内容 | 独立小节 + 举报路径演练 |
| 中国开源生态 | 开放原子仅 1 处一句、木兰 1 次、OSPO 0 次 | 独立小节（与俱乐部身份匹配） |
| 职业与人才 | "就业"仅 1 次 | 独立小节：OSPO 岗位、开源贡献与求职、开源之夏/GSoC 与导师制 |
| 度量与健康度 | CHAOSS 0 次 | 并入第 2 次课"项目健康度" |
| 开放科学/开放数据/开放硬件 | 仅在"广义开源"里各一段 | 保留为拓展阅读，不必扩 |

### 8.4 教学基础设施（"丰满"的乘数项）

1. **术语表**：把 `terminology.md` 升级为全站术语表（20–25 条：开源定义/OSD、FOSS、permissive/copyleft/source-available、SPDX 标识符、衍生作品、上游/下游、CLA/DCO、BDFL/PMC/TSC/SIG、fork、CoC、SBOM…），并在各章首次出现处链接。
2. **练习与参考答案**：目前全教材几乎没有可评分练习，而 `assessment.md` 已经设计了"许可证判断练习""本地 Git 实验"。练习必须有题、有答案、有判分要点。
3. **案例库**：每个知识点配 1 个可核查案例（优先带官方链接）。正向：Linux、Kubernetes、OpenTofu、Valkey、Blender；反向：HashiCorp/Redis 许可变更、xz-utils 后门、Log4Shell、Heartbleed、伪开源项目。
4. **延伸阅读（带来源与日期）**：把 `ch1/sec2` 的"资源库"改造为"名称｜类型｜链接｜年份｜一句话用途"的表。
5. **教师手册**：课时教案、活动脚本（辩论会、安全攻防演练都有想法但没有可执行脚本）、评分量规、常见问题与回答。
6. **写作模板**：以 `docs/ch3/sec1/subsec2/2-staging.md` 和 `docs/ch3/sec1/subsec3/5-participate-in.md` 为样板，统一为"学习目标 → 概念 → 命令与解释 → 安全提示 → 实践任务 → 完成标准"六段式。

### 8.5 建议的写作规范补充（更新 `CONTRIBUTING.md`）

在现有规范上补四条：

1. **数据必须有来源**：定量表述一律给"来源 + 年份 + 链接"；无法取证的删掉。
2. **每页必须有署名框与"最后核对日期"**。
3. **技术示例必须可执行**：命令要在作者环境下实际跑过；破坏性命令必须配 `!!! danger`。
4. **每页必须有"实践任务"和"完成标准"**，与 `assessment.md` 的评分维度挂钩。

---

## 九、实施路线图

| 阶段 | 内容 | 规模 | 优先级 |
|------|------|------|--------|
| **阶段 0：止血**（1–2 天） | 修正 §2.2 的 24 处事实错误；删除 §2.3 的无来源数字；修正 §3 的技术性错误（邮件列表、QEMU、Docker、Git）；删除 16 MB WAV；固定 CI action 版本 | 小 | **P0** |
| **阶段 1：结构整理**（2–3 天） | 目录重命名（sec0/sec1/sec2 → 有意义的名字）；拆分 4-H1 文件；迁移必修/拓展；重命名 `semeste` 文件；清空 `ch2/index.md` 三处空标题；更新 AGENTS.md | 小 | **P0** |
| **阶段 2：体例快赢**（2–3 天） | 补 36 处署名框；修复 6 处 `{： 。caption}` → `{: .caption }`；`!!! tips`→`!!! tip`、`???+ node`→`???+ note`、`??? answer`→`??? note`；统一代码围栏语言、人称、术语；标题去 emoji | 小，机械 | **P1** |
| **阶段 3：补齐当次成果**（最大的价值） | 项目画像工作纸；生态角色分析框架；许可证判断练习（含答案）；贡献提案模板 + 选题渠道 + Issue 礼仪 | 中 | **P0（就课程目标而言）** |
| **阶段 4：章节迁移与重建** | 重建第 3 次课许可证内容；第 8 次课扩写；`ch1/sec2` 重构为时间轴 + 案例并把不可考内容移出；Docker 六篇精简为三篇；效率工具改速查手册 | 大 | P1 |
| **阶段 5：教学基础设施** | 术语表、练习库、案例库、教师手册、数据与来源页 | 大 | P2 |

**建议的执行顺序**：阶段 3 与阶段 0 并行（前者是课程承诺，后者是信誉风险），阶段 1/2 可在一次集中清理中完成（多数是机械替换，适合作为学生的第一次开源贡献任务——这本身就是教材最好的素材）。

> 附带收益：阶段 1、2 的工作量小、边界清晰、验收标准明确，非常适合放进 `docs/course/project.md` 的 **A 类项目池**，作为学生的真实贡献任务。建议把本报告 §4、§5 转成 20–30 个 `good first issue`。

---

## 十、评审方法与局限

**做了的事**

- 45 个 Markdown 文件逐字通读（约 45 万字符），并按章分派逐节精读；
- 程序化检查：署名框覆盖、图注覆盖、代码围栏语言、标题层级与多 H1、图片/链接有效性、跨文件文本重复度、概念关键词覆盖度、无来源定量断言统计；
- 实际执行 `mkdocs build`（MkDocs 1.6.1 + Material 9.7.7 + Python 3.13）：**构建成功、零警告**；`nav` 覆盖全部文件，无死链；
- 检查构建产物：Mermaid 由 Material 运行时从 unpkg 动态加载（需联网）；搜索索引 `lang` 为 `en`、`separator` 含中文标点。

**没做到的事（需要你或维护者复核）**

- 本环境的 `web_search` 与 `web_fetch` 不可用（缺 API Key / 网络策略拒绝），因此涉及"当前最新版本号、项目是否仍活跃、某个标准是否真实存在"的判断，报告中已标注为**待核实**，请以联网核查为准。其中最需要优先核实的是 **《GB/T 44272-2024》**：它在正文中被引用 4 次并支撑了一整节内容。
- 未评估"教学效果"本身（没有课堂观察或学生反馈数据），§七、§八的对齐判断基于 `docs/course/` 的书面设计推导。

**建议的下一步**

1. 由你确认 §2.2 / §3 的错误修正清单，我可以按清单直接改（改动可拆分、可逐条 review）。
2. 确认目标结构（§8.1）后，我可以先做**第 3 次课许可证内容**与**第 8 次课扩写**这两块（价值最高、缺口最大），其余按 §9 分阶段推进。
