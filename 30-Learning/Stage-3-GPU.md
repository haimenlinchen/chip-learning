---
type: stage
stage: 3
status: todo
projects: [Vortex]
tags:
  - learning/roadmap
  - stage/gpu
created: 2026-11-10
---

# 阶段三：GPU 架构

## 目标

从“单核顺序”切换到“GPU（图形处理器，也用于通用并行计算）吞吐”，理解 SIMT（单指令多线程执行模型，一个 warp 的线程共享指令流；用于 GPU 吞吐计算）、cache（高速缓存，缓解处理器与主存的速度差；用于降低访存延迟）层次、TCU（张量计算单元，GPU 中的矩阵乘加加速器；用于 GEMM 与深度学习）与性能模型。

## 阅读

- [[Vortex]]
- [[Vortex-SIMT]]
- [[Vortex-Cache]]
- [[Vortex-TCU]]
- [[Vortex-DXA]]
- [[Vortex-CommandProcessor]]
- [[SIMT-and-Warp]]
- [[Cache-and-Memory]]
- [[Performance-Modeling]]
- `vortex/docs/designs/`

## 运行

```bash
# 配置与构建
mkdir -p build && cd build
../configure --xlen=64 --tooldir=$HOME/tools
./ci/toolchain_install.sh
make -s

# simx 跑 sgemm
./ci/blackbox.sh --driver=simx --app=sgemm --args="-n16"

# 改变 GPU 形状
./ci/blackbox.sh --driver=simx --app=sgemm \
  --clusters=1 --cores=2 --warps=4 --threads=4 --l2cache

# RTL 仿真
make -C tests/regression run-rtlsim
```

## 任务

- [ ] 理解 thread → warp（线程束，GPU 中一起执行的线程组；SIMT 的调度单位） → core → socket → cluster
- [ ] 理解 warp scheduler（线程束调度器，每周期挑选可发射的 warp；用于隐藏延迟）/ IPDOM（立即支配后置节点，处理分支发散后的重汇聚；用于 SIMT 控制流）/ scoreboard / IBuffer
- [ ] 理解 L1(socket 共享)/L2/L3/MSHR（未命中状态保持寄存器，跟踪未完成的缓存缺失；用于合并请求与减少停顿）/LLC（末级缓存，通常指 L3；用于降低主存访问） AMO
- [ ] 理解 TCU：WGMMA（warp 级矩阵乘加指令，一次完成 warp 范围的 GEMM；用于张量核加速）、tile、FEDP、2:4 稀疏、MX
- [ ] 理解 DXA（异步拷贝引擎，负责矩阵数据搬运；用于 TCU 的 K-major 加载）：异步拷贝、multicast、K-major
- [ ] 改 warps/threads/issue-width，画 roofline（屋顶线模型，用算力与带宽上限评估瓶颈；用于判断 compute-bound 还是 memory-bound）
- [ ] 对比 simx 与 rtlsim 的周期/退休指令

## 产出

- [ ] GPU 存储层次图
- [ ] “多 warp 隐藏延迟”的量化笔记
- [ ] 一组不同配置的性能数据
- [ ] simx vs rtlsim 对比记录

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| GPU | 图形处理器 | 图形与通用并行计算 | 现代 GPU 以吞吐为目标，用多 warp 隐藏延迟 |
| SIMT | 单指令多线程执行模型 | GPU 吞吐计算 | 与 SIMD 相比，SIMT 每线程有独立寄存器与分支状态 |
| cache | 高速缓存 | 降低访存延迟 | GPU 的 L1 常按 socket 共享，L2/L3 服务多核 |
| TCU | 张量计算单元 | GEMM 与深度学习 | 与 CUDA core 分工：TCU 做矩阵，CUDA core 做标量/向量 |
| warp | 线程束 | SIMT 调度单位 | 分支发散会让 warp 内线程串行执行 |
| warp scheduler | 线程束调度器 | 隐藏延迟 | 每周期从就绪 warp 中挑选发射，依赖 scoreboard |
| IPDOM | 立即支配后置节点 | SIMT 控制流重汇聚 | 用于处理分支发散后的 reconvergence |
| MSHR | 未命中状态保持寄存器 | 跟踪缓存缺失 | 合并对同一行的多次缺失，减少重复访存 |
| LLC | 末级缓存 | 降低主存访问 | 多核共享，容量与带宽影响带宽受限负载 |
| WGMMA | warp 级矩阵乘加指令 | 张量核加速 | 一次指令覆盖整个 warp 的矩阵乘 |
| DXA | 异步拷贝引擎 | TCU 数据搬运 | 与 TMA 类似，负责异步、多播、K-major 加载 |
| roofline | 屋顶线模型 | 判断性能瓶颈 | 用算力上限与带宽上限两条屋顶线定位优化方向 |

## 自检问题

- 为什么 L1 是 socket 共享？
- 多核没有 L2 时为什么丢 store？
- WGMMA 的 B 为什么必须来自 shared memory？
- DXA multicast 如何减少读放大？

## 相关

- [[Stage-2-RVV-VME]]
- [[Stage-4-Verification]]
- [[Four-Projects-Depth-Breadth]]
