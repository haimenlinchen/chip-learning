---
type: atomic
project: CoralNPU
layer: microarchitecture
topic: [vme, zvt, matrix, gemm]
status: learning
source_repo: /localdata/linchen/coralnpu
source_files:
  - doc/overview.md
  - hdl/verilog/rvv/design/Zvt/
tags:
  - layer/microarch
  - topic/matrix
created: 2026-11-10
---

# CoralNPU VME / Zvt 矩阵扩展

## 定义

VME（Vector Matrix Extension）/ Zvt 是 CoralNPU 中实验性的矩阵扩展：在 RVV 之外增加 matrix tile 状态与 PE 阵列，用于 INT8/FP32/BF16 GEMM。

## 如何工作

- 16 个 matrix tile 寄存器 `mt0`–`mt15`。
- 每个 tile 映射到 4 个 sub-tile block，sub-tile 为 16B。
- 配置 CSR/指令：`mtype`、`msetmtype`、`msetmtypei`、`msettn`、`msettm`、`msettk`，配置 M/N/K 与数据类型。
- PE 阵列执行 outer-product / GEMM。
- 硬件 accumulator（`zvt_acc`）与 transpose（`zvt_mt`）。
- `mload`/`mstore` 直接与 LSU/DTCM 耦合，2D tile 流式加载/写回。

## 关键细节

- 支持 INT8、FP32、BF16。
- 与 RVV 共享 LSU/DTCM 通路，tile 的 bank/布局会直接影响带宽。
- 文档明确标注 experimental/optional；成熟度低于 TCU（Vortex）。

## 在项目中的位置

- 所属项目：[[CoralNPU]]
- 相关子系统：[[CoralNPU-RVV]]、[[CoralNPU-Memory]]

## 相关概念

- [[Matrix-Accelerator]]
- [[Scratchpad-and-TCM]]

## 自检问题

- tile 的 M/N/K 如何映射到 PE 阵列？
- `mload/mstore` 与普通向量 load/store 的差异是什么？
- 为什么矩阵引擎需要独立的 accumulator/transpose？
- 16 个 tile 如何避免与 DTCM bank 冲突？

## 来源

- `doc/overview.md`
- `hdl/verilog/rvv/design/Zvt/`
- `tests/cocotb/vme_test/`
