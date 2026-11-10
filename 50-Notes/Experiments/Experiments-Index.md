---
type: index
aliases: [Experiments Index]
tags:
  - type/index
created: 2026-11-10
---

# Experiments

放“可复现实验”记录：改参数、跑仿真（simulation：用模型执行 RTL/程序；用于功能与性能观察）、测周期（cycle：时钟周期数；用于衡量性能）、对比后端（backend：如 cmodel/RTL/EMU 等仿真后端；用于比较速度与精度）。

建议命名：

```text
<Project>-<Experiment>-<Date>.md
例：Vortex-sgemm-warps-sweep-2026-11-10.md
    CoralNPU-rvv-vstart-2026-11-15.md
```

模板：`Templates/Experiment.md`

要求：

- 记录 commit（Git 提交哈希；用于锁定实验代码版本）、构建配置（build config；用于复现编译选项）、命令、原始输出；
- 结果与解释分开；
- 失败实验也保留，写清“为什么失败”。
