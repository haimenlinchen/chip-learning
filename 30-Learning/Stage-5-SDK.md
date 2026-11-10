---
type: stage
stage: 5
status: todo
projects: [Clounix-SDK]
tags:
  - learning/roadmap
  - stage/sdk
created: 2026-11-10
---

# 阶段五：SDK 软件视角

## 目标

理解芯片功能如何变成软件 API，以及寄存器/表项/中断/DMA 如何暴露给驱动。

## 阅读

- [[Clounix-SDK]]
- [[Clounix-SDK-Layering]]
- [[Clounix-SDK-HAL-TOB]]
- [[Clounix-SDK-MultiChip]]
- [[Clounix-SDK-eCPU]]
- [[Software-Interface]]
- `clounix-sdk-et/clx_sdk/include/clx/`
- `clounix-sdk-et/clx_sdk/src/hal/`
- `clounix-sdk-et/clx_sdk/src/tob/`
- `clounix-sdk-et/app/sdk_sample/sdk_sample_init.c`

## 任务

- [ ] 跟踪 `clx_l2_add → hal_l2 → tob_table → drv → osal`
- [ ] 理解 TOB 如何抽象 SRAM/TCAM/hash/table
- [ ] 理解 HAL 如何隔离 NB/KG/ET
- [ ] 理解 user/kernel 双空间构建
- [ ] 理解 eCPU 固件下载与应用选择

## 产出

- [ ] “一个 L2 表项从 API 到硬件表”的调用链图
- [ ] “寄存器/表项/中断/DMA 如何暴露给驱动”的笔记

## 自检问题

- 哪一层负责芯片差异？哪一层负责 OS 差异？
- 为什么需要 TOB 这一层？
- 37 个模块中哪些是公共逻辑？
- eCPU 与 host SDK 的职责边界？

## 相关

- [[Stage-4-Verification]]
- [[Software-Interface]]
- [[Multi-Chip-Patterns]]
