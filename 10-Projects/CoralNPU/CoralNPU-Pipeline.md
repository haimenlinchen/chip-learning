---
type: atomic
project: CoralNPU
layer: microarchitecture
topic: [pipeline, scoreboard, rob]
status: learning
source_repo: /localdata/linchen/coralnpu
source_files:
  - doc/microarch/microarch.md
  - doc/microarch/dispatch.md
  - hdl/chisel/src/coralnpu/scalar/
tags:
  - layer/microarch
  - topic/pipeline
created: 2026-11-10
---

# CoralNPU 标量流水线

## 定义

CoralNPU 标量核是 4 宽、顺序派发的前端：每个周期最多从指令缓冲中取 4 条指令，经 scoreboard 判断依赖后派发到 ALU/BRU/MLU/DVU/FPU/LSU。

## 如何工作

```text
Fetch (128-bit) → Decode/Dispatch (4-way) → Execute/Writeback → Retirement Buffer
```

- 4 个 ALU、4 个 BRU：每周期可服务 4 条整数/分支指令。
- 1 个 MLU：3 级流水，每周期最多 1 条乘法。
- 1 个 DVU：多周期，非流水，忙时反压派发。
- 1 个 FPU：多周期流水。
- LSU：每周期最多 1 条内存指令。
- Scoreboard：跟踪 RAW/WAW；所有单元在派发后下一周期读寄存器，因此不会出现 WAR。

## 关键细节

- 文档口径：`microarch.md` 写 3 级流水，README 写 4 级；以 RTL 为准。
- 文档对 retire 的表述也不完全统一：`overview.md` 说 in-order retirement，README 说 out-of-order retire；实际以 ROB/RetirementBuffer 的 RTL 行为为准。
- 控制流：不越过 `jal/jalr/ebreak/ecall/mret/wfi` 派发。
- 特殊指令（CSR、fence、wfi 等）限制在 slot 0，且通常与跳转一样处理。

## 在项目中的位置

- 所属项目：[[CoralNPU]]
- 相关子系统：[[CoralNPU-RVV]]、[[CoralNPU-Memory]]

## 相关概念

- [[Pipeline-and-Hazards]]
- [[ISA-and-Extensions]]

## 自检问题

- 一条 `lw` 在 LSU 里经历哪些状态？
- 多周期 MLU/DVU 如何回写？WAR 为什么不会发生？
- CSR 指令为什么限制在 slot 0？
- 分支冲刷时，ROB 如何处理年轻指令？

## 来源

- `doc/microarch/microarch.md`
- `doc/microarch/dispatch.md`
- `doc/microarch/mlu.md`
