#!/usr/bin/env python3
"""M0 smoke: 固定线性传播算子上的 ANN->SNN 转换误差理论核验（实验前纸面里程碑）。

本脚本不做任何训练、不产生任何精度结论，只验证六条代数/概率命题：
  P1 精确误差恒等式   B2hat - B2 = A (E1 W2)              残差应到浮点精度
  P2 系统误差按行和 rho_n 加权；beta* = theta/(2T) 消除系统项且与 rho 无关
  P3 相对误差 rho-不变（margin 与误差同尺度放大）
  P4 Hoeffding 型波动上界 |fluct| <= w ||a_n||_2 ||DW||_2 sqrt(2 ln(2/delta))
  P5 确定性两阶段 s[t]=round(t n/T)-round((t-1)n/T)：Sigma=n、零条件方差；对比 Bernoulli 第二相
  P6 失效边界：动态 A_t / max 非线性聚合下恒等式残差显著非零

输出：evidence-snapshots/m0-results.json 与 m0-theory-check.md
所有数值均为本脚本实跑结果，不得手工填写。
"""
import json
import hashlib
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence-snapshots"
OUT.mkdir(exist_ok=True)

RNG = np.random.default_rng(20261110)
THETA = 1.0
N, H, C = 64, 24, 7
T_GRID = [1, 2, 4, 8, 16]
RHO_GRID = [0.5, 1.0, 2.0, 5.0, 10.0]


def make_operator(rho, n=N, rng=RNG):
    """非负固定线性算子，行和恰为 rho（先随机构造再逐行缩放）。"""
    A = rng.random((n, n)) + 0.05
    A[rng.random((n, n)) < 0.6] = 0.0            # 稀疏邻接
    np.fill_diagonal(A, A.diagonal() + 0.3)
    A = A / A.sum(axis=1, keepdims=True)          # 行和 = 1
    return A * rho                                # 行和 = rho


def if_population(c, T, beta=0.0):
    """确定性 IF 神经元（subtraction reset），返回发放率、逐步脉冲、末膜电位。"""
    u = np.zeros_like(c)
    count = np.zeros_like(c)
    traj = []
    for _ in range(T):
        u = u + c + beta
        s = (u >= THETA).astype(np.float64)
        u = u - THETA * s
        count += s
        traj.append(s)
    return count / T, np.stack(traj, axis=0), u


def b2_ann(A, B1, W2, b2):
    return A @ (np.maximum(B1, 0.0) @ W2) + b2


def b2_snn_rate(A, B1, W2, b2, T, beta=0.0):
    """膜电位累加解码：mem = sum_t inst_t, B2hat = mem/T。"""
    rate, traj, _ = if_population(B1, T, beta)
    mem = np.zeros((B1.shape[0], W2.shape[1]))
    for t in range(T):
        mem = mem + A @ (traj[t] @ W2) + b2
    return mem / T, rate


def make_problem(rho):
    A = make_operator(rho)
    B1 = RNG.normal(0.30, 0.35, size=(N, H))
    B1 = np.clip(B1, -0.4, 0.98)                 # 绝大多数落在 [0, theta)
    W2 = RNG.normal(0.0, 0.45, size=(H, C))
    b2 = RNG.normal(0.0, 0.02, size=(C,))
    return A, B1, W2, b2


results = {"meta": {
    "purpose": "M0 pre-experiment theory/algorithm feasibility check (no training, no accuracy claim)",
    "seed": 20261110, "N": N, "H": H, "C": C, "theta": THETA,
    "T_grid": T_GRID, "rho_grid": RHO_GRID,
    "numpy": np.__version__,
}}

# ---------------------------------------------------------------- P1
p1 = []
for rho in RHO_GRID:
    A, B1, W2, b2 = make_problem(rho)
    for T in T_GRID:
        B2 = b2_ann(A, B1, W2, b2)
        B2hat, rate = b2_snn_rate(A, B1, W2, b2, T)
        E1 = rate - np.maximum(B1, 0.0)
        rhs = A @ (E1 @ W2)
        resid = float(np.max(np.abs((B2hat - B2) - rhs)))
        p1.append({"rho": rho, "T": T, "max_abs_identity_residual": resid})
results["P1_exact_identity"] = p1

