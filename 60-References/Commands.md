---
type: reference
aliases: [命令速查, Commands]
tags:
  - type/reference
created: 2026-11-10
---

# 构建 / 运行命令速查

> 命令以仓库文档为准；路径/参数可能随版本变化。

## CoralNPU

涉及 Bazel（构建系统；用于编译仿真器与示例）与 ELF（可执行与可链接格式；用于加载程序到仿真器）。

```bash
# 构建验证版仿真器
bazel build //tests/verilator_sim:core_mini_verification_axi_sim

# 构建示例
bazel build //examples:coralnpu_v2_hello_world_add_floats

# 查 ELF 实际路径
bazel cquery --output=files //examples:coralnpu_v2_hello_world_add_floats

# 运行 + 指令 trace
./bazel-bin/tests/verilator_sim/core_mini_verification_axi_sim \
  --binary="<ELF 路径>" --backdoor_load --instr_trace

# cocotb / UVM
bazel test //tests/cocotb:core_mini_axi_sim_cocotb
bazel test //tests/cocotb:nop_stress_test_uvm
```

## Vortex

涉及 simx（周期近似模型；用于快速性能评估）与 SGEMM（单精度矩阵乘；用于 GPU 基准测试）。

```bash
mkdir -p build && cd build
../configure --xlen=64 --tooldir=$HOME/tools
./ci/toolchain_install.sh
make -s

# simx
./ci/blackbox.sh --driver=simx --app=sgemm --args="-n16"

# 改 GPU 形状
./ci/blackbox.sh --driver=simx --app=sgemm \
  --clusters=1 --cores=2 --warps=4 --threads=4 --l2cache

# RTL 回归
make -C tests/regression run-rtlsim
```

## ASIC-Cosim

涉及 cmodel（C/C++ 功能模型；用于快速功能仿真）与 TUN（虚拟网络设备；用于数据面注入）。

```bash
./bootstrap.sh
./cosimbld bash
mkdir -p build && cd build && cmake -B. -S../ && make -j8

sudo ../tools/mktun.sh
bin/test_feature cmodel --debug -e --portlist=0,8,16,24
./bin/run_cosim_cmodel --help
```

## Clounix-SDK

涉及 eCPU（交换 ASIC 内置嵌入式 CPU；用于运行控制面固件）。

```bash
# 查看构建开关
cat config.mk

# 构建 SDK（具体 target 以 Makefile 为准）
make

# ASIC 仿真构建
make asicsim
make asicsim-lib

# eCPU 固件
make ecpu-fw-download
make ecpu-fw-app-list
```

## 相关

- [[Paths]]
- [[Glossary]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| Bazel | 构建系统 | 编译仿真器与示例 | 用 cquery 查产物路径 |
| ELF | 可执行与可链接格式 | 加载程序到仿真器 | 用 `--binary` 指定 |
| simx | 周期近似模型 | 快速性能评估 | 与 RTL 回归对比 |
| SGEMM | 单精度矩阵乘 | GPU 基准测试 | 调 clusters/cores/warps |
| cmodel | C/C++ 功能模型 | 快速功能仿真 | 与 RTL 对比 |
| TUN | 虚拟网络设备 | 数据面注入 | `mktun` 创建 |
| eCPU | 嵌入式 CPU | 控制面固件 | 查看 fw app list |
| SDK | 软件开发包 | 配置芯片与驱动 | API → HAL → TOB |
