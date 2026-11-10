---
type: stage
stage: 0
status: learning
projects: [CoralNPU, Vortex, ASIC-Cosim, Clounix-SDK]
tags:
  - learning/roadmap
created: 2026-11-10
---

# 学习路线

> 目标：建立从 RTL/微架构到验证，再到软硬件接口的完整芯片理解。

## 总览

| 阶段 | 主题 | 主项目 | 时间 | 核心产出 |
|---|---|---|---|---|
| [[Stage-1-Scalar-Core]] | 单核流水线 | CoralNPU | 2–3 周 | 一条指令的时序图 |
| [[Stage-2-RVV-VME]] | RVV / 矩阵 | CoralNPU | 3–4 周 | RVV/VME 数据流图 |
| [[Stage-3-GPU]] | SIMT / GPU | Vortex | 4–6 周 | GPU 存储层次 + 性能数据 |
| [[Stage-4-Verification]] | 验证方法学 | CoralNPU + ASIC-Cosim | 2–3 周 | 保真度对照表 |
| [[Stage-5-SDK]] | 软硬件接口 | Clounix-SDK | 1–2 周 | API → 表项调用链 |

## 原则

1. **先闭环再扩展**：先把一条指令、一个 kernel、一个测试跑通。
2. **以 RTL 为准**：文档口径不一致时，读 RTL。
3. **每个阶段都要动手改**：加 CSR、加指令、改参数。
4. **每个阶段都要有可观测证据**：trace、波形、周期、日志。
5. **一个概念一个家**：概念放 [[Topics-MOC]]，项目实现放对应 Hub。

## 最小可行闭环

- [ ] CoralNPU 跑通 `--instr_trace`
- [ ] 手画 `load` 路径
- [ ] 加一个 CSR/指令并通过 cocotb
- [ ] Vortex 跑 `sgemm`，改 warps/threads
- [ ] ASIC-Cosim 跑一个 feature test，对比 CMODEL/RTL

## 相关

- [[Four-Projects-Depth-Breadth]]
- [[Learning-Value]]
- [[Verification-Spectrum]]
- [[Multi-Chip-Patterns]]
