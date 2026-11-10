---
type: stage
stage: 4
status: todo
projects: [CoralNPU, ASIC-Cosim, Vortex]
tags:
  - learning/roadmap
  - stage/verification
created: 2026-11-10
---

# 阶段四：验证与系统

## 目标

理解“怎么证明设计是对的”，以及不同保真度后端的取舍。

## 阅读

- [[CoralNPU-Verification]]
- [[ASIC-Cosim]]
- [[ASIC-Cosim-Five-Backends]]
- [[ASIC-Cosim-CMODEL]]
- [[ASIC-Cosim-EMU]]
- [[ASIC-Cosim-RTL-DPI]]
- [[ASIC-Cosim-SAI-PTF]]
- [[Verification-Fidelity]]
- `coralnpu/tests/cocotb/README.md`
- `coralnpu/tests/uvm/README.md`
- `asic-cosim/README.md`

## 运行

### CoralNPU

```bash
bazel test //tests/cocotb:core_mini_axi_sim_cocotb
bazel test //tests/cocotb:nop_stress_test_uvm
```

### ASIC-Cosim

```bash
./bootstrap.sh
./cosimbld bash
mkdir -p build && cd build && cmake -B. -S../ && make -j8
sudo ../tools/mktun.sh
bin/test_feature cmodel --debug -e --portlist=0,8,16,24
```

## 任务

- [ ] 跑 cocotb + UVM
- [ ] 理解 RTL/MPACT/Spike 三方 cosim
- [ ] 理解 RVVI lockstep 与 ISG
- [ ] 跑 ASIC-Cosim 的一个 feature test
- [ ] 对比 CMODEL/RTL 的同一用例
- [ ] 理解 EMU 的 PCIe/knet 路径

## 产出

- [ ] “同一测试在 CMODEL/RTL/LAB 上各能发现什么”对照表
- [ ] “保真度 vs 速度”取舍笔记
- [ ] 一份验证方法学总结

## 自检问题

- cocotb/UVM/三方 cosim 各自能发现什么？
- 哪些 bug 只能在 RTL/EMU/LAB 暴露？
- 如何设计一个跨后端 parity gate？
- 黄金模型本身错了怎么办？

## 相关

- [[Stage-3-GPU]]
- [[Stage-5-SDK]]
- [[Verification-Spectrum]]
