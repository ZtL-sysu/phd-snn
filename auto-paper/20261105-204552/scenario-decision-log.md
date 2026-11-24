# Scenario Decision Log（6 个 idea 的通过/淘汰记录）

评估顺序：CCFA 独立评审 → 冒烟实验 → 按用户规则"不理想就换 idea"。
所有来源链接访问日期 2026-11-05。

| Idea | CCF overall / verdict | 冒烟 | 最终决策 | 决定性理由 | 来源 |
|---|---|---|---|---|---|
| I1 结构 × 脉冲动力学 | 5.4 / REVISE | **进行中** | 收窄主线，待冒烟 | 唯一具备可证伪机制交互项；S0 已解除基线兼容性致命风险；但官方基线数字显示生物图绝对精度不占优，故只能主张交互项 | https://arxiv.org/abs/2610.10023 ; `smoke-tests/results/` |
| I2 生物接线鲁棒性 | 4.6 / NO-GO | 未跑（NO-GO） | **淘汰** | 与 P4「连接组比随机 reservoir 更抗过拟合」novelty 边界未解决；度匹配对照下贡献可能塌缩 | `prior-art-dedup-log.md` P4 ; https://github.com/igdigitallab/bioreservoir |
| I3 复眼脉冲前端 | 5.2 / REVISE | **R2 失败** | **淘汰** | 真实复眼坐标下 Voronoi 相对规则网格 delta_acc = −0.0393，两轮方向一致；且被评审判为"拆 2610.10023 模块" | `smoke-tests/results/smoke_i3_report.md` ; https://doi.org/10.5281/zenodo.21549559 |
| I4 跨连接组 motif | 2.8 / NO-GO | 未跑 | **淘汰** | CVPR fit 致命（更像 graph learning / 计算神经科学），丢失 SNN 成分，11 天不可行 | `ideas/idea-cards.md` I4 自评 ; https://github.com/flyconnectome/ol_annotations |
| I5 结构蒸馏 | 3.3 / NO-GO | 未跑 | **淘汰** | 新颖性坍塌：JEPA-on-connectome 已占「连接组脉冲 + 自监督表征」；拼盘性强 | https://louistier.github.io/projects/3_hack_the_worlds |
| I6 受控基准 | 5.1 / REVISE | 待 I1 计时外推 | **兜底** | 全网格多种子在 12GB/11 天不可行；只能通过缩范围 mini-benchmark 或作为 I1 附表保留 | `ccfa-startup-packet/strong-result-feasibility-contract.md` |

## 换 idea 轨迹

```
6 ideas ──CCF 评审──> 3 REVISE (I1, I3, I6) + 3 淘汰
        ──S0 兼容性验证──> I1 致命风险解除
        ──冒烟 I3 (R0 dry-run 发现编码 bug → R1 坐标 bug → R2 修复后仍失败)──> I3 淘汰
        ──当前──> 冒烟 I1（真实生物图 2×2）
        ──若失败──> I6 缩范围成本外推 / mini-benchmark
```

## 关键硬门槛状态

- G0 文献与基线：PASS（含官方 figure 3 数值校准）。
- G1 公开数据：PASS（Zenodo 独立文件直连、MaleCNS feather 直连 200 OK）。
- G2 任务与评测：PASS（cogstim 8 类任务、固定 seed、明确主指标）。
- G3 理论契合：I1 有条件成立（机制级理由 + 可证伪消融），其余淘汰。
- G4 非重复：I1 靠"时间维度 + 交互项 + 能效轴"差异化，仍是最大风险。
- G5 硬件：PASS（本机 12GB / 31.9GB / CUDA；S0 实测兼容）。
- G6-G8、validation、handoff：本轮 PENDING，不伪造 pass。
