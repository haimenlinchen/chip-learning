---
type: atomic
layer: microarchitecture
topic: [pipeline, hazard, scoreboard, rob]
status: learning
tags:
  - layer/microarch
  - topic/pipeline
created: 2026-11-10
---

# 流水线与冒险

## 定义

流水线（pipeline，把指令执行拆成多个阶段并让不同指令重叠执行；CPU 提升吞吐的基本手段）把指令执行拆成多个阶段并行；冒险（hazard）分为结构冒险（structural hazard，两条指令争用同一硬件资源；需增加端口或调度避免）、数据冒险（data hazard，后一条指令依赖前一条的结果；需前递或停顿；含 RAW（Read-After-Write 真依赖；流水线必须等前一条指令写回）/WAW（Write-After-Write 输出依赖；顺序写回或重命名消除）/WAR（Write-After-Read 反依赖；重命名或延后读消除））、控制冒险（control hazard，分支改变取指方向导致不确定性；用预测/冲刷处理）。

## 三种常见处理

| 冒险 | 处理方式 |
|---|---|
| RAW | 前递（forwarding，把上一条指令的结果直接送给下一条；避免等待写回）或 stall，scoreboard（记分板，记录指令与功能单元的依赖/忙状态；用于调度和冲突检测）跟踪 |
| WAW | 顺序写回或重命名（register renaming，把架构寄存器映射到更多物理寄存器；消除假依赖）；in-order 核通常不需要 |
| WAR | 操作数在派发后下一周期读取，天然避免 |
| 控制 | 分支预测/延迟槽/冲刷；CoralNPU 保守不越过跳转 |

## 两种退休模型

- **顺序退休**（in-order commit，指令按程序序提交结果；保证精确异常）：ROB（Reorder Buffer，重排序缓冲，暂存乱序完成的指令并按序提交）按序提交，精确异常（precise exception，异常时年轻指令尚未提交、状态可回滚）容易；CoralNPU 标量/向量、Vortex 都是这个方向。
- **乱序退休**：实现复杂，精确异常困难；现代高性能核通常仍用“乱序执行（out-of-order execution，指令按操作数就绪而非程序序执行；提升 ILP）+ 顺序退休”。

## 在项目中的体现

- [[CoralNPU-Pipeline]]：4 宽顺序派发，scoreboard + ROB/RetirementBuffer；多周期 MLU/DVU/FPU 异步完成。
- [[Vortex-SIMT]]：6 级流水，warp scheduler + scoreboard + IPDOM；SIMT 用线程掩码处理分支发散。

## 关键问题

- 多周期单元的写回如何与 scoreboard 同步？
- 分支冲刷时，年轻指令如何清理？
- 精确异常要求哪些状态可回滚？
- 顺序退休 vs 乱序退休对验证复杂度的影响？

## 相关概念

- [[ISA-and-Extensions]]
- [[SIMT-and-Warp]]
- [[Vector-Architecture]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| 流水线 | 把指令执行拆成多阶段重叠执行 | CPU 提升吞吐 | 级数越深频率越高，但分支惩罚也越大 |
| 结构冒险 | 两条指令争用同一硬件资源 | 多发射、访存端口设计 | 增加端口或复制资源可消除 |
| 数据冒险 | 后一条指令依赖前一条的结果 | 依赖检测、调度 | 是 RAW/WAW/WAR 的统称 |
| RAW | 真依赖，必须等前一条写回 | 前递、停顿 | 唯一无法靠重命名消除的依赖 |
| WAW | 输出依赖，两条指令写同一寄存器 | 乱序写回 | 顺序核天然满足 |
| WAR | 反依赖，后写覆盖先读 | 乱序发射 | 寄存器重命名可消除 |
| 控制冒险 | 分支改变取指方向带来不确定性 | 分支预测、冲刷 | 预测越准，流水线效率越高 |
| forwarding | 把结果直接旁路给下一条指令 | 执行级依赖 | 减少停顿但增加连线与选择逻辑 |
| scoreboard | 记录指令与功能单元依赖/忙状态 | 顺序/乱序调度 | 与 ROB 配合完成发射与写回控制 |
| 重命名 | 架构寄存器映射到更多物理寄存器 | 乱序核 | 消除 WAW/WAR 假依赖 |
| ROB | 重排序缓冲，暂存并排序提交 | 精确异常、乱序执行 | 容量决定可容忍的在途指令数 |
| 顺序退休 | 按程序序提交结果 | 精确异常 | 乱序执行通常仍配顺序退休 |
| 精确异常 | 异常时状态可回滚、年轻指令未提交 | OS、调试 | 是乱序核验证的难点 |
| 乱序执行 | 按操作数就绪执行而非程序序 | 高性能 CPU/GPU | 提升 ILP，但面积与验证成本高 |
