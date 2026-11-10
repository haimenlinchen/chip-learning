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

asic-cosim 用 SAI-Thrift、CLI、PTF、pytest/gtest 组成统一的测试面，同一套用例可以跑在不同后端上。

## 如何工作

- **SAI-Thrift**：默认 TCP 6800，SONiC/SAI 客户端通过 thrift 调用交换芯片 API。
- **CLI**：默认 telnet 6500，人工调试与脚本化命令。
- **PTF**：Packet Test Framework，发/收包并断言。
- **pytest / gtest**：功能测试与单元测试。
- **pcap / traffic / chassis**：包样例、流量生成、机箱模拟。
- **netlink/FRR**：路由协议集成。
- **iPython / iCling / Jupyter**：交互式调试。

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

## 来源

- `README.md`
- `tests/features/`
- `saithriftv2/ptf/`
