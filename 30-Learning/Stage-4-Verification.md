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

## 代码阅读路线

完整路线见 [[ASIC-Cosim#代码阅读路线]] 与 [[CoralNPU#代码阅读路线]]；本阶段把“验证手段”本身当代码读。

- ASIC-Cosim 第 1–3 步：`cosim_app*` 与 `*_access.cpp`，看五后端如何共享同一套控制面与访问语义。
- ASIC-Cosim 第 4–6 步：分别深入 `cmodel/`、`rtl/`、`emu/`，记录每个后端能暴露的问题类型。
- ASIC-Cosim 第 7–8 步：`mountains/nb/design.cpp` + `tests/features/test_l2.cpp`，跑通同一用例。
- CoralNPU 第 5、9 步：`RetirementBuffer.scala`/`RvviTrace.scala` + `tests/cocotb/`、`tests/uvm/`，理解 lockstep 观测点。

每读完一个后端，用 Hub 里该步的“读完能回答”自检，并把结论填进“保真度 vs 速度”对照表。

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

- [ ] 跑 cocotb（Python 驱动的 RTL 仿真框架；用于模块级功能验证） + UVM（通用验证方法学，SystemVerilog 验证框架；用于随机激励与覆盖率驱动验证）
- [ ] 理解 RTL（寄存器传输级设计；仿真时作为黄金参考）/MPACT（CoralNPU 的参考模型；用于与 RTL 对照）/Spike（RISC-V 官方指令集模拟器；用作黄金参考） 三方 cosim（协同仿真，多个模型同步运行并逐项比对；用于发现模型与 RTL 的偏差）
- [ ] 理解 RVVI（RISC-V 验证接口，暴露指令退休等观测点；用于 lockstep 比对） lockstep（锁步比对，参考模型与 RTL 逐指令同步；用于快速定位偏差） 与 ISG（指令序列生成器，自动产生随机激励；用于验证覆盖）
- [ ] 跑 ASIC-Cosim 的一个 feature test
- [ ] 对比 CMODEL（C/C++ 行为级参考模型；用于软件提前开发与结果对照）/RTL 的同一用例
- [ ] 理解 EMU（硬件仿真加速器，用 FPGA/专用硬件承载 RTL；用于大规模系统与软件验证） 的 PCIe/knet 路径

## 产出

- [ ] “同一测试在 CMODEL/RTL/LAB 上各能发现什么”对照表
- [ ] “保真度 vs 速度”取舍笔记
- [ ] 一份验证方法学总结

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| cocotb | Python 驱动的 RTL 仿真框架 | 模块级功能验证 | 与 UVM 相比更轻量，适合小型模块与快速回归 |
| UVM | 通用验证方法学 | 随机激励与覆盖率驱动验证 | 基于 SystemVerilog，适合芯片级 TB 复用 |
| RTL | 寄存器传输级设计 | 仿真时的黄金参考 | 只有 RTL 能暴露周期、时序与微架构问题 |
| MPACT | CoralNPU 的参考模型 | 与 RTL 对照 | 参考模型跑得快，但需警惕与 RTL 同时出错 |
| Spike | RISC-V 官方指令集模拟器 | 黄金参考 | 适合做指令流与架构状态的独立对照 |
| cosim | 协同仿真 | 发现模型与 RTL 的偏差 | 三方 cosim 比两方更容易定位谁错 |
| RVVI | RISC-V 验证接口 | lockstep 比对 | 提供指令退休等观测点，便于逐指令同步 |
| lockstep | 锁步比对 | 快速定位偏差 | 参考与实现逐指令同步，偏差出现处即嫌疑点 |
| ISG | 指令序列生成器 | 验证覆盖 | 自动产生随机激励，扩大状态空间 |
| CMODEL | C/C++ 行为级参考模型 | 软件提前开发与结果对照 | 便宜、跑得快，但保真度低于 RTL |
| EMU | 硬件仿真加速器 | 大规模系统与软件验证 | 比 RTL 仿真快，能跑驱动与 PCIe 路径 |

## 自检问题

- cocotb/UVM/三方 cosim 各自能发现什么？
- 哪些 bug 只能在 RTL/EMU/LAB 暴露？
- 如何设计一个跨后端 parity gate？
- 黄金模型本身错了怎么办？

## 相关

- [[Stage-3-GPU]]
- [[Stage-5-SDK]]
- [[Verification-Spectrum]]
