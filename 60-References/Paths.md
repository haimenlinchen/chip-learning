---
type: reference
aliases: [路径速查, Paths]
tags:
  - type/reference
created: 2026-11-10
---

# 关键路径速查

目录树用于定位文件；先读哪个文件、按什么顺序读，由各项目 Hub 的「代码阅读路线」决定。本页只回答“东西在哪”。

## tiny-gpu

关键术语：SIMT（单指令多线程；GPU 执行模型）、LSU（加载存储单元；处理 load/store）。阅读顺序见 [[Stage-0-tiny-gpu]]。

```text
/localdata/linchen/tiny-gpu/
├── README.md                    架构 / ISA / 执行流程
├── src/gpu.sv                   顶层：DCR、dispatch、cores、memory controllers
├── src/dispatch.sv              block 划分与 core 分发
├── src/core.sv                  每线程寄存器 / ALU / LSU / PC
├── src/scheduler.sv             六状态控制流
├── src/controller.sv            访存仲裁与带宽节流
├── test/test_matadd.py          矩阵加 kernel 与断言
├── test/test_matmul.py          矩阵乘 kernel 与断言
└── test/helpers/                时钟、内存模型与 trace 格式化
```

## CoralNPU

关键术语：RTL（寄存器传输级；用于描述硬件）、RVV（RISC-V 向量扩展；用于向量计算）。

```text
/localdata/linchen/coralnpu/
├── doc/overview.md                 架构总览
├── doc/microarch/microarch.md      流水线
├── doc/microarch/dispatch.md       派发规则
├── doc/microarch/lsu.md            LSU
├── doc/microarch/mlu.md            MLU
├── doc/integration_guide.md        AXI/内存映射/启动
├── hdl/chisel/src/coralnpu/scalar/ 标量核
├── hdl/chisel/src/coralnpu/rvv/    RVV 包装
├── hdl/verilog/rvv/design/         RVV 后端
├── hdl/verilog/rvv/design/Zvt/     矩阵扩展
├── tests/cocotb/                   cocotb 测试
├── tests/uvm/                      UVM 测试
└── examples/                       示例程序
```

## Vortex

关键术语：SIMT（单指令多线程；GPU 执行模型）、TCU（张量核；用于矩阵乘）。

```text
/localdata/linchen/vortex/
├── docs/designs/microarchitecture.md        SIMT/流水线
├── docs/designs/cache_subsystem.md          存储层次
├── docs/designs/tensor_core_wgmma_engine.md TCU
├── docs/designs/dxa_async_copy_multicast.md DXA
├── docs/designs/command_processor.md        命令处理器
├── VX_config.toml                           配置系统
├── hw/rtl/                                  RTL
├── sim/simx/                                周期近似模型
├── sw/runtime/                              host runtime
└── tests/regression/                        回归测试
```

## ASIC-Cosim

关键术语：DPI（SystemVerilog 与 C 的接口；用于协同仿真）、EMU（硬件仿真；用于接近实速验证）。

```text
/localdata/linchen/asic-cosim/
├── README.md                               构建/运行入口
├── src/cosim/cmodel/cmodel.h               C-model 接口
├── src/cosim/rtl/rtl_dpi.h                 RTL DPI
├── src/cosim/emu/emu.h                     EMU 后端
├── src/cosim/lab/                          LAB 后端
├── src/cosim/mountains/{nb,kg}/            芯片相关模型
├── tests/features/                         gtest 功能测试
└── saithriftv2/ptf/                        PTF 测试
```

## Clounix-SDK

关键术语：HAL（硬件抽象层；屏蔽底层差异）、TOB（表操作总线；用于表项读写）。

```text
/localdata/linchen/clounix-sdk-et/
├── clx_sdk/include/clx/      CLX API（约 37 个模块）
├── clx_sdk/src/clx/          API 实现
├── clx_sdk/src/hal/          HAL
├── clx_sdk/src/tob/          Table Operation Bus
├── clx_sdk/src/drv/          驱动（IO/DMA）
├── clx_sdk/src/osal/         OSAL / knet
├── app/sdk_sample/           最小示例
├── app/diag_shell/           诊断 CLI
├── app/neutrino_server/      RPC 服务端
└── ecpu_fw.mk                eCPU 固件
```

## 相关

- [[Commands]]
- [[Glossary]]

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| RTL | 寄存器传输级 | 描述与仿真硬件 | 对应 `hdl/` 目录 |
| RVV | RISC-V 向量扩展 | 向量计算 | 对应 `rvv/` 目录 |
| SIMT | 单指令多线程 | GPU 执行模型 | 对应 `sim/simx/` |
| TCU | 张量核 | 矩阵乘加速 | 对应 tensor core 文档 |
| DXA | 异步拷贝/多播单元 | 数据搬运 | 对应 DXA 文档 |
| DPI | SV 与 C 的接口 | 协同仿真 | 对应 `rtl_dpi.h` |
| HAL | 硬件抽象层 | 屏蔽底层差异 | 对应 `src/hal/` |
| TOB | 表操作总线 | 表项读写 | 对应 `src/tob/` |
