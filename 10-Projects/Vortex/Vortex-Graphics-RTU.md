---
type: atomic
project: Vortex
layer: microarchitecture
topic: [graphics, rasterizer, texture, ray-tracing]
status: learning
source_repo: /localdata/linchen/vortex
source_files:
  - docs/designs/ray_tracing_architecture.md
  - docs/designs/graphics_hardware_stack.md
tags:
  - layer/microarch
  - topic/graphics
created: 2026-11-10
---

# Vortex 图形与光追

## 定义

Vortex 除通用计算外，还实现了固定功能图形流水线与硬件光追单元，用于验证 GPU 的图形/光追能力。

## 如何工作

### 图形流水线

- Rasterizer：tile-based，粗 bin（128px）→ block → quad，支持 early-Z。
- Texture：纹理采样、tcache。
- Output Merger（OM）：深度/颜色合并、ocache。
- 软件栈：Mesa/vortexpipe 提供 Vulkan/OpenGL 路径。

### 光追单元（RTU）

- CW-BVH4 遍历，ray-box / ray-triangle 相交。
- Slot 池：每个 slot 暂存一条 `vx_rt_wtrace`（ray + 控制状态 + 结果）。
- Context：一条 ray 的 live BVH walk；`NUM_CTX = NUM_SLOTS × NUM_THREADS`。
- MSHR 合并重复节点 fetch；根节点附近多 context 共享同一节点。
- K-major / 纹理缓存：rcache/rtcache/tcache/ocache 分别服务不同单元。

## 关键细节

- RTU 是可选扩展（`VX_CFG_EXT_RTU_ENABLE`）。
- 光追与图形共享 cache 层次，但有私有 L1（rcache/rtcache）。
- 图形与光追是理解“GPU 通用性”的好例子：同一套 SIMT 核 + 专用固定功能单元。

## 在项目中的位置

- 所属项目：[[Vortex]]
- 相关子系统：[[Vortex-SIMT]]、[[Vortex-Cache]]

## 相关概念

- [[SIMT-and-Warp]]
- [[Cache-and-Memory]]

## 自检问题

- tile-based rasterizer 与 immediate-mode 的差异？
- RTU 的 slot/context 两个维度分别解决什么问题？
- 为什么光追需要私有 L1（rtcache）？
- early-Z 需要哪些前置条件？

## 来源

- `docs/designs/ray_tracing_architecture.md`
- `docs/designs/graphics_hardware_stack.md`
- `hw/rtl/rtu/`、`hw/rtl/raster/`、`hw/rtl/tex/`、`hw/rtl/om/`
