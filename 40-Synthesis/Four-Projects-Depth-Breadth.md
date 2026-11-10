---
type: synthesis
aliases: [四项目深度广度对比, Depth and Breadth]
tags:
  - type/synthesis
  - layer/microarch
created: 2026-11-10
---

# 四项目技术深度与广度

## 两个尺子

- **技术深度**：从接口往下钻了多少层，以及单层机制有多复杂。
- **技术广度**：横向覆盖了多少类技术、子系统、工作负载、芯片与验证手段。

## 技术层覆盖图

● = 核心覆盖，◐ = 部分覆盖，○ = 基本不涉及。

| 技术层 | Vortex | CoralNPU | clounix-sdk-et | asic-cosim |
|---|---|---|---|---|
| 应用/工作负载 | ● ML、图形、光追、HPC（高性能计算，算力密集的科学与工程计算；用于衡量 GPU 的通用计算广度） | ◐ 边缘 ML、DSP | ● L2–L7 交换 | ● 交换芯片功能/包测试 |
| 编程接口 | ● OpenCL（跨平台并行计算 API；用于 GPU/加速器通用计算）/Vulkan/HIP | ◐ RVV（RISC-V 向量扩展；用于向量化编程） intrinsics、LiteRT | ● clx API、CLI、RPC | ● SAI（交换机抽象接口，定义交换芯片统一 API；用于多厂商交换机）-Thrift、PTF（包测试框架，构造与校验报文；用于交换芯片功能测试）、CLI |
| 指令集/执行模型 | ● SIMT（单指令多线程执行模型；用于 GPU 吞吐执行） + 自定义扩展 | ● RV32 + RVV + Zvt（RISC-V 自定义矩阵扩展；CoralNPU 的 tile 级加速） | ○ | ○ |
| 微架构 | ● warp/TCU/RTU/图形 | ● 4 宽 + RVV + VME | ○（查表/转发流水线） | ○（模型级） |
| RTL（寄存器传输级设计；芯片实现与仿真的基准）/模型 | ● SystemVerilog RTL | ● Chisel（基于 Scala 的硬件构造语言；生成 Verilog，用于参数化设计） + SV | ○ | ● C-model + RTL DPI（直接编程接口，连接 SystemVerilog 与 C/C++；用于 cosim 与参考模型集成） |
| 存储/表项 | ● cache/VM/LMEM | ◐ TCM（紧耦合存储器，片上低延迟 SRAM；用于暂存指令/数据） | ● SRAM/TCAM/hash | ◐ 模型内存/backdoor |
| 系统/多芯片 | ● 多核/cluster/PCIe（高速串行外设总线；用于主机与加速卡互连） | ◐ 单核 AXI/TL-UL | ● user/kernel、3 代芯片 | ● 5 种执行后端 |
| 验证 | ● simx/rtlsim/FPGA | ● cocotb/UVM/三方 cosim | ◐ mock/asicsim | ● 5 后端 + SAI/PTF |

## 分轴排序

### 三条纵深轴

| 纵深类型 | 排序 | 理由 |
|---|---|---|
| 计算/芯片微架构纵深 | Vortex ≈ CoralNPU > asic-cosim > clounix-sdk-et | 前两者有 ISA + 微架构 + RTL；cosim 只到模型/DPI；SDK 不碰微架构 |
| 系统软件纵深 | clounix-sdk-et > asic-cosim > Vortex > CoralNPU | SDK 有 API/HAL/TOB/DRV/OSAL + user/kernel；cosim 有 SAI/PTF/CLI；Vortex 有 runtime/driver；CoralNPU 是裸机 |
| 验证技术纵深 | CoralNPU ≈ asic-cosim > Vortex > clounix-sdk-et | CoralNPU 有三方 cosim/RVVI/ISG；cosim 有五后端/SAI/PTF；Vortex 有 simx parity；SDK 主要靠 mock/asicsim |

### 两条广度轴

| 广度类型 | 排序 | 理由 |
|---|---|---|
| 功能/工作负载广度 | clounix-sdk-et > Vortex > asic-cosim > CoralNPU | SDK 覆盖 L2–L7；Vortex 覆盖 ML/图形/光追/HPC；cosim 覆盖多种验证形态；CoralNPU 聚焦边缘 ML/DSP |
| 技术栈覆盖广度 | Vortex > asic-cosim > clounix-sdk-et > CoralNPU | Vortex 从应用到验证全填；cosim 覆盖验证+系统；SDK 覆盖软件/系统；CoralNPU 集中在执行+验证 |

## 四种技术形状

```text
技术广度 ↑
  高 │   clounix-sdk-et            Vortex
     │        asic-cosim
     │
  低 │                    CoralNPU
     └──────────────────────────────→ 计算/芯片技术深度
         低                        高
```

## 结论

- **Vortex：深而广**——ISA、微架构、RTL、性能模型、GPU 软件栈全覆盖。
- **CoralNPU：深而窄**——单核标量 + RVV + 矩阵钻得很深，系统/应用层刻意收窄。
- **clounix-sdk-et：广而偏软件**——L2–L7、3 代芯片、user/kernel；深度在 HAL/TOB 抽象。
- **asic-cosim：广而偏验证**——五种后端和 SAI/PTF/CLI 工具面；深度在多保真度集成。

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| HPC | 高性能计算 | 算力密集的科学与工程计算 | 与 ML 不同，HPC 更强调双精度与互连带宽 |
| OpenCL | 跨平台并行计算 API | GPU/加速器通用计算 | 与 CUDA 相比更开放，但生态与工具链较弱 |
| RVV | RISC-V 向量扩展 | 向量化编程 | intrinsics 让编译器直接映射向量指令 |
| SAI | 交换机抽象接口 | 多厂商交换机统一 API | 常与 Thrift 搭配，把交换芯片能力暴露为服务 |
| PTF | 包测试框架 | 交换芯片功能测试 | 构造并校验报文，验证转发、ACL、VLAN 等行为 |
| SIMT | 单指令多线程执行模型 | GPU 吞吐执行 | 与 SIMD 相比，每线程有独立的寄存器与分支状态 |
| Zvt | RISC-V 自定义矩阵扩展 | CoralNPU 的 tile 级加速 | 与标准 RVV 互补，专攻矩阵数据流 |
| RTL | 寄存器传输级设计 | 芯片实现与仿真基准 | 只有 RTL 能同时表达周期行为与可综合结构 |
| Chisel | 基于 Scala 的硬件构造语言 | 参数化设计 | 生成 Verilog，便于复用与配置化 |
| DPI | 直接编程接口 | cosim 与参考模型集成 | 把 C/C++ 模型接入 SystemVerilog 仿真 |
| TCM | 紧耦合存储器 | 暂存指令/数据 | 与 cache 相比，延迟确定且由软件显式管理 |
| PCIe | 高速串行外设总线 | 主机与加速卡互连 | 是 GPU/加速器系统集成的关键接口 |

## 相关

- [[Projects-MOC]]
- [[Verification-Spectrum]]
- [[Multi-Chip-Patterns]]
- [[Learning-Value]]
