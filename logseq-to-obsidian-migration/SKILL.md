---
name: logseq-to-obsidian-migration
description: 将 Logseq 笔记迁移到 Obsidian 格式。当用户需要将 Logseq 知识库转为 Obsidian、在两个工具之间迁移、提到 Logseq 转 Obsidian 迁移、想将笔记移到 Obsidian、有 Logseq 页面或日记需要转换、或询问 Logseq 与 Obsidian 格式差异时使用。
---

# Logseq 到 Obsidian 迁移

将 Logseq 仓库迁移到 Obsidian 的格式转换与迁移指南。

## 执行方式

1. **确认路径**：向用户确认源仓库和目标仓库路径；若未指定，使用默认路径。
2. **确认分类**：根据 `category_mapping.json` 将文件分配到对应文件夹；无法匹配的放入根目录。
3. **小范围试跑**：先转换 1–2 个文件验证效果，再批量执行。
4. **批量转换**：使用 `scripts/migrate.py` 进行批量迁移。

## 路径配置

| 项目 | 默认路径 |
|------|----------|
| Logseq 源仓库 | `/Users/guoyiding/Desktop/第二大脑` |
| Obsidian 目标仓库 | `/Users/guoyiding/Desktop/Obsidian仓库` |

**Logseq 目录结构：** `pages/`（页面）、`journals/`（日记）、`assets/`（图片）

**Obsidian 目标文件夹：**
| 文件夹 | 用途 |
|--------|------|
| `研发` | 技术学习笔记（Vue、React、Node、构建工具等） |
| `AI` | AI 相关笔记 |
| `商业` | 商业相关笔记 |
| `架构` | 架构设计笔记 |
| `日记` | 日记（对应 Logseq journals） |

## 文件分类规则

根据 `category_mapping.json` 自动匹配文件到目标文件夹：

| 分类 | 关键词 | 目标文件夹 |
|------|--------|------------|
| Vue | Vue, Vuex, Pinia, Vue-Router, Composition | `研发` |
| React | React, Redux, Hooks | `研发` |
| 构建工具 | Webpack, Rollup, Vite, Loader, Plugin, 工程化 | `研发` |
| Node | Node, Koa, Express, NPM, SSR, Serverless | `研发` |
| TypeScript | TS, TypeScript | `研发` |
| 前端基础 | HTML, CSS, JS, ES6, Canvas, Promise, Git, Shell | `研发` |
| 面试 | 面经, 面试, STAR法则, HR | `研发` |
| AI | AI, GPT, LLM | `AI` |
| 日记 | （来自 journals 目录） | `日记` |

**匹配规则：**
- 按文件名中的关键词匹配，匹配成功即停止
- 无法匹配的文件放入根目录
- 日记文件从 `journals/` 目录迁移到 `日记/`

## 格式转换规则

### 1. 大纲转标准 Markdown

- `- # 标题` → `## 标题`
- `- ## 标题` → `### 标题`
- 普通列表项保留 `- ` 格式
- 空行 `- ` 删除

### 2. 内部链接

- `[[页面名]]` → 保持不变
- `[[YYYY_MM_DD]]` → `[[YYYY-MM-DD]]`

### 3. 块引用

- `((uuid))` → `[[当前页面名#^uuid]]`

### 4. 任务状态

- `- TODO 内容` → `- [ ] 内容`
- `- DONE 内容` → `- [x] 内容`

### 5. 属性与高亮

- `id:: uuid` → 删除
- `[[$red]]==高亮文本==` → `==高亮文本==`

### 6. 资源路径

- `../assets/xxx.png` → `assets/xxx.png`

### 7. 日记文件

- 文件名：`2024_10_11.md` → `2024-10-11.md`
- 目标位置：`日记/2024-10-11.md`

## 迁移流程

1. **备份**：复制整个 Logseq 仓库
2. **复制 assets**：`源仓库/assets/*` → `目标仓库/assets/`
3. **分类转换页面**：根据关键词匹配，转换后放入目标文件夹
4. **转换日记**：重命名并放入 `日记/` 目录
5. **验证链接**：检查 `[[链接]]` 是否有效
6. **清理**：删除 Logseq 特有属性

## 批量迁移脚本

```bash
# 执行完整迁移
python scripts/migrate.py --source "/Users/guoyiding/Desktop/第二大脑" --target "/Users/guoyiding/Desktop/Obsidian仓库"

# 仅转换单个文件（预览模式）
python scripts/migrate.py --file "pages/Vue面经.md" --preview
```

## 配置文件

- `category_mapping.json`：分类映射配置，可自定义关键词和目标文件夹

## 注意事项

- Obsidian 不原生支持 `((uuid))` 块引用
- 转换后建议在 Obsidian 中检查双向链接
- 可通过修改 `category_mapping.json` 自定义分类规则