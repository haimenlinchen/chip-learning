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

ISA 是软件与硬件的契约。RISC-V 的模块化设计允许按需组合基础指令集与扩展，也允许厂商用自定义 opcode/MISA 位加入加速器。

## 两类扩展路线

| 路线 | 代表 | 特点 |
|---|---|---|
| 标准扩展 | CoralNPU（RVV 1.0、Zba/Zbb、Zfbfmin） | 可直接用现成编译器/intrinsics；生态成本低 |
| 自定义扩展 | Vortex（SIMT 控制指令、TCU/DXA/RTU） | 需要自定义编译器/运行时；可深度贴合架构 |
| 实验性标准 | CoralNPU VME/Zvt | 介于两者之间；标准化程度低，但方向开放 |

## Vortex 的 ISA 选择

- 基础：RV32IMAFC / RV64IMAFDC。
- SIMT 控制：`TMC`、`WSPAWN`、`SPLIT/JOIN/PRED`、`BAR`。
- 加速器：TCU/DXA/TEX/RASTER/OM/RTU/MUFU 通过 MISA 扩展位或 custom opcode 暴露。

## CoralNPU 的 ISA 选择

- 基础：RV32IMF + Zba/Zbb/Zicsr/Zifencei/Zfbfmin。
- 向量：RVV 1.0（`Zve32x`、`Zve32f`、`Zvfbfmin`），VLEN=128。
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

## 来源

- `vortex/docs/designs/microarchitecture.md`
- `coralnpu/doc/overview.md`
