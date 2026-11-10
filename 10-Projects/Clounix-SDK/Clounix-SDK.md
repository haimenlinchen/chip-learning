---
type: project-hub
project: Clounix-SDK
aliases: [clounix-sdk-et, Clounix SDK, 交换 SDK]
status: learning
tags:
  - project/clounix-sdk
  - chip/switch
source_repo: /localdata/linchen/clounix-sdk-et
created: 2026-11-10
---

# Clounix SDK

## 一句话定位

Clounix 交换 ASIC 的软件 SDK：把多代交换芯片的差异压进 HAL/TOB/DRV/OSAL，向上提供统一的 `clx_*` API、CLI 与 RPC。

## 架构骨架

- 芯片：NamchaBarwa（NB）、Kawagarbo（KG）、Everest（ET）；API 文档标注 CLX84/86/88
- 分层：CLX API → HAL → TOB → DRV → OSAL
- API：约 37 个模块（L2/L3/VLAN/MPLS/SRv6/TM/QoS/mirror/meter/LAG/BFD/PTP/telemetry/security/WLAN/VM/STP/SWC/netif/pkt/stat）
- 表项：TOB 抽象 SRAM/TCAM/hash/table
- 系统：user/kernel 双空间、knet、eCPU 固件

## 关键子系统

- [[Clounix-SDK-Layering]]
- [[Clounix-SDK-HAL-TOB]]
- [[Clounix-SDK-MultiChip]]
- [[Clounix-SDK-eCPU]]

## 相关概念

- [[Software-Interface]]
- [[Multi-Chip-Patterns]]
- [[Cache-and-Memory]]（对照表项/缓存抽象）

## 学习阶段

- [[Stage-5-SDK]]

## 代码入口

- `clx_sdk/include/clx/`
- `clx_sdk/src/clx/`
- `clx_sdk/src/hal/`
- `clx_sdk/src/tob/`
- `clx_sdk/src/drv/`
- `clx_sdk/src/osal/`
- `app/sdk_sample/`
- `app/diag_shell/`
- `app/neutrino_server/`

## 实验记录

- [ ] 跟踪 `clx_l2_add` 到硬件表项的调用链
- [ ] 读 TOB 的 entry/bank/field 操作
- [ ] 比较 NB/KG/ET 的 `hal/mt` 差异
- [ ] 理解 user/kernel 两种构建

## 开放问题

- 37 个模块中，哪些是芯片无关的公共逻辑，哪些必须 per-chip 实现？
- TOB 如何屏蔽 SRAM/TCAM/hash 的访问差异？
- eCPU 固件与 host SDK 的职责边界在哪里？

## 来源

- `config.mk`
- `build.mk`
- `clx_sdk/Makefile`
- `clx_sdk/include/clx/`
- `clx_sdk/include/tob/tob.h`
