---
type: atomic
project: Clounix-SDK
layer: software
topic: [multi-chip, hal, portability]
status: learning
source_repo: /localdata/linchen/clounix-sdk-et
source_files:
  - config.mk
  - clx_sdk/src/hal/mt/
  - clx_sdk/src/drv/mt/
  - clx_sdk/src/tob/mt/
tags:
  - layer/software
  - topic/multi-chip
created: 2026-11-10
---

# 多芯片抽象

## 定义

SDK 用“统一 API + 分层 mt 目录”支持多代交换芯片：NamchaBarwa（NB）、Kawagarbo（KG）、Everest（ET），API 文档标注 CLX84/86/88。

## 如何工作

- `config.mk`：`ENABLED_CHIPS := namchabarwa kawagarbo everest`。
- 芯片差异下沉三层：
  - `hal/mt/{nb,kg,et}`：功能语义差异。
  - `drv/mt/{nb,kg,et}`：IO/DMA 差异。
  - `tob/mt/{sram,tcam,hash,tbl}`：表项访问差异。
- `clx_cfg.h`：`CLX_CFG_MAXIMUM_CHIPS_PER_SYSTEM = 2`、`CLX_CFG_MAXIMUM_CORES_PER_CHIP = 4`。
- 构建期通过 `ENABLED_CHIPS` 选择芯片；运行期通过 `unit`/`inst_idx` 区分实例。

## 关键细节

- 多芯片系统里，SDK 需要处理跨芯片的端口、LAG、L2/L3 多播索引偏移。
- `clx_cfg` 提供端口 lane/polarity、L2/L3 表大小、DMA 队列、统计轮询等配置。
- `hal/mt/common` 放跨芯片公共逻辑，避免每个芯片重复实现。
- `mock` 目录支持无硬件/单元测试。

## 在项目中的位置

- 所属项目：[[Clounix-SDK]]
- 相关子系统：[[Clounix-SDK-Layering]]、[[Clounix-SDK-HAL-TOB]]

## 相关概念

- [[Multi-Chip-Patterns]]
- [[Software-Interface]]

## 自检问题

- 三代芯片的差异分别落在 HAL、DRV、TOB 的哪些文件？
- 哪些逻辑应该放 `mt/common`，哪些必须 per-chip？
- 多芯片系统的索引偏移如何处理？
- 构建期选择 vs 运行期选择各有什么取舍？

## 来源

- `config.mk`
- `clx_sdk/src/hal/mt/`
- `clx_sdk/src/drv/mt/`
- `clx_sdk/src/tob/mt/`
