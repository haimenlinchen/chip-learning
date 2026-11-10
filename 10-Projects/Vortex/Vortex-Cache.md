---
type: atomic
project: Vortex
layer: memory
topic: [cache, mshr, amo, virtual-memory]
status: learning
source_repo: /localdata/linchen/vortex
source_files:
  - docs/designs/cache_subsystem.md
  - VX_config.toml
tags:
  - layer/memory
  - topic/cache
created: 2026-11-10
---

# Vortex 存储层次

## 定义

Vortex 有完整的 GPU cache 层次：L1（icache/dcache）、L2、L3、共享 LMEM，以及可选的虚拟内存/TLB。

## 如何工作

```text
core → socket (L1) → cluster (L2) → L3 → memory
```

- L1 位于 socket 内，由最多 `SOCKET_SIZE` 个 core 共享；`VX_mem_unit` 只暴露 `dcache_bus_if`，不实例化 cache。
- 默认：icache/dcache 16KB 4-way；L2 1MB 8-way；L3 2MB 8-way。
- L2/L3 默认关闭；关闭时通过 `VX_cache_bypass` 透传，不是条件实例化。
- 非阻塞 cache：每 bank 一个 MSHR，支持 fill forwarding。
- sectored line：tag 与 fill 粒度解耦（L2/L3）。
- AMO 只在 LLC 执行；上层透传。
- LLC 判定：`DCACHE_IS_LLC = !L2 && !L3`；`L2_IS_LLC = L2 && !L3`；`L3_IS_LLC = L3`。
- 私有 L1 是 write-through；只有 LLC 可以 write-back。

## 关键细节

- 多核必须有共享层：`cores > 1` 且无 L2 时，每个 socket 独立写内存，store 会丢。
- 跨 cluster 必须有 L3。
- 虚拟内存：TLB（L1 D/I TLB、L2 TLB、PTW）、页表格式在 `VX_types.toml`。
- LMEM：shared memory，默认至少 16KB，按 LSU lane 数分 bank。

## 在项目中的位置

- 所属项目：[[Vortex]]
- 相关子系统：[[Vortex-SIMT]]、[[Vortex-DXA]]、[[Vortex-CommandProcessor]]

## 相关概念

- [[Cache-and-Memory]]
- [[Scratchpad-and-TCM]]

## 自检问题

- 为什么 L1 是 socket 共享而不是 per-core？
- 多核没有 L2 时为什么会丢 store？
- LLC 上的 AMO 与上层透传的 AMO 有什么区别？
- sectored line 如何减少 tag 开销？

## 来源

- `docs/designs/cache_subsystem.md`
- `VX_config.toml`
