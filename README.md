---
type: reference
aliases: [Chip Vault README]
tags:
  - type/reference
created: 2026-11-10
---

# Chip Learning Vault

一个用于学习芯片架构、验证与软硬件接口的 Obsidian（Markdown 笔记软件；用于本地知识库）vault（Obsidian 的笔记库；一个文件夹即一个 vault）。

## 快速开始

1. 用 Obsidian 打开本目录（`Open folder as vault`）。
2. 从 `00-Home/Home.md` 开始。
3. 推荐安装插件：
   - **Dataview**（Obsidian 查询插件；用查询动态生成列表/表格）：动态索引（Home/MOC（Map of Content，内容地图/索引页；用于组织入口）里的查询需要它）
   - **Templater**（模板插件；用于自动填充日期/标题）：模板变量（`{{date}}`、`{{title}}`）
   - **Advanced Tables**：表格编辑
   - **Excalidraw**（手绘风格绘图插件；用于画架构图）：手绘架构图（可选）
   - **Git**：版本管理（可选）

## 目录

```text
00-Home/        入口与 MOC
10-Projects/    四个项目 Hub + 子系统笔记
20-Topics/      跨项目概念笔记
30-Learning/    学习路线与阶段
40-Synthesis/   横向对比/总结
50-Notes/       代码阅读、实验、Q-A
60-References/  路径、命令、术语
90-Assets/      图片/图表
Templates/      笔记模板
```

## 约定

- 文件名用英文 + 连字符，中文名放 `aliases`。
- 概念笔记放 `20-Topics`，项目实现放 `10-Projects`，对比放 `40-Synthesis`。
- 每个原子笔记链接回项目 Hub 和相关概念。
- 每个实验记录 commit/配置/命令/原始输出。
- 一个概念只在一个地方详细写，其他地方用双链指过去。

## 校验

```bash
python3 scripts/validate_vault.py
```

CI（持续集成；用于自动校验）会在 push/PR 时运行同一脚本，检查 wikilink、frontmatter 与 Canvas JSON（Obsidian 白板文件格式；用于保存手绘图）。

## 推荐阅读顺序

1. `00-Home/Home.md`
2. `30-Learning/Roadmap.md`
3. `40-Synthesis/Four-Projects-Depth-Breadth.md`
4. `10-Projects/CoralNPU/CoralNPU.md`
5. `30-Learning/Stage-1-Scalar-Core.md`
