---
type: moc
aliases: [Topics MOC, 技术主题索引]
tags:
  - type/moc
created: 2026-11-10
---

# 技术主题索引

## ISA 与执行模型

- [[ISA-and-Extensions]]（ISA：指令集架构，软件与硬件的契约；用于理解扩展与兼容性）
- [[Pipeline-and-Hazards]]
- [[SIMT-and-Warp]]（SIMT：单指令多线程，warp 内线程共享 PC；用于 GPU 线程执行模型）
- [[Vector-Architecture]]（向量架构；RVV 等向量扩展的基础，用于数据并行计算）
- [[Matrix-Accelerator]]（矩阵加速器；NPU/TCU 等专用单元，用于矩阵乘加速）

## 存储与数据通路

- [[Cache-and-Memory]]（Cache：缓存，位于 CPU 与主存之间的高速存储；用于降低访存延迟）
- [[Scratchpad-and-TCM]]（TCM：紧耦合存储器，靠近核的片上存储；用于低延迟数据访问）

## 验证与仿真

- [[Verification-Fidelity]]（保真度：模型与硬件行为的一致程度；用于在验证速度与精度之间取舍）
- [[Performance-Modeling]]

## 软硬件接口

- [[Software-Interface]]（软硬件接口；API/HAL/驱动分层，用于连接软件与芯片）

## 按层级查看

```dataview
TABLE project, status
FROM #type/atomic
GROUP BY layer
```

## 按项目查看

```dataview
TABLE layer, status
FROM #type/atomic
GROUP BY project
```
