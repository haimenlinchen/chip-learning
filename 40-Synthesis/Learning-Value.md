---
type: synthesis
aliases: [学习价值, Learning Value]
tags:
  - type/synthesis
  - learning/roadmap
created: 2026-11-10
---

# 学习价值

## 按目标选项目

| 学习目标 | 首选 | 次选 | 理由 |
|---|---|---|---|
| 数字前端/RTL/流水线 | [[CoralNPU]] | [[Vortex]] | CoralNPU 规模可控、文档全、可端到端追踪 |
| 计算机体系结构（顺序核） | [[CoralNPU]] | — | 4 宽、scoreboard、ROB、RVV |
| GPU/SIMT/存储层次 | [[Vortex]] | — | 完整 SIMT、cache/MSHR、TCU、DXA |
| 向量/矩阵加速器 | [[CoralNPU]] | [[Vortex]] | RVV + VME；Vortex TCU 更复杂 |
| 性能建模 | [[Vortex]] | [[CoralNPU]] | simx + roofline + parity gate |
| 验证方法学 | [[CoralNPU]] + [[ASIC-Cosim]] | [[Vortex]] | 三方 cosim、五后端、SAI/PTF |
| 软硬件接口/驱动 | [[Clounix-SDK]] | [[CoralNPU]] | API/HAL/TOB/DRV/OSAL、user/kernel |
| 多芯片/产品化 | [[Clounix-SDK]] | — | 3 代芯片、HAL/TOB 分层 |

## 推荐路径

```text
CoralNPU（单核 → RVV/VME）
   ↓
Vortex（SIMT → cache → TCU → 性能模型）
   ↓
ASIC-Cosim（五后端 → SAI/PTF → 验证方法学）
   ↓
Clounix-SDK（API → HAL → TOB → 驱动）
```

## 一句话

- **CoralNPU 教你“一颗核怎么工作”。**
- **Vortex 教你“一颗 GPU 怎么工作”。**
- **ASIC-Cosim 教你“怎么证明它工作”。**
- **Clounix-SDK 教你“软件怎么用它”。**

## 相关

- [[Roadmap]]
- [[Four-Projects-Depth-Breadth]]
- [[Verification-Spectrum]]
