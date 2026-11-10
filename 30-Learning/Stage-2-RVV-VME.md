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

理解解耦向量后端的执行模型，以及矩阵扩展的 tile（矩阵分块，把大矩阵切成小块；用于匹配片上存储与并行度）数据流。

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

- [ ] 画出 CQ(8)（命令队列，缓存待发射的向量指令；用于解耦前端取指与后端执行） → 2 级译码 → UQ(16) → RS（保留站，缓存已发射待执行的指令；用于动态调度） → VROB(16)（向量重排序缓冲，向量指令按序提交；用于精确异常） 的解耦后端
- [ ] 理解 SEW（元素宽度，向量中每个元素的位数；决定运算与访存粒度）/LMUL（向量寄存器分组倍数；控制向量长度与寄存器占用）/mask/strided/indexed 对 LSU（加载存储单元；处理向量 load/store） 的影响
- [ ] 理解 `vstart` 与精确异常
- [ ] 读 VME（CoralNPU 的矩阵扩展单元；用于 tile 级矩阵乘加）：16 个 matrix tile、M/N/K CSR（控制状态寄存器，这里存放矩阵维度 M/N/K）、PE array（处理单元阵列，二维乘加网格；用于矩阵乘加）
- [ ] 理解 `mload/mstore` 与 DTCM 的耦合
- [ ] 写一个小 GEMM（通用矩阵乘法，AI 与科学计算的核心算子），观察 tile 映射

## 产出

- [ ] RVV 后端框图
- [ ] VME tile 数据流图
- [ ] “解耦执行 vs 顺序执行”对比笔记

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| tile | 矩阵分块 | 匹配片上存储与并行度 | 分块大小要同时满足带宽、容量与 PE 阵列形状 |
| CQ | 命令队列 | 解耦前端取指与后端执行 | 队列深度影响向量核的吞吐与反压 |
| RS | 保留站 | 动态调度 | 与 VROB 配合，实现乱序执行、顺序提交 |
| VROB | 向量重排序缓冲 | 向量指令按序提交与精确异常 | 向量指令跨多周期，提交需等整条指令完成 |
| SEW | 元素宽度 | 决定运算与访存粒度 | SEW 与 LMUL 共同决定向量长度 |
| LMUL | 向量寄存器分组倍数 | 控制向量长度与寄存器占用 | LMUL 越大并行度越高，但寄存器压力也越大 |
| LSU | 加载存储单元 | 向量 load/store | strided/indexed 模式会显著改变访存效率 |
| VME | CoralNPU 的矩阵扩展单元 | tile 级矩阵乘加 | 与 RVV 解耦，专门处理矩阵数据流 |
| CSR | 控制状态寄存器 | 存放矩阵维度 M/N/K | M/N/K CSR 决定 tile 的循环边界 |
| PE array | 处理单元阵列 | 矩阵乘加 | 二维 PE 网格的形状直接影响吞吐与利用率 |
| GEMM | 通用矩阵乘法 | AI 与科学计算核心算子 | 观察 tile 映射是理解矩阵加速器的捷径 |
| bank conflict | 存储体冲突 | 评估片上存储带宽 | 合理的 tile 布局与填充可减少冲突 |

## 自检问题

- 向量指令为什么需要独立的 VROB？
- `vstart` 在精确异常里起什么作用？
- LMUL 如何影响寄存器分组与访存模式？
- ordered indexed 为什么要 strict 模式？
- VME 的 tile 布局如何避免 bank conflict（存储体冲突，多个访问命中同一 bank 导致串行化；用于评估片上存储带宽）？

## 相关

- [[Stage-1-Scalar-Core]]
- [[Stage-3-GPU]]
- [[Scratchpad-and-TCM]]
