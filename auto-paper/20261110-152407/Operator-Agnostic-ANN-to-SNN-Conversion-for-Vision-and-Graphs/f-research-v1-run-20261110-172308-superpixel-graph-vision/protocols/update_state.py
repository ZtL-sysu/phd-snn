#!/usr/bin/env python3
"""Advance the f-research-v1 ledger through P3 using REAL local smoke evidence.

P3A onward stays pending: the full 5-seed campaign is in flight on novix 20049.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
PY = r"C:\Users\xhf\miniconda3\envs\dyg-cold\python.exe"
S = r"C:\Users\xhf\.workbuddy\skills\f-research-v1\scripts\pipeline_state.py"


def sha(p):
    return hashlib.sha256((R / p).read_bytes()).hexdigest()


def fh(p):
    return {"path": p, "sha256": sha(p)}


def run(args):
    p = subprocess.run([PY, S, str(R / "pipeline-state.json")] + args,
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, (p.stdout or "").strip()


readiness = {
    "schema_version": 1,
    "delivery_mode": "preparation",
    "submission_ready": False,
    "workflow_complete": False,
    "deferred_items": [
        {"id": "DR1", "category": "author-fact", "status": "pending", "owner": "作者",
         "requirement": "作者姓名、单位、通讯作者与贡献声明", "source": "用户本轮未指定",
         "unblock_action": "由作者提供后写入稿件元数据",
         "affected_surfaces": ["title page", "metadata"], "scientific_effect": "none"},
        {"id": "DR2", "category": "author-approval", "status": "pending", "owner": "作者",
         "requirement": "确认新篇与已成稿 GNN2SNN 分开投稿及两篇引用关系",
         "source": "用户明确成稿先不动",
         "unblock_action": "由作者确认两篇关系与投稿时序",
         "affected_surfaces": ["related work", "cover letter"], "scientific_effect": "none"},
        {"id": "DR3", "category": "author-fact", "status": "pending", "owner": "作者",
         "requirement": "具体目标 venue 与 tier，当前按 IEEE TNNLS / Q1–Q2 档设计",
         "source": "P1B 独立评审标为 must-know，官方当年规则未核验",
         "unblock_action": "作者确认 venue 后核验官方当年规则",
         "affected_surfaces": ["length", "figure rules", "artifact policy"],
         "scientific_effect": "none"},
        {"id": "DR4", "category": "access-route", "status": "pending", "owner": "作者",
         "requirement": "代码、teacher 权重与冻结图文件的发布或审稿访问安排",
         "source": "用户本轮未指定", "unblock_action": "由作者决定公开范围与时机",
         "affected_surfaces": ["artifact", "reproduction package"], "scientific_effect": "none"},
        {"id": "DR5", "category": "production", "status": "pending", "owner": "作者",
         "requirement": "LaTeX 模板、页限与图表规则",
         "source": "目标 venue 官方当年规则未核验",
         "unblock_action": "venue 确认后由官方页核验",
         "affected_surfaces": ["typesetting", "appendix"], "scientific_effect": "none"},
        {"id": "DR6", "category": "portal", "status": "pending", "owner": "作者",
         "requirement": "投稿系统账号、ORCID、基金与利益冲突声明",
         "source": "用户本轮未指定", "unblock_action": "由作者在投稿前填写",
         "affected_surfaces": ["submission form", "declarations"], "scientific_effect": "none"},
        {"id": "DR7", "category": "author-approval", "status": "pending", "owner": "作者",
         "requirement": "最终稿审批与全体作者同意投稿", "source": "用户本轮未授权投稿",
         "unblock_action": "由作者显式批准",
         "affected_surfaces": ["submission action"], "scientific_effect": "none"},
    ],
}
(R / "delivery-readiness.json").write_text(
    json.dumps(readiness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state = json.loads((R / "pipeline-state.json").read_text(encoding="utf-8"))
state["contract_version"] = "v1"
state["delivery_mode"] = "preparation"
state["contract"] = [
    fh("execution-contract-v1.md"),
    fh("contracts/guidance-v2.snapshot.md"),
    fh("contracts/contract-change-v1-to-v2.md"),
    fh("contracts/core-1028.snapshot.py"),
]
state["readiness"] = [fh("delivery-readiness.json")]

evidence = {
    "P0": ["execution-contract-v1.md", "pipeline-state.md",
           "contracts/path-containment-manifest.md"],
    "P1": ["contracts/guidance-validation.md", "contracts/guidance-v2.snapshot.md"],
    "P1A": ["contracts/strong-result-feasibility-lock.md",
            "contracts/claim-evidence-matrix-v2.md"],
    "P1B": ["audits/ccfa-pre-experiment-review.md",
            "audits/ccfa-pre-experiment-integrity.md",
            "audits/concern-to-action-ledger.md"],
    "P2": ["protocols/vision_pipeline.py", "protocols/run_experiments.py",
           "novix/in-flight-task.md", "novix/query-header.md"],
    "P3": ["results/gpu_MNIST_seed0.json", "audits/baseline-reproducibility.md",
           "results/experiment-traceability.md"],
}

for p in {x for v in evidence.values() for x in v}:
    assert (R / p).is_file() and (R / p).stat().st_size > 0, p

rows = state["stages"]
log = []
for i, stage_id in enumerate(["P0", "P1", "P1A", "P1B", "P2", "P3"]):
    assert rows[i]["id"] == stage_id
    ev = [fh(p) for p in evidence[stage_id]]
    rows[i].update({"status": "passed", "contract_version": "v1",
                    "gate_verdict": "pass", "inputs": ev, "evidence": ev})
    state["history"].append({"action": "pass", "stage": stage_id})
    (R / "pipeline-state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nxt = rows[6]["id"] if i == 5 else rows[i + 1]["id"]
    rc, out = run(["--before", nxt])
    log.append((nxt, rc, out.splitlines()[0] if out else ""))
    assert rc == 0, f"{nxt}: {out}"

rc, out = run(["--workflow-complete"])
log.append(("--workflow-complete (expected FAIL)", rc,
            out.splitlines()[0] if out else ""))

report = ["# Pipeline State Update Log", "",
          "由 `protocols/update_state.py` 实跑；P0–P3 以本机 smoke 真实证据逐门接受，P3A 起保持 pending（全量在 novix 20049 在途）。",
          "", "| 校验 | rc | stdout |", "|---|---:|---|"]
for name, rc, out in log:
    report.append(f"| `{name}` | {rc} | {out[:300]} |")
report += ["", "## 当前状态", "",
           "- P0 / P1 / P1A / P1B / P2 / P3：`passed`",
           "- P3A → P21：`pending`（全量实验在 4090 在途，结果未回收）",
           "- `--workflow-complete` 预期 rc=1：本地工作流**未**完成，不得进 P6 写作",
           "- `submission_ready = false`", ""]
(R / "audits" / "pipeline-state-update-log.md").write_text(
    "\n".join(report), encoding="utf-8")

for name, rc, out in log:
    print(f"[{rc}] {name}: {out[:120]}")
print("ADVANCED_TO_P3")
