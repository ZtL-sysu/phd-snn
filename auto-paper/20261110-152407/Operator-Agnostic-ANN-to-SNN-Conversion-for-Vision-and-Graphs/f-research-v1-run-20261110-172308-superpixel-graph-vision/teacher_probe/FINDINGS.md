# FINDINGS · teacher 归因 + 强 teacher 全量实验

> 生成 2026-11-12T06:13:00.546138｜来源：novix `21591`（RTX 4090）真实全量 A/B/C/D +
> 本机 3060 的 T0/T2 五 seed 与复现审计。所有数值来自 `novix_delivery_21591/results/*.csv`。

## 三句话总结

1. **34.02%/27.27% 的弱 teacher 主要是 `unit_mask` 把有效宽度压到 ~10**：宽度效应
   MNIST **+32.03pp**（CI ±1.96）、
   CIFAR10 **+7.15pp**（CI ±1.25）；
   而「只用 2k 图」的数据规模效应仅 +1.00pp（CI ±3.54，不显著）/ +2.29pp（CI ±0.96）。
2. **强 teacher 上转换仍成立**：T4 全量+全宽+边特征 teacher（MNIST val 61.42%、CIFAR10 37.40%），
   T=8/β=0 的 conversion loss **−1.52±0.97pp / −0.09±0.44pp**，见 Q2；去 β⋆ 的收益在强 teacher 上仍为正（Q3）。
3. **论文按「双轨报告」改**：主表只报同一配置的四列；另表报规模/宽度归因与精度—能耗 frontier。
   跨配置拼接 Table 1(teacher 34.02/27.27%) 与 Table 2(Ours 65.79/34.10) 会造成
   「converted 比 teacher 高 31.77pp 而 loss 为正」的表观矛盾。

## 逐问回答（Q1–Q5）

### Q1 · teacher 归因（60/60 runs 全量）
- MNIST：T0 33.81±1.67%；数据规模 T1−T0 **+1.00pp**（CI ±3.54，不显著）；宽度 T2−T0 **+32.03pp**（CI ±1.96）；
  全量+全宽 T3−T0 +34.37pp；**edge-feature T4−T3 −6.62pp**（CI ±2.60，负结果保留）。
- CIFAR10：T0 26.95±0.67%；数据规模 +2.29pp（CI ±0.96）；宽度 +7.15pp（CI ±1.25）；T3−T0 +10.09pp；edge-feat −1.56pp（CI ±1.42）。
- 上限探针 T5（BN/dropout/cosine）teacher 反而低于 T4（`bcd_summary.json`：T4 61.42/37.40 vs T5 54.02/35.70，按 `teacher_val` 选 T4 作强 teacher）。
- 结论：弱 teacher 的主因是宽度，不是数据规模；加边特征不涨反跌，作为负结果保留。

### Q2 · 强 teacher 上的 conversion loss
- MNIST T=8/β=0：loss **−1.52±0.97pp**（95% CI ±0.85），teacher≈61.4%。
- CIFAR10 T=8/β=0：loss **−0.09±0.44pp**（CI ±0.39），teacher≈37.4%。
- 高精度区 loss 未显著变大，margin/量化并未更受限；个别工作点为负 loss（converted 略高于 teacher@point，见 Q5）。
- 恒等式残差在 fp64 同一 forward 下 ~1e-14（逐 T 见 `strong_teacher_conversion.csv`）。

### Q3 · 去 β⋆ 是绝对还是相对收益
- MNIST：β⋆ 相对 β=0 的 loss 增量均值 **+0.73pp**（逐 T +0.13~+1.46）；CIFAR10 **+0.72pp**（−0.16~+2.42）。
- 机制是「确定性两阶段已精确实现发放率，β⋆ 再补偿 floor 量化 → 双重校正」，与 teacher 强弱无关，
  在强 teacher 上仍成立；属绝对量（pp）而非比例。

### Q4 · 能量 frontier（提示词口径）
- MNIST：$R_{\rm cons}$ 均值 **1.539×**、最小 0.283×；CIFAR10 均值 **2.046×**、最小 0.253×。
- **强 teacher 上 5× 优势消失**：teacher 更宽 → spike 更多；拐点见 `fig_frontier_strong.pdf`（横轴 teacher 精度，虚线 5×）。
- 只报 `teacher > 2× chance` 的可采用点，零脉冲不算优势；两套口径都记在 `energy.csv`。
- 这与论文原「弱 teacher 上 20 seeds 全部 ≥5×」并不矛盾，是同一 frontier 的两端。

