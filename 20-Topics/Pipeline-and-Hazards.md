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

流水线把指令执行拆成多个阶段并行；冒险（hazard）分为结构冒险、数据冒险（RAW/WAW/WAR）、控制冒险。

## 三种常见处理

| 冒险 | 处理方式 |
|---|---|
| RAW | 前递（forwarding）或 stall，scoreboard 跟踪 |
| WAW | 顺序写回或重命名；in-order 核通常不需要 |
| WAR | 操作数在派发后下一周期读取，天然避免 |
| 控制 | 分支预测/延迟槽/冲刷；CoralNPU 保守不越过跳转 |

## 两种退休模型

- **顺序退休**：ROB 按序提交，精确异常容易；CoralNPU 标量/向量、Vortex 都是这个方向。
- **乱序退休**：实现复杂，精确异常困难；现代高性能核通常仍用“乱序执行 + 顺序退休”。

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
