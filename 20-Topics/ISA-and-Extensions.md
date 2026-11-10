---
type: atomic
layer: isa
topic: [risc-v, isa-extension, misa]
status: learning
tags:
  - layer/isa
  - topic/isa
created: 2026-11-10
---

# ISA 与扩展

## 定义

ISA（指令集架构，软件与硬件之间的契约；决定编译器、操作系统与芯片如何交互）是软件与硬件的契约。RISC-V（开放、模块化的指令集架构；广泛用于 MCU、AI 加速器、边缘 NPU 与服务器）的模块化设计允许按需组合基础指令集与扩展，也允许厂商用自定义 opcode（操作码，指令中标识操作类型的编码字段；扩展指令集时用来分配新指令）/MISA（Machine ISA 寄存器，记录芯片支持哪些扩展的位图；OS 与固件据此判断可用指令）位加入加速器。

## 两类扩展路线

| 路线 | 代表 | 特点 |
|---|---|---|
| 标准扩展 | CoralNPU：RVV 1.0（RISC-V Vector 向量扩展；用变长向量寄存器加速数据并行）、Zba/Zbb（RISC-V 标准位操作扩展；加速地址生成与通用位运算）、Zfbfmin（BF16 浮点最小转换扩展；为 AI 推理提供低精度数据通路） | 可直接用现成编译器/intrinsics（编译器内建函数，把高级语言直接映射到底层指令；向量/加速器编程常用）；生态成本低 |
| 自定义扩展 | Vortex：SIMT（单指令多线程，一组线程共享 PC 执行同一指令；GPU 与 Vortex 用它隐藏延迟）控制指令、TCU（Tensor Core Unit，矩阵乘加速单元；执行 WMMA/WGMMA 等 tensor 运算）/DXA（DMA 加速器，把大块 tile 从全局存储搬到本地存储；为矩阵运算供给数据）/RTU | 需要自定义编译器/运行时；可深度贴合架构 |
| 实验性标准 | CoralNPU VME（Vector Matrix Extension，实验性向量矩阵扩展；用 RVV 风格指令表达矩阵 tile 运算）/Zvt | 介于两者之间；标准化程度低，但方向开放 |

## Vortex 的 ISA 选择

- 基础：RV32IMAFC / RV64IMAFDC。
- SIMT 控制：`TMC`、`WSPAWN`、`SPLIT/JOIN/PRED`、`BAR`。
- 加速器：TCU/DXA/TEX/RASTER/OM/RTU/MUFU 通过 MISA 扩展位或 custom opcode 暴露。

## CoralNPU 的 ISA 选择

- 基础：RV32IMF + Zba/Zbb/Zicsr/Zifencei（CSR 访问与指令流同步的标准扩展；运行 OS/固件所需）/Zfbfmin。
- 向量：RVV 1.0（`Zve32x`、`Zve32f`、`Zvfbfmin`），VLEN（向量寄存器位宽；决定单条向量指令一次能处理多少数据）=128。
- 矩阵：实验性 VME/Zvt。

## 设计取舍

- 标准扩展：编译器和库可直接复用，但硬件必须实现完整语义。
- 自定义扩展：硬件更高效，但软件栈要自己维护。
- 混合：核心用标准 ISA，加速器用 custom opcode（Vortex 的 TCU/DXA 就是这种）。

## 在项目中的体现

- [[CoralNPU]]：[[CoralNPU-RVV]]、[[CoralNPU-VME]]
- [[Vortex]]：[[Vortex-SIMT]]、[[Vortex-TCU]]、[[Vortex-DXA]]

## 自检问题

- 为什么 Vortex 选择“最小 ISA 改动 + 自定义 SIMT 指令”？
- CoralNPU 为什么优先 RVV 1.0 而不是自定义向量 ISA？
- MISA 扩展位与 custom opcode 各自的优缺点？
- 自定义扩展如何影响编译器/调试器/OS？

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| ISA | 指令集架构，软件与硬件的契约 | 编译器、OS、芯片设计 | ISA 是规范，微架构是实现，二者需分开讨论 |
| RISC-V | 开放、模块化的指令集架构 | MCU、AI 加速器、边缘 NPU、服务器 | 与 x86/ARM 的核心差异在开放性与可扩展性 |
| opcode | 指令中标识操作类型的编码字段 | 自定义指令、加速器暴露 | RISC-V 预留 custom opcode 空间给厂商 |
| MISA | 记录已支持扩展的 CSR 位图 | OS/固件探测硬件能力 | 与设备树、运行时 probe 机制互补 |
| RVV | RISC-V 向量扩展 | 数据并行、AI 预处理 | 与 SIMT 的 TLP 路线相对，RVV 走 DLP |
| Zba/Zbb | 标准位操作扩展 | 地址生成、通用位运算 | 属于标准扩展，编译器可直接复用 |
| Zfbfmin | BF16 最小转换扩展 | 低精度 AI 推理 | 只保证转换，BF16 运算能力需其他扩展 |
| intrinsics | 编译器内建函数 | 向量/加速器编程 | 介于可移植 C 与手写汇编之间 |
| SIMT | 一组线程共享 PC 的并行模型 | GPU、Vortex | 与 SIMD 的区别在每线程独立寄存器与掩码 |
| TCU | 矩阵乘加速单元 | WMMA/WGMMA、tensor 运算 | 依赖 warp/warpgroup 概念 |
| DXA | DMA 加速器 | tile 搬运、转置 | 与 TCM/LMEM 配合完成数据供给 |
| VME | 实验性向量矩阵扩展 | NPU 矩阵引擎 | 标准化程度低，方向开放 |
| VLEN | 向量寄存器位宽 | RVV 配置 | 与 SEW/LMUL 共同决定向量能力 |
| Zicsr/Zifencei | CSR 访问与指令流同步扩展 | OS、固件 | 运行特权软件的基础扩展 |

## 来源

- `vortex/docs/designs/microarchitecture.md`
- `coralnpu/doc/overview.md`
