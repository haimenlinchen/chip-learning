---
type: atomic
layer: performance
topic: [performance, simx, roofline, profiling]
status: learning
tags:
  - layer/performance
  - topic/performance
created: 2026-11-10
---

# 性能建模

## 定义

性能模型用可接受的抽象精度预测芯片行为，用于设计空间探索、软件调优和回归门禁。

## 模型类型

| 类型 | 代表 | 精度 | 速度 |
|---|---|---|---|
| 解析模型 | roofline | 低 | 极快 |
| 周期近似 | Vortex simx | 中 | 快 |
| 周期精确 | RTL/Verilator | 高 | 慢 |
| 黄金 ISS | Spike/MPACT | ISA 级 | 快 |

## 关键方法

- **roofline**：用峰值算力/带宽判断 kernel 是 compute-bound 还是 memory-bound。
- **parity gate**：模型与 RTL 的退休指令/周期对比，防止模型漂移。
- **counter/trace**：IPC、cache miss、带宽、occupancy、stall reason。
- **设计空间探索**：扫 warps/threads/cache size/issue width。
- **基线管理**：perf baseline 作为 golden data，变更需解释。

## 在项目中的体现

- [[Vortex]]：simx + roofline + perf gate；`ci/roofline.py`。
- [[CoralNPU]]：MPACT/Spike 作为参考模型；RVVI trace。
- [[ASIC-Cosim]]：C-model 用于功能/性能快速迭代。
- [[Clounix-SDK]]：统计/计数器/diag shell 提供运行时可观测性。

## 自检问题

- 周期近似模型在哪些情况下会失真？
- 如何避免“为了过 gate 而放宽容差”？
- roofline 的峰值算力/带宽如何选？
- 性能回归与功能回归如何解耦？

## 相关概念

- [[Verification-Fidelity]]
- [[Cache-and-Memory]]
- [[SIMT-and-Warp]]
