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

能独立讲清一条指令从取指到退休的全过程，并理解 scoreboard（记分板，跟踪寄存器与执行单元就绪状态的硬件表；用于动态调度与冒险检测）/ROB（重排序缓冲，按程序顺序提交指令；用于乱序执行与精确异常）如何保证正确性。

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

- [ ] 手画 `add` 的 Fetch → Decode → Dispatch → ALU（算术逻辑单元，执行整数加减、逻辑与移位；用于通用整数运算） → ROB retire
- [ ] 手画 `load` 的 LSU（加载存储单元，处理 load/store 与地址计算；用于访存指令） → DTCM（紧耦合数据存储器，片上低延迟 SRAM；用于暂存数据）/AXI（AMBA 高级可扩展接口总线；用于 SoC 片内高带宽互连） → 写回
- [ ] 手画 `branch` 的 BRU（分支处理单元，判断分支并产生重定向；用于控制流） → 冲刷/重定向
- [ ] 理解 scoreboard 如何避免 RAW/WAW（数据冒险类型：先写后读、先写后写；决定是否需要停顿或旁路）
- [ ] 理解 ROB/RetirementBuffer 如何保证精确异常
- [ ] 加一个 CSR（控制状态寄存器；用于配置、异常处理与性能计数）或简单指令，跑 cocotb（Python 驱动的 RTL 仿真框架；用于模块级功能验证）

## 产出

- [ ] 一张流水线时序图
- [ ] 一份 scoreboard/ROB 笔记
- [ ] 一个能跑通的新 CSR/指令补丁

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| scoreboard | 记分板，跟踪寄存器与执行单元就绪状态 | 动态调度与冒险检测 | 与 ROB 分工：scoreboard 管就绪，ROB 管顺序提交 |
| ROB | 重排序缓冲 | 乱序执行与精确异常 | 分支冲刷时按 ROB 顺序回收年轻指令 |
| ALU | 算术逻辑单元 | 通用整数运算 | 与多周期执行单元共享写回端口 |
| LSU | 加载存储单元 | 访存指令 | load 需经地址计算、总线访问、写回等多个阶段 |
| DTCM | 紧耦合数据存储器 | 低延迟数据暂存 | 与 cache 不同，TCM 由软件显式管理 |
| AXI | AMBA 高级可扩展接口 | SoC 片内互连 | AXI 支持多 outstanding 与突发传输 |
| BRU | 分支处理单元 | 控制流与重定向 | 分支冲刷要清理年轻指令并恢复 PC |
| RAW/WAW | 数据冒险类型 | 流水线停顿与旁路判断 | WAR 由顺序发射天然避免 |
| CSR | 控制状态寄存器 | 配置、异常、计数 | CSR 指令常限制在特定流水槽以简化异常 |
| cocotb | Python 驱动的 RTL 仿真框架 | 模块级功能验证 | 可与 Verilator、Icarus 等仿真器配合 |

## 自检问题

- 一条 `lw` 在 LSU 里经历哪些状态？
- 多周期 MLU/DVU 如何回写？
- WAR 为什么不会发生？
- CSR 指令为什么限制在 slot 0？
- 分支冲刷时年轻指令如何清理？

## 相关

- [[Stage-2-RVV-VME]]
- [[Verification-Fidelity]]
