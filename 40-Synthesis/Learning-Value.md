---
type: synthesis
aliases: [学习价值, Learning Value]
tags:
  - type/synthesis
  - learning/roadmap
created: 2026-11-10
---

# 学习价值

## 按目标选项目

| 学习目标 | 首选 | 次选 | 理由 |
|---|---|---|---|
| 数字前端/RTL（寄存器传输级设计；芯片实现与仿真的基准）/流水线 | [[CoralNPU]] | [[Vortex]] | CoralNPU 规模可控、文档全、可端到端追踪 |
| 计算机体系结构（顺序核） | [[CoralNPU]] | — | 4 宽、scoreboard（记分板，跟踪寄存器与执行单元就绪状态；用于动态调度）、ROB（重排序缓冲；用于按序提交与精确异常）、RVV（RISC-V 向量扩展；用于向量运算） |
| GPU/SIMT/存储层次 | [[Vortex]] | — | 完整 SIMT（单指令多线程执行模型；用于 GPU 吞吐执行）、cache/MSHR、TCU（张量计算单元；用于矩阵乘加）、DXA |
| 向量/矩阵加速器 | [[CoralNPU]] | [[Vortex]] | RVV + VME（CoralNPU 的矩阵扩展单元；用于 tile 级矩阵加速）；Vortex TCU 更复杂 |
| 性能建模 | [[Vortex]] | [[CoralNPU]] | simx（Vortex 的 C++ 周期近似模拟器；用于快速性能评估） + roofline（屋顶线模型；用于判断 compute-bound 还是 memory-bound） + parity gate |
| 验证方法学 | [[CoralNPU]] + [[ASIC-Cosim]] | [[Vortex]] | 三方 cosim（协同仿真，多个模型同步比对；用于发现模型与 RTL 的偏差）、五后端、SAI（交换机抽象接口；用于交换芯片统一 API）/PTF |
| 软硬件接口/驱动 | [[Clounix-SDK]] | [[CoralNPU]] | API/HAL（硬件抽象层，屏蔽芯片差异；上层 API 的统一实现层）/TOB/DRV/OSAL、user/kernel |
| 多芯片/产品化 | [[Clounix-SDK]] | — | 3 代芯片、HAL/TOB 分层 |

## 推荐路径

```text
CoralNPU（单核 → RVV/VME）
   ↓
Vortex（SIMT → cache → TCU → 性能模型）
   ↓
ASIC-Cosim（五后端 → SAI/PTF → 验证方法学）
   ↓
Clounix-SDK（API → HAL → TOB → 驱动）
```

## 一句话

- **CoralNPU 教你“一颗核怎么工作”。**
- **Vortex 教你“一颗 GPU 怎么工作”。**
- **ASIC-Cosim 教你“怎么证明它工作”。**
- **Clounix-SDK 教你“软件怎么用它”。**

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| RTL | 寄存器传输级设计 | 芯片实现与仿真基准 | 数字前端学习的核心交付物，也是验证的黄金参考 |
| scoreboard | 记分板 | 动态调度与冒险检测 | 与 ROB 分工：scoreboard 管就绪，ROB 管顺序提交 |
| ROB | 重排序缓冲 | 按序提交与精确异常 | 顺序核也能用 ROB 支持乱序执行 |
| RVV | RISC-V 向量扩展 | 向量运算 | 是理解向量后端与数据并行的入口 |
| SIMT | 单指令多线程执行模型 | GPU 吞吐执行 | Vortex 用它展示多 warp 隐藏延迟 |
| TCU | 张量计算单元 | 矩阵乘加 | 与 RVV/VME 对比：GPU 的矩阵加速更通用也更复杂 |
| VME | CoralNPU 的矩阵扩展单元 | tile 级矩阵加速 | 与 RVV 配合，专注矩阵数据流 |
| simx | Vortex 的 C++ 周期近似模拟器 | 快速性能评估 | 与 rtlsim 做 parity，兼顾速度与可信度 |
| roofline | 屋顶线模型 | 判断性能瓶颈 | 用算力与带宽上限定位优化方向 |
| cosim | 协同仿真 | 发现模型与 RTL 的偏差 | 三方 cosim 比两方更容易定位谁错 |
| SAI | 交换机抽象接口 | 交换芯片统一 API | 是理解交换芯片软件栈的关键抽象 |
| HAL | 硬件抽象层 | 屏蔽芯片差异 | 与 TOB 分工：HAL 管芯片，TOB 管表资源 |

## 相关

- [[Roadmap]]
- [[Four-Projects-Depth-Breadth]]
- [[Verification-Spectrum]]
