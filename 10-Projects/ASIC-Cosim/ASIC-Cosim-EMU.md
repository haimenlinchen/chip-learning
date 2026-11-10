---
type: atomic
project: ASIC-Cosim
layer: verification
topic: [emu, pcie, knet, dma]
status: learning
source_repo: /localdata/linchen/asic-cosim
source_files:
  - src/cosim/emu/emu.h
  - src/cosim/emu/emu_dma.cpp
tags:
  - layer/verification
  - topic/emu
created: 2026-11-10
---

# EMU 后端

## 定义

EMU 用 PCIe 设备模拟 + knet 把 ASIC 模型的寄存器/包路径暴露给主机内核，用于验证驱动、PCIe、中断和 DMA。

## 如何工作

- `clxsim_emu_t` 继承 `clxsim_rtl_t`，复用 RTL 的寄存器/包接口。
- PCIe：模拟 vendor/device ID（`NB_VENDOR_DEVICE_ID`），BAR 映射，PCIe 读写。
- DMA：`pdma_ring_base`、`kg_descriptor_t`、RX/TX 队列、`buffer_size`。
- FIFO：learning FIFO（49152×32B）、IOAM FIFO（65535×20B）、NFE FIFO（49932×84B）。
- 包：最大 10200B，默认 MTU 9216。
- 中断：`intr_handler_f` 回调，IRQ 注入。

## 关键细节

- EMU 比 CMODEL 多出“内核/PCIe/中断”路径，所以能暴露驱动类问题。
- 比 RTL 快，但不如 CMODEL 快。
- 需要 `/dev/net/tun`、PCIe 资源、root 权限。

## 在项目中的位置

- 所属项目：[[ASIC-Cosim]]
- 相关子系统：[[ASIC-Cosim-Five-Backends]]、[[ASIC-Cosim-RTL-DPI]]

## 相关概念

- [[Verification-Fidelity]]
- [[Software-Interface]]

## 自检问题

- 哪些问题只在 EMU 暴露，而 CMODEL 看不到？
- DMA ring 的 descriptor 生命周期如何管理？
- learning/IOAM/NFE FIFO 各自服务什么功能？
- EMU 与真实 PCIe 设备的差异在哪里？

## 来源

- `src/cosim/emu/emu.h`
- `src/cosim/emu/`
