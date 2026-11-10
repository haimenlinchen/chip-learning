---
type: index
aliases: [Assets Index]
tags:
  - type/index
created: 2026-11-10
---

# Assets

存放图片、波形（waveform：信号随时间变化的记录；用于分析时序）截图、手绘图、Canvas（Obsidian 白板/画布；用于绘制架构图）导出图等。

建议：

```text
90-Assets/
├── diagrams/       # 架构图、流水线图、数据流图
└── images/         # 截图、波形、照片
```

命名：

```text
<Project>-<Topic>-<Version>.png
例：CoralNPU-RVV-Backend-v1.png
    Vortex-Cache-Hierarchy-v1.png
```

在笔记中使用 Obsidian 的 embed（嵌入语法：把图片/笔记内容直接显示在当前笔记；用于图文对照）语法（`!` + 双链（wikilink：笔记间链接；用于建立关联））引用图片，例如把上面的文件名嵌入到对应笔记中。

大文件建议不要进 Git（版本管理系统；用于跟踪笔记与资产变更）；用 `.gitignore` 排除或在外部备份。
