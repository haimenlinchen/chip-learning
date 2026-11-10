---
type: index
aliases: [Code-Reading Index]
tags:
  - type/index
created: 2026-11-10
---

# Code-Reading

放“逐文件/逐模块”的代码阅读笔记。

建议命名：

```text
<Project>-<Module>-<Topic>.md
例：CoralNPU-RVV-Decode.md
    Vortex-Cache-MissPath.md
```

模板：`Templates/Code-Reading.md`

Frontmatter 至少包含：

```yaml
type: code-reading
project: CoralNPU
file: hdl/chisel/src/coralnpu/scalar/SCore.scala
commit: <hash>
status: learning
```