### Q5 · Table 1 自洽性
- 同配置四列（`tab_table1_fixed.tex`）：converted−teacher@point 均值 **−3.04pp**，无系统性反超；
  逐 seed 见 `table1_reaudit.csv`。
- mask 在 train 之后、转换之前由**训练集**激活生成；校准只用 validation；R 是固定线性 sum pooling，未见标签 → 无泄露。
- 论文 Table 1 与 Table 2 的冲突是**跨配置比较**（2000 图窄网 vs 5000 图全宽 v2），不是信息泄露。
- 本机复现审计：5-seed 均值 T0 33.81±1.58 / 27.00±0.83 vs 论文 34.02±1.60 / 27.27±1.67，偏差 −0.21/−0.27pp → **PASS**（详见 `REPRO.md` / `REPRO_BLOCKER.md` §7）。

## 报告方案推荐：**双轨**
1. 主表：同一配置四列（Teacher full / Teacher@working-point / Converted / Loss），消除跨配置矛盾。
2. 副表：规模×宽度×边特征归因（Q1）+ 强 teacher 的精度—能耗 frontier（Q4）。
理由：既保留「强 teacher 上转换成立」和「能耗优势在弱 teacher 上稳定」两端结论，又不再把不同配置的数字拼成一张表。三轨（再加弱 teacher 专表）会重复，不推荐。

---

<details><summary>远端 `21591` 原始 FINDINGS（保留作证据，不改写）</summary>

# FINDINGS

> 三句话总结：窄配置 teacher 低的原因由 T1/T2 差值分解（见 Q1）；强 teacher 上转换仍成立与否见 Q2/Q3；论文应按「同配置四列」双轨报告（Table 1 与 Table 2 不得跨配置拼接）。

## 逐问回答

Q1 (teacher 归因)：见 `tab_teacher_probe.tex`。
MNIST: T0=33.81±1.67%；数据规模效应 T1−T0=+1.00pp；宽度效应 T2−T0=+32.03pp。
CIFAR10: T0=26.95±0.67%；数据规模效应 T1−T0=+2.29pp；宽度效应 T2−T0=+7.15pp。

Q2 (强 teacher 上 loss)：
MNIST T=8/β=0：loss=-1.52±0.97pp (95% CI ±0.85)，teacher≈61.4%。
CIFAR10 T=8/β=0：loss=-0.09±0.44pp (95% CI ±0.39)，teacher≈37.4%。

Q3 (β⋆ 收益)：
MNIST: β⋆ 相对 β=0 的 loss 增量均值 +0.73pp (逐 T 范围 +0.13~+1.46)；机制为双重校正，与 teacher 强弱无关。
CIFAR10: β⋆ 相对 β=0 的 loss 增量均值 +0.72pp (逐 T 范围 -0.16~+2.42)；机制为双重校正，与 teacher 强弱无关。

Q4 (能量 frontier)：
MNIST: $R_{\rm cons}$ 均值 1.539×、最小 0.283×；见 `fig_frontier_strong.pdf`（横轴 teacher 精度、虚线 5×）。
CIFAR10: $R_{\rm cons}$ 均值 2.046×、最小 0.253×；见 `fig_frontier_strong.pdf`（横轴 teacher 精度、虚线 5×）。

Q5 (Table 1 自洽)：同配置四列见 `tab_table1_fixed.tex`。
同配置下 converted−teacher@point 均值 -3.04pp，无系统性反超；论文 Table1(teacher 34.02/27.27%) 与 Table2(Ours 65.79/34.10) 来自不同配置（2000 图窄网 vs 5000 图全宽 v2），是跨配置比较而非泄露。

## 报告方案建议

**推荐双轨**：(1) 主表只报同一配置下的 Teacher(full)/Teacher@working-point/Converted/Loss 四列；(2) 另表报不同规模/宽度配置的 teacher 归因与精度—能耗 frontier。理由：跨配置拼接会造成「converted 比 teacher 高 31.77pp 而 loss 为正」的表观矛盾，双轨既保留强 teacher 的结论，又消除口径不自洽。


</details>
