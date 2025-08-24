# 提交规范深度解析与实践指南：三大体系对比与应用

---

## 一、Linux 内核提交规范：工程艺术的典范

### 1. 设计哲学溯源

Linux 内核的提交规范起源于 Linus Torvalds 对代码管理的哲学思考：

- **原子性原则**：每个提交必须是独立的最小功能单元（类似 Unix 的“Do One Thing Well”）
- **可追溯性**：通过子系统标签实现快速定位，减少代码审查成本
- **责任溯源**：强制签名机制建立开发者问责体系

### 2. 格式规范详解

```text
[子系统标签]: [动词开头描述] (50 字符内)

[详细说明（72 字符/行）]
[空行]
[签名区]
[关联标记]
```

#### 核心要素

- **标签系统**：精确到文件路径级别的分类（示例见下表）
- **动词规范**：fix/add/remove 等现在时态动词
- **行长度限制**：标题 50 字符，正文 72 字符（适配 80 列终端）

#### 标签类型速查表

| 标签         | 对应目录     | 典型变更示例       |
| ------------ | ------------ | ------------------ |
| net:         | net/         | 网络协议栈优化     |
| mm/vmalloc:  | mm/vmalloc.c | 虚拟内存分配器改进 |
| drivers/usb: | drivers/usb/ | USB 驱动兼容性修复  |
| arch/arm64:  | arch/arm64/  | ARM64 架构特定优化  |
| tools/perf:  | tools/perf/  | 性能分析工具增强   |

### 3. 典型示例深度解析

**优秀案例**：

```text
mm/page_alloc: fix high-order page allocation regression

When allocating a high-order page from a non-movable zone falls back
to a movable pageblock, ensure proper migration type tracking.

Fixes: 6bb15432f9e4 ("mm, page_alloc: spread allocations across zones")
Cc: <stable@vger.kernel.org>
Signed-off-by: Mel Gorman <mgorman@techsingularity.net>
```

**结构拆解**：

1. 标签精确到子模块 `mm/page_alloc`
2. 动词 `fix` 明确变更类型
3. 引用具体 commit hash 实现问题溯源
4. 添加稳定分支标记 `Cc: <stable@vger.kernel.org>`
5. 清晰描述问题现象和修复逻辑

**常见错误模式**：

```text
Fixed some memory bugs
```

问题分析：

- 未使用子系统标签
- 动词时态错误（应使用现在时）
- 描述过于模糊
- 缺少签名和追踪信息

