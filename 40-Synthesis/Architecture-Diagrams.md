---
type: synthesis
aliases: [架构图索引, Architecture Diagrams]
tags:
  - type/synthesis
created: 2026-11-10
---

# 架构图索引

所有架构图都用 Mermaid 写在对应笔记里，Obsidian 可直接渲染。

## CoralNPU

| 图 | 位置 | 内容 |
|---|---|---|
| 顶层架构 | [[CoralNPU#架构图]] | 标量前端 / 标量执行 / RVV+VME / TCM+AXI |
| 标量流水线 | [[CoralNPU-Pipeline#架构图]] | Fetch → Decode → Dispatch → Execute → Writeback → ROB |
| RVV 后端 | [[CoralNPU-RVV#架构图]] | CQ → Decode → UQ → RS → VU → VRF → VROB |
| VME 矩阵 | [[CoralNPU-VME#架构图]] | matrix tiles / PE array / accumulator / transpose |
| 存储系统 | [[CoralNPU-Memory#架构图]] | IBus/DBus → crossbar → ITCM/DTCM/CSR/AXI |

## Vortex

| 图 | 位置 | 内容 |
|---|---|---|
| 顶层架构 | [[Vortex#架构图]] | host → CP → GPU → cluster → L2/L3 → memory |
| SIMT 流水线 | [[Vortex-SIMT#架构图]] | Schedule → Fetch → Decode → Issue → Execute → Commit |
| 存储层次 | [[Vortex-Cache#架构图]] | L1(socket) → L2 → L3 → DRAM + LMEM/MSHR/AMO |
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
| 五后端 | [[ASIC-Cosim#架构图]] | tests → control plane → CMODEL/EMU/RTL/LAB/NOMODEL |
| 五后端细节 | [[ASIC-Cosim-Five-Backends#架构图]] | 同一测试语料 + 五种执行环境 |
| C-model 流水线 | [[ASIC-Cosim-CMODEL#架构图]] | IGR → PP/PL → TM → PCX → EGR |
| RTL DPI | [[ASIC-Cosim-RTL-DPI#架构图]] | cosim ↔ RTL 的寄存器/包/回调 |

## 相关

- [[Projects-MOC]]
- [[Topics-MOC]]
- [[Four-Projects-Depth-Breadth]]
