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

向量体系结构用一条指令处理一组数据（SIMD/DLP），通过 VLEN、SEW、LMUL 描述向量寄存器组和数据宽度。

## RVV 关键参数

| 参数 | 含义 | CoralNPU |
|---|---|---|
| VLEN | 单个向量寄存器位宽 | 128 bit |
| SEW | 元素位宽 | 8/16/32 |
| LMUL | 寄存器组倍数 | 1/8 … 8 |
| VL | 实际处理的元素数 | `vsetvl` 设置 |

## 执行方式

- **耦合式**：向量指令在标量流水线内执行，简单但难乱序。
- **解耦式**：向量指令进入独立后端，自有译码/队列/ROB，可与标量重叠；CoralNPU 采用这种。

## 访存模式

- unit-stride：连续
- strided：固定步长
- indexed：gather/scatter
- masked：按 mask 选择
- fault-only-first：只报告第一个 fault

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
