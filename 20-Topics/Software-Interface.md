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

软硬件接口是“芯片功能如何暴露给软件”的契约：指令/CSR/寄存器/表项/中断/DMA/命令队列。

## 四种典型接口

| 形态 | 代表 | 特点 |
|---|---|---|
| GPU runtime + 命令队列 | Vortex | host 提交命令 ring，设备异步执行 |
| 裸机 CSR + AXI | CoralNPU | host 写 TCM/CSR，轮询 halted/fault |
| SDK API + HAL + 表项 | Clounix-SDK | `clx_*` API 隐藏寄存器/表项细节 |
| SAI/CLI/PTF | ASIC-Cosim | 标准化交换 API + 测试框架 |

## 关键抽象

- **寄存器/CSR**：单点控制/状态。
- **表项**：交换芯片的 L2/L3/ACL/QoS 表；通过 TOB 抽象。
- **命令队列**：GPU 的 kernel launch/DMA/fence。
- **中断/事件**：完成/错误通知。
- **DMA**：批量数据搬运。
- **内存映射**：TCM/DTCM/CSR/外部空间。

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
