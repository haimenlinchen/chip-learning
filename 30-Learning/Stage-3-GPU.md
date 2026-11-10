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

从“单核顺序”切换到“GPU 吞吐”，理解 SIMT、cache 层次、TCU 与性能模型。

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

- [ ] 理解 thread → warp → core → socket → cluster
- [ ] 理解 warp scheduler / IPDOM / scoreboard / IBuffer
- [ ] 理解 L1(socket 共享)/L2/L3/MSHR/LLC AMO
- [ ] 理解 TCU：WGMMA、tile、FEDP、2:4 稀疏、MX
- [ ] 理解 DXA：异步拷贝、multicast、K-major
- [ ] 改 warps/threads/issue-width，画 roofline
- [ ] 对比 simx 与 rtlsim 的周期/退休指令

## 产出

- [ ] GPU 存储层次图
- [ ] “多 warp 隐藏延迟”的量化笔记
- [ ] 一组不同配置的性能数据
- [ ] simx vs rtlsim 对比记录

## 自检问题

- 为什么 L1 是 socket 共享？
- 多核没有 L2 时为什么丢 store？
- WGMMA 的 B 为什么必须来自 shared memory？
- DXA multicast 如何减少读放大？

## 相关

- [[Stage-2-RVV-VME]]
- [[Stage-4-Verification]]
- [[Four-Projects-Depth-Breadth]]
