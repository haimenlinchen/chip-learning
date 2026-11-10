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

性能模型（performance model，用抽象层次预测芯片性能；服务于设计探索与软件调优）用可接受的抽象精度预测芯片行为，用于设计空间探索（DSE，Design Space Exploration，扫描参数组合寻找最优配置；如 warp 数/cache 大小）、软件调优和回归门禁。

## 模型类型

| 类型 | 代表 | 精度 | 速度 |
|---|---|---|---|
| 解析模型（analytical model，用公式而非仿真估计性能；如 roofline） | roofline（性能上界模型，用算力/带宽比判断瓶颈在计算还是访存） | 低 | 极快 |
| 周期近似（cycle-approximate，粗略建模周期数；比 RTL 快但精度有限） | Vortex simx | 中 | 快 |
| 周期精确（cycle-accurate，逐周期还原时序；最准但最慢） | RTL/Verilator | 高 | 慢 |
| 黄金 ISS（Instruction Set Simulator，指令集模拟器；快速跑软件、验证 ISA 行为） | Spike/MPACT | ISA 级 | 快 |

## 关键方法

- **roofline**：用峰值算力/带宽判断 kernel（GPU/NPU 上执行的计算任务；性能分析的基本单位）是 compute-bound（计算受限，算力先于带宽成为瓶颈；优化方向是减少运算或提高利用率）还是 memory-bound（访存受限，带宽先于算力成为瓶颈；优化方向是数据复用与合并访问）。
- **parity gate**（一致性门禁，模型与 RTL 的退休指令/周期需对齐；防止模型漂移）：模型与 RTL 的退休指令/周期对比，防止模型漂移。
- **counter/trace**：IPC（Instructions Per Cycle，每周期退休指令数；衡量流水线吞吐）、cache miss、带宽、occupancy（占用率，活跃 warp/线程占硬件上限的比例；影响延迟隐藏）、stall reason（停顿原因，定位流水线/访存瓶颈）。
- **设计空间探索**：扫 warps/threads/cache size/issue width。
- **基线管理**：perf baseline 作为 golden data，变更需解释。

## 在项目中的体现

- [[Vortex]]：simx + roofline + perf gate；`ci/roofline.py`。
- [[CoralNPU]]：MPACT/Spike 作为参考模型；RVVI trace。
- [[ASIC-Cosim]]：C-model 用于功能/性能快速迭代。
- [[Clounix-SDK]]：统计/计数器/diag shell 提供运行时可观测性。

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| 性能模型 | 用抽象层次预测芯片性能 | 设计探索、软件调优 | 精度与速度需按用途权衡 |
| 设计空间探索 | 扫描参数组合寻找最优配置 | 微架构选型 | 参数维度过高时需采样或解析模型 |
| 解析模型 | 用公式估计性能 | 早期评估 | 快但忽略大量微架构细节 |
| roofline | 用算力/带宽比判断瓶颈 | kernel 分析 | 上界模型，不代表实际可达性能 |
| 周期近似 | 粗略建模周期数 | 快速迭代 | 在复杂交互下容易失真 |
| 周期精确 | 逐周期还原时序 | 微架构验证 | 最准但速度最慢 |
| ISS | 指令集模拟器 | 软件 bring-up | 不建模周期，但可作功能对照 |
| kernel | GPU/NPU 上执行的计算任务 | 性能分析 | 优化通常从热点 kernel 开始 |
| compute-bound | 算力先于带宽成为瓶颈 | 提升利用率 | 与 memory-bound 是 roofline 的两侧 |
| memory-bound | 带宽先于算力成为瓶颈 | 数据复用、合并访问 | 提高算术强度可跨过拐点 |
| parity gate | 模型与 RTL 的指标对齐门禁 | 防止模型漂移 | 容差设定过宽会失去意义 |
| IPC | 每周期退休指令数 | 流水线吞吐 | 受 issue width 与停顿共同限制 |
| occupancy | 活跃 warp/线程占上限比例 | GPU 延迟隐藏 | 过高可能增加资源争用 |
| stall reason | 停顿原因计数 | 瓶颈定位 | 需与 IPC、miss 率联合解读 |

## 自检问题

- 周期近似模型在哪些情况下会失真？
- 如何避免“为了过 gate 而放宽容差”？
- roofline 的峰值算力/带宽如何选？
- 性能回归与功能回归如何解耦？

## 相关概念

- [[Verification-Fidelity]]
- [[Cache-and-Memory]]
- [[SIMT-and-Warp]]
