---
type: stage
stage: 0
status: todo
projects: [tiny-gpu]
tags:
  - learning/roadmap
  - stage/gpu-warmup
created: 2026-11-11
---

# 阶段零：tiny-gpu 热身

> 可选阶段。用约 1.3k 行 RTL 的最小 GPU 补齐 Verilog（硬件描述语言；用模块与时钟描述电路）、仿真闭环与 SIMT（单指令多线程执行模型，一个 block 的线程共享指令流；用于 GPU 吞吐计算）基础，再进入 [[Stage-1-Scalar-Core]]。

## 定位

- 3–5 天，不替代任何阶段，只把先修补到「能读、能跑、能改」。
- **它补的**：Verilog 读代码、iverilog/cocotb 仿真闭环、block/thread/调度/访存带宽直觉。
- **它不教的**：流水线冒险与 scoreboard（记分板，跟踪寄存器与执行单元就绪状态；用于动态调度）/ROB（重排序缓冲，按程序顺序提交；用于精确异常）（Stage 1）、warp（线程束，GPU 中一起执行的线程组；SIMT 调度单位）/分支发散/cache 层次/TCU（张量计算单元；用于矩阵乘加）（Stage 3）、RVV（RISC-V 向量扩展；用于向量计算）/VME（CoralNPU 的矩阵扩展；用于 tile 级矩阵运算）（Stage 2）、验证方法学（Stage 4）、SDK（Stage 5）。
- 结论先行：**它适合起步，但不是 Stage 1 的替代**。它的 core 是「一条指令走完六个状态再取下一条」的状态机，不是流水线。

## 目标

- 讲清一个 block（线程块，分发到单个 core 执行的一组线程；SIMT 的调度单位）从 dispatch 到 core 完成的全过程。
- 讲清一条 `LDR` 从 decode 到寄存器写回的完整路径，包括 `REQUEST`/`WAIT` 两个等待状态。
- 改一条指令、改一组参数，用 trace（执行轨迹，逐周期记录 PC、寄存器与状态；用于定位与验证）和 cycles 解释结果。

## 先修

最低门槛，明显缺口先补 1–2 周：

- **数字电路**：组合/时序逻辑、寄存器、时钟、有限状态机。能读懂即可，不必会设计。
- **Verilog**：`module`/端口、`always @(posedge clk)`、阻塞与非阻塞赋值、testbench（测试平台，给 DUT 加激励并检查输出；用于功能验证）概念。
- **工具**：Linux 命令行、git、make；Python 能读简单脚本。

不需要：RISC-V 指令集、Chisel/Scala、乱序执行、cache 一致性。这些在后续阶段补。

## 环境准备

```bash
# Ubuntu/Debian
sudo apt install iverilog
pip install cocotb
# sv2v：从 https://github.com/zachjs/sv2v/releases 下载二进制放进 $PATH

cd /localdata/linchen/tiny-gpu
mkdir -p build test/logs   # Makefile 与 logger 都不会自动建目录
make test_matadd
make test_matmul
```

跑通后确认三件事：结果断言通过、`test/logs/log_*.txt` 里有完整 trace、输出里的 cycles 与 trace 行数对得上。

## 阅读

- `README.md`：架构、11 条指令的 ISA（指令集架构，软硬件契约；用于定义指令编码与语义）、执行流程、advanced functionality
- `docs/images/`：`gpu.png`、`core.png`、`thread.png`、`isa.png`、`trace.png`
- 源码顺序：
  1. `src/gpu.sv`：顶层接线与参数
  2. `src/dcr.sv`：DCR（设备控制寄存器；存放 kernel 元数据，本项目只存 `thread_count`）
  3. `src/dispatch.sv`：block 划分与 core 分发
  4. `src/core.sv`：每线程资源与 core 内接线
  5. `src/scheduler.sv`：六状态控制流
  6. `src/fetcher.sv` / `src/decoder.sv`：取指与控制信号
  7. `src/alu.sv` / `src/lsu.sv` / `src/registers.sv` / `src/pc.sv`：数据通路
  8. `src/controller.sv`：memory controller（访存控制器，仲裁并节流多核请求；用于匹配外部带宽）
- 测试：`test/test_matadd.py`、`test/test_matmul.py`、`test/helpers/`

## 代码阅读路线

按天推进，每天用一个自检问题收口。

1. **跑通与看 trace**：跑两个 kernel，在 trace 里找出一条 `LDR` 的 `REQUEST`/`WAIT` 周期。答：一次 `LDR` 至少占几个周期？
2. **顶层与分发**：`gpu.sv` → `dcr.sv` → `dispatch.sv`。答：8 个线程、每 block 4 线程时 `total_blocks` 是多少，两个 core 如何拿到各自的 `block_id`？
3. **core 与调度**：`core.sv` → `scheduler.sv`。答：`FETCH`/`DECODE`/`REQUEST`/`WAIT`/`EXECUTE`/`UPDATE` 中哪些固定一周期、哪些要等外部信号？
4. **数据通路**：`fetcher` / `decoder` / `alu` / `lsu` / `registers` / `pc`。答：`%threadIdx` 存在哪，`CMP` 的结果写到哪里？
5. **存储与带宽**：`controller.sv`。答：`NUM_CHANNELS=1` 时 4 个 LSU 同时请求会发生什么？
6. **动手改**：见下方任务。

