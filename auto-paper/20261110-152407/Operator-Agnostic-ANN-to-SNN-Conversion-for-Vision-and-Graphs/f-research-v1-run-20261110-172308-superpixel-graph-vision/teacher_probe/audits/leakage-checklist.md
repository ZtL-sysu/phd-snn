# Q5 · 反超审计与泄露检查（同配置）

检查项（全部基于 `results/table1_audit.json`，seed=10，两数据集同配置）：

1. **mask 生成时机**：`make_mask` 在全宽 base teacher 训练后、转换前，用**训练集** `mean(relu(B1))` 排序生成；不使用 val/test。→ 无 test 泄露。
2. **校准集**：FTBC 的 β 只在 validation 上校准；主臂 β=0 不需要校准；工作点只在 validation 多 seed 上选。→ test 未被用于选择。
3. **读出 R**：固定线性 sum pooling，不含标签信息。→ 无标签泄露。
4. **Converted > Teacher@working-point 是否合理**：converted 是 masked teacher 的脉冲版。膜电位解码 `argmax B̂` 用的是 `B̂ = mean_t inst_t`（每步瞬时图读出），而 teacher 的 ANN 前向是 `B`。二者数值不同属正常，`converted − teacher@point` 可以为正，这不是泄露，而是**两种读出方式的差**。真正需要警惕的是**跨配置比较**。
5. **论文现值的不自洽来源**：Table 1 的 teacher 34.02%/27.27% 是 **E17 窄网络 + 2000 图 + 800 epochs** 的 teacher@working-point；Table 2 的 Ours 62.60/65.79、32.76/34.10 来自 **local_full_v2 的 5000 图 + 1000 epochs 全宽 v2** 转换结果。**二者训练集、epoch、宽度、mask、margin、θ、T 全不同**，因此「converted 比 teacher 高 31.77pp 而 loss 为正」不是同一配置下的矛盾，而是**跨配置比较**造成的表观不自洽。

结论与处置见 `FINDINGS.md` Q5；四列同配置表见 `tables/tab_table1_fixed.tex`。
