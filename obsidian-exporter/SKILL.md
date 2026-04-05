---
name: obsidian-exporter
description: 将 Cursor/对话/会话内容整理为可分享的 Obsidian Markdown 技术文章（含 YAML Frontmatter、章节模板与文件命名）。当用户要「导出到 Obsidian」「保存为笔记」「Obsidian 格式」「整理成笔记/文章」「整理聊天记录成文」「把对话写成博客/长文」「export to obsidian」或需要一篇结构完整、可对外发布的 Markdown 而非碎片笔记时，应优先使用本技能。
triggers:
  - "导出到 obsidian"
  - "保存为笔记"
  - "obsidian 格式"
  - "整理成笔记"
  - "export to obsidian"
  - "生成文章"
  - "整理成文章"
  - "整理聊天记录"
  - "cursor chat"
  - "会话导出"
  - "博客稿"
---

# Obsidian 技术文章写作规范

> **定位说明**：本规范用于生成**可分享的技术文章**，而非个人知识卡片。文章应具备完整的叙事结构、清晰的逻辑脉络，让读者能够独立理解并获得价值。

## 导出执行流程

当用户请求导出文章时，按以下流程执行：

### 1. 确定目标路径

**路径选择逻辑：**

| 用户意图 | 处理方式 |
|---------|---------|
| 用户明确指定了路径 | 直接使用用户指定的路径 |
| 用户说"指定文件夹"、"选择位置"、"另存为"等 | 调起系统文件夹选择对话框 |
| 用户未提及路径 | 若工作区存在可解析的 `.cursor-obsidian.json`，使用其中 `vaultPath` + `notesSubdir`；否则保存到下方「默认导出路径」 |

**默认导出路径**：`/Users/guoyiding/Desktop/Obsidian仓库/Cursor Chat`

> [!TIP] 快速导出
> 大多数情况下，用户无需关心保存位置，直接使用默认路径即可。如需更改位置，说"指定文件夹"即可调起选择对话框。

#### 系统文件选择弹窗实现

**macOS（使用 osascript）：**

```bash
# 需要 required_permissions: ["all"] 来绕过沙盒限制
osascript -e 'POSIX path of (choose folder with prompt "选择 Obsidian Vault 保存位置" default location (POSIX file "/Users/guoyiding/Desktop/Obsidian仓库/Cursor Chat" as alias))'
```

**默认打开路径**：弹窗默认打开 `/Users/guoyiding/Desktop/Obsidian仓库/Cursor Chat` 文件夹，用户可以快速导航到常用位置。

**返回格式**：用户选定文件夹的 POSIX 路径字符串，末尾通常带 `/`，例如 `/Users/guoyiding/Desktop/Obsidian仓库/Cursor Chat/` 或用户另选的其他目录。

**用户取消处理：**
- 用户点击「取消」时，`osascript` 会返回非零退出码（如 `-128`），表示未选择目录。
- **默认策略**：视为用户放弃在本次对话中自选目录，**直接回退到上文「默认导出路径」保存**，并在回复中简短说明（例如：「已保存到默认目录 …，若需另存请再说指定文件夹」）。
- 若用户明确表示不想用默认路径、也不愿再弹窗，再通过对话请其**直接打出目标路径**，或协助创建/编辑 `.cursor-obsidian.json`（见文末配置说明）。

**跨平台约定**：以下 Windows / Linux 示例中，**初始目录**应与「**默认导出路径**」指向同一文件夹；若本机路径不同，将变量或字符串替换为当前机器的绝对路径。

**Windows（使用 PowerShell）：**

```powershell
Add-Type -AssemblyName System.Windows.Forms
$folder = New-Object System.Windows.Forms.FolderBrowserDialog
$folder.Description = "选择 Obsidian Vault 保存位置"
# 与「默认导出路径」一致，便于从常用目录开始浏览（请按本机实际路径修改）
$defaultExport = "$env:USERPROFILE\Desktop\Obsidian仓库\Cursor Chat"
if (Test-Path -LiteralPath $defaultExport) { $folder.SelectedPath = $defaultExport }
if ($folder.ShowDialog() -eq "OK") { $folder.SelectedPath }
```

**Linux（使用 zenity）：**

```bash
# --filename 为起始目录，应与「默认导出路径」一致（请按本机实际路径修改）
zenity --file-selection --directory --title="选择 Obsidian Vault 保存位置" \
  --filename="$HOME/Desktop/Obsidian仓库/Cursor Chat/"
```

### 2. 生成文章

根据本文档的规范生成文章内容：
- 按文章结构模板组织内容
- 使用正确的 YAML Frontmatter
- 遵循叙事技巧和内容提炼原则

### 3. 保存并反馈

- 将文件保存到确定的目标路径
- 文件名格式：`YYYY-MM-DD <描述性标题>.md`
- 向用户反馈保存位置和文章概览

