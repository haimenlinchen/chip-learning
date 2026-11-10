---
type: atomic
project: CoralNPU
layer: verification
topic: [cocotb, uvm, cosim, rvvi, isg]
status: learning
source_repo: /localdata/linchen/coralnpu
source_files:
  - tests/cocotb/README.md
  - tests/uvm/README.md
  - tests/isg/
tags:
  - layer/verification
  - topic/cosim
created: 2026-11-10
---

# CoralNPU 验证体系

## 定义

CoralNPU 的验证覆盖 RTL（Register Transfer Level，寄存器传输级硬件描述；用于仿真与综合的黄金参考）、网表与黄金模型：cocotb（Coroutine-based Cosimulation Testbench，Python 协程驱动的验证框架；用于 RTL/网表的用例编写） + UVM（Universal Verification Methodology，SystemVerilog 验证方法学；用于可复用验证平台） + Verilator（开源 Verilog 仿真器；用于快速 RTL 回归）/SystemC（C++ 系统级建模库；用于事务级/性能建模） + VCS（Synopsys 商业 Verilog 仿真器；用于签核级仿真），并有 RTL/MPACT（参考指令集模拟器，作为黄金模型；用于三方 cosim 对照）/Spike（RISC-V 官方指令集模拟器，作为黄金模型；用于 ISA 行为对照）三方 cosim（协同仿真，让 RTL 与参考模型同步执行同一程序；用于发现微架构与 ISA 偏差） 与 RVVI（RISC-V Verification Interface，RTL 与参考模型的指令级接口；用于 lockstep 对比） lockstep（锁步，逐指令比对 RTL 与模型状态；用于定位第一条分歧指令）。

## 如何工作

- **cocotb**：Python 驱动 RTL/网表仿真，覆盖 ISA、CSR、异常、RVV、VME、DMA、PLIC（Platform-Level Interrupt Controller，平台级中断控制器；用于中断相关用例） 等。
- **UVM**：面向 `RvvCoreMiniVerificationAxi`/`VmeCoreMiniVerificationAxi` 的 UVM 环境，AXI master/slave + IRQ。
- **仿真器**：Verilator（默认）、VCS（`--config=vcs`）。
- **三方 cosim**：RTL vs MPACT vs Spike，默认开启 LSU（加载/存储单元，执行访存事务；用于检查读写一致性） 读写事务检查。
- **RVVI**：lockstep 指令 trace，对比 RTL 与参考模型。
- **ISG**（Instruction Stream Generator，指令流生成器，随机生成合法指令序列；用于覆盖难构造的边界场景）：指令流生成器，随机生成测试程序；另有 riscv-dv。
- **调试**：`--instr_trace`（需要 verification 版 simulator）、FST 波形、`fst_query`。

## 关键细节

- 非 verification 版 simulator 的 ROB 是 `mini` 模式，不保存指令字，`--instr_trace` 会打印 0；要看反汇编必须用 verification 版。
- UVM 的 LSU 事务检查默认开启，可用 `--config=no_lsu_mem_check` 关闭。
- VME UVM 需要 `+define+ZVT_ON` 并选择 VME DUT。

## 在项目中的位置

- 所属项目：[[CoralNPU]]
- 相关子系统：[[CoralNPU-Pipeline]]、[[CoralNPU-RVV]]、[[CoralNPU-VME]]

## 相关概念

- [[Verification-Fidelity]]
- [[Performance-Modeling]]

## 自检问题

- cocotb、UVM、三方 cosim 各自能发现什么问题？
- RVVI lockstep 与普通 trace 的差别是什么？
- ISG 生成的随机程序如何保证可复现？
- 网表仿真与 RTL 仿真分别覆盖什么？

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| RTL | 寄存器传输级硬件描述 | 仿真与综合的黄金参考 | 网表仿真与 RTL 仿真覆盖不同抽象层 |
| cocotb | Python 协程驱动的验证框架 | RTL/网表的用例编写 | 与 UVM 对比：更轻量、迭代更快 |
| UVM | Universal Verification Methodology | 可复用验证平台 | 适合子系统级 AXI/IRQ 场景 |
| Verilator | 开源 Verilog 仿真器 | 快速 RTL 回归 | 默认仿真器，速度优先 |
| SystemC | C++ 系统级建模库 | 事务级/性能建模 | 可与 RTL 协同做混合仿真 |
| VCS | Synopsys 商业 Verilog 仿真器 | 签核级仿真 | 通过 --config=vcs 切换 |
| MPACT | 参考指令集模拟器 | 三方 cosim 的黄金模型之一 | 与 Spike 独立实现，降低共模错误 |
| Spike | RISC-V 官方指令集模拟器 | ISA 行为对照 | 与 MPACT 并列做三方 cosim |
| cosim | 协同仿真 | RTL 与参考模型同步执行 | 可检查指令流与 LSU 事务 |
| RVVI | RISC-V Verification Interface | 指令级 lockstep 对比 | 与普通 trace 的区别是逐指令状态比对 |
| lockstep | 锁步逐指令比对 | 定位第一条分歧指令 | 需要 verification 版 simulator |
| ISG | 指令流生成器 | 随机生成测试程序 | 与 riscv-dv 互补，注意随机种子复现 |
| LSU | 加载/存储单元 | 访存事务检查 | UVM 默认开启，可用 no_lsu_mem_check 关闭 |
| PLIC | 平台级中断控制器 | 中断相关用例 | cocotb 覆盖 PLIC，UVM 侧用 IRQ |

## 来源

- `tests/cocotb/README.md`
- `tests/uvm/README.md`
- `tests/isg/`
