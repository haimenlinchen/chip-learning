---
type: synthesis
aliases: [验证保真度光谱, Verification Fidelity]
tags:
  - type/synthesis
  - layer/verification
created: 2026-11-10
---

# 验证保真度光谱

## 三种项目的对照

| 项目 | 快模型 | 中间层 | 准模型 | 真实环境 |
|---|---|---|---|---|
| **Vortex** | simx（C++ 周期近似） | — | rtlsim（Verilator） | FPGA/PCIe |
| **CoralNPU** | Verilator/cocotb、MPACT、Spike | UVM | RTL 三方 cosim | 硅后/板级 |
| **ASIC-Cosim** | CMODEL | EMU | RTL DPI | LAB |

## 共同规律

1. **便宜模型跑回归**：功能、协议、表项、包转发。
2. **贵模型抓 bug**：周期、时序、微架构、信号。
3. **黄金模型做对照**：Spike/MPACT/独立 ISS，防“自洽但错误”。
4. **真实环境兜底**：EMU/LAB/FPGA 暴露驱动、PCIe、模拟前端问题。

## 三种等价性机制

| 机制 | 代表 | 比较对象 |
|---|---|---|
| **lockstep / parity** | Vortex simx ↔ rtlsim | 退休指令完全一致、周期 ±5% |
| **三方 cosim** | CoralNPU RTL/MPACT/Spike | 指令流、LSU 事务、寄存器 |
| **跨后端用例** | ASIC-Cosim CMODEL/RTL/LAB | 包、寄存器、表项、日志 |

## 可落地的 parity gate

```text
同一测试用例
  ├─ 跑 CMODEL：记录寄存器/表项/包/周期
  ├─ 跑 RTL：记录同样的观测点
  ├─ 逐项比对：寄存器、表项、包内容、事务顺序
  └─ 周期只在容差内比较，不要求完全一致
```

## 关键问题

- 比较点选在哪里：架构寄存器、表项、包、事务、周期？
- 容差如何设定，避免“为了过 gate 而放宽容差”？
- 黄金模型本身错了怎么办？
- 功能回归与性能回归如何解耦？

## 相关

- [[Verification-Fidelity]]
- [[CoralNPU-Verification]]
- [[ASIC-Cosim-Five-Backends]]
- [[Performance-Modeling]]
