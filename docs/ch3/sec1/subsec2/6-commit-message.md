# 为 RustSBI 贡献

---

## 行为准则

采用行为准则制定社区标准，欢迎大家参与贡献。

## 提交信息指南

一个优秀的*提交*应该只解决一个问题，使得功能完整，即便只有一行代码也可以提交。而一个优秀的*提交信息*是项目的标杆，这是未来其他贡献者给项目贡献的规范。他们会按照你的*提交信息*去编写他们的贡献，从标题的格式到内容的详细程度。所以如何写好一个*提交信息*就显得十分重要。不仅要遵循项目的风格指南，确保*提交信息*的一致；还要使得*提交信息*的标题清晰简洁，能够准确反映变更的内容。

需要注意的是，RustSBI 社区采用**全英文**编写的*提交信息*。同时， `rustsbi/rustsbi` 若干个模块都具有自己的更改日志文件，我们使用*提交信息*来生成 `CHANGELOG.md` 文档。我们通过*集成测试*检查对本模块文件夹下的任何文件的修改，**必须一并为对应的 `CHANGELOG.md` 增加 CHANGELOG 条目**。否则检查不通过，可能会导致您的更改无法出现在下一个版本的更新日志中。

其次，每个*提交*都需要签名，每次*拉取请求*或*推送*都由*集成测试*检查更新的*提交*是否具有 `Signed-off-by` 标记。

### 提交信息格式

在标题之后，应提供详细的变更说明。如果你是一个新贡献者，这里推荐可以按照是什么、为什么、怎么做的思路去整理你的*提交信息*。

- **是什么**：首先可以描述变更的背景，你所试图解决的是一个什么样的问题。
- **为什么**：说明变更的影响，与之前进行对比，比如修复了哪些bug、增加了哪些功能或是改善了哪些性能等。
- **怎么做**：描述你所做出的具体修改。

至此，如果你已经清楚地组织了你的*提交信息*或是有了大致思路。那么恭喜你可以进入到下面的格式环节了。

一个*提交信息*必须包含标题和脚注，正文部分是可选项。如果你是向项目直接*提交* 的贡献者，那么正文部分则是必要的：

```
<header>

[optional <body>]

<footer>
```

> 为了更好的可读性，提交信息每行都不应该超过 100 个字符！

#### 标题

作为提交信息的第一行， `<标题>` 有着严格的格式要求，通常为：

```
<scope or type>: <subject>
```

如果你已习惯了**约定式提交**也可以同时使用 `<类型>` 和 `<范围>` ：

```
<type>(<scope>): <suject> 
```

> `<范围 或 类型>/<类型>(范围)` 后面有一个  `!`  ，或在 `<脚注>` 中包含  `BREAKING CHANGE:`  ，提醒注意**破坏性变更**。破坏性变更可以是任意 `<类型>` 提交的一部分。

#### 范围

`<范围>` 是所主要更改的子模块名称，多个子模块和具有重名的子模块的更改可以取上层模块名称作为 `<标题>` 的前缀。 `<范围>` 的使用适合于一个提交中涵盖了多个 `<类型>` 或不适合用 `<类型>` 来界定的场景。

示例：

