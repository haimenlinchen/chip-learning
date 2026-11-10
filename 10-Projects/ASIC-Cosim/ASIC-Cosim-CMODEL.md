---
type: atomic
project: ASIC-Cosim
layer: verification
topic: [cmodel, switch-pipeline]
status: learning
source_repo: /localdata/linchen/asic-cosim
source_files:
  - src/cosim/cmodel/cmodel.h
  - CMakeLists.txt
tags:
  - layer/verification
  - topic/cmodel
created: 2026-11-10
---

# CMODEL

## 定义

CMODEL 是交换 ASIC 的预编译功能模型：`libcx_model.so` + `libutils.so`，由 asic-cosim 的 `clxsim_cmodel_t` 驱动。

## 如何工作

- CMake 链接预编译库：
  - `${PREBUILT_PATH}/lib/libcx_model.so`
  - `${PREBUILT_PATH}/lib/libutils.so`
- 模型覆盖交换流水线：PP/PL/TM/PCX/CSS/IGR/EGR/FPU、bloomfilter、hash、PacketGen、parser、sampler。
- `clxsim_cmodel_t` 实现 `clxsim_chip_i`，提供 startup/shutdown/ticking/recirc 等接口。
- 支持 packet send/recv、寄存器访问、backdoor load。

## 关键细节

- NB：1 pie × 25.6T；KG：2 pie × 51.2T。
- 8 slices/pie、4 front-panel MAC/slice、8 PAM4 112Gbps SerDes/MAC（NB），KG 为 16 SerDes/MAC。
- 端口/切片常量：`PIE_PER_CHIP`、`SLICE_PER_PIE`、`PORT_PER_SLICE`、`FP_PORT_PER_SLICE`。
- chassis 索引偏移：source/tunnel/LAG/L2MC/L3MC 各有 per-slot offset。

## 在项目中的位置

- 所属项目：[[ASIC-Cosim]]
- 相关子系统：[[ASIC-Cosim-Five-Backends]]、[[ASIC-Cosim-SAI-PTF]]

## 相关概念

- [[Verification-Fidelity]]
- [[Performance-Modeling]]

## 自检问题

- C-model 的“功能级”具体省略了哪些时序细节？
- 25.6T/51.2T 与 slice/MAC/SerDes 的关系？
- backdoor load 与 frontdoor AXI load 的差异？
- chassis 索引偏移为什么按 slot 计算？

## 来源

- `src/cosim/cmodel/cmodel.h`
- `CMakeLists.txt`
- `config/skucfg/`
