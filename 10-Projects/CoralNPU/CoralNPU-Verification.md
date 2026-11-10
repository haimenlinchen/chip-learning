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

CoralNPU 的验证覆盖 RTL、网表与黄金模型：cocotb + UVM + Verilator/SystemC + VCS，并有 RTL/MPACT/Spike 三方 cosim 与 RVVI lockstep。

## 如何工作

- **cocotb**：Python 驱动 RTL/网表仿真，覆盖 ISA、CSR、异常、RVV、VME、DMA、PLIC 等。
- **UVM**：面向 `RvvCoreMiniVerificationAxi`/`VmeCoreMiniVerificationAxi` 的 UVM 环境，AXI master/slave + IRQ。
- **仿真器**：Verilator（默认）、VCS（`--config=vcs`）。
- **三方 cosim**：RTL vs MPACT vs Spike，默认开启 LSU 读写事务检查。
- **RVVI**：lockstep 指令 trace，对比 RTL 与参考模型。
- **ISG**：指令流生成器，随机生成测试程序；另有 riscv-dv。
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

## 来源

- `tests/cocotb/README.md`
- `tests/uvm/README.md`
- `tests/isg/`
