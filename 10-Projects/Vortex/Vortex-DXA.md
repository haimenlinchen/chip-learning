---
type: atomic
project: Vortex
layer: microarchitecture
topic: [dxa, dma, multicast, tma]
status: learning
source_repo: /localdata/linchen/vortex
source_files:
  - docs/designs/dxa_async_copy_multicast.md
  - VX_config.toml
tags:
  - layer/microarch
  - topic/dma
created: 2026-11-10
---

# Vortex DXA（异步拷贝 + 多播）

## 定义

DXA（Direct eXecution Accelerator）是 NVIDIA Hopper TMA 风格的异步批量拷贝单元：一条 warp 指令启动 GMEM→LMEM 的 tiled copy，warp 立即释放。

## 如何工作

- 操作：1–5 维 tiled copy、越界 clamp/constant fill、multicast、K-major transpose。
- 描述符：`base_addr` + `meta` + tile sizes + `cfill` + OOB bounds + strides + `smem_stride`。
- 集群级 `VX_dxa_core`：请求仲裁 → 16 项队列 → 描述符表 → dispatch → worker。
- 每个 worker：setup → addr_gen（滚动游标 + 4 级 odometer）→ GMEM read（≤8 in-flight）→ SMEM write（barrel shift）。
- multicast：`cta_mask` 多 bit 时，读一次 GMEM，按 `smem_stride` 重放到多个 CTA。
- 完成：最后一个 cache line 带 completion flag，写入 LMEM 后通过 `txbar` 释放 barrier。

## 关键细节

- ISA：`INST_SFU_DXA`（SFU opcode 9），custom0/funct7=3；4 lane `vx_wgather` 打包参数。
- 描述符由 host 通过 DCR 写入，16 个 slot。
- 只有 GMEM→LMEM 方向，没有 LMEM→GMEM。
- K-major transpose 是 DXA 与 TCU 的主要耦合点。

## 在项目中的位置

- 所属项目：[[Vortex]]
- 相关子系统：[[Vortex-TCU]]、[[Vortex-Cache]]、[[Vortex-SIMT]]

## 相关概念

- [[Matrix-Accelerator]]
- [[Performance-Modeling]]

## 自检问题

- DXA 的 multicast 如何减少 GMEM 读放大？
- 为什么 DXA 只做 GMEM→LMEM？
- K-major transpose 如何配合 WGMMA 的 B 布局？
- 完成 flag 为什么挂在最后一个 cache line 上？

## 来源

- `docs/designs/dxa_async_copy_multicast.md`
- `hw/rtl/dxa/`
- `VX_config.toml`
