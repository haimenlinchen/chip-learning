---
type: reference
aliases: [术语表, Glossary]
tags:
  - type/reference
created: 2026-11-10
---

# 术语表

## 体系结构

- **ISA**：指令集架构，软件/硬件契约。
- **SIMT**：单指令多线程，warp 内线程共享 PC。
- **Warp**：SIMT 的线程组，共享 PC、各有寄存器。
- **IPDOM**：分支发散的后支配栈，保存/恢复线程掩码。
- **ROB**：重排序缓冲，保证顺序退休/精确异常。
- **Scoreboard**：跟踪寄存器依赖与在飞指令。
- **RVV**：RISC-V Vector Extension。
- **VLEN/SEW/LMUL**：向量寄存器位宽/元素位宽/寄存器组倍数。
- **VME/Zvt**：CoralNPU 的矩阵扩展。
- **TCU/WGMMA**：Vortex 的张量核/ warpgroup MMA。
- **DXA**：Vortex 的异步拷贝/多播单元（TMA 风格）。
- **RTU**：Vortex 的光追单元（BVH 遍历/求交）。
- **TCM**：紧耦合存储器（scratchpad）。
- **MSHR**：miss status holding register。
- **LLC**：最后一级 cache。
- **AMO**：原子内存操作。
- **TLB/PTW**：地址翻译/页表遍历。
- **LMEM**：Vortex 的 shared memory/local memory。

## 验证

- **Cocotb**：Python 驱动的 RTL 仿真框架。
- **UVM**：Universal Verification Methodology。
- **DPI**：Direct Programming Interface，SystemVerilog 与 C 的接口。
- **CMODEL**：C/C++ 功能模型。
- **EMU**：硬件仿真/PCIe 设备模拟。
- **PTF**：Packet Test Framework。
- **SAI**：Switch Abstraction Interface。
- **RVVI**：RISC-V Verification Interface，lockstep trace。
- **ISG**：Instruction Stream Generator。
- **Parity gate**：模型与 RTL 的一致性门禁。

## 交换芯片

- **CLX API**：Clounix SDK 的对外 API。
- **HAL**：Hardware Abstraction Layer。
- **TOB**：Table Operation Bus，表项操作抽象。
- **DRV**：驱动层（IO/DMA）。
- **OSAL**：OS Abstraction Layer。
- **knet**：内核网络通道。
- **eCPU**：交换 ASIC 内的嵌入式 CPU。
- **NB/KG/ET**：NamchaBarwa / Kawagarbo / Everest。
- **PIE/Slice/MAC/SerDes**：交换芯片的物理/逻辑层级。

## 相关

- [[Paths]]
- [[Commands]]
