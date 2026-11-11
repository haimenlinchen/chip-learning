---
type: moc
aliases: [Chip Vault Home, 芯片学习入口]
tags:
  - type/moc
  - status/learning
created: 2026-11-10
---

# 芯片学习 Vault

> 目标：从 RTL（寄存器传输级，用寄存器与组合逻辑描述硬件的抽象层；用于芯片设计与仿真）/微架构到验证，再到软硬件接口，建立可迁移的芯片理解。

## 从这里开始

- [[Roadmap]] — 五阶段学习路线
- [[Four-Projects-Depth-Breadth]] — 四项目技术深度/广度对比
- [[Projects-MOC]] — 四个项目入口
- [[Topics-MOC]] — 技术主题入口
- [[Learning-MOC]] — 学习阶段入口

## 项目

- [[CoralNPU]] — 开源 RISC-V 边缘 ML NPU IP（NPU：神经网络处理器，专用 AI 推理加速器；用于可穿戴、手机、边缘设备）
- [[Vortex]] — 开源 RISC-V GPGPU 全栈（GPGPU：通用 GPU 计算，用 GPU 做非图形的高吞吐计算；用于并行负载）
- [[Clounix-SDK]] — 交换 ASIC SDK（ASIC：专用集成电路，为特定任务定制的芯片；SDK 用于配置交换芯片、开发驱动）
- [[ASIC-Cosim]] — 交换 ASIC 多保真度协同仿真平台（保真度：模型与硬件行为的一致程度；用于在仿真速度与精度之间取舍）

## 技术主题

- [[ISA-and-Extensions]]
- [[Pipeline-and-Hazards]]
- [[SIMT-and-Warp]]
- [[Vector-Architecture]]
- [[Matrix-Accelerator]]
- [[Cache-and-Memory]]
- [[Scratchpad-and-TCM]]
- [[Verification-Fidelity]]
- [[Software-Interface]]
- [[Performance-Modeling]]

## 架构图

- [[Architecture-Diagrams]]

## 笔记与资产

- [[Code-Reading-Index]]
- [[Experiments-Index]]
- [[Q-A-Index]]
- [[Assets-Index]]

## 学习阶段

- [[Stage-0-tiny-gpu]]
- [[Stage-1-Scalar-Core]]
- [[Stage-2-RVV-VME]]
- [[Stage-3-GPU]]
- [[Stage-4-Verification]]
- [[Stage-5-SDK]]

## 进行中的学习

```dataview
LIST
FROM "30-Learning"
WHERE status != "done"
SORT stage ASC
```

## 最近更新的项目笔记

```dataview
TABLE project, layer, status
FROM #type/atomic
SORT file.mtime DESC
LIMIT 10
```
