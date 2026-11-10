---
type: project-hub
project: Clounix-SDK
aliases: [clounix-sdk-et, Clounix SDK, 交换 SDK]
status: learning
tags:
  - project/clounix-sdk
  - chip/switch
source_repo: /localdata/linchen/clounix-sdk-et
created: 2026-11-10
---

# Clounix SDK

## 一句话定位

Clounix 交换 ASIC（Application-Specific Integrated Circuit，专用集成电路；此处指交换芯片）的软件 SDK（Software Development Kit，软件开发工具包，封装芯片能力供上层调用；用于驱动、CLI 与业务应用）：把多代交换芯片的差异压进 HAL（Hardware Abstraction Layer，硬件抽象层；屏蔽不同芯片代际差异）/TOB（Table Operation Bus，表项操作抽象；统一各类表项的访问）/DRV（Driver，驱动层，负责寄存器 IO 与 DMA；直接与硬件交互）/OSAL（Operating System Abstraction Layer，操作系统抽象层；屏蔽 Linux 用户态/内核态差异），向上提供统一的 `clx_*` API（Application Programming Interface，应用编程接口；应用通过它调用 SDK）、CLI（Command-Line Interface，命令行接口；diag_shell 提供诊断命令）与 RPC。

## 架构骨架

- 芯片：NamchaBarwa（NB）、Kawagarbo（KG）、Everest（ET）；API 文档标注 CLX84/86/88
- 分层：CLX API → HAL → TOB → DRV → OSAL
- API：约 37 个模块（L2/L3/VLAN/MPLS/SRv6/TM/QoS/mirror/meter/LAG/BFD/PTP/telemetry/security/WLAN/VM/STP/SWC/netif/pkt/stat）
- 表项：TOB 抽象 SRAM（Static RAM，静态随机存储器；芯片内高速表项存储，如 MAC/路由表）/TCAM（Ternary Content-Addressable Memory，三态内容寻址存储器，支持掩码匹配；用于 ACL 与最长前缀匹配）/hash（哈希表，按键的哈希值定位存储位置；用于 MAC 表、ECMP 等查找）/table
- 系统：user/kernel 双空间、knet（Kernel Network，内核网络模块；打通 SDK 与 Linux 协议栈的数据通道）、eCPU（embedded CPU，芯片内置嵌入式处理器；运行固件处理控制/数据面任务）固件

## 架构图

```mermaid
flowchart TB
    APP["Applications<br/>diag_shell / neutrino_server / sdk_sample / sdk_ref / sdk_asicsim"] --> API["CLX API<br/>~37 modules"]
    API --> HAL["HAL<br/>hal_*.c + hal/mt/nb/kg/et"]
    HAL --> TOB["TOB<br/>SRAM / TCAM / hash / table"]
    TOB --> DRV["DRV<br/>io / dma + drv/mt"]
    DRV --> OSAL["OSAL<br/>linux_user / linux_kernel / knet"]
    OSAL --> ASIC["ASIC<br/>NB / KG / ET"]
```

## 关键子系统

- [[Clounix-SDK-Layering]]
- [[Clounix-SDK-HAL-TOB]]
- [[Clounix-SDK-MultiChip]]
- [[Clounix-SDK-eCPU]]

## 相关概念

- [[Software-Interface]]
- [[Multi-Chip-Patterns]]
- [[Cache-and-Memory]]（对照表项/缓存抽象）

## 学习阶段

- [[Stage-5-SDK]]

## 代码入口

- `clx_sdk/include/clx/`
- `clx_sdk/src/clx/`
- `clx_sdk/src/hal/`
- `clx_sdk/src/tob/`
- `clx_sdk/src/drv/`
- `clx_sdk/src/osal/`
- `app/sdk_sample/`
- `app/diag_shell/`
- `app/neutrino_server/`

## 实验记录

- [ ] 跟踪 `clx_l2_add` 到硬件表项的调用链
- [ ] 读 TOB 的 entry/bank/field 操作
- [ ] 比较 NB/KG/ET 的 `hal/mt` 差异
- [ ] 理解 user/kernel 两种构建

## 开放问题

- 37 个模块中，哪些是芯片无关的公共逻辑，哪些必须 per-chip 实现？
- TOB 如何屏蔽 SRAM/TCAM/hash 的访问差异？
- eCPU 固件与 host SDK 的职责边界在哪里？

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| ASIC | 专用集成电路 | 交换芯片本体 | 与通用 CPU 对比：ASIC 用硬件流水线换吞吐，灵活性靠 SDK 补足 |
| SDK | 软件开发工具包 | 封装芯片能力供应用调用 | SDK 不等于驱动：驱动贴近硬件，SDK 还含 API、CLI、RPC 等 |
| HAL | 硬件抽象层 | 屏蔽多代芯片差异 | 与 OSAL 分工：HAL 抽象硬件，OSAL 抽象操作系统 |
| TOB | 表项操作抽象 | 统一访问 SRAM/TCAM/hash | 位于 HAL 之下、DRV 之上，避免 HAL 直接拼寄存器 |
| DRV | 驱动层 | 寄存器 IO 与 DMA | 芯片差异也下沉到 drv/mt 目录 |
| OSAL | 操作系统抽象层 | 用户态/内核态统一接口 | 同一套 SDK 可构建为 .so 或 .ko |
| API | 应用编程接口 | 应用调用 clx_* 函数 | 约 37 个模块，覆盖 L2/L3/QoS 等 |
| CLI | 命令行接口 | diag_shell 诊断 | 适合排障；自动化通常走 API/RPC |
| SRAM | 静态随机存储器 | 高速表项存储 | 与 TCAM 对比：SRAM 精确匹配，TCAM 支持掩码 |
| TCAM | 三态内容寻址存储器 | ACL、最长前缀匹配 | 成本/功耗高，容量通常远小于 SRAM |
| hash | 哈希表 | MAC 表、ECMP 查找 | 冲突处理与老化机制决定表项容量和稳定性 |
| knet | 内核网络模块 | SDK 与 Linux 协议栈互通 | 常用于把报文上送内核或从内核注入芯片 |
| eCPU | 芯片内置嵌入式 CPU | 运行固件处理控制/数据面任务 | 与 host SDK 通过寄存器/表项/DMA 交互 |

## 来源

- `config.mk`
- `build.mk`
- `clx_sdk/Makefile`
- `clx_sdk/include/clx/`
- `clx_sdk/include/tob/tob.h`
