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

交换 ASIC（Application-Specific Integrated Circuit，专用集成电路；此处指交换芯片）内部带嵌入式 CPU（eCPU）（芯片内置处理器，运行固件处理控制/数据面任务），SDK（Software Development Kit，软件开发工具包；此处指构建 eCPU 固件与 host 侧库的工具链）构建流程会从内部仓库下载 eCPU 固件（firmware，烧录到设备运行的程序镜像；按应用裁剪后加载到 eCPU），并按应用选择/裁剪固件。

## 如何工作

- `ecpu_fw.mk` 定义：
  - `ECPU_APP ?= HeadRoomCounter`
  - `ECPU_FW_DIR ?= $(CLX_SYSTEM_BUILD)/ecpu/`
- `ecpu-fw-latest-version`：查询内部 Artifactory（制品仓库，存放构建产物与固件包；此处用于查最新固件版本）（`proxy.clounix.com`）上最新的 `clx_ecpu_*.tar`。
- `ecpu-fw-download`：下载并解压 `clx_ecpu_*_FW.tar`。
- `ecpu-fw-prune`：根据 `ECPU_APP` 选择固件，删除不需要的 bin，并改写 `default_firmware`。
- `ecpu-fw-app-list`：列出可用应用。

## 关键细节

- 固件选择是构建期行为，依赖内部网络与 Artifactory。
- 固件应用示例：`HeadRoomCounter`。
- eCPU 与 host SDK 的分工：eCPU 跑数据面（data plane，负责报文转发与查表；对吞吐敏感）/控制面（control plane，负责协议状态与管理配置；对实时性敏感）固件，host SDK 通过寄存器（register，芯片内可读写的配置/状态单元；用于 host 与 eCPU 通信）/表项/DMA（Direct Memory Access，直接内存访问；批量搬移表项或报文数据，减少 CPU 拷贝）与它交互。

## 在项目中的位置

- 所属项目：[[Clounix-SDK]]
- 相关子系统：[[Clounix-SDK-Layering]]、[[Clounix-SDK-MultiChip]]

## 相关概念

- [[Software-Interface]]

## 自检问题

- eCPU 固件与 host SDK 的职责边界在哪里？
- 为什么固件选择放在构建期而不是运行期？
- 固件与 ASIC 版本的对应关系如何保证？
- eCPU 与 PCIe（Peripheral Component Interconnect Express，高速串行总线；连接主机与芯片，承载寄存器/DMA 访问）/knet（Kernel Network，内核网络模块；打通 SDK 与 Linux 协议栈的数据通道）数据路径如何交互？

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| ASIC | 专用集成电路 | 交换芯片本体 | 内置 eCPU 的交换 ASIC 兼具硬件转发与软件可编程性 |
| eCPU | 芯片内置嵌入式 CPU | 运行固件处理控制/数据面任务 | 与 host CPU 分工：eCPU 贴近硬件，host 跑 SDK/协议栈 |
| SDK | 软件开发工具包 | 构建固件与 host 侧库 | 此处 SDK 同时包含固件构建与 host 驱动两部分 |
| 固件 | 设备运行的程序镜像 | eCPU 应用固件 | 固件与应用需版本匹配，裁剪错误会导致功能缺失 |
| Artifactory | 制品仓库 | 下载/管理固件包 | 构建依赖内网，离线环境需预置固件包 |
| 数据面 | 报文转发路径 | 查表、转发、计数 | 与查表算法直接相关，性能要求最高 |
| 控制面 | 协议与管理路径 | 路由协议、配置下发 | 与控制面分离可避免管理流量影响转发性能 |
| 寄存器 | 芯片内配置/状态单元 | host 与 eCPU 通信 | 寄存器读写通常比表项/DMA 更慢，不宜传大数据 |
| DMA | 直接内存访问 | 批量搬移表项/报文 | 需保证内存对齐与 cache 一致性 |
| PCIe | 高速串行总线 | 主机与芯片互联 | 带宽与延迟直接影响 host-eCPU 通信效率 |
| knet | 内核网络模块 | SDK 与 Linux 协议栈互通 | 常用于报文上送与注入，需关注内核态性能开销 |

## 来源

- `ecpu_fw.mk`
- `app/sdk_asicsim/`
