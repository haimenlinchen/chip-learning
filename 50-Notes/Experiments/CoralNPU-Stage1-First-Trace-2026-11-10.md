---
type: experiment
project: CoralNPU
status: todo
tags:
  - experiment/stage1
  - project/coralnpu
created: 2026-11-10
---

# CoralNPU Stage 1：第一次指令 trace

## 问题

一条 `add` 指令从取指到退休，在 CoralNPU 的标量流水线里到底经过哪些阶段？`--instr_trace` 能观察到哪些信息？

## 环境

- 仓库：`/localdata/linchen/coralnpu`
- 分支/commit：待填
- 构建目标：`//tests/verilator_sim:core_mini_verification_axi_sim`
- 示例：`//examples:coralnpu_v2_hello_world_add_floats`

## 命令

```bash
# 1. 构建验证版仿真器
bazel build //tests/verilator_sim:core_mini_verification_axi_sim

# 2. 构建示例
bazel build //examples:coralnpu_v2_hello_world_add_floats

# 3. 查 ELF 实际路径
bazel cquery --output=files //examples:coralnpu_v2_hello_world_add_floats

# 4. 运行并打印 trace
./bazel-bin/tests/verilator_sim/core_mini_verification_axi_sim \
  --binary="<ELF 路径>" --backdoor_load --instr_trace
```

## 结果

- 观察到的 PC 序列：
- `add` 的 retire 周期：
- 写回的目的寄存器/数据：
- 异常/中断：

## 解释

- 这条指令经过了哪些流水级？
- 与 [[CoralNPU-Pipeline]] 的描述是否一致？
- 文档中 3 级/4 级流水的差异，在 trace 里能否判断？

## 下一步

- [ ] 再跑一条 `load`，对比 LSU 路径
- [ ] 再跑一条 `branch`，观察冲刷
- [ ] 把 trace 片段贴到 [[CoralNPU-Pipeline]]

## 相关

- [[Stage-1-Scalar-Core]]
- [[CoralNPU]]
- [[CoralNPU-Pipeline]]
