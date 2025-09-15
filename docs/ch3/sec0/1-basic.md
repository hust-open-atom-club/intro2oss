# Markdown 基本语法

!!! note "主要作者"

    [@Paulkm2006](https://github.com/Paulkm2006)

Markdown 是一种轻量级标记语言，具有**语法简洁、易读易写**的特点，广泛应用于文档编写、笔记记录和博客撰写等场景。GitHub、Gitee 等代码托管平台默认支持 Markdown 渲染，项目仓库中的 `README.md`、`CONTRIBUTING.md` 文件，以及 Issue 和 Pull Request 的描述信息，均采用 Markdown 语法。

## 1. 标题

使用 `#` 表示标题，`#` 的数量决定标题级别（从 1 级到 5 级）。合理设置标题层级，有助于提升文档结构清晰度，方便他人快速查找所需。

```md preview
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
内容
```

## 2. 段落与换行

直接输入文本即为一个段落，段落之间需空一行。例如：

```md preview
这是第一段。

这是第二段。
```

如需在同一段落内换行，可在行末添加两个空格后回车：

```md preview
这是第一行。(注意当前行最后有两个空格)  
这是第二行。
```

## 3. 强调

```md preview
- **加粗**：`**加粗**` 或 `__加粗__`
- *斜体*：`*斜体*` 或 `_斜体_`
- ~~删除线~~：`~~删除线~~`

或者以上方法的混用，如：

- ***加粗斜体***
- ~~*斜体删除*~~

```

## 4. 列表

- 无序列表：使用 `-`、`*` 或 `+`
- 有序列表：使用数字加点

```md preview
- 项目 1
- 项目 2

---

1. 第一项
2. 第二项
```

## 5. 链接与图片

- 链接：`[描述](链接地址)`
- 图片：`![描述](图片地址)`
- 可点击的图片：`[![描述](图片地址)](点击后打开的地址)`

```md preview
[华科开放原子俱乐部](https://oss.openatom.club)
![Logo](https://oss.openatom.club/assets/logo.png)
[![Logo](https://oss.openatom.club/assets/logo.png)](https://hust.openatom.club)
```

!!! warning

    在插入图片时，我们必须保证该链接**可以被外界访问**，这意味着你的图片必须满足以下条件之一

    1. 图片必须作为附件随 markdown 文件上传到当前仓库，且路径为相对路径（如 `assets/img.jpg`）
    2. 图片已上传到互联网可访问的托管服务

    有关插入图片的更多用法，请参考本章第二节 - Markdown 进阶语法。

## 6. 引用

使用 `>` 表示引用。

```md preview
> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

## 7. 代码

代码块常用于展示示例代码、命令行操作或配置文件内容，便于理解与复制。

- 行内代码：用反引号包裹，如 `` `print()` ``
- 代码块：用三个反引号包裹。通常来说，Markdown 编辑器能自动识别代码语言并高亮；但当遇到识别错误时，我们可以使用 ` ```<语言名称> ` 来告诉编辑器。

```md preview
```python
print("Hello, Markdown!")
```
```

## 8. 表格

```md preview
| 姓名 | 年龄 |
| ---- | ---- |
| 张三 |  18  |
| 李四 |  20  |
```

插入表格时，需要注意以下几点

1. 表头和数据行之间必须有分隔线
2. 分隔线至少需要三个连字符 ---
3. 两端的竖线 | 是可选的，但建议保留以提高可读性

我们还可以为表格设置对对齐

- `---:` 设置内容和标题栏居右对齐。
- `:---` 设置内容和标题栏居左对齐。
- `:---:` 设置内容和标题栏居中对齐。

!!! tips

    通常来说，手工实现的 markdown 表格在源文件中不甚美观。因此，我们可以使用 [Markdown 表格生成器](https://www.tablesgenerator.com/markdown_tables)来生成一个表格。

## 9. 分割线

使用三个及以上的 `-`、`*` 或 `_` 可表示分割线。

```markdown
---
```

---
!!! question

    尝试完成最终效果如下的 Markdown 文件

    ## 这是标题

    ### 这也是一个标题

    > 这是引用

    [![这是图片](https://oss.openatom.club/assets/logo.png)](https://oss.openatom.club/)

    *图片的链接为 `https://oss.openatom.club/assets/logo.png`，打开后跳转到`https://oss.openatom.club/`*

     [这是链接](https://oss.openatom.club/)

    ---

    这里是下一页！

    ```cpp
    // 这是一段 C++ 代码，我们通常使用 cpp 表示 C++
    #include <iostream>

    int main(){
        std::cout << "Hello, world!" << std::endl;
    }
    ```

    | 这是 | 一张 | 表格 |
    | :---- | :----: | ---- |
     | 左对齐 |  这里需要居中！！  | hello |
     | 文本 |  114514  | world |

---

以上是 Markdown 的常用基础语法，更多高级用法可参考 [Markdown 官方文档](https://markdown.com.cn/basic-syntax/)。
