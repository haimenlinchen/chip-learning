---
type: moc
aliases: [Projects MOC, 项目索引]
tags:
  - type/moc
created: 2026-11-10
---

# 项目索引

| 项目 | 一句话定位 | 技术层 | 学习优先级 |
|---|---|---|---|
| [[CoralNPU]] | 可嵌入 SoC（片上系统，把 CPU/外设集成到单芯片）的开源 RISC-V NPU（神经网络处理器，专用 AI 推理加速器；用于边缘 AI 推理） IP | 芯片 IP + 验证 | 1（入门主线） |
| [[Vortex]] | 开源 RISC-V GPGPU（通用 GPU 计算，用 GPU 做非图形的高吞吐计算；用于并行负载）全栈 | 芯片 + 软件栈 | 2（GPU 进阶） |
| [[ASIC-Cosim]] | 交换 ASIC（专用集成电路，为特定任务定制的芯片；用于网络交换）多保真度（cmodel/RTL/EMU 等不同精度模型；用于速度与精度取舍）协同仿真平台 | 验证基础设施 | 3（验证补充） |
| [[Clounix-SDK]] | 交换 ASIC SDK（软件开发包；用于配置交换芯片与开发驱动） | 芯片软件/驱动 | 4（软件视角） |

## 项目 Hub

```dataview
TABLE project, status, source_repo
FROM "10-Projects"
WHERE type = "project-hub"
SORT file.name ASC
```

## 相关对比

- [[Four-Projects-Depth-Breadth]]
- [[Verification-Spectrum]]
- [[Multi-Chip-Patterns]]
- [[Learning-Value]]
