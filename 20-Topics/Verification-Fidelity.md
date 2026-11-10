---
type: atomic
layer: verification
topic: [verification, cosim, fidelity, parity]
status: learning
tags:
  - layer/verification
  - topic/cosim
created: 2026-11-10
---

# 验证与保真度

## 定义

芯片验证是在“模型速度”和“模型保真度”之间做取舍：便宜的模型跑回归，贵的模型抓 bug，黄金模型做对照。

## 保真度光谱

| 层级 | 例子 | 速度 | 能发现的问题 |
|---|---|---|---|
| 功能模型 | asic-cosim CMODEL、Vortex simx | 快 | 功能/协议/表项/包转发 |
| 指令集模拟 | CoralNPU MPACT/Spike | 快 | ISA/软件行为 |
| RTL 仿真 | Verilator/VCS、rtlsim | 慢 | 周期/时序/微架构 |
| 硬件仿真 | EMU/FPGA | 中 | 内核/PCIe/中断/驱动 |
| 真实硅 | LAB/芯片 | 真实 | 模拟/物理/系统集成 |

## 常见对照手段

- **lockstep / parity**：同一程序在模型与 RTL 上逐指令/逐周期对比。
- **三方 cosim**：RTL vs 两个独立黄金模型（CoralNPU：RTL/MPACT/Spike）。
- **事务检查**：LSU 读写、寄存器、包内容逐笔比对。
- **性能 baseline**：周期/带宽/面积回归门禁（Vortex：perf/synthesis gate）。

## 在项目中的体现

- [[CoralNPU-Verification]]：cocotb/UVM/三方 cosim/RVVI/ISG。
- [[Vortex]]：simx ↔ rtlsim parity、perf/synthesis baseline。
- [[ASIC-Cosim-Five-Backends]]：CMODEL/EMU/RTL/LAB/NOMODEL。
- [[Clounix-SDK]]：mock + asicsim，等价性依赖 cosim。

## 自检问题

- 同一测试在不同保真度后端上分别能发现什么？
- 如何定义一个可自动化的 parity gate？
- 黄金模型本身错了怎么办？
- 性能回归门禁与功能回归门禁如何分离？

## 相关概念

- [[Performance-Modeling]]
- [[Software-Interface]]
