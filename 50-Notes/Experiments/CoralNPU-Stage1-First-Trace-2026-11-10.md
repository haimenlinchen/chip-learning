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

一条 `add`（整数加法指令；用于观察最基本的数据通路）指令从取指到退休（retire：指令完成并写回架构状态；用于衡量流水线延迟），在 CoralNPU 的标量流水线里到底经过哪些阶段？`--instr_trace`（仿真器指令跟踪开关；用于打印逐条指令执行信息）能观察到哪些信息？

## 环境

- 仓库：`/localdata/linchen/coralnpu`
- 分支/commit：待填
- 构建目标（Bazel：构建系统；用于编译仿真器与示例）：`//tests/verilator_sim:core_mini_verification_axi_sim`
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

- 观察到的 PC（程序计数器；指向当前指令地址）序列：
- `add` 的 retire 周期：
- 写回（writeback：把执行结果写入目的寄存器；用于确认数据通路）的目的寄存器/数据：
- 异常/中断：

## 解释

- 这条指令经过了哪些流水级（pipeline stage：流水线的一个执行阶段；用于分析指令时序）？
- 与 [[CoralNPU-Pipeline]] 的描述是否一致？
- 文档中 3 级/4 级流水的差异，在 trace 里能否判断？

## 下一步

- [ ] 再跑一条 `load`，对比 LSU（加载/存储单元；处理 load/store 访存指令）路径
- [ ] 再跑一条 `branch`，观察冲刷（flush：分支跳转时清除错误路径指令；用于理解控制冒险）
- [ ] 把 trace 片段贴到 [[CoralNPU-Pipeline]]

## 相关

- [[Stage-1-Scalar-Core]]
- [[CoralNPU]]
- [[CoralNPU-Pipeline]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| add | 整数加法指令 | 观察数据通路与写回 | 与 load/branch 对比 |
| trace | 逐条执行轨迹 | 调试流水线行为 | `--instr_trace` 开关 |
| PC | 程序计数器 | 定位指令地址 | 对比跳转前后 PC |
| retire | 指令退休 | 衡量流水线延迟 | 与 issue 周期对比 |
| writeback | 写回 | 确认结果落入寄存器 | 查目的寄存器 |
| LSU | 加载/存储单元 | 处理访存指令 | 对比 load/store 路径 |
| flush | 流水线冲刷 | 分支预测失败恢复 | 观察错误路径指令 |
| Bazel | 构建系统 | 编译仿真器与示例 | 查 target 与产物路径 |
