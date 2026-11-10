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

Vortex 除通用计算外，还实现了固定功能图形流水线与硬件光追单元（RTU，ray tracing unit，光线求交专用硬件；实时光追加速），用于验证 GPU 的图形/光追能力。

## 如何工作

### 图形流水线

- Rasterizer（光栅化器，把图元转换为像素/片元；实时渲染）：tile-based（分块光栅化，按屏幕 tile 局部处理；降低带宽与缓存压力），粗 bin（128px，分桶：把图元按屏幕 tile 归类；tile-based 前置）→ block → quad（2×2 像素组，光栅化与着色的最小执行单位；导数与纹理采样），支持 early-Z（提前深度测试，着色前剔除被遮挡片元；降低带宽与算力）。
- Texture（纹理，2D/3D 图像数据及其采样硬件；3D 渲染贴图）：纹理采样、tcache。
- Output Merger（OM，输出合并器：深度测试与颜色混合后写回；光栅化末端）：深度/颜色合并、ocache。
- 软件栈：Mesa/vortexpipe 提供 Vulkan（跨平台低开销图形与计算 API；游戏、实时渲染）/OpenGL 路径。

### 光追单元（RTU）

- CW-BVH4（compressed wide BVH，压缩宽层次包围盒，4 叉节点加速结构；光追求交加速）遍历，ray-box / ray-triangle 相交。
- Slot（硬件上下文槽位，暂存一条光线请求的状态；并行光线追踪）池：每个 slot 暂存一条 `vx_rt_wtrace`（ray + 控制状态 + 结果）。
- Context（一条光线的 BVH 遍历现场，含遍历栈与命中信息；光追线程级并行）：一条 ray 的 live BVH walk；`NUM_CTX = NUM_SLOTS × NUM_THREADS`。
- MSHR（miss status holding register，跟踪未完成 cache miss 并合并重复请求；BVH 节点 fetch）合并重复节点 fetch；根节点附近多 context 共享同一节点。
- K-major / 纹理缓存：rcache/rtcache/tcache/ocache 分别服务不同单元。

## 关键细节

- RTU 是可选扩展（`VX_CFG_EXT_RTU_ENABLE`）。
- 光追与图形共享 cache 层次，但有私有 L1（rcache/rtcache）。
- 图形与光追是理解“GPU 通用性”的好例子：同一套 SIMT（单指令多线程，warp 内线程共享 PC；GPU 执行模型）核 + 专用固定功能单元。

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

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| RTU | 硬件光线追踪单元 | 实时光线求交 | 与图形流水线共享 cache 层次，但有私有 rcache/rtcache |
| Rasterizer | 光栅化器 | 实时渲染图元转片元 | tile-based 实现适合低带宽场景 |
| tile-based | 分块光栅化 | 移动 GPU、低带宽渲染 | 与 immediate-mode 相比，先把图元按屏幕 tile 分桶 |
| bin | 图元分桶 | tile-based 光栅化前置 | 粗 bin 用 128px 粒度降低排序与存储开销 |
| quad | 2×2 像素组 | 光栅化与片元着色 | 纹理采样与导数计算以 quad 为单位 |
| early-Z | 提前深度测试 | 遮挡剔除 | 需先完成深度测试再着色，依赖深度缓冲一致性 |
| Texture | 纹理采样硬件 | 3D 渲染贴图 | 与 tcache 配合，采样带宽是图形性能关键 |
| Output Merger | 输出合并器 | 深度/颜色写回 | ocache 减少对主存的读写，与 early-Z 配合 |
| Vulkan | 低开销图形/计算 API | 游戏、实时渲染 | Mesa/vortexpipe 提供 Vulkan 路径，验证软件栈 |
| BVH | 层次包围盒加速结构 | 光线求交加速 | CW-BVH4 为 4 叉宽节点，减少遍历深度 |
| slot | 硬件上下文槽位 | 并行光线追踪 | 槽位暂存单条光线状态，数量决定硬件并发度 |
| context | 单条光线的遍历现场 | BVH walk | NUM_CTX = NUM_SLOTS × NUM_THREADS，体现两级并行 |
| MSHR | 未完成请求跟踪表 | BVH 节点 fetch 合并 | 根节点附近多 context 共享，显著减少重复读取 |
| SIMT | 单指令多线程执行模型 | GPU 通用计算 | 图形/光追复用同一 SIMT 核，体现 GPU 通用性 |

## 来源

- `docs/designs/ray_tracing_architecture.md`
- `docs/designs/graphics_hardware_stack.md`
- `hw/rtl/rtu/`、`hw/rtl/raster/`、`hw/rtl/tex/`、`hw/rtl/om/`