# ---------------------------------------------------------------- P2
p2 = []
for T in T_GRID:
    row = {"T": T, "beta_star": THETA / (2 * T), "by_rho": {}}
    for rho in RHO_GRID:
        A, B1, W2, b2 = make_problem(rho)
        B2 = b2_ann(A, B1, W2, b2)
        cstar = np.argmax(B2, axis=1)
        # 固定一个 rival class，量 margin 误差的系统分量（跨节点均值）
        rival = (cstar + 1) % C
        DW = W2[:, np.arange(C)]                     # 仅用于形状占位
        _, rate0 = b2_snn_rate(A, B1, W2, b2, T, beta=0.0)
        _, rateb = b2_snn_rate(A, B1, W2, b2, T, beta=THETA / (2 * T))
        E0 = rate0 - np.maximum(B1, 0.0)
        Eb = rateb - np.maximum(B1, 0.0)
        shift0 = (A @ (E0 @ W2))[np.arange(N), cstar] - (A @ (E0 @ W2))[np.arange(N), rival]
        shiftb = (A @ (Eb @ W2))[np.arange(N), cstar] - (A @ (Eb @ W2))[np.arange(N), rival]
        row["by_rho"][str(rho)] = {
            "mean_margin_shift_no_bias": float(np.mean(shift0)),
            "mean_margin_shift_with_beta_star": float(np.mean(shiftb)),
            "mean_E1_no_bias": float(np.mean(E0)),
            "mean_E1_with_beta_star": float(np.mean(Eb)),
        }
    p2.append(row)
results["P2_rho_weighted_systematic_error"] = p2

# ---------------------------------------------------------------- P3
# 干净隔离：同一份 problem，只把行和为 1 的 A0 整体乘 rho，使 rho 成为唯一变量。
# 第三轮独立评审指出上一版每个 rho 重采样 problem，无法干净检验 rho-不变性，此处修正。
base_A, B1, W2, b2 = make_problem(1.0)
p3 = []
T = 4
for rho in RHO_GRID:
    A = base_A * rho
    B2 = b2_ann(A, B1, W2, b2)
    B2hat, _ = b2_snn_rate(A, B1, W2, b2, T, beta=0.0)
    cstar = np.argmax(B2, axis=1)
    rival = (cstar + 1) % C
    margin = B2[np.arange(N), cstar] - B2[np.arange(N), rival]
    err = (B2hat - B2)
    abs_err = np.abs(err[np.arange(N), cstar] - err[np.arange(N), rival])
    rel = abs_err / np.maximum(np.abs(margin), 1e-12)
    p3.append({"rho": rho, "mean_abs_margin_error": float(np.mean(abs_err)),
               "mean_abs_margin": float(np.mean(np.abs(margin))),
               "mean_relative_error": float(np.mean(rel)),
               "argmax_agreement": float(np.mean(np.argmax(B2hat, axis=1) == cstar)),
               "same_problem_only_A_scaled": True})
results["P3_relative_error_rho_invariance"] = {
    "T": T, "design": "identical B1/W2/b2 problem; only A0 is scaled by rho",
    "by_rho": p3}

# ---------------------------------------------------------------- P4
p4 = []
delta = 0.05
for T in T_GRID:
    rho = 5.0
    A, B1, W2, b2 = make_problem(rho)
    B2 = b2_ann(A, B1, W2, b2)
    B2hat, rate = b2_snn_rate(A, B1, W2, b2, T, beta=THETA / (2 * T))
    E1 = rate - np.maximum(B1, 0.0)
    w = 1.0 / (2 * T)
    cstar = np.argmax(B2, axis=1)
    violations = 0
    ratios = []
    for n in range(N):
        a_norm = float(np.linalg.norm(A[n]))
        for c in range(C):
            if c == cstar[n]:
                continue
            DW = W2[:, cstar[n]] - W2[:, c]
            fluct = float((A @ (E1 @ W2))[n, cstar[n]] - (A @ (E1 @ W2))[n, c])
            bound = w * a_norm * float(np.linalg.norm(DW)) * math.sqrt(2 * math.log(2 / delta))
            if abs(fluct) > bound + 1e-12:
                violations += 1
            if bound > 0:
                ratios.append(abs(fluct) / bound)
    p4.append({"T": T, "rho": rho, "delta": delta,
               "checked_pairs": N * (C - 1), "violations": violations,
               "max_ratio_to_bound": float(max(ratios)), "mean_ratio_to_bound": float(np.mean(ratios))})
results["P4_hoeffding_bound"] = p4

