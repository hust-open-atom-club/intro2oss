#!/usr/bin/env python3
"""
智能批量增强 Markdown 文件，充分利用 Material 主题特性。
"""
import os
import re
import glob

DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')

# 文件路径 -> 标题 emoji 映射
EMOJI_MAP = {
    'ch0/index.md': '📖',
    'ch1/index.md': '🌐',
    'ch1/sec1/what-is-oss.md': '🔓',
    'ch1/sec2/history-of-oss.md': '📜',
    'ch1/sec3/why-oss.md': '💡',
    'ch1/sec4/how-to-oss.md': '🛠️',
    'ch2/sec1/1-open_source_ecosystem.md': '🌱',
    'ch2/sec1/2-open_source_licenses.md': '📋',
    'ch2/sec1/terminology.md': '📖',
    'ch2/sec2/culture.md': '🎭',
    'ch2/sec3/1-project-operations.md': '⚙️',
    'ch2/sec3/2-contributions-rewards.md': '🤝',
    'ch2/sec3/3-legal-and-compliance.md': '⚖️',
    'ch2/sec3/rules.md': '📜',
    'ch3/sec0/1-basic.md': '📝',
    'ch3/sec0/2-advanced.md': '✨',
    'ch3/sec1/index.md': '🔀',
    'ch3/sec1/subsec1/1-git-introduction.md': '🔀',
    'ch3/sec1/subsec1/2-code-hosting-platforms.md': '🌐',
    'ch3/sec1/subsec2/1-basic-configuration.md': '⚙️',
    'ch3/sec1/subsec2/2-staging.md': '📦',
    'ch3/sec1/subsec2/3-commit-message.md': '💬',
    'ch3/sec1/subsec3/1-rebase-merge.md': '🔀',
    'ch3/sec1/subsec3/2-Control-Process.md': '🔄',
    'ch3/sec1/subsec3/3-advanced-theory.md': '🧠',
    'ch3/sec1/subsec3/4-help-open.md': '🆘',
    'ch3/sec1/subsec3/5-participate-in.md': '🤝',
    'ch3/sec2/4-other-commands.md': '🐧',
    'ch3/sec3/1_foundation.md': '🐳',
    'ch3/sec3/2_dockerfile.md': '📄',
    'ch3/sec3/3_storage.md': '💾',
    'ch3/sec3/4_network.md': '🌐',
    'ch3/sec3/5_compose.md': '🔧',
    'ch3/sec3/6_management.md': '📊',
    'ch3/sec4/1-qemu-foundation.md': '🖥️',
    'ch3/sec4/2-qemu-send-email.md': '📧',
    'ch3/sec5/1-useful-oss.md': '🧰',
    'ch3/sec5/2-the-missing-semeste-of-your-CS-education.md': '🎓',
    'ch4/index.md': '🌟',
    'ch99/abouts.md': '📎',
}


def add_emoji_to_title(content, rel_path):
    """给一级标题添加 emoji（如果还没有的话）。"""
    emoji = EMOJI_MAP.get(rel_path)
    if not emoji:
        return content

    lines = content.splitlines()
    if not lines:
        return content

    # 第一行是一级标题？
    if lines[0].startswith('# ') and not lines[0].startswith('# ' + emoji) and not lines[0].startswith('# :'):
        title = lines[0][2:].strip()
        lines[0] = f'# {emoji} {title}'
        return '\n'.join(lines)

    return content


