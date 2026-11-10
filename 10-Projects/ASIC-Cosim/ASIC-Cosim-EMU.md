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

EMU（Emulation，硬件仿真平台；用于流片前跑驱动与系统级软件）用 PCIe（Peripheral Component Interconnect Express，高速串行外设总线；用于主机与设备互联）设备模拟 + knet（内核态网络数据路径，把仿真设备挂到主机网络栈；用于主机与仿真设备间收发报文）把 ASIC（专用集成电路，为特定任务定制的芯片；用于交换、网络等大批量场景）模型的寄存器/包路径暴露给主机内核，用于验证驱动、PCIe、中断和 DMA（Direct Memory Access，直接内存访问；用于设备与内存间无 CPU 搬运数据）。

## 如何工作

- `clxsim_emu_t` 继承 `clxsim_rtl_t`，复用 RTL（Register Transfer Level，寄存器传输级硬件描述；用于周期精确仿真）的寄存器/包接口。
- PCIe：模拟 vendor/device ID（`NB_VENDOR_DEVICE_ID`），BAR（Base Address Register，PCIe 设备基址寄存器；用于把设备寄存器/内存映射到主机地址空间）映射，PCIe 读写。
- DMA：`pdma_ring_base`、`kg_descriptor_t`（descriptor，描述符，描述一次 DMA 传输的元数据；用于队列化收发）、RX/TX 队列、`buffer_size`。
- FIFO（First In First Out，先进先出缓冲队列；用于报文/描述符排队）：learning FIFO（MAC 地址学习队列，记录源 MAC 与端口的映射；用于二层转发表同步，49152×32B）、IOAM FIFO（IOAM，In-situ Operations, Administration, and Maintenance，随流带内运维信息；用于网络遥测，65535×20B）、NFE FIFO（49932×84B）。
- 包：最大 10200B，默认 MTU（Maximum Transmission Unit，最大传输单元；用于限制单帧报文长度）9216。
- 中断：`intr_handler_f` 回调，IRQ（Interrupt Request，硬件中断请求；用于通知主机驱动处理事件）注入。

## 关键细节

- EMU 比 CMODEL（C/C++ 功能模型，用软件模拟芯片行为；用于早期软件开发和回归）多出“内核/PCIe/中断”路径，所以能暴露驱动类问题。
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

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| EMU | 硬件仿真平台 | 驱动、PCIe、中断、DMA 验证 | 比 RTL 快但比 CMODEL 慢，胜在系统路径完整 |
| PCIe | 高速串行外设总线 | 主机与设备互联 | 设备模拟需正确实现配置空间与 BAR |
| knet | 内核态网络数据路径 | 主机与仿真设备间收发报文 | 依赖内核网络栈，常需 TUN 设备配合 |
| ASIC | 专用集成电路 | 交换、网络等大批量场景 | 仿真目标是让软件在流片前跑起来 |
| DMA | 直接内存访问 | 设备与内存间无 CPU 搬运数据 | 描述符环的完整性直接影响收发正确性 |
| RTL | 寄存器传输级硬件描述 | 周期精确仿真 | EMU 复用 RTL 的寄存器/包接口 |
| BAR | PCIe 设备基址寄存器 | 把设备寄存器/内存映射到主机地址空间 | BAR 大小与类型错误是驱动枚举失败常见原因 |
| descriptor | 描述符 | 队列化收发 | 描述一次 DMA 传输的地址、长度与状态 |
| FIFO | 先进先出缓冲队列 | 报文/描述符排队 | 深度不足会导致突发流量丢包 |
| learning FIFO | MAC 地址学习队列 | 二层转发表同步 | 学习结果需及时同步给软件面 |
| IOAM | 随流带内运维信息 | 网络遥测 | 在报文路径中携带逐跳统计信息 |
| MTU | 最大传输单元 | 限制单帧报文长度 | 仿真默认 9216，接近 10200B 上限 |
| IRQ | 硬件中断请求 | 通知主机驱动处理事件 | 中断注入时序错误会导致驱动超时 |
| CMODEL | C/C++ 功能模型 | 早期软件开发、回归测试 | 缺少内核/PCIe 路径，看不到驱动类问题 |

## 来源

- `src/cosim/emu/emu.h`
- `src/cosim/emu/`
