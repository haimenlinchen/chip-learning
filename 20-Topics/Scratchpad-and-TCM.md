---
type: atomic
layer: memory
topic: [tcm, scratchpad, dma, determinism]
status: learning
tags:
  - layer/memory
  - topic/tcm
created: 2026-11-10
---

# Scratchpad 与 TCM

## 定义

TCM（Tightly-Coupled Memory）是挂在核旁边的低延迟 SRAM，由软件显式管理，不经过 cache 一致性协议。

## 为什么用 TCM

- **确定性**：访问延迟固定（常见单周期），适合实时/推理。
- **低功耗/小面积**：无 tag/比较器/一致性逻辑。
- **高带宽**：多 bank + 本地 crossbar，可并行服务多个单元。
- **软件可控**：编译器/运行时决定数据放置，避免 thrashing。

## 代价

- 容量小，需要 DMA/双缓冲把数据搬进来。
- 软件复杂度高：bank 分配、布局、同步都要手写。
- 不适合大工作集/不规则访问。

## 在项目中的体现

- [[CoralNPU-Memory]]：8KB ITCM + 32KB DTCM，4×32b bank，可扩到 1MB/1MB；DMA + AXI。
- [[Vortex-Cache]]：LMEM 是 GPU 的 scratchpad，但 Vortex 同时保留 cache 层次。
- [[Clounix-SDK-HAL-TOB]]：表项 SRAM/TCAM 也是软件可见的存储资源。

## 相关概念

- [[Cache-and-Memory]]
- [[Vector-Architecture]]
- [[Software-Interface]]
