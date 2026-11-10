---
type: stage
stage: 2
status: todo
projects: [CoralNPU]
tags:
  - learning/roadmap
  - stage/rvv
created: 2026-11-10
---

# 阶段二：RVV 与 VME

## 目标

理解解耦向量后端的执行模型，以及矩阵扩展的 tile 数据流。

## 阅读

- [[CoralNPU-RVV]]
- [[CoralNPU-VME]]
- [[Vector-Architecture]]
- [[Matrix-Accelerator]]
- `coralnpu/doc/overview.md` 的 RVV/VME 部分
- `coralnpu/hdl/chisel/src/coralnpu/rvv/`
- `coralnpu/hdl/verilog/rvv/design/`
- `coralnpu/hdl/verilog/rvv/design/Zvt/`

## 运行

```bash
# RVV intrinsics 示例
bazel build //examples:rvv_add_intrinsic

# cocotb RVV 测试（具体 target 以 tests/cocotb/BUILD 为准）
bazel test //tests/cocotb:rvv_load_store_test
```

## 任务

- [ ] 画出 CQ(8) → 2 级译码 → UQ(16) → RS → VROB(16) 的解耦后端
- [ ] 理解 SEW/LMUL/mask/strided/indexed 对 LSU 的影响
- [ ] 理解 `vstart` 与精确异常
- [ ] 读 VME：16 个 matrix tile、M/N/K CSR、PE array
- [ ] 理解 `mload/mstore` 与 DTCM 的耦合
- [ ] 写一个小 GEMM，观察 tile 映射

## 产出

- [ ] RVV 后端框图
- [ ] VME tile 数据流图
- [ ] “解耦执行 vs 顺序执行”对比笔记

## 自检问题

- 向量指令为什么需要独立的 VROB？
- `vstart` 在精确异常里起什么作用？
- LMUL 如何影响寄存器分组与访存模式？
- ordered indexed 为什么要 strict 模式？
- VME 的 tile 布局如何避免 bank conflict？

## 相关

- [[Stage-1-Scalar-Core]]
- [[Stage-3-GPU]]
- [[Scratchpad-and-TCM]]
