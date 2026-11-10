---
type: atomic
layer: microarchitecture
topic: [rvv, vector, vlen, lmuls]
status: learning
tags:
  - layer/microarch
  - topic/vector
created: 2026-11-10
---

# 向量体系结构

## 定义

向量体系结构（vector architecture）用一条指令处理一组数据，利用 SIMD（Single Instruction, Multiple Data：单指令多数据；一条指令并行处理多个元素）与 DLP（Data-Level Parallelism：数据级并行；向量/SIMD 利用的并行形式），并通过 VLEN（向量寄存器位宽；决定单个向量寄存器能容纳多少位数据）、SEW（Selected Element Width，元素位宽；决定一个向量元素占多少位）、LMUL（向量寄存器组倍数；把多个向量寄存器拼成更宽的逻辑寄存器）描述向量寄存器组和数据宽度。

## RVV 关键参数

| 参数 | 含义 | CoralNPU |
|---|---|---|
| VLEN | 单个向量寄存器位宽 | 128 bit |
| SEW | 元素位宽 | 8/16/32 |
| LMUL | 寄存器组倍数 | 1/8 … 8 |
| VL（Vector Length，实际处理的元素数；运行时由 vsetvl 设置） | 实际处理的元素数 | `vsetvl` 设置 |

## 执行方式

- **耦合式**（coupled vector，向量单元内嵌在标量流水线中；实现简单但与标量难以重叠）：向量指令在标量流水线内执行，简单但难乱序。
- **解耦式**（decoupled vector，向量指令进入独立后端，可与标量重叠执行；吞吐更高）：向量指令进入独立后端，自有译码/队列/ROB（Reorder Buffer，重排序缓冲，暂存指令并按序提交；支撑精确异常），可与标量重叠；CoralNPU 采用这种。

## 访存模式

- unit-stride（单位步长访存，元素在内存中连续排列；最常见、最高效）：连续
- strided（跨步访存，元素间隔固定步长；适合按行/列访问矩阵）：固定步长
- indexed（索引访存，用索引向量做 gather/scatter；适合稀疏/不规则访问）：gather/scatter
- masked（掩码访存，只对 mask 为真的元素读写；避免分支开销）：按 mask 选择
- fault-only-first（只报告第一个越界 fault 的向量访存；用于安全的边界检查）：只报告第一个 fault

## 关键设计点

- 向量寄存器堆的 bank/port 设计。
- 向量指令的精确异常（`vstart`）。
- LMUL 对寄存器分组和访存模式的影响。
- 与标量的同步（`vfmv.f.s`、reduction、`vsetvl`）。

## 在项目中的体现

- [[CoralNPU-RVV]]
- [[Vortex]] 的 SIMT 是另一条并行路线（TLP 而非 DLP）

## 相关概念

- [[SIMT-and-Warp]]
- [[Matrix-Accelerator]]
- [[Scratchpad-and-TCM]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| 向量体系结构 | 用一条指令操作一组数据 | 规则数据并行 | 与 SIMT 的 TLP 路线形成对照 |
| SIMD | 单指令多数据 | 多媒体、AI 预处理 | 固定宽度 SIMD 需要处理尾部元素 |
| DLP | 数据级并行 | 向量/SIMD | 与 TLP 正交，可叠加使用 |
| VLEN | 向量寄存器位宽 | RVV 硬件配置 | 越大单指令吞吐越高，但面积也越大 |
| SEW | 元素位宽 | 选择数据精度 | 与 LMUL 共同决定寄存器占用 |
| LMUL | 向量寄存器组倍数 | 调整有效向量长度 | 大于 1 时多条指令共享寄存器组 |
| VL | 实际处理的元素数 | 循环尾部处理 | 由 vsetvl 运行时设置，不必等于 VLEN |
| 耦合式 | 向量单元内嵌标量流水线 | 轻量实现 | 实现简单但与标量难以重叠 |
| 解耦式 | 向量指令进入独立后端 | CoralNPU | 可与标量重叠，吞吐更高 |
| unit-stride | 连续地址访存 | 数组遍历 | 最易合并，带宽效率最高 |
| strided | 固定步长访存 | 矩阵行/列访问 | 步长越大，事务数越多 |
| indexed | 用索引向量 gather/scatter | 稀疏、不规则访问 | 难以合并，带宽开销大 |
| masked | 按 mask 选择性访存 | 条件读写 | 避免分支，但掩码生成有成本 |
| fault-only-first | 只报告第一个越界 fault | 边界检查 | 适合安全的向量化循环 |
