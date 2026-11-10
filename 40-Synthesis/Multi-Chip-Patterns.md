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
| Vortex | TOML + profiles | `VX_config.toml`、`profiles/` |
| CoralNPU | 三种 core 变体 + AXI/TL-UL | `CoreMini/Rvv/Vme` |
| clounix-sdk-et | `ENABLED_CHIPS` + `hal/mt` | `config.mk`、`hal/mt/{nb,kg,et}` |
| asic-cosim | `TARGET_CHIP` + `mountains` | `CMakeLists.txt`、`src/cosim/mountains/{nb,kg}` |

## 对比

| 维度 | Vortex | CoralNPU | Clounix-SDK | ASIC-Cosim |
|---|---|---|---|---|
| 配置时机 | 构建期（TOML/`-D`） | 构建期（Bazel target/Chisel 参数） | 构建期 + 运行期（`clx_cfg`） | 构建期（`TARGET_CHIP`）+ 运行期 CLI/JSON |
| 差异位置 | 单一 TOML | 变体目录/参数 | HAL/TOB/DRV 的 `mt` 目录 | `mountains/{nb,kg}` |
| 优点 | 单一事实源、可生成头文件 | 变体清晰、易裁剪 | 多代芯片、API 统一 | 同一测试面切后端 |
| 风险 | 参数组合爆炸 | 变体分叉 | 维护矩阵大 | 预编译模型/版本同步 |

## 可借鉴的点

- **Vortex**：单一配置源 + 生成 RTL/软件头文件，避免两边不一致。
- **CoralNPU**：把“功能变体”和“总线封装”分开，减少组合数。
- **Clounix-SDK**：芯片差异下沉到固定目录，上层 API 不感知。
- **ASIC-Cosim**：同一控制面 + 多后端，用 `TARGET_CHIP` 而不是复制测试。

## 相关

- [[Clounix-SDK-MultiChip]]
- [[CoralNPU]]
- [[Vortex]]
- [[ASIC-Cosim]]