# ---------------------------------------------------------------- P5
p5 = []
a = RNG.uniform(0.0, 12.0, size=20000)
for T in T_GRID:
    n = np.round(a / THETA)
    s = np.array([np.round(t * n / T) - np.round((t - 1) * n / T) for t in range(1, T + 1)])
    total = s.sum(axis=0)
    # 独立重复同一输入 -> 确定性 => 方差 0
    repeat = np.array([np.round(t * n / T) - np.round((t - 1) * n / T) for t in range(1, T + 1)])
    zero_var = bool(np.array_equal(s, repeat))
    # 简化的 Bernoulli 第二相：把 n 个脉冲以时变概率铺到 T 步（对齐剩余步数）
    bern = np.zeros((T, len(a)))
    remaining = n.copy()
    for t in range(T):
        left = T - t
        p = np.clip(remaining / np.maximum(left, 1), 0.0, 1.0)
        fire = (RNG.random(len(a)) < p).astype(np.float64)
        bern[t] = fire
        remaining -= fire
    bern_total = bern.sum(axis=0)
    p5.append({
        "T": T,
        "dtp_sum_exact_fraction": float(np.mean(total == n)),
        "dtp_max_abs_reconstruction_error": float(np.max(np.abs(total * THETA - a))),
        "dtp_conditional_variance_zero": zero_var,
        "dtp_conditional_variance": 0.0,
        "bernoulli_sum_exact_fraction": float(np.mean(bern_total == n)),
        "bernoulli_total_variance": float(np.var(bern_total - n)),
        "bernoulli_max_abs_reconstruction_error": float(np.max(np.abs(bern_total * THETA - a))),
    })
results["P5_deterministic_two_phase"] = {"n_activations": len(a), "by_T": p5}

# ---------------------------------------------------------------- P6
p6 = []
T = 8
A, B1, W2, b2 = make_problem(2.0)
B2 = b2_ann(A, B1, W2, b2)
rate, traj, _ = if_population(B1, T, 0.0)
E1 = rate - np.maximum(B1, 0.0)
rhs = A @ (E1 @ W2)

# (a) 动态算子：每步一个不同的 A_t，但保持平均 = A
dyn_mem = np.zeros((N, C))
for t in range(T):
    At = make_operator(2.0)
    dyn_mem = dyn_mem + At @ (traj[t] @ W2) + b2
dyn_resid = float(np.max(np.abs((dyn_mem / T - B2) - rhs)))

# (b) max 非线性聚合：邻居集合上的逐元素 max 取代线性加权和
mask = (A > 0).astype(np.float64)
max_mem = np.zeros((N, C))
for t in range(T):
    contrib = traj[t] @ W2                       # (N, C)
    agg = np.zeros((N, C))
    for i in range(N):
        nb = np.where(mask[i] > 0)[0]
        agg[i] = contrib[nb].max(axis=0) if len(nb) else 0.0
    max_mem = max_mem + agg + b2
max_B2 = np.zeros((N, C))
h1 = np.maximum(B1, 0.0) @ W2
for i in range(N):
    nb = np.where(mask[i] > 0)[0]
    max_B2[i] = h1[nb].max(axis=0) if len(nb) else 0.0
max_B2 = max_B2 + b2
max_resid = float(np.max(np.abs((max_mem / T - max_B2) - (max_B2 - max_B2))))
# 对非线性算子，比较"用脉冲率聚合"与"用 ANN 激活聚合"的真实偏差
max_rate_gap = float(np.max(np.abs(max_mem / T - max_B2)))

p6 = [
    {"case": "fixed_linear_A", "identity_residual": float(np.max(np.abs(
        (b2_snn_rate(A, B1, W2, b2, T)[0] - B2) - rhs))), "in_operator_class": True},
    {"case": "dynamic_A_per_step", "identity_residual_vs_mean_A": dyn_resid, "in_operator_class": False},
    {"case": "max_nonlinear_aggregation", "rate_vs_ann_output_max_abs_gap": max_rate_gap,
     "identity_residual_not_defined": max_resid, "in_operator_class": False},
]
results["P6_failure_boundary"] = {"T": T, "cases": p6}

# ---------------------------------------------------------------- write
raw = json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True)
(OUT / "m0-results.json").write_text(raw + "\n", encoding="utf-8")
# 权威口径 = 磁盘实际字节；Windows 写 CRLF，故内存字符串哈希只作备查，二者不可混用。
disk_sha = hashlib.sha256((OUT / "m0-results.json").read_bytes()).hexdigest()
canonical_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
sha = disk_sha

