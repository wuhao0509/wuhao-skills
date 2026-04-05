# 转换示例

## 示例 1：大纲与标题

**Logseq 输入：**
```
- # 一、浏览器模块化存在的问题
	- 效率问题：精细的模块划分...
	- 兼容性问题：...
```

**Obsidian 输出：**
```markdown
## 一、浏览器模块化存在的问题
  - 效率问题：精细的模块划分...
  - 兼容性问题：...
```

## 示例 2：块引用

**Logseq 输入：**
```
- vdom如何生成
  - ((66c9da55-0766-452f-94ce-52e29d13112b))
```

**Obsidian 输出：**（当前文件名为「一 Vue框架设计.md」）
```markdown
- vdom如何生成
  - [[一 Vue框架设计#^66c9da55-0766-452f-94ce-52e29d13112b]]
```

## 示例 3：任务与属性

**Logseq 输入：**
```
- DONE [nextTick 实现原理](https://...)
- TODO 这里的 Watcher 是不是就是 track 函数
  id:: 66cc726b-e813-423f-bc72-43dfa689c1d9
```

**Obsidian 输出：**
```markdown
- [x] [nextTick 实现原理](https://...)
- [ ] 这里的 Watcher 是不是就是 track 函数
```