def wrap_section_admonition(content, heading_pattern, admonition_type, admonition_title):
    """
    将匹配到的二级标题及其后续内容（直到下一个二级标题或文件尾）
    包装成 admonition 或 details 块。
    """
    lines = content.splitlines()
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        match = re.match(heading_pattern, line)

        if match:
            # 检查下一行是否已经是 admonition（避免重复包装）
            if i + 1 < len(lines) and (lines[i + 1].strip().startswith('!!!') or lines[i + 1].strip().startswith('???')):
                result.append(line)
                i += 1
                continue

            result.append(line)
            i += 1
            # 收集该小节的所有内容
            section_lines = []
            while i < len(lines):
                if re.match(r'^## ', lines[i]):
                    break
                section_lines.append(lines[i])
                i += 1

            # 包装成 admonition
            result.append(f'')
            result.append(f'{admonition_type} "{admonition_title}"')
            result.append('')
            for sl in section_lines:
                if sl.strip() == '':
                    result.append('')
                else:
                    result.append('    ' + sl)
            result.append('')
            continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def generate_fancy_placeholder(rel_path):
    """为空白/占位文件生成 fancy 内容。"""
    if rel_path == 'ch4/index.md':
        return '''# 🌟 领导开源社区

!!! abstract "章节导览"

    本章将深入探讨如何从零开始构建并领导一个健康的开源社区。
    我们将涵盖社区治理、项目管理、贡献者激励以及长期可持续发展等核心议题。

!!! tip "核心能力模型"

    ```mermaid
    graph TD
        A[开源社区领导力] --> B[技术愿景]
        A --> C[社区运营]
        A --> D[生态治理]
        B --> B1[路线图规划]
        B --> B2[架构决策]
        C --> C1[新人引导]
        C --> C2[活动组织]
        D --> D1[规则制定]
        D --> D2[利益平衡]
    ```

## 🚧 内容建设中

!!! warning "敬请期待"

    本章节内容正在紧锣密鼓地筹备中，我们将尽快为您呈现高质量的学习材料。

    在此期间，您可以：

    - [回顾前三章的内容](../ch3/)
    - [参与本教程的建设](https://github.com/hust-open-atom-club/intro2oss)
    - [加入我们的社区](https://hust.openatom.club/)

## 💬 讨论与反馈

!!! info "我们想听到你的声音"

    如果你有关于"开源社区领导力"的话题建议，或者希望贡献相关内容，欢迎通过以下方式联系我们：

    - 在 GitHub 上提交 [Issue](https://github.com/hust-open-atom-club/intro2oss/issues)
    - 发送邮件至我们的公开邮件列表
    - 参与线下开源沙龙活动
'''
    elif rel_path == 'ch99/abouts.md':
        return '''# 📎 关于本教程

!!! abstract "项目愿景"

    本教程由 [华中科技大学开放原子开源俱乐部](https://hust.openatom.club/) 主导编写，
    秉持**"以开源方式来建设开源课程"**的理念，希望能为高校开源教育贡献一份力量。

## 🎯 我们的目标

<div class="grid cards" markdown>

-   :material-school-outline:{ .lg .middle } __面向学生__

    ---

    为零基础同学提供系统、可实践的开源通识教育，
    帮助大家从"开源消费者"成长为"开源贡献者"。

-   :material-account-group:{ .lg .middle } __面向社区__

    ---

    建立一个开放、协作的课程内容生态，
    让社区的智慧和经验能够沉淀为可持续的教育资源。

-   :material-github:{ .lg .middle } __面向教育者__

    ---

    提供一套可复制、可扩展的开源课程框架，
    降低高校开设开源通识课程的门槛。

</div>

## 🤝 如何参与

!!! tip "欢迎任何形式的贡献"

    本教程完全开源，采用 MIT 许可证。你可以通过以下方式参与：

    - **修正错误**：发现 typo 或内容错误？直接提交 PR！
    - **补充内容**：某一章节你有更深入的见解？欢迎扩充！
    - **翻译工作**：帮助我们将教程翻译成更多语言。
    - **案例分享**：分享你的开源实践故事，激励更多同学。

    [:octicons-mark-github-16: 在 GitHub 上贡献](https://github.com/hust-open-atom-club/intro2oss){ .md-button .md-button--primary }

## 📝 许可证

!!! info "MIT License"

    本教程内容采用 [MIT 许可证](https://opensource.org/license/mit/) 开源。

    你可以自由使用、修改和再分发本教程的内容，
    只需在衍生作品中保留原始版权声明即可。

## 🙏 致谢

!!! success "感谢所有贡献者"

    本教程的成长离不开每一位贡献者的付出。

    特别感谢：

    - 华中科技大学开放原子开源俱乐部的全体成员
    - 为本教程提交 Issue 和 Pull Request 的社区伙伴
    - 所有在课程建设和推广中给予支持的老师们

    *排名不分先后，感谢有你！*
'''
    return None


def process_file(filepath, rel_path):
    """处理单个 Markdown 文件。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # 如果是占位文件，直接生成 fancy 内容
    if content.strip() in ('[待补充]', '[TODO]', 'TBD', '待补充', ''):
        new_content = generate_fancy_placeholder(rel_path)
        if new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'  [GENERATED] {rel_path}')
            return

    # 1. 给标题加 emoji
    content = add_emoji_to_title(content, rel_path)

    # 2. 包装"本节小结"
    content = wrap_section_admonition(
        content,
        r'^## 本节小结\s*$',
        '!!! success',
        '本节小结'
    )

    # 3. 包装"参考链接"为可折叠
    content = wrap_section_admonition(
        content,
        r'^## 参考链接\s*$',
        '??? info',
        '参考链接'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [ENHANCED] {rel_path}')
    else:
        print(f'  [SKIP] {rel_path}')


def main():
    md_files = sorted(glob.glob(os.path.join(DOCS_DIR, '**/*.md'), recursive=True))
    print(f'Found {len(md_files)} markdown files.\n')

    for filepath in md_files:
        rel_path = os.path.relpath(filepath, DOCS_DIR)
        process_file(filepath, rel_path)

    print('\nDone!')


if __name__ == '__main__':
    main()
