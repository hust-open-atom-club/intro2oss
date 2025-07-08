!!! note "主要作者"

    [@Paulkm2006](https://github.com/Paulkm2006)

# Markdown 基本语法

Markdown 是一种轻量级标记语言，常用于编写文档、说明和博客。在开源软件的贡献中，我们常常使用 Markdown 来编写文档、需求与说明等。

同时，Github 等代码分享平台默认均以 Markdown 语法渲染文档：我们常常在项目仓库中见到的`README.md`、`CONTRIBUTING.md`等文件均是 Markdown 编写的；在提出 Issue、描述 Pull Request 时，我们同样使用 Markdown 编写对应的消息。 

## 1. 标题

使用`#`表示标题，数量表示级别（1~6 级）。养成良好的标题习惯可以让他人方便地找到想要的资料。

```markdown
# 一级标题
## 二级标题
### 三级标题
```

## 2. 段落与换行

直接输入文本即为段落。段落之间空一行。

## 3. 强调

- **加粗**：`**加粗**` 或 `__加粗__`
- *斜体*：`*斜体*` 或 `_斜体_`
- ~~删除线~~：`~~删除线~~`

## 4. 列表

- 无序列表：使用`-`、`*`或`+`
- 有序列表：使用数字加点

```markdown
- 项目 1
- 项目 2

1. 第一项
2. 第二项
```

## 5. 链接与图片

- 链接：`[描述](链接地址)`
- 图片：`![描述](图片地址)`
- 可点击的图片：`[![描述](图片地址)](点击后打开的地址)`

```markdown
[百度](https://www.baidu.com)
![Logo](https://oss.hust.openatom.club/assets/logo.png)
[![Logo](https://oss.hust.openatom.club/assets/logo.png)](https://hust.openatom.club)
```

!!! warning

	在插入图片时，我们必须保证该链接**可以被外界访问**，这意味着你的图片必须满足以下条件之一

	1. 图片必须作为附件随markdown文件上传，且路径为相对路径（如`assets/img.jpg`）
	2. 图片上传到了互联网可访问的托管服务

	有关插入图片的更多用法，请参考第二节

## 6. 引用

使用`>`表示引用。

```markdown
> 这是一个引用
```
> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## 7. 代码

- 行内代码：用反引号包裹，如 `` `代码` ``
- 代码块：用三个反引号包裹。通常来说，Markdown 编辑器能自动识别代码语言并高亮；但当遇到识别错误时，我们可以使用` ```<语言名称> `来告诉编辑器。


```python
print("Hello, Markdown!")
```


## 8. 表格

```markdown
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

	通常来说，手工实现的markdown表格在源文件中不甚美观。因此，我们可以使用[Markdown表格生成器](https://www.tablesgenerator.com/markdown_tables)来生成一个表格

## 9. 分割线

使用三个及以上的`-`、`*`或`_`

```markdown
---
```

---
!!! question

	尝试完成最终效果如下的Markdown文件

	# 这是标题
	## 这也是一个标题

	> 这是引用

	[![这是图片](https://oss.hust.openatom.club/assets/logo.png)](https://oss.hust.openatom.club/)

	*图片的链接为 `https://oss.hust.openatom.club/assets/logo.png`，打开后跳转到`https://oss.hust.openatom.club/`*

	[这是链接](https://oss.hust.openatom.club/)

	---

	这里是下一页！

	```cpp
	// 这是一段C++代码，我们通常使用cpp表示C++
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

以上是 Markdown 的常用基础语法，更多高级用法可参考[Markdown 官方文档](https://markdown.com.cn/basic-syntax/)。