---
type: atomic
project: Clounix-SDK
layer: system
topic: [ecpu, firmware, boot]
status: learning
source_repo: /localdata/linchen/clounix-sdk-et
source_files:
  - ecpu_fw.mk
tags:
  - layer/software
  - topic/ecpu
created: 2026-11-10
---

# eCPU 固件

## 定义

交换 ASIC 内部带嵌入式 CPU（eCPU），SDK 构建流程会从内部仓库下载 eCPU 固件，并按应用选择/裁剪固件。

## 如何工作

- `ecpu_fw.mk` 定义：
  - `ECPU_APP ?= HeadRoomCounter`
  - `ECPU_FW_DIR ?= $(CLX_SYSTEM_BUILD)/ecpu/`
- `ecpu-fw-latest-version`：查询内部 Artifactory（`proxy.clounix.com`）上最新的 `clx_ecpu_*.tar`。
- `ecpu-fw-download`：下载并解压 `clx_ecpu_*_FW.tar`。
- `ecpu-fw-prune`：根据 `ECPU_APP` 选择固件，删除不需要的 bin，并改写 `default_firmware`。
- `ecpu-fw-app-list`：列出可用应用。

## 关键细节

- 固件选择是构建期行为，依赖内部网络与 Artifactory。
- 固件应用示例：`HeadRoomCounter`。
- eCPU 与 host SDK 的分工：eCPU 跑数据面/控制面固件，host SDK 通过寄存器/表项/DMA 与它交互。

## 在项目中的位置

- 所属项目：[[Clounix-SDK]]
- 相关子系统：[[Clounix-SDK-Layering]]、[[Clounix-SDK-MultiChip]]

## 相关概念

- [[Software-Interface]]

## 自检问题

- eCPU 固件与 host SDK 的职责边界在哪里？
- 为什么固件选择放在构建期而不是运行期？
- 固件与 ASIC 版本的对应关系如何保证？
- eCPU 与 PCIe/knet 数据路径如何交互？

## 来源

- `ecpu_fw.mk`
- `app/sdk_asicsim/`
