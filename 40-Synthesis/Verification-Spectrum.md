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
| **Vortex** | simx（C++ 周期近似）（Vortex 的周期近似模拟器；用于快速性能与功能评估） | — | rtlsim（Verilator）（周期精确的 RTL 仿真；用于验证微架构与流水线） | FPGA/PCIe |
| **CoralNPU** | Verilator/cocotb（Python 驱动的 RTL 仿真框架；用于模块级功能验证）、MPACT（CoralNPU 的参考模型；用于与 RTL 对照）、Spike（RISC-V 官方指令集模拟器；用作黄金参考） | UVM（通用验证方法学，SystemVerilog 验证框架；用于随机激励与覆盖率驱动验证） | RTL 三方 cosim（协同仿真，多个模型同步运行并比对；用于发现模型与 RTL 的偏差） | 硅后/板级 |
| **ASIC-Cosim** | CMODEL（C/C++ 行为级参考模型；用于软件提前开发与结果对照） | EMU（硬件仿真加速器；用于大规模系统与软件验证） | RTL DPI（直接编程接口，连接 SystemVerilog 与 C/C++；用于 cosim 与参考模型集成） | LAB |

## 共同规律

1. **便宜模型跑回归**：功能、协议、表项、包转发。
2. **贵模型抓 bug**：周期、时序、微架构、信号。
3. **黄金模型做对照**：Spike/MPACT/独立 ISS，防“自洽但错误”。
4. **真实环境兜底**：EMU/LAB/FPGA 暴露驱动、PCIe、模拟前端问题。

## 三种等价性机制

| 机制 | 代表 | 比较对象 |
|---|---|---|
| **lockstep（锁步比对，参考与实现逐指令同步；用于定位偏差） / parity（一致性比对；用于回归门禁）** | Vortex simx ↔ rtlsim | 退休指令完全一致、周期 ±5% |
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

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| simx | Vortex 的 C++ 周期近似模拟器 | 快速性能与功能评估 | 速度远高于 RTL，适合大范围配置扫描 |
| rtlsim | 周期精确的 RTL 仿真 | 验证微架构与流水线 | 通常用 Verilator 编译，兼顾速度与周期准确性 |
| cocotb | Python 驱动的 RTL 仿真框架 | 模块级功能验证 | 与 UVM 互补：一个轻量，一个重方法学 |
| MPACT | CoralNPU 的参考模型 | 与 RTL 对照 | 参考模型跑得快，但要防止与 RTL 同源错误 |
| Spike | RISC-V 官方指令集模拟器 | 黄金参考 | 适合做指令流与架构状态的独立对照 |
| UVM | 通用验证方法学 | 随机激励与覆盖率驱动验证 | 适合芯片级 TB 复用与覆盖率收敛 |
| cosim | 协同仿真 | 发现模型与 RTL 的偏差 | 三方 cosim 能更快定位是哪一方出错 |
| CMODEL | C/C++ 行为级参考模型 | 软件提前开发与结果对照 | 最便宜、最快，但保真度最低 |
| EMU | 硬件仿真加速器 | 大规模系统与软件验证 | 能跑驱动、PCIe 与系统软件，介于 RTL 与 LAB 之间 |
| DPI | 直接编程接口 | cosim 与参考模型集成 | 把 C/C++ 模型接入 SystemVerilog 仿真的标准手段 |
| lockstep | 锁步比对 | 定位偏差 | 逐指令同步，偏差出现处即嫌疑点 |
| parity | 一致性比对 | 回归门禁 | 通常允许周期容差，但要求架构状态一致 |

## 相关

- [[Verification-Fidelity]]
- [[CoralNPU-Verification]]
- [[ASIC-Cosim-Five-Backends]]
- [[Performance-Modeling]]
