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

SIMT（Single Instruction, Multiple Threads，单指令多线程；一组线程共享 PC 执行同一指令）让一组线程共享 PC 执行同一指令，用线程掩码（thread mask，标记哪些线程活跃并写回结果；用于处理分支发散）控制哪些线程写回。这组线程通常称为 warp（线程的逻辑分组，通常 32 个线程；共享 PC、各自持有寄存器）。

## 关键机制

- **warp**：线程的逻辑分组；共享 PC，每线程有自己的寄存器。
- **线程掩码**：分支发散（divergence，同一 warp 内线程走不同分支；硬件分时串行执行各路径）时，不同路径分时执行，掩码决定写回。
- **IPDOM stack**（Immediate Post-Dominator 栈，记录分支汇合点；保存/恢复发散状态）：保存/恢复发散状态（`SPLIT`/`JOIN`）。
- **warp scheduler**（warp 调度器，每周期从就绪 warp 中挑选一个发射；用多 warp 隐藏延迟）：每周期选择一个 ready warp 发射，隐藏延迟。
- **barrier**（屏障同步，要求所有参与 warp 到达后才能继续；用于 warp 间协作）：warp 间同步（`BAR`）。

## 为什么用 SIMT

- 用少量控制逻辑服务大量线程，面积/能效优于 MIMD（Multiple Instruction, Multiple Data，多指令多数据；每个线程独立取指，控制开销大）。
- 通过大量 warp 隐藏内存延迟，而不是依赖复杂 cache/预取。
- 编程模型接近 SPMD（Single Program, Multiple Data，单程序多数据；同一程序在不同线程上处理不同数据），编译器/运行时成熟。

## 代价

- 分支发散会串行化不同路径。
- 需要线程掩码、IPDOM、barrier 等额外硬件。
- 访存合并（memory coalescing，把同一 warp 内相邻地址的访问合并成少量事务；提升有效带宽）/共享内存 bank conflict（bank 冲突，多个线程访问同一 bank 的不同地址；导致串行化）影响性能。

## 在项目中的体现

- [[Vortex]]：完整 SIMT（warp scheduler、IPDOM、`SPLIT/JOIN/PRED/BAR`）。
- [[CoralNPU]]：不是 SIMT；用 4 宽标量 + RVV（RISC-V Vector 向量扩展；用变长向量寄存器做数据并行）的 DLP（Data-Level Parallelism，数据级并行；一条指令处理多个数据元素）替代 warp 级 TLP（Thread-Level Parallelism，线程级并行；多个线程/warp 同时推进）。

## 相关概念

- [[Pipeline-and-Hazards]]
- [[Vector-Architecture]]
- [[Cache-and-Memory]]
- [[Performance-Modeling]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| SIMT | 一组线程共享 PC 执行同一指令 | GPU、Vortex | 与 SIMD 的关键差异是每线程独立寄存器与掩码 |
| warp | 线程逻辑分组，共享 PC、各自寄存器 | GPU 调度 | 典型宽度 32，是 GPU 资源分配的基本单位 |
| 线程掩码 | 标记活跃线程并决定写回 | 分支发散处理 | 掩码变化即控制流分歧的体现 |
| 分支发散 | 同一 warp 内线程走不同分支 | 控制流密集内核 | 分时串行执行会显著降低利用率 |
| IPDOM | 记录分支汇合点的栈 | 发散/汇合恢复 | 与 SPLIT/JOIN 指令配套 |
| warp scheduler | 每周期挑选一个就绪 warp 发射 | 延迟隐藏 | 就绪 warp 越多，越能填满流水线 |
| barrier | 参与 warp 全部到达后继续 | warp 间协作 | 实现不当会引入死锁 |
| MIMD | 每线程独立指令流的多处理器模型 | 多核 CPU | 控制开销大，但灵活性高 |
| SPMD | 同一程序处理不同数据 | CUDA/OpenCL 编程模型 | 是 SIMT 在软件层的对应抽象 |
| 访存合并 | 合并同 warp 相邻地址访问 | 全局内存访问 | 地址跨度越大，事务数越多 |
| bank conflict | 多线程访问同一 bank 不同地址 | 共享内存 | 可通过 padding 或重排访问缓解 |
| DLP | 一条指令处理多个数据元素 | 向量、SIMD | 与 TLP 是两种正交并行来源 |
| TLP | 多个线程/warp 同时推进 | GPU、多核 | 靠调度隐藏延迟 |
| RVV | RISC-V 向量扩展 | CoralNPU 的数据并行 | 走 DLP 路线，与 Vortex 的 SIMT 形成对照 |
