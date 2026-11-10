---
type: synthesis
aliases: [多芯片配置手法, Multi-Chip Patterns]
tags:
  - type/synthesis
  - layer/software
created: 2026-11-10
---

# 多芯片 / 多配置手法

## 四种手法

| 项目 | 手法 | 位置 |
|---|---|---|
| Vortex | TOML（配置文件格式；用于声明构建与运行参数） + profiles | `VX_config.toml`、`profiles/` |
| CoralNPU | 三种 core 变体 + AXI（AMBA 高级可扩展接口；用于 SoC 片内高带宽互连）/TL-UL（TileLink Uncached Lightweight，轻量级片上总线协议；用于外设与控制访问） | `CoreMini/Rvv/Vme` |
| clounix-sdk-et | `ENABLED_CHIPS` + `hal/mt` | `config.mk`、`hal/mt/{nb,kg,et}` |
| asic-cosim | `TARGET_CHIP` + `mountains` | `CMakeLists.txt`、`src/cosim/mountains/{nb,kg}` |

## 对比

| 维度 | Vortex | CoralNPU | Clounix-SDK | ASIC-Cosim |
|---|---|---|---|---|
| 配置时机 | 构建期（TOML/`-D`） | 构建期（Bazel（Google 的构建系统；用于多语言、可缓存的构建与测试） target/Chisel（基于 Scala 的硬件构造语言；生成 Verilog，用于参数化设计） 参数） | 构建期 + 运行期（`clx_cfg`） | 构建期（`TARGET_CHIP`）+ 运行期 CLI（命令行接口；用于配置与调试）/JSON |
| 差异位置 | 单一 TOML | 变体目录/参数 | HAL（硬件抽象层，屏蔽芯片差异；上层 API 的统一实现层）/TOB（表项对象层，统一抽象 SRAM/TCAM/hash；用于屏蔽底层表实现）/DRV（驱动层，直接操作寄存器与表项；用于底层访问） 的 `mt` 目录 | `mountains/{nb,kg}` |
| 优点 | 单一事实源、可生成头文件 | 变体清晰、易裁剪 | 多代芯片、API 统一 | 同一测试面切后端 |
| 风险 | 参数组合爆炸 | 变体分叉 | 维护矩阵大 | 预编译模型/版本同步 |

## 可借鉴的点

- **Vortex**：单一配置源 + 生成 RTL（寄存器传输级设计；这里指由配置生成的硬件与软件寄存器视图）/软件头文件，避免两边不一致。
- **CoralNPU**：把“功能变体”和“总线封装”分开，减少组合数。
- **Clounix-SDK**：芯片差异下沉到固定目录，上层 API 不感知。
- **ASIC-Cosim**：同一控制面 + 多后端，用 `TARGET_CHIP` 而不是复制测试。

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| TOML | 配置文件格式 | 声明构建与运行参数 | 单一 TOML 便于生成 RTL 与软件头文件，减少两边漂移 |
| AXI | AMBA 高级可扩展接口 | SoC 片内高带宽互连 | 与 TL-UL 并存时，AXI 偏高性能，TL-UL 偏轻量控制 |
| TL-UL | 轻量级 TileLink 总线协议 | 外设与控制访问 | 比 AXI 简单，适合低带宽控制通路 |
| Bazel | Google 的构建系统 | 多语言、可缓存的构建与测试 | 构建期 target 选择是 CoralNPU 变体的主要手法 |
| Chisel | 基于 Scala 的硬件构造语言 | 参数化设计 | 参数在构建期展开，天然适合多配置生成 |
| CLI | 命令行接口 | 配置与调试 | 运行期 CLI/JSON 让同一镜像切换配置 |
| HAL | 硬件抽象层 | 屏蔽芯片差异 | 多代芯片共用上层 API，差异下沉到 hal/mt |
| TOB | 表项对象层 | 屏蔽底层表实现 | 统一抽象 SRAM/TCAM/hash，减少上层分支 |
| DRV | 驱动层 | 底层寄存器与表项访问 | 与 HAL/TOB 分层，隔离 OS 与芯片差异 |
| RTL | 寄存器传输级设计 | 由配置生成的硬件视图 | 生成 RTL 与软件头文件可保证寄存器视图一致 |

## 相关

- [[Clounix-SDK-MultiChip]]
- [[CoralNPU]]
- [[Vortex]]
- [[ASIC-Cosim]]
