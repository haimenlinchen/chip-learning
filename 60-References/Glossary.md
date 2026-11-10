---
type: reference
aliases: [术语表, Glossary]
tags:
  - type/reference
created: 2026-11-10
---

# 术语表

## 体系结构

- **ISA**：指令集架构，软件/硬件契约（用于定义软硬件兼容边界）。
- **SIMT**：单指令多线程，warp 内线程共享 PC（用于 GPU 线程执行模型）。
- **Warp**：SIMT 的线程组，共享 PC、各有寄存器（用于 warp 级调度与分支处理）。
- **IPDOM**：分支发散的后支配栈，保存/恢复线程掩码（用于处理分支发散）。
- **ROB**：重排序缓冲，保证顺序退休/精确异常（用于乱序执行恢复）。
- **Scoreboard**：跟踪寄存器依赖与在飞指令（用于动态调度）。
- **RVV**：RISC-V Vector Extension（RISC-V 向量扩展；用于向量/矩阵计算）。
- **VLEN/SEW/LMUL**：向量寄存器位宽/元素位宽/寄存器组倍数（用于配置向量指令的宽度与分组）。
- **VME/Zvt**：CoralNPU 的矩阵扩展（用于矩阵/tile 计算）。
- **TCU/WGMMA**：Vortex 的张量核/ warpgroup MMA（用于 GPU 矩阵乘加速）。
- **DXA**：Vortex 的异步拷贝/多播单元（TMA 风格；用于异步数据搬运与多播）。
- **RTU**：Vortex 的光追单元（BVH 遍历/求交；用于光线追踪）。
- **TCM**：紧耦合存储器（scratchpad；用作低延迟片上存储）。
- **MSHR**：miss status holding register（记录未完成 cache miss；用于支持多个 outstanding miss）。
- **LLC**：最后一级 cache（用于降低内存访问延迟）。
- **AMO**：原子内存操作（用于多线程同步与原子计数）。
- **TLB/PTW**：地址翻译/页表遍历（用于虚拟地址翻译）。
- **LMEM**：Vortex 的 shared memory/local memory（用于 warp 间数据共享）。

## 验证

- **Cocotb**：Python 驱动的 RTL 仿真框架（用于模块级功能验证）。
- **UVM**：Universal Verification Methodology（通用验证方法学；用于搭建可复用验证平台）。
- **DPI**：Direct Programming Interface，SystemVerilog 与 C 的接口（用于 RTL 与 C/C++ 协同仿真）。
- **CMODEL**：C/C++ 功能模型（用于快速功能验证与参考模型）。
- **EMU**：硬件仿真/PCIe 设备模拟（用于接近实速的系统级验证）。
- **PTF**：Packet Test Framework（报文测试框架；用于交换机数据面测试）。
- **SAI**：Switch Abstraction Interface（交换抽象接口；用于统一交换芯片 API）。
- **RVVI**：RISC-V Verification Interface，lockstep trace（用于 RTL 与模型逐步对比）。
- **ISG**：Instruction Stream Generator（指令流生成器；用于生成随机测试指令）。
- **Parity gate**：模型与 RTL 的一致性门禁（用于拦截模型/RTL 不一致）。

## 交换芯片

- **CLX API**：Clounix SDK 的对外 API（用于配置交换芯片）。
- **HAL**：Hardware Abstraction Layer（硬件抽象层；用于屏蔽底层硬件差异）。
- **TOB**：Table Operation Bus，表项操作抽象（用于表项读写）。
- **DRV**：驱动层（IO/DMA；用于寄存器与数据搬运）。
- **OSAL**：OS Abstraction Layer（操作系统抽象层；用于跨 OS 适配）。
- **knet**：内核网络通道（用于内核态收发包）。
- **eCPU**：交换 ASIC 内的嵌入式 CPU（用于运行控制面固件）。
- **NB/KG/ET**：NamchaBarwa / Kawagarbo / Everest（代表不同交换芯片平台）。
- **PIE/Slice/MAC/SerDes**：交换芯片的物理/逻辑层级（用于描述芯片组成）。

## 相关

- [[Paths]]
- [[Commands]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| ISA | 指令集架构 | 软硬件契约 | 与微架构分离：同一 ISA 可有多种实现 |
| SIMT | 单指令多线程 | GPU 执行模型 | 与 SIMD 对比：线程级并行 |
| RVV | RISC-V 向量扩展 | 向量/矩阵计算 | 与 VME 对比：通用向量 vs 专用矩阵 |
| ROB | 重排序缓冲 | 乱序执行与精确异常 | 与 scoreboard 配合使用 |
| TCM | 紧耦合存储器 | 低延迟片上数据 | 与 cache 对比：软件管理 |
| Cocotb | Python RTL 仿真框架 | 模块级功能验证 | 与 UVM 对比：轻量 vs 完整方法学 |
| UVM | 通用验证方法学 | 可复用验证平台 | 与 cocotb 互补 |
| CMODEL | C/C++ 功能模型 | 快速功能验证 | 与 RTL 构成 parity gate |
| HAL | 硬件抽象层 | 屏蔽底层差异 | 位于 API 与驱动之间 |
| TOB | 表操作总线 | 表项读写抽象 | 交换芯片 SDK 的核心 |
