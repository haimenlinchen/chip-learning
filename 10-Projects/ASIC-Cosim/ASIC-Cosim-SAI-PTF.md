---
type: atomic
project: ASIC-Cosim
layer: verification
topic: [sai, ptf, cli, traffic]
status: learning
source_repo: /localdata/linchen/asic-cosim
source_files:
  - README.md
  - tests/features/
  - saithriftv2/ptf/
tags:
  - layer/verification
  - topic/sai-ptf
created: 2026-11-10
---

# SAI / PTF / CLI 测试面

## 定义

asic-cosim 用 SAI（Switch Abstraction Interface，交换机抽象接口标准；用于统一不同交换芯片的配置 API）-Thrift（跨语言 RPC 框架；用于 SAI 客户端与芯片服务通信）、CLI（Command Line Interface，命令行接口；用于人工调试和脚本化命令）、PTF（Packet Test Framework，报文测试框架；用于交换芯片数据面测试）、pytest（Python 测试框架；用于功能与集成测试）/gtest（Google Test，C++ 单元测试框架；用于模型与工具单元测试）组成统一的测试面，同一套用例可以跑在不同后端上。

## 如何工作

- **SAI-Thrift**：默认 TCP（Transmission Control Protocol，可靠传输层协议；用于 RPC 连接）6800，SONiC（Software for Open Networking in the Cloud，开源网络操作系统；用于承载 SAI 控制面）/SAI 客户端通过 thrift 调用交换芯片 API。
- **CLI**：默认 telnet（远程终端协议；用于登录设备命令行）6500，人工调试与脚本化命令。
- **PTF**：Packet Test Framework，发/收包并断言。
- **pytest / gtest**：功能测试与单元测试。
- **pcap（packet capture，抓包文件格式；用于回放与比对报文）/ traffic / chassis（机箱，多槽位设备模型；用于多芯片/多板卡测试）**：包样例、流量生成、机箱模拟。
- **netlink（Linux 内核与用户态通信的套接字；用于路由/接口配置下发）/FRR（FRRouting，开源路由协议套件；用于 BGP/OSPF 等路由协议集成）**：路由协议集成。
- **iPython / iCling / Jupyter（交互式笔记本环境；用于脚本化调试与结果展示）**：交互式调试。

## 关键细节

- 启动后可同时提供 SAI RPC、CLI、Jupyter 三个入口。
- `test_feature cmodel --debug -e --portlist=...` 是最小功能测试入口。
- 需要 `/dev/net/tun`（`tools/mktun.sh`）和 root/privileged Docker。
- 测试既可以在 CMODEL 上跑，也可以切到 EMU/RTL/LAB。

## 在项目中的位置

- 所属项目：[[ASIC-Cosim]]
- 相关子系统：[[ASIC-Cosim-Five-Backends]]、[[ASIC-Cosim-CMODEL]]

## 相关概念

- [[Verification-Fidelity]]
- [[Software-Interface]]

## 自检问题

- 同一 SAI 用例在 CMODEL/RTL/LAB 上如何比较结果？
- PTF 与 gtest 各自适合什么测试？
- CLI 与 SAI 两条路径如何共享底层？
- chassis 模拟解决什么问题？

## 概念速览

| 概念 | 是什么 | 使用场景 | 延伸 |
|---|---|---|---|
| SAI | 交换机抽象接口标准 | 统一不同交换芯片的配置 API | 上层 SONiC 通过它屏蔽芯片差异 |
| Thrift | 跨语言 RPC 框架 | SAI 客户端与芯片服务通信 | 默认端口 6800，接口由 IDL 定义 |
| CLI | 命令行接口 | 人工调试、脚本化命令 | 默认 telnet 6500，适合快速排查 |
| PTF | 报文测试框架 | 交换芯片数据面测试 | 负责发包、收包与断言，常与 SAI 配置配合 |
| pytest | Python 测试框架 | 功能与集成测试 | 适合组织跨后端的高层用例 |
| gtest | C++ 单元测试框架 | 模型与工具单元测试 | 适合细粒度、可重复的本地测试 |
| TCP | 可靠传输层协议 | RPC 连接 | Thrift 默认基于 TCP，端口可配置 |
| SONiC | 开源网络操作系统 | 承载 SAI 控制面 | 通过 SAI 驱动不同厂商交换芯片 |
| telnet | 远程终端协议 | 登录设备命令行 | 明文传输，仅适合实验环境 |
| pcap | 抓包文件格式 | 回放与比对报文 | 可作为 PTF 用例的报文样例来源 |
| chassis | 机箱/多槽位设备模型 | 多芯片、多板卡测试 | 关注槽位偏移与跨芯片链路 |
| netlink | Linux 内核与用户态通信套接字 | 路由/接口配置下发 | 驱动与内核网络栈交互的常用通道 |
| FRR | 开源路由协议套件 | BGP/OSPF 等协议集成 | 与 netlink 配合验证路由下发路径 |
| Jupyter | 交互式笔记本环境 | 脚本化调试与结果展示 | 与 iPython、iCling 共同提供在线调试入口 |

## 来源

- `README.md`
- `tests/features/`
- `saithriftv2/ptf/`
