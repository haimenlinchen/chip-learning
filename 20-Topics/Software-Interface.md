---
type: atomic
layer: software
topic: [api, driver, runtime, hal, sai]
status: learning
tags:
  - layer/software
  - topic/software-interface
created: 2026-11-10
---

# 软硬件接口

## 定义

软硬件接口是“芯片功能如何暴露给软件”的契约：指令/CSR（Control and Status Register，控制状态寄存器；软件配置硬件、读取状态的入口）/寄存器/表项（table entry，交换/查找表的一条记录；通过读写表项控制转发行为）/中断（interrupt，硬件异步通知 CPU 的事件；用于完成/错误上报）/DMA（Direct Memory Access，直接内存访问；不占 CPU 的批量数据搬运）/命令队列（command queue，host 提交命令、设备异步取执行的队列）。

## 四种典型接口

| 形态 | 代表 | 特点 |
|---|---|---|
| GPU runtime（运行时，用户态驱动库；负责命令提交、内存管理与同步）+ 命令队列 | Vortex | host 提交命令 ring，设备异步执行 |
| 裸机（bare-metal，无操作系统直接操作硬件；常见于 MCU/NPU 固件）CSR + AXI（Advanced eXtensible Interface，AMBA 总线协议；片上高带宽主从接口） | CoralNPU | host 写 TCM/CSR，轮询 halted/fault |
| SDK API + HAL（Hardware Abstraction Layer，硬件抽象层；屏蔽不同芯片的寄存器差异）+ 表项 | Clounix-SDK | `clx_*` API 隐藏寄存器/表项细节 |
| SAI（Switch Abstraction Interface，交换机抽象接口；标准化交换芯片 API）/CLI/PTF（Packet Test Framework，数据包测试框架；网络设备自动化测试） | ASIC-Cosim | 标准化交换 API + 测试框架 |

## 关键抽象

- **寄存器/CSR**：单点控制/状态。
- **表项**：交换芯片的 L2/L3/ACL/QoS 表；通过 TOB（Table Object，表项抽象对象；Clounix SDK 中统一管理表项）抽象。
- **命令队列**：GPU 的 kernel launch/DMA/fence。
- **中断/事件**：完成/错误通知。
- **DMA**：批量数据搬运。
- **内存映射**（memory-mapped I/O，把寄存器/存储映射到地址空间；软件用 load/store 访问）：TCM/DTCM/CSR/外部空间。

## 设计问题

- 哪些操作同步、哪些异步？
- 错误如何上报（中断/状态寄存器/异常）？
- 多实例/多芯片如何寻址？
- 软件如何知道硬件版本/能力？
- 驱动在用户态还是内核态？

## 在项目中的体现

- [[Vortex-CommandProcessor]]
- [[CoralNPU-Memory]]
- [[Clounix-SDK-Layering]]
- [[ASIC-Cosim-SAI-PTF]]

## 相关概念

- [[Cache-and-Memory]]
- [[Verification-Fidelity]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| CSR | 控制状态寄存器 | 配置硬件、读取状态 | 与内存映射寄存器常统一编址 |
| 表项 | 交换/查找表的一条记录 | 转发、ACL、QoS | 表项抽象需兼顾批量与单条更新 |
| 中断 | 硬件异步通知 CPU 的事件 | 完成/错误上报 | 与轮询相比延迟低但开销高 |
| DMA | 不占 CPU 的批量数据搬运 | 大块数据传输 | 需处理地址翻译与一致性 |
| 命令队列 | host 提交、设备异步取执行的队列 | GPU、加速器 | ring 结构便于并发与批处理 |
| runtime | 用户态驱动库 | 命令提交、内存管理 | 与内核驱动分工需明确 |
| 裸机 | 无 OS 直接操作硬件 | MCU/NPU 固件 | 启动快，但缺少资源隔离 |
| AXI | AMBA 高带宽片上总线协议 | 主从设备互连 | 与 CSR/TCM 访问常共用总线 |
| HAL | 硬件抽象层 | 多芯片 SDK | 屏蔽寄存器差异，便于移植 |
| SAI | 交换机抽象接口 | 交换芯片标准化 | 与 SAI/CLI/PTF 组合成测试栈 |
| PTF | 数据包测试框架 | 网络设备自动化测试 | 关注包级行为而非寄存器 |
| TOB | 表项抽象对象 | Clounix SDK | 统一表项生命周期管理 |
| 内存映射 | 把寄存器/存储映射到地址空间 | 驱动访问硬件 | 需区分强序与弱序访问 |
