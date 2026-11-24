from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
WRITING = RUN_ROOT / "writing"
ADAPTER = Path(r"C:\Users\xhf\.codex\skills\f-research-v1\scripts\writing_adapter.py")
SOURCE_DRAFT = WRITING / "p8" / "paper-data-figures.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(path: str) -> list[dict[str, str]]:
    return [{"path": path, "sha256": sha256(RUN_ROOT / path)}]


def main() -> int:
    packet = json.loads((WRITING / "packet-p7.json").read_text(encoding="utf-8"))
    for fact in packet["facts"]:
        if fact["id"] == "F8":
            fact["statement"] = (
                "At rank 128 and 2%, the magnitude-weighted output-Jacobian selector "
                "reduced three-seed mean logit MSE relative to our matched-budget "
                "A2Q-style adaptation by 28.93%, 36.19%, and 35.24%, and relative to "
                "our matched-budget One-Spike-style adaptation by 42.83%, 47.61%, "
                "and 34.03% on Cora, Chameleon, and Squirrel."
            )
            fact["evidence"] = evidence("results/p10-f8-derivation.csv")
            fact["aggregation"] = "ratio of three-seed means per dataset and control"

    packet["facts"].extend(
        [
            {
                "id": "F10",
                "kind": "method",
                "statement": (
                    "The transported tensor is the first-layer input message M0=A_hat X "
                    "of shape N x F; rank 128 is valid because F exceeds 128 on all three "
                    "datasets. The second aggregation A_hat H1 and output layer are not "
                    "compressed by this method."
                ),
                "status": "observed_verified",
                "evidence": evidence("results/p10-implementation-spec.json"),
            },
            {
                "id": "F11",
                "kind": "method",
                "statement": (
                    "The evaluated selector ranks residual entries by the composite score "
                    "s_i=r_i^2 ||J_i||_2^2, where J_i is the analytic derivative of frozen "
                    "ANN logits with respect to a transported message entry under the ReLU "
                    "hidden mask. Selection is global per dataset and checkpoint seed over "
                    "the full transductive graph message and does not use labels."
                ),
                "status": "observed_verified",
                "evidence": evidence("results/p10-implementation-spec.json"),
            },
            {
                "id": "F12",
                "kind": "definition",
                "statement": (
                    "The 2% budget selects round(0.02*N*F) residual entries; each selected "
                    "index-value pair is charged 64 bits, and the rank-128 basis is charged "
                    "(N*128+128+128*F)*32 bits. Total padded cost is basis bits plus residual "
                    "padded bits. Cora, Chameleon, and Squirrel totals are 21,932,736, "
                    "25,630,208, and 43,771,008 bits."
                ),
                "status": "observed_verified",
                "evidence": evidence("results/p10-bit-ledger.csv"),
            },
            {
                "id": "F13",
                "kind": "result",
                "statement": (
                    "Matched-budget controls include top-absolute residual selection, random "
                    "indices, dense uniform residual quantization, an A2Q-style node-budget "
                    "adaptation, and a One-Spike-style coefficient adaptation. The proposed "
                    "composite selector beats top-absolute selection in all nine dataset-seed "
                    "logit-MSE comparisons; the full-float and SVD-only rows are references, "
                    "not matched residual-budget controls."
                ),
                "status": "observed_verified",
                "model": "frozen two-layer hidden-16 GCN checkpoints seeds 0/1/2",
                "condition": "rank 128, 2% residual-entry budget, matched total padded serialized bits",
                "metric": "logit MSE and paired dataset-seed direction",
                "value": "9/9 positive versus top-absolute selection",
                "unit": "paired comparisons",
                "aggregation": "all dataset-seed pairs",
                "uncertainty": "descriptive paired evidence; no formal CI claimed",
                "measurement_scope": "reported test split",
                "evidence": evidence("results/p10-per-seed-control-comparison.csv"),
            },
            {
                "id": "F14",
                "kind": "result",
                "statement": (
                    "Using the best matched-budget non-proposed control separately for each "
                    "dataset and task metric, the maximum three-seed-mean observed degradation "
                    "was 0.53, 1.17, and 1.86 percentage points on Cora, Chameleon, and "
                    "Squirrel; the maximum single-seed degradation across all metrics was "
                    "2.85 percentage points. These are observed maxima, not bounds or "
                    "equivalence results."
                ),
                "status": "observed_verified",
                "model": "frozen two-layer hidden-16 GCN checkpoints seeds 0/1/2",
                "condition": "T=2/4 accuracy and teacher agreement versus per-metric matched-budget control",
                "metric": "maximum observed task degradation",
                "value": [[0.53, 1.17, 1.86], 2.85],
                "unit": "percentage points",
                "aggregation": "maximum of three-seed-mean metric degradations; maximum single-seed degradation",
                "uncertainty": "descriptive maxima; no equivalence test",
                "measurement_scope": "reported test split",
                "evidence": [
                    {"path": "results/p10-task-loss-three-seed-audit.csv", "sha256": sha256(RUN_ROOT / "results" / "p10-task-loss-three-seed-audit.csv")},
                    {"path": "results/p10-task-loss-audit.csv", "sha256": sha256(RUN_ROOT / "results" / "p10-task-loss-audit.csv")},
                ],
            },
            {
                "id": "F15",
                "kind": "method",
                "statement": (
                    "Timing at rank128/1% includes basis construction, residual construction "
                    "and selection, reconstruction, rate conversion, and evaluation with the "
                    "frozen model, adjacency, and features precomputed. Each method/dataset/seed "
                    "p95 is the 0.95 quantile of seven measured elapsed times after three "
                    "warmups, with CUDA synchronization before and after each call."
                ),
                "status": "observed_verified",
                "evidence": evidence("results/p10-implementation-spec.json"),
            },
            {
                "id": "F16",
                "kind": "disclosure",
                "statement": (
                    "Validation exposed ranks 16, 32, 64, and 128 and residual budgets 0.5%, "
                    "1%, and 2%. Guidance-v3 fixed rank128 and 2% after validation exposure and "
                    "before the confirmation test run. The test is held-out confirmation after "
                    "validation exposure, not preregistered or independent replication."
                ),
                "status": "observed_verified",
                "evidence": evidence("results/p10-validation-grid.csv"),
            },
        ]
    )

    packet["brief"]["question"] = (
        "Can magnitude-weighted output-Jacobian allocation of sparse residuals improve "
        "logit fidelity for the transported first-layer input message at a matched total "
        "padded serialized-bit budget in frozen GCN-to-SNN conversion?"
    )
    packet["brief"]["answer"] = (
        "On the reported test split, rank-128 transport of M0=A_hat X with a 2% "
        "magnitude-weighted output-Jacobian residual budget reduced the ratio of "
        "three-seed means of split-specific logit MSE by 26.23%, 33.99%, and 25.83% "
        "versus the post-hoc strongest evaluated matched-budget residual control. The "
        "maximum three-seed-mean observed task degradation was 1.86 percentage points "
        "and the maximum single-seed degradation was 2.85 percentage points."
    )
    packet["brief"]["terminology"].update(
        {
            "magnitude-weighted output-Jacobian score": "s_i=r_i^2 ||J_i||_2^2 for transported input-message residual entries",
            "input-message transport": "compression of M0=A_hat X only, not A_hat H1",
            "maximum observed degradation": "descriptive maximum; not a bound or equivalence result",
            "strongest evaluated residual control": "post-hoc best non-proposed matched-budget residual control by three-seed mean logit MSE per dataset",
        }
    )
    packet["brief"]["section_jobs"]["Methods"] = (
        "Define only the transported M0 tensor, valid rank, global transductive selection, "
        "composite magnitude-weighted Jacobian score, exact 64-bit pair ledger, rate coding, "
        "split/seed semantics, controls, comparators, and validation-test chronology."
    )
    packet["internal"]["note"] = (
        "P10 repairs are evidence-backed. Independent replication, formal task equivalence, "
        "energy/downstream utility, interaction ablations, and focal 2% timing remain outside "
        "the accepted claim and must not be invented."
    )
    packet_path = WRITING / "packet-p10.json"
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    decisions = [
        {
            "proposition": "Narrow the paper to magnitude-weighted output-Jacobian residual allocation for first-layer input-message logit fidelity.",
            "evidence_status": "observed_verified",
            "action": "NARROW",
            "location": "Title, Abstract, Introduction, Discussion, Conclusion",
            "factual_check": "Preserve the three-graph/seed scope, held-out-after-validation status, and no task-superiority/energy/temporal-event/broad-GNN claims.",
            "composition": {
                "point": "The contribution is a bounded logit-fidelity coding result for M0=A_hat X, not a general GNN-to-SNN capability or deployment gain.",
                "fact_ids": ["F1", "F5", "F10"],
                "preserve": ["rank128/2% focal condition", "26.23/33.99/25.83% logit-MSE reductions", "no task superiority"],
            },
        },
        {
            "proposition": "Define the transported tensor, tensor shapes, rank validity, split counts, and global transductive selection granularity.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Section 3 Method before the SVD equations",
            "factual_check": "Only M0=A_hat X is compressed; A_hat H1 is not compressed; F>128 for all datasets; labels are not used for selection.",
            "composition": {
                "point": "Rank 128 applies only to the N x F first-layer input message, with one global residual set per dataset/checkpoint seed over the full transductive graph.",
                "fact_ids": ["F10"],
                "preserve": ["Cora N=2708/F=1433", "Chameleon N=2277/F=2325", "Squirrel N=5201/F=2089"],
            },
        },
        {
            "proposition": "Replace the gradient-only score description with the implemented magnitude-weighted composite score and analytic frozen-ANN Jacobian.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Section 3 Method score equations and Figure 1 reference",
            "factual_check": "The implementation score is r_i^2 ||J_i||^2; J differentiates frozen ANN logits, not rate-coded outputs.",
            "composition": {
                "point": "The evaluated selector is a magnitude-weighted output-Jacobian heuristic for a global sparse residual set.",
                "fact_ids": ["F11"],
                "preserve": ["ReLU hidden mask", "normalized adjacency column norm", "no causal identification claim"],
            },
        },
        {
            "proposition": "Publish the exact residual-entry budget, 64-bit pair accounting, basis formula, padding rule, and absolute matched totals.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Section 3 exact-cost ledger and Section 4.2 comparison protocol",
            "factual_check": "2% means residual entries; count=round(0.02*N*F); pair cost=64 bits; totals are 21,932,736/25,630,208/43,771,008 bits.",
            "composition": {
                "point": "Matched controls share the same total padded serialized-bit budget within each dataset/seed/rank/budget condition, while payload allocation differs.",
                "fact_ids": ["F3", "F12"],
                "preserve": ["full-float and SVD-only are references, not matched residual-budget controls"],
            },
        },
        {
            "proposition": "Define every selector control, distinguish matched residual controls from references, and disclose post-hoc comparator selection.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Section 4.2 compared methods and Section 4.4 controls",
            "factual_check": "top_abs/random/uniform/A2Q-style/One-Spike-style are defined; top_abs is the post-hoc strongest fidelity control on all three reported datasets.",
            "composition": {
                "point": "Existing raw controls isolate the composite selector from magnitude, random, dense-uniform, node-budget, and coefficient-coding alternatives without claiming a causal Jacobian-only ablation.",
                "fact_ids": ["F8", "F13"],
                "preserve": ["9/9 proposed-versus-top_abs logit comparisons positive", "A2Q/One-Spike are our matched-budget adaptations"],
            },
        },
        {
            "proposition": "Define the task-loss formula and replace bounded language with maximum observed degradation.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Abstract, Section 4.5, Discussion, Conclusion",
            "factual_check": "Three-seed-mean maxima are 0.53/1.17/1.86 pp and single-seed maximum is 2.85 pp using the best matched-budget control per dataset/seed/metric.",
            "composition": {
                "point": "Task outcomes are descriptive maxima under a per-metric comparator and do not establish equivalence or a population bound.",
                "fact_ids": ["F2", "F14"],
                "preserve": ["mixed task deltas", "failed task-superiority target"],
            },
        },
        {
            "proposition": "Define the timing boundary and p95 convention while keeping the measurement at rank128/1%.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Section 4.5 runtime paragraph and Figure 4 caption",
            "factual_check": "Timing is rank128/1%; p95 is per-method quantile over seven repeats after three warmups; CUDA is synchronized; precomputed model/adjacency/features are excluded.",
            "composition": {
                "point": "The secondary timing result measures warmed full variant construction and evaluation cost at 1%, not focal 2% cost or energy.",
                "fact_ids": ["F4", "F15"],
                "preserve": ["1.020-1.124x paired p95 ratio", "218.23 MB peak allocation", "wall-clock only"],
            },
        },
        {
            "proposition": "Document validation-exposed candidate grids and the pre-test fixation of the focal setting.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Section 4.1 experimental scope and Section 4.4 sensitivity",
            "factual_check": "Validation exposed ranks 16/32/64/128 and budgets 0.5/1/2%; guidance-v3 fixed rank128/2% before test; test is held-out confirmation after validation exposure.",
            "composition": {
                "point": "The evidence is a post-selection held-out confirmation with a disclosed validation-exposed grid, not preregistered independent replication.",
                "fact_ids": ["F5", "F16"],
                "preserve": ["no test-based focal-setting selection claim"],
            },
        },
        {
            "proposition": "Correct Figure 1 notation and Figure 4 caption/condition key.",
            "evidence_status": "observed_verified",
            "action": "REWRITE",
            "location": "Figure 1 caption and Figure 4 caption",
            "factual_check": "Figure 1 uses r_i and J_i=dz/dr_i; Figure 4 explains the dashed 3 pp reference and labels panel a as rank128/2% task/fidelity and panel b as rank128/1% timing.",
            "composition": {
                "point": "Figure notation and panel conditions must match the implemented score and evidence scopes.",
                "fact_ids": ["F11", "F14", "F15"],
                "preserve": ["Figure 1 self-draw fallback disclosure remains external", "no energy interpretation"],
            },
        },
    ]
    decisions_path = WRITING / "p10-edit-decisions.json"
    decisions_path.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    section_task = (
        "Apply every edit decision to the complete manuscript. Produce a full revised "
        "six-section manuscript, not a patch. Resolve C1-C11 and C13-C14 from the supplied "
        "facts and implementation specification. Keep the contribution explicitly limited "
        "to logit-fidelity coding of M0=A_hat X. Do not add independent replication, formal "
        "equivalence, energy, downstream utility, interaction ablations, or focal 2% timing. "
        "Preserve all four figures and their nearby discussion. Keep citation placeholders "
        "unchanged because the 36-reference audit is a later P12 gate. Return JSON with "
        "manuscript and notes; notes must map each revision to the edit decision and list "
        "preserved facts."
    )
    request_path = WRITING / "request-p10-revision.json"
    subprocess.run(
        [
            sys.executable,
            str(ADAPTER),
            "--packet",
            str(packet_path),
            "--run-root",
            str(RUN_ROOT),
            "--stage",
            "P10",
            "--section-task",
            section_task,
            "--section-role",
            "local-revision",
            "--subskill",
            "paper-refine",
            "--manuscript",
            str(SOURCE_DRAFT),
            "--edits",
            str(decisions_path),
            "--output",
            str(request_path),
        ],
        check=True,
    )

    revision_run = WRITING / "arc-revision-v1"
    if revision_run.exists():
        raise RuntimeError(f"ARC revision output already exists: {revision_run}")
    for directory in ("stage-12/runs", "stage-17", "stage-18", "stage-19"):
        (revision_run / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_DRAFT, revision_run / "stage-17" / "paper_draft.md")
    shutil.copyfile(WRITING / "arc-review-v1" / "stage-18" / "reviews.md", revision_run / "stage-18" / "reviews.md")
    shutil.copyfile(
        WRITING / "arc-draft-v1" / "stage-12" / "runs" / "migrated-verification.json",
        revision_run / "stage-12" / "runs" / "migrated-verification.json",
    )

    manifest = {
        "schema_version": 1,
        "packet": {"path": str(packet_path.relative_to(RUN_ROOT)), "sha256": sha256(packet_path)},
        "source_draft": {"path": str(SOURCE_DRAFT.relative_to(RUN_ROOT)), "sha256": sha256(SOURCE_DRAFT)},
        "decisions": {"path": str(decisions_path.relative_to(RUN_ROOT)), "sha256": sha256(decisions_path)},
        "request": {"path": str(request_path.relative_to(RUN_ROOT)), "sha256": sha256(request_path)},
        "evidence_manifest": {"path": "results/p10-evidence-manifest.json", "sha256": sha256(RUN_ROOT / "results" / "p10-evidence-manifest.json")},
    }
    (WRITING / "p10-input-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
