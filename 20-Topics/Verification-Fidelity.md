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

芯片验证是在“模型速度”和“模型保真度”（fidelity，模型对真实硬件行为的逼近程度；越高越慢）之间做取舍：便宜的模型跑回归（regression，重复运行大量测试防止功能退化；验证门禁手段），贵的模型抓 bug，黄金模型（golden model，作为正确性基准的参考模型；用于与 RTL 对照）做对照。

## 保真度光谱

| 层级 | 例子 | 速度 | 能发现的问题 |
|---|---|---|---|
| 功能模型 | asic-cosim CMODEL（C/C++ 功能模型，快速模拟芯片行为；常作黄金模型或软件原型）、Vortex simx | 快 | 功能/协议/表项/包转发 |
| 指令集模拟（ISS，Instruction Set Simulator，指令级模拟器；快速验证软件与 ISA 行为） | CoralNPU MPACT/Spike | 快 | ISA/软件行为 |
| RTL（Register Transfer Level，寄存器传输级硬件描述；可综合、可精确仿真）仿真 | Verilator/VCS、rtlsim | 慢 | 周期/时序/微架构 |
| 硬件仿真（emulation，用 FPGA/专用硬件逼近真实芯片；可跑驱动与系统软件） | EMU/FPGA（Field-Programmable Gate Array，可编程逻辑阵列；用于原型验证） | 中 | 内核/PCIe/中断/驱动 |
| 真实硅 | LAB/芯片 | 真实 | 模拟/物理/系统集成 |

## 常见对照手段

- **lockstep / parity**（lockstep 锁步对比：模型与 RTL 同步执行并逐指令/逐周期比对，偏差立即报错；parity 一致性对照：两个实现的输出需逐笔相同）：同一程序在模型与 RTL 上逐指令/逐周期对比。
- **三方 cosim**（co-simulation，协同仿真；让不同抽象级的模型一起跑并互相比对）：RTL vs 两个独立黄金模型（CoralNPU：RTL/MPACT/Spike）。
- **事务检查**：LSU（Load-Store Unit，访存单元；负责读写内存与地址翻译）读写、寄存器、包内容逐笔比对。
- **性能 baseline**：周期/带宽/面积回归门禁（Vortex：perf/synthesis gate）。

## 在项目中的体现

- [[CoralNPU-Verification]]：cocotb（用 Python 写 RTL 测试平台的框架；便于快速搭验证环境）/UVM（Universal Verification Methodology，SystemVerilog 验证方法学；标准化测试平台）/三方 cosim/RVVI/ISG。
- [[Vortex]]：simx ↔ rtlsim parity、perf/synthesis baseline。
- [[ASIC-Cosim-Five-Backends]]：CMODEL/EMU/RTL/LAB/NOMODEL。
- [[Clounix-SDK]]：mock + asicsim，等价性依赖 cosim。

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| 保真度 | 模型逼近真实硬件的程度 | 选择验证手段 | 保真度与速度通常此消彼长 |
| 回归 | 重复运行大量测试防退化 | CI、发布门禁 | 用例覆盖比数量更重要 |
| 黄金模型 | 作为正确性基准的参考模型 | 与 RTL 对照 | 黄金模型自身也可能有 bug |
| CMODEL | C/C++ 功能模型 | 软件原型、黄金模型 | 快但通常不建模周期细节 |
| ISS | 指令集模拟器 | 软件 bring-up、ISA 验证 | 适合跑大程序，但不反映微架构 |
| RTL | 寄存器传输级硬件描述 | 综合、精确仿真 | 周期/时序信息最完整 |
| 硬件仿真 | 用 FPGA/专用硬件逼近芯片 | 驱动、系统集成 | 速度介于 RTL 与硅之间 |
| FPGA | 可编程逻辑阵列 | 原型验证 | 可重配置，但容量受限 |
| lockstep | 模型与 RTL 锁步逐指令/周期比对 | 发现功能偏差 | 需要精确的同步点 |
| parity | 两个实现输出逐笔相同 | cosim 门禁 | 与 lockstep 常配合使用 |
| cosim | 不同抽象级模型协同仿真 | 三方对照 | 关键是统一激励与检查点 |
| LSU | 访存单元 | 地址翻译、读写通路 | 事务级检查常以 LSU 为观察点 |
| cocotb | Python 写 RTL 测试平台的框架 | 快速搭验证环境 | 与 UVM 可并存，偏轻量 |
| UVM | SystemVerilog 验证方法学 | 大型 IP/SoC 验证 | 标准化组件复用性好 |

## 自检问题

- 同一测试在不同保真度后端上分别能发现什么？
- 如何定义一个可自动化的 parity gate？
- 黄金模型本身错了怎么办？
- 性能回归门禁与功能回归门禁如何分离？

## 相关概念

- [[Performance-Modeling]]
- [[Software-Interface]]
