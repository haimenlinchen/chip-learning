---
type: index
aliases: [Experiments Index]
tags:
  - type/index
created: 2026-11-10
---

# Experiments

放“可复现实验”记录：改参数、跑仿真、测周期、对比后端。

建议命名：

```text
<Project>-<Experiment>-<Date>.md
例：Vortex-sgemm-warps-sweep-2026-11-10.md
    CoralNPU-rvv-vstart-2026-11-15.md
```

模板：`Templates/Experiment.md`

要求：

- 记录 commit、构建配置、命令、原始输出；
- 结果与解释分开；
- 失败实验也保留，写清“为什么失败”。
