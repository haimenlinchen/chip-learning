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

TCM（Tightly-Coupled Memory，紧耦合存储；挂在核边、低延迟、软件显式管理）是挂在核旁边的低延迟 SRAM（Static RAM，静态随机存储；片上高速存储的基本单元），由软件显式管理，不经过 cache 一致性协议（coherence protocol，维护多核 cache 的数据一致；TCM 绕过它换取确定性）。

## 为什么用 TCM

- **确定性**：访问延迟固定（常见单周期），适合实时/推理。
- **低功耗/小面积**：无 tag（缓存行地址标签，用于判断命中；TCM 不需要）/比较器/一致性逻辑。
- **高带宽**：多 bank（存储体，可独立访问的分区；多 bank 并行提升带宽）+ 本地 crossbar（交叉开关，把多个主设备连到多个存储体；提供并行通路），可并行服务多个单元。
- **软件可控**：编译器/运行时决定数据放置，避免 thrashing（缓存抖动，数据反复换入换出；scratchpad 由软件放置可避免）。

## 代价

- 容量小，需要 DMA（Direct Memory Access，直接内存访问；不占核地批量搬数据）/双缓冲（double buffering，计算当前块时预取下一块；掩盖搬运延迟）把数据搬进来。
- 软件复杂度高：bank 分配、布局、同步都要手写。
- 不适合大工作集/不规则访问。

## 在项目中的体现

- [[CoralNPU-Memory]]：8KB ITCM + 32KB DTCM（指令/数据紧耦合存储；分别存放代码与数据、延迟固定），4×32b bank，可扩到 1MB/1MB；DMA + AXI（Advanced eXtensible Interface，AMBA 总线协议；片上高带宽主从接口）。
- [[Vortex-Cache]]：LMEM（Local Memory，GPU 的片上便签存储；可由软件管理、供工作组共享）是 GPU 的 scratchpad，但 Vortex 同时保留 cache 层次。
- [[Clounix-SDK-HAL-TOB]]：表项 SRAM/TCAM（Ternary Content-Addressable Memory，三态内容寻址存储；按内容并行匹配、用于表项查找）也是软件可见的存储资源。

## 相关概念

- [[Cache-and-Memory]]
- [[Vector-Architecture]]
- [[Software-Interface]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| TCM | 挂在核边、软件显式管理的低延迟存储 | MCU、NPU 实时任务 | 与 cache 的核心差异是确定性 |
| SRAM | 片上静态存储单元 | 寄存器堆、cache、TCM | 比 DRAM 快，但密度低、成本高 |
| cache 一致性协议 | 维护多核 cache 数据一致的协议 | 多核 SoC | TCM 绕过它以换取确定性 |
| tag | 缓存行地址标签 | cache 命中判断 | TCM 无需 tag，因此面积更小 |
| bank | 可独立访问的存储体 | 多端口/高带宽存储 | bank 越多，并行访问能力越强 |
| crossbar | 连接多主多从的交叉开关 | 片上互连 | 提供并行通路，但面积随端口增长 |
| thrashing | 数据反复换入换出 | cache 大工作集 | 软件放置数据可避免 |
| DMA | 不占核的批量数据搬运 | TCM 填充、双缓冲 | 与双缓冲配合掩盖搬运延迟 |
| 双缓冲 | 计算当前块同时预取下一块 | 流式数据处理 | 需要两倍缓冲空间 |
| ITCM/DTCM | 指令/数据紧耦合存储 | CoralNPU | 分离代码与数据，延迟固定 |
| AXI | AMBA 高带宽片上总线协议 | 主从设备互连 | 与 TCM/DMA 配合完成数据搬移 |
| LMEM | GPU 片上本地存储 | Vortex、工作组共享 | 是 GPU 的 scratchpad 形态 |
| TCAM | 按内容并行匹配的存储 | ACL、转发表 | 比普通 SRAM 面积大、功耗高 |