- **`rt`**: `sbi-rt/src/legacy.rs` 更改 ([cfbb772](https://github.com/rustsbi/rustsbi/commit/cfbb7724d0b1a9ab37d2d18177db778aef5f04a3))
- **`spec`**: `sbi-spec/CHANGELOG.md`和 `sbi-spec/Cargo.toml` 更改 ([0837da8](https://github.com/rustsbi/rustsbi/commit/0837da8fc325fca23c5ac7423f087e1d4d54783e))
- **`binary`**: `sbi-spec/src/binary.rs` 文件更改 ([f87e9fc](https://github.com/rustsbi/rustsbi/commit/f87e9fc2cdb5575d49146fd3b5b25dc0d279236c))
- **`lib`**: `src/cppc.rs`、`src/hsm.rs`、`src/rfence.rs` 文件更改 ([c7ce73b](https://github.com/rustsbi/rustsbi/commit/c7ce73bb84eef7cf3aa1683b1d15094eb081ed73))
- **`tests`**: `tests/build-full.rs`、`tests/build-rename.rs`、`tests/build-skip.rs` 文件更改 ([2753980](https://github.com/rustsbi/rustsbi/commit/2753980672348c745ac84a074695b96363d22d71))
- **`deps`**: `Cargo.toml`、`sbi-testing/Cargo.toml` 中 `[dependencies]`依赖项更改 ([44b6aea](https://github.com/rustsbi/rustsbi/commit/44b6aea92cb807397108629e852354683e9b2943))
- **`crate`**: `Cargo.toml` 更改 ([a3b2fc4](https://github.com/rustsbi/rustsbi/commit/a3b2fc49bea59b12a77f912f304126d887351fa4))
- **`readme`**: `README.md` 更改 ([84a2876](https://github.com/rustsbi/rustsbi/commit/84a287617a23612e17278396b5e8505cb0b21465))

#### 类型

作为对 `<范围>` 的补充，遵循**约定式提交**，必须为下列之一，同时附上示例：

- **`feat`**: 新增了一个功能 ([5baa946](https://github.com/rustsbi/rustsbi/commit/5baa946c4036bccba760be36c049ad1626b8d5e0))
- **`fix`**: 修复了一个 bug ([293db69](https://github.com/rustsbi/rustsbi/commit/293db697b39daf69eae1315cb85996e134d0d0b7))
- **`build`**: 修改项目构建清单，例如修改依赖项、对象或者升级包 (Crate) 版本等 ([3b5daf8](https://github.com/rustsbi/rustsbi-d1/commit/3b5daf8e81f6eab4f2c00f734c096036b8ff4219))
- **`refactor`**: 重构代码，例如修改代码结构、变量、函数等但不修改功能逻辑 ([e0f842c](https://github.com/rustsbi/rustsbi-qemu/commit/e0f842cea963a7a8dbaf93c80a0cbabcfdf31e36))
- **`docs`**: 用于修改文档 ([204ca9e](https://github.com/rustsbi/rustsbi/commit/204ca9eafa45b91642536356e19edb4bef0e53d6))
- **`ci`**:  用于修改持续集成流程 ([52c4c55](https://github.com/rustsbi/allwinner-hal/commit/52c4c553437f913b9d4677683c4fdbca963af317))
- **`test`**: 添加测试用例

#### 主题

概括总结你的贡献：

- 除专有名词、缩略语和涉及代码的词语（如函数/变量名）外，全部使用小写字母
- 采用命令式的现在时态，如“add”、“fix”、“update”
- 末尾不加英文句号 `.`
- 最好不超过 50 个字符，建议不超过 72 个字符即可

#### 正文

在 `<标题>` 与 `<正文>` 之间隔一个空行，即保持第二行为空，正文另起一行。这里可以对你的变更说明进行详细的展开了，希望上面整理思路的方式可以帮到你。记得和 `<主题>` 同样使用命令式的现在时态："change" 而不是 "changed" 或 "changes"。

#### 脚注

`<脚注>` 与之前的 `<正文>` 也要隔一个空行。 `<脚注>` 部分包含签名和与该提交相关的其他引用：

- **`Signed-off-by:`** `git commit` 命令中通过 `-s` 参数指定。
- **`Fix:`** 如果该提交修复了一个开放问题，在日志末尾添加对该问题的引用。
  - 示例：`Fix: https://github.com/rustsbi/rustsbi/issues/63` 或 `Fix: #63`
- **`Refs:`** 用于添加其他引用。
  - 示例：`Refs: https://github.com/riscv-non-isa/riscv-sbi-doc/releases/download/vv3.0-rc1/riscv-sbi.pdf` ([fbbab51](https://github.com/rustsbi/rustsbi/commit/fbbab51bd9fdf6ca9b459f19714c8fd9a75240cc))
- **`BREAKING CHANGE:`** 表示引入了破坏性变更，可能无法兼容依赖于原有功能的代码。这些变更要求社区用户在更新到包含此提交的版本后修改他们的代码。引入破坏性变更的同时进行如下操作：
  - **文档更新：** 更新相关文档，明确说明变更内容、影响以及可能的迁移步骤。
  - **版本升级：** 发布一个新版本时，在发布说明中清晰地标明 `BREAKING CHANGE`。
  - **通知：** 向用户、开发者或团队成员提供足够的通知，提前告知即将发生的变更，以便做好准备。

### Commit Messages 模板

```
rt: refine constant declaration and document on legacy extensions

Modify links on document; do not expose legacy extension EID constants, 
developers should use from `sbi-spec` crate. 

Signed-off-by: Zhouqi Jiang <luojia@hust.edu.cn>
```

```
main: add embedded-cli based serial command line console support

- Add embedded-cli based serial command line console support for bouffaloader, 
which features the command-line menu with autocomplete, history, and help command. 
- Add flash guide for bouffaloader on Windows in `README.md`, with which 
we can have a test on M1s Dock. 

Refs: https://github.com/rustsbi/bouffalo-hal/pull/4
Refs: https://github.com/rustsbi/bouffalo-hal/pull/5
Signed-off-by: DongQing <placebo27@hust.edu.cn>
```

```
binary: enhance `SbiRet` structure functions to match `core::result::Result` APIs

- binary: change `SbiRet::and` signature to `fn and<U>(self, res: Result<U, Error>) -> Result<U, Error>`

- binary: add function `is_ok_and`, `is_err_and`, `inspect` and `inspect_err` for `SbiRet` structure 

Signed-off-by: Zhouqi Jiang <luojia@hust.edu.cn>
```

当你看完这篇文档，相信你也可以独立完成一个优秀的*提交信息*了。经过多次实战编写*提交信息*之后，你也会逐渐拥有属于自己的思路，形成自己的风格，更加自由灵活多变。