## YAML Frontmatter 标准字段

```yaml
---
title: 文章标题
date: YYYY-MM-DD
description: 一句话摘要（用于 SEO 和社交分享预览）
tags:
  - article
  - <技术领域标签>
  - <主题标签>
author: <作者名>
reading_time: <预估阅读时长，如 8 min>
source: Cursor Agent
project: <项目名>
status: draft | published
---
```

**标签命名规范：**
- 使用小写字母和连字符（`machine-learning`，不用 `MachineLearning`）
- 类型标签（必选）：`article`、`tutorial`、`case-study`、`deep-dive`、`quick-tip`
- 技术栈标签：`python`、`typescript`、`react`、`rust`、`docker` 等
- 领域标签：`backend`、`frontend`、`devops`、`ai`、`database`

## 文章结构模板

### 推荐结构

```markdown
# 标题：用一句话说清楚文章价值

## 引言（钩子）
- 用一个具体场景或问题开场
- 激发读者兴趣，说明"为什么要读这篇文章"
- 给出文章路线图，让读者知道接下来会学到什么

## 背景与问题
- 交代必要的上下文
- 明确问题的边界和约束
- 解释为什么现有方案不理想

## 核心内容
### 概念解释
### 实现细节
### 代码示例

## 实践应用
- 完整的可运行示例
- 常见问题和解决方案
- 性能考量或最佳实践

## 总结
- 回顾要点
- 指出局限性
- 提供延伸阅读方向

## 参考资料
- 相关链接
- 进一步学习资源
```

### 标题层级规范
- `#` 一级标题：文章标题（唯一，需吸引眼球且准确）
- `##` 二级标题：主要章节（每个章节应该有明确的主题）
- `###` 三级标题：章节内的细分主题
- `####` 四级标题：必要时使用，但应尽量避免层级过深

### 标题写作原则

**好的标题：**
- `如何用 Rust 实现一个高性能 JSON 解析器`
- `从崩溃到稳定：一次生产环境内存泄漏排查实录`
- `别再用 if-else 了：策略模式在业务代码中的正确打开方式`

**避免的标题：**
- `关于 Python 异步 IO 的笔记`（太模糊，没有价值承诺）
- `今天学到的 Docker 知识`（没有明确的收获预期）
- `Vue3 学习记录`（像是私人日志，不是可分享的文章）

## 叙事技巧

### 开头（Hook）的几种方式

1. **场景代入**
   > 上周，我们的 API 响应时间突然从 200ms 飙升到 5 秒，用户投诉电话打爆了客服……

2. **数据震撼**
   > 仅仅一个索引优化，查询性能提升了 47 倍。这不是魔法，只是理解了数据库索引的底层原理。

3. **痛点共鸣**
   > 你是否也遇到过这种情况：代码跑得好好的，一到生产环境就出各种诡异问题？

4. **认知反差**
   > 很多人以为 async/await 就是多线程，这其实是一个常见的误解……

### 内容组织原则

1. **渐进式展开**：从简单到复杂，让读者逐步建立理解
2. **问题驱动**：先抛出问题，再给出解决方案
3. **代码即文档**：代码示例应该完整可运行，而非片段
4. **对比说明**：通过"改进前/改进后"的对比突出价值
5. **图表辅助**：复杂概念考虑用 Mermaid 图表说明

### Wikilink 使用规范

适度使用 `[[相关笔记]]` 建立知识网络：
- 链接到**相关主题的深入文章**
- 链接到**前置知识文章**（如"阅读本文前建议先了解 [[X]]"）
- 避免过度链接，保持阅读流畅性

示例：`[[Rust 所有权机制]]`、`[[React Hooks 最佳实践]]`

## 代码块规范

### 必须标注语言

````markdown
```python
# 完整的、可运行的代码示例
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```
````

### 代码示例原则

1. **完整性**：代码应该是完整可运行的，而非零散片段
2. **注释适度**：只在非显而易见处添加注释
3. **命名清晰**：变量和函数名要有意义
4. **渐进复杂**：从最简单的例子开始，逐步增加复杂度

### 代码块与正文的关系

```markdown
在介绍完概念后，我们来看一个简单的例子：

```python
# 示例代码
```

上面的代码展示了……（解释代码的关键点）
```

**不要**把代码块孤立放置，每个代码块前后都应该有文字引导和解释。

## Callout 块使用指南

适当使用 Obsidian callout 增强可读性：

```markdown
> [!TIP] 实用技巧
> 这里分享一个小窍门……

> [!WARNING] 常见陷阱
> 这个错误我犯过很多次，希望你避免……

> [!NOTE] 深入理解
> 如果你想深入了解背后的原理……

> [!IMPORTANT] 关键结论
> 这是本文最重要的一个结论……
```

**使用原则**：
- 每篇文章 callout 数量控制在 3-5 个
- 只用于真正重要或容易被忽视的内容
- 不要让 callout 成为主体内容的替代

