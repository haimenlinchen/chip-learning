---
type: stage
stage: 0
status: learning
projects: [CoralNPU, Vortex, ASIC-Cosim, Clounix-SDK]
tags:
  - learning/roadmap
created: 2026-11-10
---

# 学习路线

> 目标：建立从 RTL（寄存器传输级硬件描述，用寄存器与组合逻辑描述数字电路；是芯片设计与验证的基准）/微架构到验证，再到软硬件接口的完整芯片理解。

## 总览

| 阶段 | 主题 | 主项目 | 时间 | 核心产出 |
|---|---|---|---|---|
| [[Stage-0-tiny-gpu]] | GPU 热身（可选） | tiny-gpu | 3–5 天 | 一条 LDR 路径图 |
| [[Stage-1-Scalar-Core]] | 单核流水线 | CoralNPU | 2–3 周 | 一条指令的时序图 |
| [[Stage-2-RVV-VME]] | RVV（RISC-V 向量扩展；用于向量与矩阵运算加速） / 矩阵 | CoralNPU | 3–4 周 | RVV/VME（CoralNPU 的矩阵扩展单元；用于 tile 级矩阵运算） 数据流图 |
| [[Stage-3-GPU]] | SIMT（单指令多线程执行模型，一个 warp 的线程共享指令流；用于 GPU 吞吐计算） / GPU（图形处理器，也用于通用并行计算） | Vortex | 4–6 周 | GPU 存储层次 + 性能数据 |
| [[Stage-4-Verification]] | 验证方法学 | CoralNPU + ASIC-Cosim | 2–3 周 | 保真度对照表 |
| [[Stage-5-SDK]] | 软硬件接口 | Clounix-SDK | 1–2 周 | API → 表项调用链 |

> Stage 0 可选：用 `/localdata/linchen/tiny-gpu` 上约 1.3k 行 RTL 的最小 GPU 补齐 Verilog、仿真与 SIMT 基础，不替代 Stage 1。

## 原则

1. **先闭环再扩展**：先把一条指令、一个 kernel（GPU 上并行执行的计算函数；是性能调优的基本单位）、一个测试跑通。
2. **以 RTL 为准**：文档口径不一致时，读 RTL。
3. **每个阶段都要动手改**：加 CSR、加指令、改参数。
4. **每个阶段都要有可观测证据**：trace、波形、周期、日志。
5. **一个概念一个家**：概念放 [[Topics-MOC]]，项目实现放对应 Hub。

## 最小可行闭环

- [ ] tiny-gpu 跑通 `matadd`/`matmul`，保存 trace
- [ ] CoralNPU 跑通 `--instr_trace`
- [ ] 手画 `load` 路径
- [ ] 加一个 CSR（控制状态寄存器；用于配置、异常处理与性能计数）/指令并通过 cocotb（Python 驱动的 RTL 仿真框架；用于模块级功能验证）
- [ ] Vortex 跑 `sgemm`，改 warps（线程束，GPU 中一起执行的线程组；SIMT 的调度单位）/threads
- [ ] ASIC-Cosim 跑一个 feature test，对比 CMODEL（C/C++ 行为级参考模型；用于软件提前开发与结果对照）/RTL

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| RTL | 寄存器传输级硬件描述 | 芯片设计与验证基准 | 与行为级、门级相比，RTL 既可综合又可仿真，是交接的关键抽象 |
| RVV | RISC-V 向量扩展 | 向量与矩阵运算加速 | 与 SIMD 不同，RVV 支持可伸缩的向量长度 |
| VME | CoralNPU 的矩阵扩展单元 | tile 级矩阵运算 | 与 RVV 分工：RVV 管向量，VME 管矩阵 |
| SIMT | 单指令多线程执行模型 | GPU 吞吐计算 | 与 SIMD 相比，SIMT 每线程有独立寄存器与分支状态 |
| GPU | 图形处理器 | 图形与通用并行计算 | 现代 GPU 用大量 warp 隐藏访存延迟 |
| kernel | GPU 并行计算函数 | 性能调优基本单位 | 一个 kernel 内线程按 grid/block 组织 |
| CSR | 控制状态寄存器 | 配置、异常、性能计数 | RISC-V 的 CSR 通过专用指令访问 |
| cocotb | Python 驱动的 RTL 仿真框架 | 模块级功能验证 | 与 UVM 相比上手快，适合小型模块与回归 |
| warp | 线程束 | SIMT 调度单位 | 分支发散会让 warp 内线程串行执行 |
| CMODEL | C/C++ 行为级参考模型 | 软件提前开发与结果对照 | 黄金模型也可能有 bug，需与 RTL 交叉验证 |

## 相关

- [[Four-Projects-Depth-Breadth]]
- [[Learning-Value]]
- [[Verification-Spectrum]]
- [[Multi-Chip-Patterns]]
