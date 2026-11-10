---
type: atomic
project: Clounix-SDK
layer: software
topic: [api, hal, tob, drv, osal]
status: learning
source_repo: /localdata/linchen/clounix-sdk-et
source_files:
  - clx_sdk/Makefile
  - config.mk
  - build.mk
tags:
  - layer/software
  - topic/sdk-layering
created: 2026-11-10
---

# Clounix SDK 分层

## 定义

SDK 采用典型的交换芯片软件分层：CLX API → HAL → TOB → DRV → OSAL，向上提供统一的 `clx_*` 接口，向下屏蔽芯片/总线/OS 差异。

## 如何工作

```text
app/        diag_shell · neutrino_server(RPC) · sdk_sample · sdk_ref · sdk_asicsim · sdk_phy_lib
   ↓
CLX API     ~37 个模块：L2/L3/VLAN/MPLS/SRv6/TM/QoS/mirror/meter/LAG/BFD/PTP/
            telemetry/security/WLAN/VM/STP/SWC/netif/pkt/stat ...
   ↓
HAL         hal_*.c，含 hal/mt/{nb,kg,et} 芯片特化、mock
   ↓
TOB         Table Operation Bus：SRAM/TCAM/hash/tbl，支持 instance 广播
   ↓
DRV         drv_io / drv_dma，含 drv/mt/{nb,kg,et}
   ↓
OSAL        linux_user / linux_kernel / knet
   ↓
ASIC        NamchaBarwa(NB) / Kawagarbo(KG) / Everest(ET)
```

## 关键细节

- `WORK_SPACE` 可切 `USER_SPACE` / `KERNEL_SPACE`；用户态产出 `libclx_sdk.so`，内核态产出 `clx_dev.ko`/`clx_sdk.ko`。
- `BUILD_LIST` 默认包含 `CLX_SDK` + `SDK_REF`；`asicsim` 目标只构建 `SDK_ASICSIM`。
- `app/sdk_sample` 是最小初始化示例；`app/sdk_ref` 是参考应用；`app/diag_shell` 是诊断 CLI。
- `clx_cfg` 暴露大量运行时配置：端口、L2/L3 表大小、线程优先级、DMA 队列、统计轮询等。

## 在项目中的位置

- 所属项目：[[Clounix-SDK]]
- 相关子系统：[[Clounix-SDK-HAL-TOB]]、[[Clounix-SDK-MultiChip]]、[[Clounix-SDK-eCPU]]

## 相关概念

- [[Software-Interface]]

## 自检问题

- 哪一层负责芯片差异？哪一层负责 OS 差异？
- 为什么需要 TOB 这一层，而不是 HAL 直接访问寄存器？
- user/kernel 两种构建的边界在哪里？
- `clx_cfg` 的配置如何传到 HAL/TOB？

## 来源

- `clx_sdk/Makefile`
- `config.mk`
- `build.mk`
