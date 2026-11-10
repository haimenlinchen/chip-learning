---
type: stage
stage: 1
status: todo
projects: [CoralNPU]
tags:
  - learning/roadmap
  - stage/scalar-core
created: 2026-11-10
---

# 阶段一：单核流水线

## 目标

能独立讲清一条指令从取指到退休的全过程，并理解 scoreboard/ROB 如何保证正确性。

## 阅读

- [[CoralNPU]]
- [[CoralNPU-Pipeline]]
- [[Pipeline-and-Hazards]]
- `coralnpu/doc/overview.md`
- `coralnpu/doc/microarch/microarch.md`
- `coralnpu/doc/microarch/dispatch.md`
- `coralnpu/doc/microarch/lsu.md`
- `coralnpu/doc/microarch/mlu.md`

## 运行

```bash
# 构建验证版仿真器
bazel build //tests/verilator_sim:core_mini_verification_axi_sim

# 构建示例
bazel build //examples:coralnpu_v2_hello_world_add_floats

# 找到 ELF 的实际路径
bazel cquery --output=files //examples:coralnpu_v2_hello_world_add_floats

# 运行并打印指令 trace
./bazel-bin/tests/verilator_sim/core_mini_verification_axi_sim \
  --binary="<ELF 路径>" --backdoor_load --instr_trace
```

## 任务

- [ ] 手画 `add` 的 Fetch → Decode → Dispatch → ALU → ROB retire
- [ ] 手画 `load` 的 LSU → DTCM/AXI → 写回
- [ ] 手画 `branch` 的 BRU → 冲刷/重定向
- [ ] 理解 scoreboard 如何避免 RAW/WAW
- [ ] 理解 ROB/RetirementBuffer 如何保证精确异常
- [ ] 加一个 CSR 或简单指令，跑 cocotb

## 产出

- [ ] 一张流水线时序图
- [ ] 一份 scoreboard/ROB 笔记
- [ ] 一个能跑通的新 CSR/指令补丁

## 自检问题

- 一条 `lw` 在 LSU 里经历哪些状态？
- 多周期 MLU/DVU 如何回写？
- WAR 为什么不会发生？
- CSR 指令为什么限制在 slot 0？
- 分支冲刷时年轻指令如何清理？

## 相关

- [[Stage-2-RVV-VME]]
- [[Verification-Fidelity]]