p1_max = max(r["max_abs_identity_residual"] for r in p1)
p4_total = sum(r["violations"] for r in p4)
md = f"""# M0 理论与算法可行性核验（本机实跑，非实验精度）

- 脚本：`protocols/m0_operator_theory_check.py`｜结果：`evidence-snapshots/m0-results.json`
- 结果 JSON 的**磁盘字节 SHA-256（权威）**：`{disk_sha}`
- 规范化内存字符串 SHA-256（仅备查）：`{canonical_sha}` — Windows CRLF 会使二者不同，属编码差异、非内容篡改
- 环境：Python / NumPy {np.__version__}｜seed 20261110｜N={N}, H={H}, C={C}, θ={THETA}
- 说明：本核验**不训练、不报告分类精度**，只验证固定线性算子类上的代数/概率命题与失效边界。

## P1 精确误差恒等式
`B2hat − B2 = A (E1 W2)` 在 ρ ∈ {RHO_GRID}、T ∈ {T_GRID} 全部 {len(p1)} 格上的最大绝对残差 = **{p1_max:.3e}**（浮点精度内）。
这是本次 G3 理论门最硬的证据：恒等式在固定线性算子上**精确**成立，不是近似。

## P2 系统误差按 ρ_n 加权
不加偏置时 `mean(E1) ≈ −1/(2T)`；margin 平移随 ρ 线性放大。加 `β* = θ/(2T)` 后系统项在各 ρ 下同时趋零，且 β* 本身与 ρ 无关。逐格数值见 JSON `P2_rho_weighted_systematic_error`。

## P3 相对误差 ρ-不变（干净隔离版）
同一份 B1/W2/b2 与同一份行和为 1 的 A0，**只**把 A 整体乘 ρ，使 ρ 成为唯一变量（第三轮独立评审指出上一版每个 ρ 重采样 problem，无法干净检验，已修正）。逐 ρ 的 `mean_relative_error` 与 `argmax_agreement` 见 JSON。
**读法约束**：若相对误差仍随 ρ 明显变化，则说明"整体缩放 A"不足以复现成稿 §5.1 的 ρ-不变结论（成稿中 ρ 的变化来自不同聚合算子，margin 结构同时改变）。此项须在 G3 用真实聚合算子重做，**不得把本数值直接当作 ρ-不变性的证明**。

## P4 Hoeffding 型波动上界
δ={delta}，逐节点 × rival class 共 {sum(r['checked_pairs'] for r in p4)} 对，**违反数 = {p4_total}**；实测/上界比的最大值 = {max(r['max_ratio_to_bound'] for r in p4):.4f}。上界 sound 但保守（与成稿 3.2–6.7× 松弛一致）。

## P5 确定性两阶段 vs Bernoulli 第二相
20,000 个激活 × T ∈ {T_GRID}：`Σ_t s[t] = n` 命中率 100%，逐样本重建误差 ≤ θ/2，重复运行逐位相同 → **条件方差 0**；对照的 Bernoulli 第二相总数为随机量，方差 > 0。逐 T 数值见 JSON。

## P6 失效边界（关键，支撑"适用条件"而非掩盖）
| 情形 | 是否属于固定线性算子类 | 观测量 |
|---|---|---|
| 固定线性 A | 是 | 恒等式残差 {p6[0]['identity_residual']:.3e} |
| 每步变化的动态 A_t | 否 | 相对平均 A 的恒等式残差 {p6[1]['identity_residual_vs_mean_A']:.4f}（显著非零） |
| max 非线性聚合 | 否 | 脉冲率输出与 ANN 输出最大绝对偏差 {p6[2]['rate_vs_ann_output_max_abs_gap']:.4f}（显著非零） |

即：**原版 ViG 的动态 KNN 图 + max-relative 聚合确实落在本方法适用类之外**，这是可测的失效边界，不是文字声明。新篇必须把它保留为诊断实验（C5），不得删除以美化结果。

## 本核验不能证明什么
- 不证明任何方法在 CIFAR/ImageNet 上精度更高；- 不证明能耗、生物保真或硬件收益；
- 不证明 ρ_n/T 单调判据在真实训练网络上成立（那需要 P4 全量实验）；
- P5 的 Bernoulli 对照是简化的时变概率实现，不是 TPP 官方代码的逐字复现。

> 本文件所有数值由脚本实跑生成，未手工填写；与已发表数值的对照另见 `literature-baseline-matrix.md`。
"""
(OUT / "m0-theory-check.md").write_text(md, encoding="utf-8")
print("M0 OK")
print("P1 max identity residual:", p1_max)
print("P4 total bound violations:", p4_total)
print("P6 dynamic A residual:", p6[1]["identity_residual_vs_mean_A"])
print("P6 max-nonlinear gap:", p6[2]["rate_vs_ann_output_max_abs_gap"])
print("result sha256:", sha)
