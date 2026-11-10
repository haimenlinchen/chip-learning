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

矩阵加速器用 PE（Processing Element，处理单元；阵列中执行乘加的基本单元）阵列/脉动阵列（systolic array，PE 按节奏传递数据并复用中间结果；经典矩阵乘结构）/tensor core（张量核心，专用于小矩阵乘加的硬件单元；一条指令完成 tile 级 GEMM）执行 GEMM（General Matrix Multiply，通用矩阵乘；深度学习与 HPC 的核心算子，`C += A·B`），通过 tile（分块，把大矩阵切成能放进寄存/片上存储的小块；提升复用与并行）化、数据复用和专用数据通路提高算力密度。

## 两种典型形态

| 形态 | 代表 | 特点 |
|---|---|---|
| GPU tensor core | Vortex TCU | 与 warp/warpgroup（warp 组，多个 warp 协同执行一条更大粒度的矩阵指令；如 4 warp 一组）绑定；tile 由指令描述；支持稀疏/MX（Microscaling，块级缩放格式；用共享指数压缩低精度数值、节省带宽） |
| NPU matrix engine | CoralNPU VME/Zvt | 与 RVV/标量紧耦合；matrix tile 状态；INT8/FP32/BF16 |

## 关键设计维度

- **tile 几何**：M/N/K 如何映射到 PE 阵列和寄存器。
- **操作数来源**：寄存器 vs shared memory（GPU 片上共享存储，warp 间可见；用于矩阵分块的数据复用）/TCM（Tightly-Coupled Memory，紧耦合存储；低延迟、软件显式管理）。
- **数据复用**：A/B 的广播、K-major（按 K 维连续排布，便于沿 K 累加时连续读取；矩阵乘常用布局）布局、transpose。
- **累加器**：寄存器/独立 accumulator（累加寄存器，保存 C 的部分和；GEMM 全程驻留以减少访存）。
- **数据类型**：FP32/TF32/FP16/BF16/FP8/INT8/INT4。
- **稀疏**：2:4 结构化稀疏（每 4 个权重最多保留 2 个非零；GPU 稀疏 tensor core 的硬件格式）、metadata。
- **量化**（quantization，用低位宽数值近似权重与激活；降低带宽与算力成本）：MX block scaling、per-tensor/per-channel。

## 在项目中的体现

- [[Vortex-TCU]]：WMMA/WGMMA（Warpgroup Matrix Multiply-Accumulate，warpgroup 级矩阵乘累加指令；一次覆盖更大 tile）、FEDP 网格、2:4 稀疏、MX、8/16/32 累加器。
- [[CoralNPU-VME]]：16 个 matrix tile、M/N/K CSR、PE 阵列、INT8/FP32/BF16。
- [[Vortex-DXA]]：把 GMEM tile 异步搬到 LMEM，并做 K-major transpose。

## 相关概念

- [[Vector-Architecture]]
- [[Cache-and-Memory]]
- [[Performance-Modeling]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| PE | 阵列中执行乘加的基本单元 | 矩阵/卷积加速 | 数量与互连决定峰值算力 |
| 脉动阵列 | PE 按节奏传递数据并复用中间结果 | 经典矩阵乘 | 数据复用高，但灵活性较低 |
| tensor core | 专用于小矩阵乘加的硬件单元 | GPU 深度学习 | 一条指令完成 tile 级运算 |
| GEMM | 通用矩阵乘 C = A·B | 深度学习、HPC | 多数算子最终可归约为 GEMM |
| tile | 大矩阵切成的片上小块 | 分块计算、数据复用 | tile 越大复用越高，但受片上存储限制 |
| warpgroup | 多个 warp 协同执行更大粒度指令 | WGMMA | 比单 warp 提供更高的矩阵吞吐 |
| MX | 块级缩放的低精度格式 | 量化推理 | 共享指数减少元数据开销 |
| shared memory | GPU 片上、warp 间可见的存储 | 矩阵分块复用 | 与 TCM 类似，但通常由硬件一致性管理 |
| TCM | 低延迟、软件显式管理的片上存储 | NPU 矩阵引擎 | 与 scratchpad 同源，强调确定性 |
| K-major | 按 K 维连续排布的布局 | 沿 K 累加的矩阵乘 | 便于连续读取，减少 transpose 开销 |
| accumulator | 保存 C 部分和的寄存器 | GEMM 全程累加 | 驻留片上可显著减少访存 |
| 2:4 结构化稀疏 | 每 4 个权重最多 2 个非零 | 稀疏 tensor core | 需要 metadata 指示非零位置 |
| 量化 | 用低位宽数值近似权重/激活 | 推理加速 | per-channel 通常比 per-tensor 更准 |
| WGMMA | warpgroup 级矩阵乘累加指令 | Vortex TCU | 相比 WMMA 覆盖更大 tile |
