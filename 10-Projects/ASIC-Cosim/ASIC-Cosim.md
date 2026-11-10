---
type: project-hub
project: ASIC-Cosim
aliases: [asic-cosim, ASIC Cosim, 交换芯片协同仿真]
status: learning
tags:
  - project/asic-cosim
  - chip/verification
source_repo: /localdata/linchen/asic-cosim
created: 2026-11-10
---

# ASIC-Cosim

## 一句话定位

Clounix 内部 ASIC（专用集成电路，为特定任务定制的芯片；用于交换、AI、网络等大批量场景）验证协同仿真（co-simulation，软件控制面与芯片模型联合运行；用于流片前验证功能）环境：同一套 SAI（Switch Abstraction Interface，交换机抽象接口标准；用于统一不同交换芯片的配置 API）/CLI（Command Line Interface，命令行接口；用于人工调试和脚本化下发命令）/PTF（Packet Test Framework，报文测试框架；用于交换芯片数据面测试）控制面，接 CMODEL（C/C++ 功能模型，用软件模拟芯片行为；用于早期软件开发和回归）/EMU（Emulation，硬件仿真平台；用于流片前跑驱动与系统级软件）/RTL（Register Transfer Level，寄存器传输级硬件描述；用于周期精确仿真）/LAB/NOMODEL（无模型模式，仅运行控制面；用于脚本和测试框架开发）五种执行后端。

## 架构骨架

- 后端：CMODEL（预编译 `libcx_model.so`）、EMU（PCIe/knet）、RTL（DPI）、LAB（真实硬件）、NOMODEL
- C-model：交换流水线 PP/PL/TM（Traffic Manager，流量管理器；负责队列、调度与缓存）/PCX（Packet Crossbar，报文交叉开关；负责切片间报文转发）/CSS/IGR（Ingress，入方向处理流水线；用于解析、查表和准入）/EGR（Egress，出方向处理流水线；用于报文修改与转发）/FPU、bloomfilter（布隆过滤器，概率型集合查询结构；用于快速判断表项是否存在）、hash、PacketGen
- 规模：NB 1 pie × 25.6T；KG 2 pie × 51.2T；112G PAM4 SerDes
- 控制面：SAI-Thrift、CLI telnet、PTF、pytest、gtest、pcap、traffic、chassis、netlink/FRR
- 调试：iPython / iCling / Jupyter / gdb / valgrind

## 架构图

```mermaid
flowchart TB
    TEST["Tests / SAI / CLI / PTF"] --> ENV["Cosim Control Plane"]
    ENV --> CM["CMODEL<br/>libcx_model.so"]
    ENV --> EMU["EMU<br/>PCIe / knet"]
    ENV --> RTL["RTL<br/>DPI"]
    ENV --> LAB["LAB<br/>real hardware"]
    ENV --> NM["NOMODEL"]
    CM --> PIPE["Switch pipeline model<br/>PP / PL / TM / PCX / CSS / IGR / EGR / FPU"]
```

## 关键子系统

- [[ASIC-Cosim-Five-Backends]]
- [[ASIC-Cosim-CMODEL]]
- [[ASIC-Cosim-EMU]]
- [[ASIC-Cosim-RTL-DPI]]
- [[ASIC-Cosim-SAI-PTF]]

## 相关概念

- [[Verification-Fidelity]]
- [[Software-Interface]]
- [[Cache-and-Memory]]（对照模型内存/backdoor）

## 学习阶段

- [[Stage-4-Verification]]

## 代码入口

- `README.md`
- `src/cosim/cmodel/cmodel.h`
- `src/cosim/rtl/rtl_dpi.h`
- `src/cosim/emu/emu.h`
- `src/cosim/lab/`
- `src/cosim/mountains/{nb,kg}/`
- `tests/features/`
- `saithriftv2/ptf/`

## 实验记录

- [ ] 跑一个 feature gtest（cmodel）
- [ ] 对比 CMODEL 与 RTL 的同一用例
- [ ] 理解 EMU 的 PCIe/knet 路径
- [ ] 画五后端与 SAI/PTF 的关系图

## 开放问题

- 同一 SAI 用例在 CMODEL/RTL/LAB 上的差异如何自动比对？
- EMU 与 RTL 的边界：哪些问题只能在 EMU 暴露？
- 预编译 C-model 与 RTL 的版本如何保持同步？

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| ASIC | 专用集成电路 | 交换、AI、网络等大批量场景 | 与 FPGA 相比流片成本高，但量产功耗和单位成本更优 |
| 协同仿真 | co-simulation，控制面与芯片模型联合运行 | 流片前功能验证 | 保真度越高越慢，需按问题类型选择后端 |
| SAI | 交换机抽象接口标准 | 统一不同交换芯片的配置 API | 由 OCP 推动，SONiC 等网络操作系统依赖它 |
| CLI | 命令行接口 | 人工调试、脚本化命令 | 与 SAI 路径共享底层寄存器/表项访问 |
| PTF | 报文测试框架 | 交换芯片数据面测试 | 常与 pytest 组织用例、pcap 提供报文样例 |
| CMODEL | C/C++ 功能模型 | 早期软件开发、日常回归 | 快但时序不精确，适合功能级验证 |
| EMU | 硬件仿真平台 | 驱动、PCIe、中断、DMA 验证 | 比 RTL 快、比 CMODEL 慢，补齐内核路径 |
| RTL | 寄存器传输级硬件描述 | 周期/信号级仿真 | 最慢但能暴露微架构与时序问题 |
| NOMODEL | 无模型模式 | 脚本/测试框架开发 | 不执行芯片行为，只验证控制面流程 |
| TM | 流量管理器 | 队列、调度、缓存管理 | 拥塞与 QoS 问题通常先在此暴露 |
| PCX | 报文交叉开关 | 切片/端口间报文转发 | 与 TM、EGR 一起决定实际转发带宽 |
| IGR | 入方向流水线 | 解析、查表、准入 | 与 EGR 对称，常按 CIA/DIS/FPU 等子模块拆分 |
| EGR | 出方向流水线 | 报文修改与转发 | 与 IGR 共享表项但职责相反 |
| bloomfilter | 概率型集合查询结构 | 快速判断表项是否存在 | 有假阳性无假阴性，常配合 hash 表二次确认 |

## 来源

- `README.md`
- `src/cosim/CMakeLists.txt`
- `src/cosim/cmodel/cmodel.h`
