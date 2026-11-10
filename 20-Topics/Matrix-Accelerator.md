---
type: atomic
layer: microarchitecture
topic: [matrix, tensor-core, gemm, sparsity]
status: learning
tags:
  - layer/microarch
  - topic/matrix
created: 2026-11-10
---

# 矩阵加速器

## 定义

矩阵加速器用 PE 阵列/脉动阵列/tensor core 执行 GEMM（`C += A·B`），通过 tile 化、数据复用和专用数据通路提高算力密度。

## 两种典型形态

| 形态 | 代表 | 特点 |
|---|---|---|
| GPU tensor core | Vortex TCU | 与 warp/warpgroup 绑定；tile 由指令描述；支持稀疏/MX |
| NPU matrix engine | CoralNPU VME/Zvt | 与 RVV/标量紧耦合；matrix tile 状态；INT8/FP32/BF16 |

## 关键设计维度

- **tile 几何**：M/N/K 如何映射到 PE 阵列和寄存器。
- **操作数来源**：寄存器 vs shared memory/TCM。
- **数据复用**：A/B 的广播、K-major 布局、transpose。
- **累加器**：寄存器/独立 accumulator。
- **数据类型**：FP32/TF32/FP16/BF16/FP8/INT8/INT4。
- **稀疏**：2:4 结构化稀疏、metadata。
- **量化**：MX block scaling、per-tensor/per-channel。

## 在项目中的体现

- [[Vortex-TCU]]：WMMA/WGMMA、FEDP 网格、2:4 稀疏、MX、8/16/32 累加器。
- [[CoralNPU-VME]]：16 个 matrix tile、M/N/K CSR、PE 阵列、INT8/FP32/BF16。
- [[Vortex-DXA]]：把 GMEM tile 异步搬到 LMEM，并做 K-major transpose。

## 相关概念

- [[Vector-Architecture]]
- [[Cache-and-Memory]]
- [[Performance-Modeling]]
