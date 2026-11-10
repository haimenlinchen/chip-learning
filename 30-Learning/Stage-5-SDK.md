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

理解芯片功能如何变成软件 API（应用程序编程接口；软件调用硬件能力的入口），以及寄存器（芯片内可读写的配置/状态单元；用于控制与状态查询）/表项/中断/DMA（直接内存访问，外设绕开 CPU 搬运数据；用于高吞吐收发与卸载）如何暴露给驱动。

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
- [ ] 理解 TOB（表项对象层，统一抽象 SRAM/TCAM/hash 等表资源；用于屏蔽底层表实现） 如何抽象 SRAM（静态随机存储器，片上高速存储；用于表项与缓存）/TCAM（三态内容寻址存储器，支持掩码匹配；用于 ACL 与路由查找）/hash（哈希表，按键值快速查找；用于转发表与流表）/table
- [ ] 理解 HAL（硬件抽象层，屏蔽芯片差异；上层 API 的统一实现层） 如何隔离 NB/KG/ET（Clounix 三代交换芯片代号；HAL 按代隔离差异）
- [ ] 理解 user/kernel（用户态与内核态；SDK 同时构建两种运行环境） 双空间构建
- [ ] 理解 eCPU（嵌入式 CPU，芯片内管理面处理器；用于运行固件与卸载控制面任务） 固件下载与应用选择

## 产出

- [ ] “一个 L2 表项从 API 到硬件表”的调用链图
- [ ] “寄存器/表项/中断/DMA 如何暴露给驱动”的笔记

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| API | 应用程序编程接口 | 软件调用硬件能力 | 好的 API 让上层不感知芯片代际差异 |
| 寄存器 | 芯片内可读写的配置/状态单元 | 控制与状态查询 | 寄存器访问通常由 HAL/DRV 封装，不直接暴露给应用 |
| DMA | 直接内存访问 | 高吞吐收发与卸载 | DMA 描述符与中断配合，减少 CPU 拷贝 |
| TOB | 表项对象层 | 屏蔽底层表实现 | 统一抽象 SRAM/TCAM/hash，便于上层按表项编程 |
| SRAM | 静态随机存储器 | 表项与缓存 | 片上 SRAM 带宽高但容量有限，需合理分区 |
| TCAM | 三态内容寻址存储器 | ACL 与路由查找 | 支持掩码匹配，但面积与功耗高于普通 SRAM |
| hash | 哈希表 | 转发表与流表 | 冲突处理方式影响查找确定性与最坏延迟 |
| HAL | 硬件抽象层 | 屏蔽芯片差异 | 与 TOB 分工：HAL 管芯片，TOB 管表资源 |
| NB/KG/ET | Clounix 三代交换芯片代号 | HAL 按代隔离差异 | 多代芯片共用上层 API，差异下沉到 hal/mt |
| user/kernel | 用户态与内核态 | SDK 同时构建两种运行环境 | 内核态负责硬件访问，用户态提供易用接口 |
| eCPU | 嵌入式 CPU | 运行固件与卸载控制面任务 | 与 host SDK 分工：eCPU 管芯片内控制面 |

## 自检问题

- 哪一层负责芯片差异？哪一层负责 OS 差异？
- 为什么需要 TOB 这一层？
- 37 个模块中哪些是公共逻辑？
- eCPU 与 host SDK 的职责边界？

## 相关

- [[Stage-4-Verification]]
- [[Software-Interface]]
- [[Multi-Chip-Patterns]]
