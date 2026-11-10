---
type: index
aliases: [Code-Reading Index]
tags:
  - type/index
created: 2026-11-10
---

# Code-Reading

放“逐文件/逐模块”的代码阅读笔记（Code-Reading：按文件/模块逐层理解实现；用于把 RTL 与文档对应起来）。

建议命名：

```text
<Project>-<Module>-<Topic>.md
例：CoralNPU-RVV-Decode.md
    Vortex-Cache-MissPath.md
```

模板（可复用的笔记骨架；用于统一 code-reading 记录格式）：`Templates/Code-Reading.md`

Frontmatter（Obsidian 笔记顶部的 YAML 元数据；用于分类、筛选与 dataview 查询）至少包含：

```yaml
type: code-reading
project: CoralNPU
file: hdl/chisel/src/coralnpu/scalar/SCore.scala
commit: <hash>
status: learning
```