完整的 Linux 社区贡献指南可见：[Submitting patches：the essential guide to getting your code into the kernel](https://docs.kernel.org/process/submitting-patches.html)

---

## 二、Conventional Commits：现代协作的标准化方案

### 1. 规范演进历程

2019 年由 Angular 团队提出，现已成为 GitHub 80% 以上开源项目的选择，特点：

- **机器可读**：支持自动化生成 CHANGELOG
- **语义化版本**：通过提交类型自动确定版本号
- **协作友好**：降低跨团队沟通成本

### 2. 完整语法结构

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 类型语义字典（扩展版）

| 类型     | 适用场景               | 版本影响 |
| -------- | ---------------------- | -------- |
| feat     | 新增功能/API           | minor↑  |
| fix      | 错误修复               | patch↑  |
| perf     | 性能优化               | patch↑  |
| refactor | 代码重构（不改变行为） | -        |
| revert   | 回滚提交               | patch↑  |
| ci       | CI 配置变更             | -        |
| chore    | 日常维护（不影响功能） | -        |

### 3. 高级应用技巧

#### 破坏性变更标记

```text
feat(api)!: remove deprecated methods

BREAKING CHANGE: The following deprecated methods are removed:
- User#setName
- User#getName
```

#### 多问题关联

```text
fix(core): handle null pointer in renderer

Closes #1234
Related to #1122
```

### 4. 实战案例对比

**标准提交**：

```text
feat(auth): add OAuth2 support

- Implement OpenID Connect flow
- Add token refresh mechanism
- Update configuration docs

Closes #45
```

**优化提交**：

```text
feat(auth)!: migrate to OpenID Connect

BREAKING CHANGE: Removed legacy SAML authentication flow
- Implement RFC-compliant OIDC integration
- Add dynamic client registration support
- Update security configuration templates

Closes #45, #78
Refs: https://openid.net/specs/openid-connect-core-1_0.html
```

完整的 [conventional commits 指南](https://www.conventionalcommits.org/en/v1.0.0/)

---

## 三、RustSBI 规范实践：领域特定的演进

一个优秀的*提交*应该只解决一个问题，使得功能完整，即便只有一行代码也可以提交。而一个优秀的*提交信息*是项目的标杆，这是未来其他贡献者给项目贡献的规范。他们会按照你的*提交信息*去编写他们的贡献，从标题的格式到内容的详细程度。所以如何写好一个*提交信息*就显得十分重要。不仅要遵循项目的风格指南，确保*提交信息*的一致；还要使得*提交信息*的标题清晰简洁，能够准确反映变更的内容。

需要注意的是，RustSBI 社区采用**全英文**编写的*提交信息*。同时，`rustsbi/rustsbi` 若干个模块都具有自己的更改日志文件，我们使用*提交信息*来生成 `CHANGELOG.md` 文档。我们通过*集成测试*检查对本模块文件夹下的任何文件的修改，**必须一并为对应的 `CHANGELOG.md` 增加 CHANGELOG 条目**。否则检查不通过，可能会导致您的更改无法出现在下一个版本的更新日志中。

其次，每个*提交*都需要签名，每次*拉取请求*或*推送*都由*集成测试*检查更新的*提交*是否具有 `Signed-off-by` 标记。

### 提交信息格式

在标题之后，应提供详细的变更说明。如果你是一个新贡献者，这里推荐可以按照是什么、为什么、怎么做的思路去整理你的*提交信息*。

- **是什么**：首先可以描述变更的背景，你所试图解决的是一个什么样的问题。
- **为什么**：说明变更的影响，与之前进行对比，比如修复了哪些 bug、增加了哪些功能或是改善了哪些性能等。
- **怎么做**：描述你所做出的具体修改。

至此，如果你已经清楚地组织了你的*提交信息*或是有了大致思路。那么恭喜你可以进入到下面的格式环节了。

一个*提交信息*必须包含标题和脚注，正文部分是可选项。如果你是向项目直接*提交*的贡献者，那么正文部分则是必要的：

```bash
<header>

[optional <body>]

<footer>
```

> 为了更好的可读性，提交信息每行都不应该超过 100 个字符！

#### 标题

作为提交信息的第一行，`<标题>` 有着严格的格式要求，通常为：

```bash
<scope or type>: <subject>
```

如果你已习惯了**约定式提交**也可以同时使用 `<类型>` 和 `<范围>`：

```bash
<type>(<scope>): <suject> 
```

> `<范围 或 类型>/<类型>(范围)` 后面有一个 `!`，或在 `<脚注>` 中包含 `BREAKING CHANGE:`，提醒注意**破坏性变更**。破坏性变更可以是任意 `<类型>` 提交的一部分。

#### 范围

`<范围>` 是所主要更改的子模块名称，多个子模块和具有重名的子模块的更改可以取上层模块名称作为 `<标题>` 的前缀。`<范围>` 的使用适合于一个提交中涵盖了多个 `<类型>` 或不适合用 `<类型>` 来界定的场景。

示例：

- **`rt`**：`sbi-rt/src/legacy.rs` 更改 ([cfbb772](https://github.com/rustsbi/rustsbi/commit/cfbb7724d0b1a9ab37d2d18177db778aef5f04a3))
- **`spec`**：`sbi-spec/CHANGELOG.md` 和 `sbi-spec/Cargo.toml` 更改 ([0837da8](https://github.com/rustsbi/rustsbi/commit/0837da8fc325fca23c5ac7423f087e1d4d54783e))
- **`binary`**：`sbi-spec/src/binary.rs` 文件更改 ([f87e9fc](https://github.com/rustsbi/rustsbi/commit/f87e9fc2cdb5575d49146fd3b5b25dc0d279236c))
- **`lib`**：`src/cppc.rs`、`src/hsm.rs`、`src/rfence.rs` 文件更改 ([c7ce73b](https://github.com/rustsbi/rustsbi/commit/c7ce73bb84eef7cf3aa1683b1d15094eb081ed73))
- **`tests`**：`tests/build-full.rs`、`tests/build-rename.rs`、`tests/build-skip.rs` 文件更改 ([2753980](https://github.com/rustsbi/rustsbi/commit/2753980672348c745ac84a074695b96363d22d71))
- **`deps`**：`Cargo.toml`、`sbi-testing/Cargo.toml` 中 `[dependencies]` 依赖项更改 ([44b6aea](https://github.com/rustsbi/rustsbi/commit/44b6aea92cb807397108629e852354683e9b2943))
- **`crate`**：`Cargo.toml` 更改 ([a3b2fc4](https://github.com/rustsbi/rustsbi/commit/a3b2fc49bea59b12a77f912f304126d887351fa4))
- **`readme`**：`README.md` 更改 ([84a2876](https://github.com/rustsbi/rustsbi/commit/84a287617a23612e17278396b5e8505cb0b21465))

#### 类型

作为对 `<范围>` 的补充，遵循**约定式提交**，必须为下列之一，同时附上示例：

- **`feat`**：新增了一个功能 ([5baa946](https://github.com/rustsbi/rustsbi/commit/5baa946c4036bccba760be36c049ad1626b8d5e0))
- **`fix`**：修复了一个 bug ([293db69](https://github.com/rustsbi/rustsbi/commit/293db697b39daf69eae1315cb85996e134d0d0b7))
- **`build`**：修改项目构建清单，例如修改依赖项、对象或者升级包 (Crate) 版本等 ([3b5daf8](https://github.com/rustsbi/rustsbi-d1/commit/3b5daf8e81f6eab4f2c00f734c096036b8ff4219))
- **`refactor`**：重构代码，例如修改代码结构、变量、函数等但不修改功能逻辑 ([e0f842c](https://github.com/rustsbi/rustsbi-qemu/commit/e0f842cea963a7a8dbaf93c80a0cbabcfdf31e36))
- **`docs`**：用于修改文档 ([204ca9e](https://github.com/rustsbi/rustsbi/commit/204ca9eafa45b91642536356e19edb4bef0e53d6))
- **`ci`**：用于修改持续集成流程 ([52c4c55](https://github.com/rustsbi/allwinner-hal/commit/52c4c553437f913b9d4677683c4fdbca963af317))
- **`test`**：添加测试用例

#### 主题

概括总结你的贡献：

- 除专有名词、缩略语和涉及代码的词语（如函数/变量名）外，全部使用小写字母
- 采用命令式的现在时态，如“add”、“fix”、“update”
- 末尾不加英文句号 `.`
- 最好不超过 50 个字符，建议不超过 72 个字符即可

#### 正文

在 `<标题>` 与 `<正文>` 之间隔一个空行，即保持第二行为空，正文另起一行。这里可以对你的变更说明进行详细的展开了，希望上面整理思路的方式可以帮到你。记得和 `<主题>` 同样使用命令式的现在时态：“change”而不是“changed”或“changes”。

#### 脚注

`<脚注>` 与之前的 `<正文>` 也要隔一个空行。`<脚注>` 部分包含签名和与该提交相关的其他引用：

- **`Signed-off-by:`** `git commit` 命令中通过 `-s` 参数指定。
- **`Fix:`** 如果该提交修复了一个开放问题，在日志末尾添加对该问题的引用。
  - 示例：`Fix: https://github.com/rustsbi/rustsbi/issues/63` 或 `Fix: #63`
- **`Refs:`** 用于添加其他引用。
  - 示例：`Refs: https://github.com/riscv-non-isa/riscv-sbi-doc/releases/download/vv3.0-rc1/riscv-sbi.pdf` ([fbbab51](https://github.com/rustsbi/rustsbi/commit/fbbab51bd9fdf6ca9b459f19714c8fd9a75240cc))
- **`BREAKING CHANGE:`** 表示引入了破坏性变更，可能无法兼容依赖于原有功能的代码。这些变更要求社区用户在更新到包含此提交的版本后修改他们的代码。引入破坏性变更的同时进行如下操作：
  - **文档更新：**更新相关文档，明确说明变更内容、影响以及可能的迁移步骤。
  - **版本升级：**发布一个新版本时，在发布说明中清晰地标明 `BREAKING CHANGE`。
  - **通知：**向用户、开发者或团队成员提供足够的通知，提前告知即将发生的变更，以便做好准备。

### Commit Messages 模板

```bash
rt: refine constant declaration and document on legacy extensions

Modify links on document; do not expose legacy extension EID constants, 
developers should use from `sbi-spec` crate. 

Signed-off-by: Zhouqi Jiang <luojia@hust.edu.cn>
```

```bash
main: add embedded-cli based serial command line console support

- Add embedded-cli based serial command line console support for bouffaloader, 
which features the command-line menu with autocomplete, history, and help command. 
- Add flash guide for bouffaloader on Windows in `README.md`, with which 
we can have a test on M1s Dock. 

Refs: https://github.com/rustsbi/bouffalo-hal/pull/4
Refs: https://github.com/rustsbi/bouffalo-hal/pull/5
Signed-off-by: DongQing <placebo27@hust.edu.cn>
```

```bash
binary: enhance `SbiRet` structure functions to match `core::result::Result` APIs

- binary: change `SbiRet::and` signature to `fn and<U>(self, res: Result<U, Error>) -> Result<U, Error>`

- binary: add function `is_ok_and`, `is_err_and`, `inspect` and `inspect_err` for `SbiRet` structure 

Signed-off-by: Zhouqi Jiang <luojia@hust.edu.cn>
```

---

## 四、提交文化的演进趋势

1. **AI 辅助时代**：GitHub Copilot 已支持自动生成符合规范的提交信息
2. **可视化分析**：基于提交类型的代码健康度仪表盘
3. **安全增强**：结合 Sigstore 的提交签名验证
4. **跨平台统一**：GitLab/BitBucket 逐步支持 Conventional Commits

通过掌握这些规范，开发者不仅能提升个人工程能力，更能深入理解开源社区治理的底层逻辑。规范的本质不是约束，而是建立高效协作的共同语言。
