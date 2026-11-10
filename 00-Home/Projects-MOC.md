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
| [[CoralNPU]] | 可嵌入 SoC 的开源 RISC-V NPU IP | 芯片 IP + 验证 | 1（入门主线） |
| [[Vortex]] | 开源 RISC-V GPGPU 全栈 | 芯片 + 软件栈 | 2（GPU 进阶） |
| [[ASIC-Cosim]] | 交换 ASIC 多保真度协同仿真平台 | 验证基础设施 | 3（验证补充） |
| [[Clounix-SDK]] | 交换 ASIC SDK | 芯片软件/驱动 | 4（软件视角） |

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
