---
type: reference
aliases: [路径速查, Paths]
tags:
  - type/reference
created: 2026-11-10
---

# 关键路径速查

## CoralNPU

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
