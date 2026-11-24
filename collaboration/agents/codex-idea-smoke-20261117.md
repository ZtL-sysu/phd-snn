# Agent: codex-idea-smoke-20261117

## 任务

按用户长期目标系统检索 GNN→SNN 空白，结合本机 RTX 3060/现有数据反复生成候选并做 smoke，直到形成 10 个经创新性筛查和强 smoke 的 idea。

## 已完成

- 读取项目状态、历史研究日志、数据/权重清单和失败家族；确认本机 `dyg-cold`、RTX 3060 12GB、32GB RAM。
- 独立检索 2022–2026 转换与直接训练 spiking GNN 文献，区分 One-Spike/ASGCN 等已有图转换与真正剩余缺口；写入 `auto-paper/20261117-210314/literature-baseline-matrix.md`。
- 循环执行 19 个候选：10 个通过各自冻结门槛，9 个拒绝/不确定。强 smoke 采用真实本地 DAVIS、MaleCNS、FlyWire、Chameleon/Squirrel/Planetoid/OGBN-Arxiv 与冻结 checkpoint；发现性选择不读测试集。
- 最终 32/32 单元测试通过，16 个核心证据文件 SHA256 复核通过，CCFA 路径隐私检查通过。

## 最终十个 idea

入口：`auto-paper/20261117-210314/idea-portfolio.md`。

1. DYN-C01 因果时间残差事件；2. EQ-C02 旋转等变径向事件；3. PERM-C03 图置换证书；4. SIGN-C04 兴奋/抑制消息双库；5. LR-C05 算子低秩消息事件；6. EDGE-C06 生物边权量化事件；7. CERT-C11 仿射误差证书；8. POS-C13 hop 位置事件；9. DLY-C14 延迟对齐因果残差；10. READ-C18 top-two margin-pair readout。

## 边界与下一步

- “强 smoke”只表示预注册机制门槛通过，不等于论文准确率/能效强结果；DYN/DLY 尚缺真正动态边 GNN，EQ 尚缺端到端 E(3) teacher，压缩类尚缺强转换基线。
- 建议每次只选 2–3 个 idea，按 `ccfa-startup-packet/startup-decision.md` 逐个生成 guidance；不要同时启动十篇论文。
- 负证据严禁改名复用。HOM-C17 因 seed6 checkpoint 缺失只记录为不确定，不计通过。