## 文件命名规则

格式：`YYYY-MM-DD <描述性标题>.md`

**好的文件名：**
- `2026-03-18 从零实现一个 Promise.md`
- `2026-03-18 生产环境内存泄漏排查实录.md`
- `2026-03-18 为什么你应该用 TypeScript.md`

**避免：**
- 过长标题（超过 60 字符）
- 特殊字符（`/`、`:`、`*`、`?`、`"`）
- 过于模糊的标题（如"笔记"、"学习记录"）

## 内容提炼原则

### 从会话到文章的转换

1. **确定主题**：从对话中提炼出核心主题和价值点
2. **重新组织**：按文章结构重组内容，而非按对话顺序
3. **补充背景**：添加必要的背景说明，让读者无需上下文也能理解
4. **删除冗余**：去除来回确认、试错过程、无关讨论
5. **强化叙事**：加入过渡句、小结、引导语
6. **完善示例**：确保代码示例完整、可运行

### 质量检查清单

- [ ] 标题是否清晰表达了文章价值？
- [ ] 开头是否能吸引读者继续阅读？
- [ ] 内容是否有清晰的结构和逻辑脉络？
- [ ] 代码示例是否完整可运行？
- [ ] 是否有足够的解释引导代码块？
- [ ] 结尾是否有总结和延伸方向？
- [ ] 通读一遍，是否流畅易读？

### 避免的问题

- ❌ 知识点罗列式写作（"X 是什么，Y 是什么，Z 是什么"）
- ❌ 缺乏背景的代码堆砌
- ❌ 过多的假设（"读者应该已经知道……"）
- ❌ 没有结论的开放式结尾
- ❌ 私人日记风格的表述（"今天我学到了……"）

## 配置文件格式（.cursor-obsidian.json）

**与默认导出路径的关系（必读）：**

- 本技能**默认**将文章保存到上文「**默认导出路径**」；用户若在对话里**明确写了别的路径**，以用户路径为准。
- `.cursor-obsidian.json` 为**可选**：若工作区存在该文件，且用户**既未口述路径、也未要求弹窗选文件夹**，可将 `vaultPath` + `notesSubdir` 解析为保存目录，**覆盖**技能内写的默认导出路径（便于多机器或多 Vault 时统一配置）。
- 若不存在配置文件或解析失败，继续沿用技能中的「默认导出路径」。

```json
{
  "vaultPath": "~/Documents/MyVault",
  "notesSubdir": "Articles",
  "defaultTags": ["article"],
  "dateFormat": "YYYY-MM-DD",
  "author": "<默认作者名>",
  "includeReadingTime": true
}
```

字段说明：
- `vaultPath`：Obsidian Vault 的绝对路径或 `~` 相对路径
- `notesSubdir`：在 Vault 内的存储子目录，默认 `Articles`
- `defaultTags`：每篇文章自动包含的标签
- `dateFormat`：日期格式，默认 `YYYY-MM-DD`
- `author`：默认作者名
- `includeReadingTime`：是否自动计算阅读时长

## 示例文章结构

```markdown
---
title: 用 Rust 重写 Python 热点代码：一次性能优化的完整记录
date: 2026-03-18
description: 记录一次通过 PyO3 将 Python 性能瓶颈代码用 Rust 重写的完整过程，性能提升 20 倍。
tags:
  - article
  - rust
  - python
  - performance
author: Your Name
reading_time: 12 min
---

# 用 Rust 重写 Python 热点代码

## 引言

上周，我们的数据分析服务响应时间从 2 秒飙升至 30 秒。排查后发现，一个简单的数据处理函数成了性能瓶颈。本文记录了用 Rust 重写这段代码的完整过程，以及踩过的所有坑。

## 问题背景

我们的服务需要处理大量 JSON 数据，核心逻辑是一个嵌套循环……

（此处展开问题分析）

## 解决方案

### 为什么选择 Rust

在考虑了 Cython、Numba、Rust 等方案后……

### 实现步骤

首先，创建一个新的 Rust 项目……

```rust
use pyo3::prelude::*;

#[pyfunction]
fn process_data(data: &str) -> PyResult<String> {
    // 实现细节
}
```

### 踩坑记录

> [!WARNING] 注意版本兼容性
> PyO3 0.20 的 API 与之前版本有较大变化，网上很多教程已经过时……

## 性能对比

重写后的性能测试结果：

| 数据规模 | Python 原版 | Rust 重写 | 提升倍数 |
|---------|------------|-----------|---------|
| 1K 条   | 2.3s       | 0.12s     | 19x     |
| 10K 条  | 23.5s      | 1.1s      | 21x     |

## 总结

通过这次优化，我们学到了……

如果想深入了解 Rust 与 Python 交互，推荐阅读 [[PyO3 入门指南]]。
```