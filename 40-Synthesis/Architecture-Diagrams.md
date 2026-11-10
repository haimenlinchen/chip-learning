---
type: synthesis
aliases: [架构图索引, Architecture Diagrams]
tags:
  - type/synthesis
created: 2026-11-10
---

# 架构图索引

所有架构图都用 Mermaid（文本描述的图表语言；用于在 Markdown 里画流程图与架构图）写在对应笔记里，Obsidian 可直接渲染。

## CoralNPU

| 图 | 位置 | 内容 |
|---|---|---|
| 顶层架构 | [[CoralNPU#架构图]] | 标量前端 / 标量执行 / RVV（RISC-V 向量扩展；用于向量运算）+VME（CoralNPU 的矩阵扩展单元；用于 tile 级矩阵加速） / TCM（紧耦合存储器，片上低延迟 SRAM；用于指令/数据暂存）+AXI（AMBA 高级可扩展接口总线；用于 SoC 片内高带宽互连） |
| 标量流水线 | [[CoralNPU-Pipeline#架构图]] | Fetch → Decode → Dispatch → Execute → Writeback → ROB（重排序缓冲；用于按序提交与精确异常） |
| RVV 后端 | [[CoralNPU-RVV#架构图]] | CQ → Decode → UQ → RS → VU → VRF → VROB |
| VME 矩阵 | [[CoralNPU-VME#架构图]] | matrix tiles / PE array（处理单元阵列，二维乘加网格；用于矩阵乘加） / accumulator / transpose |
| 存储系统 | [[CoralNPU-Memory#架构图]] | IBus/DBus → crossbar → ITCM/DTCM/CSR/AXI |

## Vortex

| 图 | 位置 | 内容 |
|---|---|---|
| 顶层架构 | [[Vortex#架构图]] | host → CP（命令处理器，从 host 取命令并调度 GPU；用于启动 kernel） → GPU → cluster → L2/L3 → memory |
| SIMT 流水线 | [[Vortex-SIMT#架构图]] | Schedule → Fetch → Decode → Issue → Execute → Commit |
| 存储层次 | [[Vortex-Cache#架构图]] | L1(socket) → L2 → L3 → DRAM + LMEM/MSHR（未命中状态保持寄存器；用于跟踪缓存缺失）/AMO |
| TCU | [[Vortex-TCU#架构图]] | instruction → micro-op → FEDP → accumulator |
| DXA | [[Vortex-DXA#架构图]] | warp issue → cluster queue → worker → GMEM read → SMEM write |
| 命令处理器 | [[Vortex-CommandProcessor#架构图]] | host ring → N engines → KMU/DMA/DCR/event |

## Clounix SDK

| 图 | 位置 | 内容 |
|---|---|---|
| 分层架构 | [[Clounix-SDK#架构图]] | app → CLX API → HAL → TOB → DRV → OSAL → ASIC |
| 分层细节 | [[Clounix-SDK-Layering#架构图]] | app/CLX/HAL/TOB/DRV/OSAL |
| HAL/TOB | [[Clounix-SDK-HAL-TOB#架构图]] | HAL mt / TOB sram/tcam/hash/tbl |
| 多芯片 | [[Clounix-SDK-MultiChip#架构图]] | ENABLED_CHIPS → nb/kg/et → 统一 API |

## ASIC-Cosim

| 图 | 位置 | 内容 |
|---|---|---|
| 五后端 | [[ASIC-Cosim#架构图]] | tests → control plane → CMODEL（C/C++ 行为级参考模型；用于软件提前开发与结果对照）/EMU（硬件仿真加速器；用于大规模系统验证）/RTL/LAB/NOMODEL |
| 五后端细节 | [[ASIC-Cosim-Five-Backends#架构图]] | 同一测试语料 + 五种执行环境 |
| C-model 流水线 | [[ASIC-Cosim-CMODEL#架构图]] | IGR → PP/PL → TM → PCX → EGR |
| RTL DPI | [[ASIC-Cosim-RTL-DPI#架构图]] | cosim（协同仿真，多个模型同步运行并比对；用于发现模型与 RTL 的偏差） ↔ RTL 的寄存器/包/回调 |

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| Mermaid | 文本描述的图表语言 | 在 Markdown 里画流程图与架构图 | Obsidian 原生渲染，适合把图与笔记放在一起版本化 |
| RVV | RISC-V 向量扩展 | 向量运算 | 与 VME 分工：RVV 处理通用向量，VME 处理矩阵 |
| VME | CoralNPU 的矩阵扩展单元 | tile 级矩阵加速 | 图中与 RVV 并列，但数据通路独立 |
| TCM | 紧耦合存储器 | 指令/数据暂存 | 与 cache 不同，TCM 地址空间由软件显式管理 |
| AXI | AMBA 高级可扩展接口 | SoC 片内高带宽互连 | 图中连接 TCM 与外部总线，是访存主通路 |
| ROB | 重排序缓冲 | 按序提交与精确异常 | 流水线图中的最后一站，决定退休顺序 |
| PE array | 处理单元阵列 | 矩阵乘加 | VME 的吞吐核心，形状决定并行度 |
| CP | 命令处理器 | 启动 kernel 与调度 GPU | host 通过命令队列/ring 与 CP 交互 |
| MSHR | 未命中状态保持寄存器 | 跟踪缓存缺失 | 与 AMO 一起影响 cache 一致性与原子操作 |
| CMODEL | C/C++ 行为级参考模型 | 软件提前开发与结果对照 | 五后端中最便宜、最快的一档 |
| EMU | 硬件仿真加速器 | 大规模系统验证 | 比 RTL 仿真快，适合跑驱动与系统软件 |
| cosim | 协同仿真 | 发现模型与 RTL 的偏差 | DPI 是把 C/C++ 模型接入 RTL 仿真的常用手段 |

## 相关

- [[Projects-MOC]]
- [[Topics-MOC]]
- [[Four-Projects-Depth-Breadth]]
