# 完成开源贡献

本章聚焦一个具体目标：帮助你把想法转化为一项符合社区规范、可以被真实项目评审的贡献。

## 课堂必修

### 协作写作

先学习 [Markdown 基本语法](writing/1-basic.md)，掌握标题、列表、链接、图片、引用、代码和表格。需要编写公式、图表或复杂页面时，再查阅 [Markdown 进阶语法](writing/2-advanced.md)。

### Git 与平台协作

按以下顺序完成学习：

1. [Git 简介](git/1-introduction.md)：理解仓库、提交、分支和分布式版本控制。
2. [代码托管平台简介](git/platform/index.md)：认识仓库、Issue、Fork 和 Pull Request；随后完成[注册与熟悉平台](git/platform/practice-register.md)、[创建并管理仓库](git/platform/practice-repository.md)、[Fork 一个仓库](git/platform/practice-fork.md)三项实践。
3. [Git 基础配置](git/3-basic-configuration.md)：配置身份、SSH，并创建或克隆仓库。
4. [Git 暂存区与提交](git/4-staging.md)：选择修改、查看差异并形成提交。
5. [提交信息规范](git/5-commit-message.md)：用提交信息准确说明修改动机。
6. [参与开源项目](git/6-participate-in.md)：把工具串联成完整贡献流程。

### 按需使用 Linux

[常用 Linux 命令与工具](linux/1-commands.md)作为实践手册使用。课程不要求背诵命令，重点是能够查阅帮助、理解命令影响并记录实际验证过程。

## 真实贡献流程

```mermaid
graph LR
    A[阅读项目规范] --> B[确认问题]
    B --> C[创建个人分支]
    C --> D[修改与验证]
    D --> E[提交贡献]
    E --> F[响应评审]
    F --> G[复盘与继续参与]
```

贡献项目的里程碑、证据和异常情况处理见[真实贡献项目](../course/project.md)。

## 拓展学习

以下内容不占用核心课时，可根据项目方向选择：

- **Git 进阶**：合并与变基、分布式协作、对象数据库和本地开发技巧（[Rebase 与 Merge](git/advanced/1-rebase-merge.md)、[分布式版本控制原理](git/advanced/2-control-process.md)、[Git 底层原理](git/advanced/3-advanced-theory.md)、[Git 辅助本地开发](git/advanced/4-help-local.md)）；
- **Docker**：镜像、存储、网络、Compose 和容器管理（[Docker 基础](docker/1-foundation.md)起）；
- **QEMU**：系统模拟、RISC-V 环境和邮件列表补丁协作（[QEMU 基础](qemu/1-foundation.md)、[参与 QEMU 邮件列表讨论](qemu/2-send-email.md)）；
- **效率工具**：tmux、btop、tldr 等命令行工具（[常用的开源工具](tools/1-useful-oss.md)），以及 [Missing Semester 课程](tools/2-missing-semester.md)。

!!! tip "学习原则"

    不必在首次贡献前学完所有工具。先选择一个范围合适的问题，再按目标项目的要求补充知识。
