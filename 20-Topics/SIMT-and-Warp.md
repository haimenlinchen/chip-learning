---
type: atomic
layer: microarchitecture
topic: [simt, warp, divergence, latency-hiding]
status: learning
tags:
  - layer/microarch
  - topic/simt
created: 2026-11-10
---

# SIMT 与 Warp

## 定义

SIMT（Single Instruction, Multiple Threads）让一组线程共享 PC 执行同一指令，用线程掩码控制哪些线程写回。这组线程通常称为 warp。

## 关键机制

- **warp**：线程的逻辑分组；共享 PC，每线程有自己的寄存器。
- **线程掩码**：分支发散时，不同路径分时执行，掩码决定写回。
- **IPDOM stack**：保存/恢复发散状态（`SPLIT`/`JOIN`）。
- **warp scheduler**：每周期选择一个 ready warp 发射，隐藏延迟。
- **barrier**：warp 间同步（`BAR`）。

## 为什么用 SIMT

- 用少量控制逻辑服务大量线程，面积/能效优于 MIMD。
- 通过大量 warp 隐藏内存延迟，而不是依赖复杂 cache/预取。
- 编程模型接近 SPMD，编译器/运行时成熟。

## 代价

- 分支发散会串行化不同路径。
- 需要线程掩码、IPDOM、barrier 等额外硬件。
- 访存合并/共享内存 bank conflict 影响性能。

## 在项目中的体现

- [[Vortex]]：完整 SIMT（warp scheduler、IPDOM、`SPLIT/JOIN/PRED/BAR`）。
- [[CoralNPU]]：不是 SIMT；用 4 宽标量 + RVV 的 DLP 替代 warp 级 TLP。

## 相关概念

- [[Pipeline-and-Hazards]]
- [[Vector-Architecture]]
- [[Cache-and-Memory]]
- [[Performance-Modeling]]
