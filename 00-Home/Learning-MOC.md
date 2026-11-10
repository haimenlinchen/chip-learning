---
type: moc
aliases: [Learning MOC, 学习阶段索引]
tags:
  - type/moc
created: 2026-11-10
---

# 学习阶段索引

| 阶段 | 主题 | 主项目 | 目标 |
|---|---|---|---|
| [[Stage-1-Scalar-Core]] | 单核流水线 | CoralNPU | 讲清一条指令从取指到退休 |
| [[Stage-2-RVV-VME]] | RVV / 矩阵 | CoralNPU | 理解解耦执行与 tile 数据流 |
| [[Stage-3-GPU]] | SIMT / GPU | Vortex | 理解 warp、cache、TCU |
| [[Stage-4-Verification]] | 验证方法学 | CoralNPU + ASIC-Cosim | 理解保真度 vs 速度 |
| [[Stage-5-SDK]] | 软硬件接口 | Clounix-SDK | 理解 API → HAL → 表项 |

## 未完成阶段

```dataview
LIST
FROM "30-Learning"
WHERE status != "done"
SORT stage ASC
```

## 总路线

- [[Roadmap]]
