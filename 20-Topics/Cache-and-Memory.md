---
type: atomic
layer: memory
topic: [cache, mshr, coherence, virtual-memory]
status: learning
tags:
  - layer/memory
  - topic/cache
created: 2026-11-10
---

# Cache 与存储层次

## 定义

Cache 用局部性把慢速大容量存储映射到快速小容量存储；GPU 用多级 cache + 大量线程隐藏延迟，NPU 常用 scratchpad 避免不确定性。

## 关键机制

- **多级层次**：L1/L2/L3，容量/延迟/带宽逐级变化。
- **MSHR**：跟踪未完成 miss，支持非阻塞和 fill forwarding。
- **sectored line**：tag 粒度与 fill 粒度解耦。
- **一致性**：多核共享层 + 原子操作；LLC 上执行 AMO。
- **虚拟内存**：TLB、页表遍历（PTW）、地址翻译。
- **写策略**：write-through vs write-back；只有 LLC 适合 write-back。

## 两种哲学

| 方案 | 代表 | 优点 | 代价 |
|---|---|---|---|
| Cache | Vortex | 自动管理、通用、大工作集 | 一致性/时序不确定、面积大 |
| Scratchpad | CoralNPU | 确定性、低延迟、省面积 | 软件手动管理、容量小 |

## 在项目中的体现

- [[Vortex-Cache]]：L1 socket 共享、L2/L3、MSHR、LLC AMO、VM/TLB。
- [[CoralNPU-Memory]]：ITCM/DTCM、无 cache、AXI/TL-UL。
- [[Clounix-SDK-HAL-TOB]]：表项/TCAM/hash 是另一种“存储抽象”。

## 相关概念

- [[Scratchpad-and-TCM]]
- [[Performance-Modeling]]
- [[Software-Interface]]
