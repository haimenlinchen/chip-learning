---
type: moc
aliases: [Topics MOC, 技术主题索引]
tags:
  - type/moc
created: 2026-11-10
---

# 技术主题索引

## ISA 与执行模型

- [[ISA-and-Extensions]]
- [[Pipeline-and-Hazards]]
- [[SIMT-and-Warp]]
- [[Vector-Architecture]]
- [[Matrix-Accelerator]]

## 存储与数据通路

- [[Cache-and-Memory]]
- [[Scratchpad-and-TCM]]

## 验证与仿真

- [[Verification-Fidelity]]
- [[Performance-Modeling]]

## 软硬件接口

- [[Software-Interface]]

## 按层级查看

```dataview
TABLE project, status
FROM #type/atomic
GROUP BY layer
```

## 按项目查看

```dataview
TABLE layer, status
FROM #type/atomic
GROUP BY project
```
