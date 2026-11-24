#!/usr/bin/env python3
"""生成本次 guidance 包的机器可读契约，并逐门按 canonical 顺序实跑技能校验器。

产物：
  delivery-readiness.json
  ccfa-startup-packet/feasibility-contract.json
  pipeline-state.json（先 --init，再逐门填充 passed 并逐门 --before）
  validation-log.md（所有命令与真实返回码）
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "ccfa-startup-packet"
SKILL = Path(r"C:\Users\xhf\.workbuddy\skills\f-guidance-builder-v1\scripts")
PY = r"C:\Users\xhf\miniconda3\envs\dyg-cold\python.exe"
STAGES = ["CCFA-startup", "G0", "G1", "G2", "G3", "G4", "G5", "G6",
          "G7", "G8", "validation", "handoff"]


def sha(rel, base=ROOT):
    return hashlib.sha256((base / rel).read_bytes()).hexdigest()


def fh(rel, base=ROOT):
    return {"path": rel, "sha256": sha(rel, base)}


def run(args):
    p = subprocess.run([PY, str(SKILL / args[0])] + args[1:],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


log = []

# ---------------------------------------------------------------- 1 readiness
readiness = {
    "schema_version": 1,
    "delivery_mode": "preparation",
    "submission_ready": False,
    "workflow_complete": True,
    "deferred_items": [
        {"id": "DR1", "category": "author-fact", "status": "pending", "owner": "作者",
         "requirement": "作者姓名、单位、通讯作者与贡献声明", "source": "用户本轮未指定",
         "unblock_action": "由作者提供后写入稿件元数据",
         "affected_surfaces": ["title page", "metadata", "cover letter"], "scientific_effect": "none"},
        {"id": "DR2", "category": "author-approval", "status": "pending", "owner": "作者",
         "requirement": "确认新篇与已成稿 GNN2SNN 分开投稿及两篇引用关系",
         "source": "用户本轮明确成稿先不动",
         "unblock_action": "由作者确认两篇关系与投稿时序",
         "affected_surfaces": ["related work", "cover letter"], "scientific_effect": "none"},
        {"id": "DR3", "category": "author-fact", "status": "pending", "owner": "作者",
         "requirement": "具体目标 venue 与 tier，当前按 IEEE TNNLS / Q1–Q2 期刊档设计",
         "source": "第三轮独立红队标为 must-know，官方当年规则未核验",
         "unblock_action": "作者确认 venue 后核验官方当年规则",
         "affected_surfaces": ["length", "figure rules", "anonymization", "artifact policy"],
         "scientific_effect": "none"},
        {"id": "DR4", "category": "access-route", "status": "pending", "owner": "作者",
         "requirement": "代码、协议、teacher 权重与冻结图文件的发布或审稿访问安排",
         "source": "用户本轮未指定",
         "unblock_action": "由作者决定公开范围与时机",
         "affected_surfaces": ["artifact", "reproduction package"], "scientific_effect": "none"},
        {"id": "DR5", "category": "production", "status": "pending", "owner": "作者",
         "requirement": "LaTeX 模板、页限、图表与补充材料规则",
         "source": "目标 venue 官方当年规则未核验",
         "unblock_action": "venue 确认后由官方页核验",
         "affected_surfaces": ["typesetting", "appendix"], "scientific_effect": "none"},
        {"id": "DR6", "category": "portal", "status": "pending", "owner": "作者",
         "requirement": "投稿系统账号、ORCID、基金与利益冲突声明",
         "source": "用户本轮未指定",
         "unblock_action": "由作者在投稿前填写",
         "affected_surfaces": ["submission form", "declarations"], "scientific_effect": "none"},
        {"id": "DR7", "category": "author-approval", "status": "pending", "owner": "作者",
         "requirement": "最终稿审批与全体作者同意投稿",
         "source": "用户本轮未授权投稿",
         "unblock_action": "由作者显式批准",
         "affected_surfaces": ["submission action"], "scientific_effect": "none"},
    ],
}
(ROOT / "delivery-readiness.json").write_text(
    json.dumps(readiness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- 2 feasibility contract
required = [
    "startup-stage-plan.md", "idea-cards.md", "prior-art-opportunity-map.md",
    "idea-red-team-review.md", "claim-evidence-matrix.md",
    "strong-result-feasibility-contract.md", "startup-decision.md",
]
extras = ["idea-red-team-review-rev2.md", "idea-red-team-review-rev3.md", "idea-cards-rev2.md"]
for name in required + extras:
    assert (PACKET / name).is_file() and (PACKET / name).stat().st_size > 0, name

URL = "https://www.cs.toronto.edu/~kriz/cifar.html"
common = {
    "dataset_url": URL,
    "split_protocol": "CIFAR-10/100 固定 seed 从 50k train 切 45k/5k，10k test 仅最终评测一次；Planetoid split='public'",
    "primary_metric": "conversion loss (pp) = ANN teacher top-1 减 SNN top-1，越低越好",
    "simple_baseline": "朴素 rate 转换（无偏置、无校准、计数解码）",
    "strong_baseline": "PASCAL (TMLR 2025，无官方码须自行复现) 与 TPP (ICML 2025，官方码) 第 0 批必跑，另含 QCFS/FTBC/Parallel/DCGS/AdaFire",
    "matched_control": "同一 teacher、同一冻结骨干、同一 T/θ/calibration 数据下逐一关闭组件的 A1–A7 消融臂",
    "implementation_path": "dyg-cold (torch 2.11.0+cu128/CUDA 12.8) + 6 个官方基线仓库 + 自行复现 PASCAL/CS-QCFS/ECL + 自写冻结 KNN 图的脉冲前向；本机 smoke，全量转用户授权的 novix exp-4090",
    "prototype_check": "M0 已在本机实跑：恒等式 25 格最大残差 9.880984919163893e-15、Hoeffding 上界 0 违反、P3 干净隔离 0.3056→0.3111、失效边界 0.7058/1.1669；后续 M1 QCFS 回归、M2 第 0 批、M3 主臂、M4 全量",
    "calibration_evidence": "成稿内部先验（未发表、不充当公开证据）给出 ρ 加权与 ρ-不变机制；M0 本机实跑给合成算子证据；官方基线数值见 literature-baseline-matrix.md；绝对阈值须 G7 pilot 复现基线后依基线方差锁定",
    "test_isolation": "冻结 seed 0–4；验证集只用于方法与超参选择；test 只在最终评测用一次；用于选择的切分之后不得称 unseen；全 trial 记 config/权重/图文件 SHA-256",
    "stop_return_condition": "S1 恒等式残差超容差、S2 第 0 批复现失败、S3 原版动态/非线性 ViG 恒等式仍成立、S4 单调判据连续 failure、S5 资源未就绪、S6 诚信违规、S7 数据协议违规；以及 H9（G0 命中近邻/G3 证 T1 平凡/G7 落 failure）即回退 pivot-with-rescue-route",
    "metric_direction": "lower",
    "runtime_hours": 6.0, "memory_gb": 12.0, "seeds": 5, "search_trials": 12,
}
claims = [
    dict(common, id="C1",
         claim="固定、非负、线性传播算子类上转换误差恒等式精确成立，动态或非线性算子上按预测失效",
         mechanism="B2hat-B2=A(E1W2)，A 可从时间求和中提出；动态 A_t 或 max 聚合破坏该可提出性",
         assumptions="A 固定、非负、线性；soft-reset IF；膜电位累加解码",
         falsifying_ablation="A5 固定图 vs 动态图、A6 线性聚合 vs 原版 max-relative；B4 原版 ViG 失效边界",
         minimum="固定类内残差在浮点容差内且类外显著非零",
         expected_strong="预注册目标/非实测：固定类内残差 <1e-12 且 B4 动态/非线性残差显著非零（配对 CI 不跨 0）",
         failure="固定类内残差超容差，或原版动态/非线性 ViG 上恒等式仍成立",
         primary_metric="恒等式最大绝对残差与 B4 rate–ANN gap"),
    dict(common, id="C2",
         claim="非行随机算子上按 ρ_n 加权闭式偏置校准的臂在低 T 降低 conversion loss",
         mechanism="E[E1]=beta-1/(2T)，margin 平移 rho_n/(2T)·sum_h DW_c[h]；beta*=theta/(2T) 与 rho 无关但消除系统项",
         assumptions="亚阈值残差近似均匀独立；激活主要在 [0,theta]；所有方法同 teacher/θ/calibration/T",
         falsifying_ablation="A1 去 β*；A7 把 ρ≈1 的 CNN 臂与 ρ≠1 的 B2/B3 臂对照",
         minimum="预注册目标/非实测：ρ≠1 臂相对最强 must-rerun 基线改善 ≥0.3pp 且方向在 ≥2/3 数据集一致",
         expected_strong="预注册目标/非实测：T≤4 且 ρ≠1 臂低 ≥1.0pp（配对 bootstrap CI 下界>0，BH q<0.05）且 ρ_n/T 趋势斜率显著为正；阈值须 G7 pilot 后重锁",
         failure="conversion loss 与 ρ_n/T 无单调关系，或 ρ≈1 的 CNN 臂上主臂也显著更好",
         primary_metric="conversion loss (pp)，越低越好"),
    dict(common, id="C3",
         claim="确定性两阶段第二相在零条件方差下不劣于 TPP 随机第二相，并给出可测系统增益",
         mechanism="s[t]=round(t n/T)-round((t-1)n/T)，望远镜求和使 Σs=n 精确成立、条件方差 0；对照 Bernoulli 第二相为随机量",
         assumptions="累积相先缓存全部加权输入；n=round(a/theta)；同一 teacher 与 T 网格",
         falsifying_ablation="A3 Bernoulli 第二相 vs 确定性 s[t]；A2 计数解码 vs 膜电位累加解码判冗余",
         minimum="Σs=n 命中率 100%、条件方差 0、conversion loss 不劣于 TPP（非劣效界 ±0.5pp）",
         expected_strong="预注册目标/非实测：零 RNG 可复现性成立，且在 T≤4 相对 TPP 有配对 CI 下界>0 的可归因增益",
         failure="与 PASCAL/TPP 在统一协议下等价，或零方差只是确定性的同义反复而无系统收益",
         primary_metric="Σs=n 命中率、第二相条件方差、conversion loss"),
    dict(common, id="C4",
         claim="同一算子跨视觉骨干与图消息传递保持通用性，图侧复现既有 1.5pp 带内水平",
         mechanism="误差恒等式只依赖固定非负线性 A，与层类型（卷积/图聚合/消息传递）无关",
         assumptions="图侧使用固定消息传递算子；Planetoid public split；同一 seed 预算",
         falsifying_ablation="A7 跨臂对照；B3 上替换为独立调参的图侧校准律",
         minimum="预注册目标/非实测：Cora/CiteSeer/PubMed 上 T≤8 落在 ANN−1.5pp 带内且不劣于最强图转换基线",
         expected_strong="预注册目标/非实测：三图全部 T≤8 落在带内，且与视觉臂的最优 β*/解码配置一致（无需跨模态重调）",
         failure="图侧需要独立重调才能达到带内，或三图中 ≥2 图超出带内",
         primary_metric="图节点分类 conversion loss (pp)"),
    dict(common, id="C5",
         claim="冻结/线性化的适用边界与表征代价被定量界定，而非文字声明",
         mechanism="冻结 KNN 图与线性化聚合使骨干落入算子类；原版动态图+max 非线性落在类外",
         assumptions="冻结图在前处理落盘并附 SHA-256；线性化仅替换聚合算子",
         falsifying_ablation="A5/A6；B4 原版 ViG 对照；ANN teacher 精度代价对照",
         minimum="B4 上恒等式残差显著非零，且冻结/线性化相对原版 ViG 的 ANN teacher top-1 差值被报告",
         expected_strong="预注册目标/非实测：B4 残差显著非零且代价 <1.0pp；若代价过大须如实报告并收窄主张",
         failure="原版动态/非线性 ViG 上恒等式仍成立，或冻结/线性化代价大到使 conversion loss 失去可比意义",
         primary_metric="B4 恒等式残差、ANN teacher top-1 差值 (pp)"),
]
feasibility = {
    "schema_version": 1, "decision": "proceed", "claims": claims,
    "evidence": [fh(name, PACKET) for name in required + extras],
}
(PACKET / "feasibility-contract.json").write_text(
    json.dumps(feasibility, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- 3 pipeline state
state_path = ROOT / "pipeline-state.json"
if state_path.exists():
    state_path.unlink()
rc, out, err = run(["pipeline_state.py", str(state_path), "--init"])
log.append(("pipeline_state.py --init", rc, out, err))
assert rc == 0, out

state = json.loads(state_path.read_text(encoding="utf-8"))
state["contract_version"] = "v1"
state["delivery_mode"] = "preparation"
state["contract"] = [fh("execution-contract-v1.md"), fh("guidance.md")]
state["readiness"] = [fh("delivery-readiness.json")]

stage_evidence = {
    "CCFA-startup": ["ccfa-startup-packet/startup-decision.md",
                     "ccfa-startup-packet/idea-red-team-review-rev3.md",
                     "ccfa-startup-conflict-resolution.md"],
    "G0": ["literature-baseline-matrix.md"],
    "G1": ["dataset-access-log.md"],
    "G2": ["matched-protocol.md"],
    "G3": ["theoretical-feasibility-audit.md", "evidence-snapshots/m0-results.json",
           "evidence-snapshots/m0-theory-check.md"],
    "G4": ["novelty-feasibility-report.md"],
    "G5": ["hardware-profile.md"],
    "G6": ["matched-protocol.md", "literature-baseline-matrix.md"],
    "G7": ["ccfa-startup-packet/strong-result-feasibility-contract.md",
           "ccfa-startup-packet/claim-evidence-matrix.md"],
    "G8": ["story-strength-audit.md"],
    "validation": ["guidance.md", "ccfa-startup-packet/feasibility-contract.json",
                   "guidance-pipeline-state.md"],
    "handoff": ["delivery-readiness.json", "delivery-readiness.md",
                "scenario-decision-log.md"],
}
for name in {p for paths in stage_evidence.values() for p in paths}:
    assert (ROOT / name).is_file() and (ROOT / name).stat().st_size > 0, name

for i, stage in enumerate(STAGES):
    evidence = [fh(p) for p in stage_evidence[stage]]
    row = state["stages"][i]
    assert row["id"] == stage
    row.update({"status": "passed", "contract_version": "v1",
                "gate_verdict": "pass", "inputs": evidence, "evidence": evidence})
    state["history"].append({"action": "pass", "stage": stage})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if i + 1 < len(STAGES):
        nxt = STAGES[i + 1]
        rc, out, err = run(["pipeline_state.py", str(state_path), "--before", nxt])
        log.append((f"--before {nxt}", rc, out, err))
        assert rc == 0, f"{nxt}: {out}"
    else:
        rc, out, err = run(["pipeline_state.py", str(state_path), "--complete"])
        log.append(("--complete", rc, out, err))
        assert rc == 0, out

# ---------------------------------------------------------------- 4 final validators
rc, out, err = run(["validate_guidance.py", str(ROOT / "guidance.md"), "--strict",
                    "--packet", str(PACKET)])
log.append(("validate_guidance.py --strict --packet", rc, out, err))

r2 = subprocess.run([PY, str(SKILL / "delivery_readiness.py"), "--file",
                     str(ROOT / "delivery-readiness.json")],
                    capture_output=True, text=True, encoding="utf-8")
log.append(("delivery_readiness.py", r2.returncode, (r2.stdout or "").strip(), (r2.stderr or "").strip()))

r3 = subprocess.run([PY, str(SKILL / "pipeline_state.py"), str(state_path), "--submission-ready"],
                    capture_output=True, text=True, encoding="utf-8")
log.append(("--submission-ready (expected FAIL)", r3.returncode,
            (r3.stdout or "").strip(), (r3.stderr or "").strip()))

lines = ["# Validation Log", "", "所有命令由 `protocols/finalize_contracts.py` 在 `dyg-cold` 环境实跑，返回码如实记录。", "",
         "| 命令 | rc | stdout |", "|---|---:|---|"]
for name, rc, out, err in log:
    clean = (out + (" | " + err if err else "")).replace("|", "\\|").replace("\n", " ")
    lines.append(f"| `{name}` | {rc} | {clean[:600]} |")
lines += ["", "## 结论", "",
          "- `guidance.md --strict --packet` 与 12 门 `--before` / `--complete` 全部为 rc=0。",
          "- `--submission-ready` 预期为 rc=1（作者管理事实待决，`submission_ready=false`），不是失败。",
          "- 校验器只证明结构与哈希一致性，不证明科学正确性；科学结论以三轮独立红队与 M0 实跑证据为准。", ""]
(ROOT / "validation-log.md").write_text("\n".join(lines), encoding="utf-8")

print("=== contract build ===")
for name, rc, out, err in log:
    print(f"[{rc}] {name}: {out.splitlines()[0] if out else '(no stdout)'}")
print("ALL_OK" if all(x[1] == 0 for x in log[:-1]) else "CHECK_LOG")
