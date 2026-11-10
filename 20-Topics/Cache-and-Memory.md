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

Cache（高速缓存，利用时间/空间局部性自动缓存近期数据；降低平均访存延迟）用局部性（locality，程序倾向重复访问近期或邻近数据；cache 有效性的基础）把慢速大容量存储映射到快速小容量存储；GPU 用多级 cache + 大量线程隐藏延迟，NPU 常用 scratchpad（便签式片上存储，由软件显式管理；延迟确定、无一致性开销）避免不确定性。

## 关键机制

- **多级层次**：L1/L2/L3（多级 cache 层次；越靠近核越快越小，越靠后越大越慢），容量/延迟/带宽逐级变化。
- **MSHR**（Miss Status Holding Register，跟踪未完成 miss 的表项；支持多个 outstanding miss）：跟踪未完成 miss，支持非阻塞（non-blocking，miss 未返回时仍可服务其他请求；靠 MSHR 支撑）和 fill forwarding（填充转发，miss 数据返回时直接转给等待的请求；减少往返延迟）。
- **sectored line**（分段缓存行，tag 按整行但数据按 sector 独立填充；减少无用取数）：tag 粒度与 fill 粒度解耦。
- **一致性**（coherence，多核 cache 对同一地址保持一致视图；靠协议与原子操作维护）：多核共享层 + 原子操作；LLC（Last-Level Cache，最后一级共享 cache；多核一致性与 AMO 常在此处理）上执行 AMO（Atomic Memory Operation，RISC-V 的原子内存操作；在 LLC 上执行保证原子性）。
- **虚拟内存**（virtual memory，用页表把虚拟地址映射到物理地址；提供隔离与大地址空间）：TLB（Translation Lookaside Buffer，页表项缓存；加速地址翻译）、页表遍历（PTW，Page Table Walk；TLB miss 时查页表）、地址翻译。
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

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| Cache | 利用局部性自动缓存数据的高速存储 | CPU/GPU 通用访存 | 自动管理但时序不确定 |
| 局部性 | 重复访问近期或邻近数据 | cache 有效性分析 | 时间局部性与空间局部性需分别优化 |
| scratchpad | 软件显式管理的片上存储 | NPU、GPU 本地存储 | 延迟确定，但需手动布局与同步 |
| L1/L2/L3 | 多级 cache 层次 | 处理器存储系统 | 越靠后容量越大、延迟越高 |
| MSHR | 跟踪未完成 miss 的表项 | 非阻塞 cache | 数量决定可并发的 miss 数 |
| 非阻塞 | miss 未返回时仍服务其他请求 | 高带宽 cache | 依赖 MSHR 记录在途请求 |
| fill forwarding | 把返回的 fill 数据直接转给等待者 | 降低 miss 延迟 | 与 MSHR 合并逻辑紧密相关 |
| sectored line | tag 整行、数据按 sector 填充 | 减少无用取数 | 与预取策略配合效果更好 |
| 一致性 | 多核 cache 对同一地址保持一致视图 | 多核 SoC | 协议开销随核数增加 |
| LLC | 最后一级共享 cache | 多核一致性与 AMO | 常作为内存侧的最后屏障 |
| AMO | 原子内存操作 | 同步、计数器 | RISC-V 在 LLC 上执行以保证原子性 |
| 虚拟内存 | 页表映射虚拟地址到物理地址 | OS、进程隔离 | 需要 TLB 加速翻译 |
| TLB | 页表项缓存 | 地址翻译 | miss 时触发页表遍历 |
| PTW | 页表遍历 | TLB miss 处理 | 可由硬件或软件完成 |
