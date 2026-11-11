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
| [[Stage-0-tiny-gpu]] | GPU 热身（可选） | tiny-gpu（约 1.3k 行 RTL 的教学 GPU；用于补齐 Verilog 与 SIMT 基础） | 跑通两个 kernel 并加一条指令 |
| [[Stage-1-Scalar-Core]] | 单核流水线 | CoralNPU（开源 RISC-V 边缘 NPU IP；用于入门标量核与验证） | 讲清一条指令从取指到退休 |
| [[Stage-2-RVV-VME]] | RVV（RISC-V Vector Extension，向量扩展；用于向量/矩阵计算） / 矩阵 | CoralNPU | 理解解耦执行与 tile 数据流 |
| [[Stage-3-GPU]] | SIMT（单指令多线程；GPU 线程执行模型） / GPU | Vortex（开源 RISC-V GPGPU 全栈；用于 GPU 进阶） | 理解 warp、cache、TCU |
| [[Stage-4-Verification]] | 验证方法学 | CoralNPU + ASIC-Cosim（交换 ASIC 协同仿真平台；用于多后端对比） | 理解保真度（模型与硬件行为的一致程度；用于速度与精度取舍） vs 速度 |
| [[Stage-5-SDK]] | 软硬件接口 | Clounix-SDK（交换 ASIC 软件开发包；用于软硬件接口学习） | 理解 API → HAL（硬件抽象层；屏蔽底层寄存器/表项差异） → 表项 |

## 未完成阶段

```dataview
LIST
FROM "30-Learning"
WHERE status != "done"
SORT stage ASC
```

## 总路线

- [[Roadmap]]
