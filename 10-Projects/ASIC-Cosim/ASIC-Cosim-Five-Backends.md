---
type: atomic
project: ASIC-Cosim
layer: verification
topic: [cosim, backend, fidelity]
status: learning
source_repo: /localdata/linchen/asic-cosim
source_files:
  - README.md
  - src/cosim/cmodel/cmodel.h
  - src/cosim/emu/emu.h
  - src/cosim/rtl/rtl_dpi.h
tags:
  - layer/verification
  - topic/cosim
created: 2026-11-10
---

# 五种执行后端

## 定义

asic-cosim 用统一的控制面（SAI/CLI/PTF）驱动五种执行环境，用保真度换速度。

| 后端 | 模型 | 速度 | 保真度 | 典型用途 |
|---|---|---|---|---|
| CMODEL | 预编译 `libcx_model.so` | 快 | 功能级 | 日常回归、表项/包转发 |
| EMU | PCIe/knet + DMA ring | 中 | 内核/PCIe 路径 | 驱动、中断、DMA |
| RTL | DPI 连接 RTL DUT | 慢 | 周期/信号级 | 微架构、时序、联调 |
| LAB | i2c/PCIe 真实硬件 | 真实 | 硅后 | 实验室验证、模拟前端 |
| NOMODEL | 无模型 | 最快 | 无 | Python 脚本/测试框架开发 |

## 如何工作

- `cmodel`：`clxsim_cmodel_t` 实现 `clxsim_chip_i`，链接 `libcx_model.so`/`libutils.so`。
- `emu`：`clxsim_emu_t` 继承 `clxsim_rtl_t`，通过 PCIe/knet 访问设备，维护 DMA ring 与 FIFO。
- `rtl`：`nbrtl_*` DPI API，支持寄存器读写、收发包、复位、命令。
- `lab`：`lab_access`/`lab_i2c`/`lab_cli`，访问真实硬件。
- `nomodel`：只跑控制面/脚本。

## 关键细节

- `sim_level`：0-API、1-Register。
- `--backdoor_load` 可直接把 ELF 写入仿真 SRAM。
- CMODEL/EMU/RTL 都能接 SAI-Thrift（默认 6800）与 CLI（默认 6500）。
- 同一测试脚本可切换后端，但不同后端的可见问题不同。

## 在项目中的位置

- 所属项目：[[ASIC-Cosim]]
- 相关子系统：[[ASIC-Cosim-CMODEL]]、[[ASIC-Cosim-EMU]]、[[ASIC-Cosim-RTL-DPI]]、[[ASIC-Cosim-SAI-PTF]]

## 相关概念

- [[Verification-Fidelity]]
- [[Performance-Modeling]]

## 自检问题

- 哪些 bug 只能在 RTL 暴露，哪些在 CMODEL 就能发现？
- EMU 与 RTL 的边界在哪里？
- LAB 后端为什么不可替代？
- 如何保证同一用例在不同后端上可比？

## 来源

- `README.md`
- `src/cosim/cmodel/cmodel.h`
- `src/cosim/emu/emu.h`
- `src/cosim/rtl/rtl_dpi.h`