## 运行

```bash
cd /localdata/linchen/tiny-gpu
mkdir -p build test/logs
make test_matadd
make test_matmul
```

Makefile 先用 `sv2v` 把 `src/*.sv` 合成 `build/gpu.v`，再用 `iverilog` 编译，最后由 `vvp` + cocotb 运行并输出 trace。

## 任务

- [ ] 跑通 matadd/matmul，保存两份 trace
- [ ] 手画一个 block 从 dispatch 到 done 的时序图（含 `core_start`/`core_done`）
- [ ] 手画 `LDR` 路径：decoder → LSU（加载存储单元；处理 load/store） → controller → 外部内存 → registers
- [ ] 加一条指令（建议 `AND` 或 `SHL`）：改 `decoder.sv` 的 16-bit 编码、`alu.sv` 的运算，并补一个 cocotb 测试
- [ ] 改 `NUM_CORES` / `THREADS_PER_BLOCK` / `DATA_MEM_NUM_CHANNELS`，记录 cycles，解释变化来自并行度还是带宽
- [ ] 二选一：加 instruction cache，或做 memory coalescing（访存合并，把相邻地址请求合成一个事务；用于降低事务数）
- [ ] 写一张「tiny-gpu 省略了什么 → 在 Vortex 哪里补」对照表

## 产出

- [ ] 一条 `LDR` 的路径图
- [ ] 一组「参数 → cycles」数据
- [ ] 一个新增指令的补丁与测试
- [ ] 「省略特性 → Vortex 对应机制」对照表

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| SIMT | 单指令多线程 | GPU 吞吐计算 | 一个 block 的线程共享控制流 |
| block | 分发到单个 core 的线程组 | 线程组织与调度 | 大小受每 core 的 ALU/LSU/寄存器资源限制 |
| thread | 独立寄存器/ALU/LSU/PC 的执行流 | kernel 并行基本单位 | 用 `%threadIdx` 区分数据 |
| DCR | 设备控制寄存器 | 存放 kernel 元数据 | 本项目只存 `thread_count` |
| dispatcher | block 分发器 | 把 block 分给空闲 core | 所有 block 完成才置 `done` |
| scheduler | core 内控制流状态机 | 单指令六状态推进 | 非流水，指令间串行 |
| LSU | 加载存储单元 | 访存指令 | 异步请求，需 `WAIT` 等待 |
| memory controller | 访存仲裁与节流 | 匹配外部带宽 | channel 数决定并发请求数 |
| 分支发散 | 线程走不同 PC | 真实 GPU 必需 | 本项目假设所有线程收敛 |
| cache | 片上缓存 | 降低访存延迟 | 本项目未实现，README 标 WIP |
| coalescing | 访存合并 | 降低事务数 | 真实 GPU 与 Vortex 实现 |
| pipelining | 多指令重叠执行 | 提高资源利用率 | 本项目每条指令串行走完六状态 |
| warp scheduling | 多 warp 交替发射 | 隐藏访存延迟 | Vortex 的调度器 |
| barrier | block 内线程同步 | 线程交换数据 | 本项目未实现 |

## 自检问题

- 为什么每个线程需要独立的 PC、寄存器和 ALU？
- block 与 thread 在硬件上分别落到哪个模块？
- `LDR` 为什么必须拆出 `REQUEST`/`WAIT`？去掉 `WAIT` 会错在哪？
- memory controller 的 channel 数与外部带宽是什么关系？
- matmul kernel 里的分支为什么能在这版硬件上跑对？换成数据相关分支会怎样？
- 加 instruction cache 后，trace 里哪个状态会变短？
- 它省略的六个特性（cache 层次、coalescing、pipelining、warp scheduling、分支发散、barrier）各自解决什么问题？

## 与后续阶段

| 这里缺的 | 去哪里补 |
|---|---|
| 流水线、冒险、旁路、scoreboard、ROB、精确异常 | [[Stage-1-Scalar-Core]] |
| RVV、VME、tile 数据流、向量访存 | [[Stage-2-RVV-VME]] |
| warp、分支发散、warp scheduler、cache 层次、MSHR、TCU、DXA | [[Stage-3-GPU]] |
| cocotb/UVM、lockstep、三方 cosim、保真度 | [[Stage-4-Verification]] |
| API/HAL/TOB、DMA、中断、eCPU | [[Stage-5-SDK]] |

进入 [[Stage-1-Scalar-Core]] 前，至少完成「跑通 + 读完全部 12 个 RTL 文件 + 加一条指令」。

## 相关

- [[Roadmap]]
- [[Stage-1-Scalar-Core]]
- [[Stage-3-GPU]]
- [[SIMT-and-Warp]]
- [[Cache-and-Memory]]
- [[Performance-Modeling]]
- [[Vortex]]
- [[Glossary]]
