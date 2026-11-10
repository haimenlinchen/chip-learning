---
type: project-hub
project: ASIC-Cosim
aliases: [asic-cosim, ASIC Cosim, 交换芯片协同仿真]
status: learning
tags:
  - project/asic-cosim
  - chip/verification
source_repo: /localdata/linchen/asic-cosim
created: 2026-11-10
---

# ASIC-Cosim

## 一句话定位

Clounix 内部 ASIC 验证协同仿真环境：同一套 SAI/CLI/PTF 控制面，接 CMODEL/EMU/RTL/LAB/NOMODEL 五种执行后端。

## 架构骨架

- 后端：CMODEL（预编译 `libcx_model.so`）、EMU（PCIe/knet）、RTL（DPI）、LAB（真实硬件）、NOMODEL
- C-model：交换流水线 PP/PL/TM/PCX/CSS/IGR/EGR/FPU、bloomfilter、hash、PacketGen
- 规模：NB 1 pie × 25.6T；KG 2 pie × 51.2T；112G PAM4 SerDes
- 控制面：SAI-Thrift、CLI telnet、PTF、pytest、gtest、pcap、traffic、chassis、netlink/FRR
- 调试：iPython / iCling / Jupyter / gdb / valgrind

## 关键子系统

- [[ASIC-Cosim-Five-Backends]]
- [[ASIC-Cosim-CMODEL]]
- [[ASIC-Cosim-EMU]]
- [[ASIC-Cosim-RTL-DPI]]
- [[ASIC-Cosim-SAI-PTF]]

## 相关概念

- [[Verification-Fidelity]]
- [[Software-Interface]]
- [[Cache-and-Memory]]（对照模型内存/backdoor）

## 学习阶段

- [[Stage-4-Verification]]

## 代码入口

- `README.md`
- `src/cosim/cmodel/cmodel.h`
- `src/cosim/rtl/rtl_dpi.h`
- `src/cosim/emu/emu.h`
- `src/cosim/lab/`
- `src/cosim/mountains/{nb,kg}/`
- `tests/features/`
- `saithriftv2/ptf/`

## 实验记录

- [ ] 跑一个 feature gtest（cmodel）
- [ ] 对比 CMODEL 与 RTL 的同一用例
- [ ] 理解 EMU 的 PCIe/knet 路径
- [ ] 画五后端与 SAI/PTF 的关系图

## 开放问题

- 同一 SAI 用例在 CMODEL/RTL/LAB 上的差异如何自动比对？
- EMU 与 RTL 的边界：哪些问题只能在 EMU 暴露？
- 预编译 C-model 与 RTL 的版本如何保持同步？

## 来源

- `README.md`
- `src/cosim/CMakeLists.txt`
- `src/cosim/cmodel/cmodel.h`
