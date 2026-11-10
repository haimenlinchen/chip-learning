---
type: index
aliases: [Code-Reading Index]
tags:
  - type/index
created: 2026-11-10
---

# Code-Reading

放“逐文件/逐模块”的代码阅读笔记（Code-Reading：按文件/模块逐层理解实现；用于把 RTL 与文档对应起来）。

## 路线总览

先按项目 Hub 的“代码阅读路线”走一遍，再为卡住的模块建单独的 code-reading 笔记。路线按“文档 → 顶层接线 → 单条指令/调用链 → 子系统 → 验证”组织。

| 项目 | 路线入口 | 对应阶段 | 一句话读法 |
|---|---|---|---|
| CoralNPU | [[CoralNPU#代码阅读路线]] | [[Stage-1-Scalar-Core]]、[[Stage-2-RVV-VME]] | `Core.scala` → `SCore.scala` → 单条指令 → RVV/VME |
| Vortex | [[Vortex#代码阅读路线]] | [[Stage-3-GPU]] | 一个 warp 的生命周期 → 存储 → TCU/DXA → simx 对照 |
| ASIC-Cosim | [[ASIC-Cosim#代码阅读路线]] | [[Stage-4-Verification]] | 五后端入口 → 统一访问口 → 单后端 → 流水线模型 |
| Clounix-SDK | [[Clounix-SDK#代码阅读路线]] | [[Stage-5-SDK]] | `clx_l2_addr_add` 一条链 → TOB → DRV → OSAL |

路线只写顺序与自检问题；每个文件的细节仍记在单独的 code-reading 笔记里。

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
