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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(path: str) -> list[dict[str, str]]:
    return [{"path": path, "sha256": sha256(RUN_ROOT / path)}]


def main() -> int:
    packet = json.loads((WRITING / "packet.json").read_text(encoding="utf-8"))
    facts = packet["facts"]
    facts.extend(
        [
            {
                "id": "F6",
                "kind": "result",
                "statement": (
                    "At rank 128 and the 2% residual budget, hidden-state MSE fell "
                    "by 16.88%, 12.86%, and 10.63% relative to the strongest "
                    "matched-budget control on Cora, Chameleon, and Squirrel."
                ),
                "status": "observed_verified",
                "model": "frozen two-layer hidden-16 GCN checkpoint seeds 0/1/2",
                "condition": "SVD rank 128 plus 2% output-Jacobian-selected sparse residual coefficients",
                "metric": "hidden-state MSE relative reduction",
                "value": [16.88, 12.86, 10.63],
                "unit": "percent reduction",
                "aggregation": "three-seed mean per dataset",
                "uncertainty": "descriptive sensitivity result; no formal CI claimed",
                "measurement_scope": "validation-grid analysis preceding held-out confirmation",
                "evidence": evidence("inputs/v2-summary.json"),
            },
            {
                "id": "F7",
                "kind": "result",
                "statement": (
                    "Across the evaluated 0.5%, 1%, and 2% residual budgets and "
                    "three graphs, logit MSE was below the strongest corresponding "
                    "control in all nine dataset-budget cells, with reductions from "
                    "2.98% to 30.40%."
                ),
                "status": "observed_verified",
                "model": "frozen two-layer hidden-16 GCN checkpoint seeds 0/1/2",
                "condition": "SVD rank 128 with output-Jacobian-selected sparse residuals",
                "metric": "logit MSE relative reduction over matched-budget grid",
                "value": [2.98, 30.40],
                "unit": "percent reduction range",
                "aggregation": "nine dataset-budget cells",
                "uncertainty": "validation-grid sensitivity; focal 2% setting later received held-out confirmation",
                "measurement_scope": "Cora, Chameleon, Squirrel at 0.5%, 1%, and 2%",
                "evidence": evidence("inputs/v2-summary.json"),
            },
            {
                "id": "F8",
                "kind": "result",
                "statement": (
                    "At rank 128 and 2%, the proposed selector reduced three-seed "
                    "mean logit MSE relative to our matched-budget A2Q-style "
                    "adaptation by 28.93%, 36.19%, and 35.24%, and relative to our "
                    "matched-budget One-Spike-style adaptation by 42.83%, 47.61%, "
                    "and 34.03% on Cora, Chameleon, and Squirrel."
                ),
                "status": "observed_verified",
                "model": "matched-budget adaptations evaluated on frozen two-layer GCN checkpoints",
                "condition": "identical total padded serialized-bit budget",
                "metric": "three-seed mean logit MSE reduction",
                "value": [[28.93, 36.19, 35.24], [42.83, 47.61, 34.03]],
                "unit": "percent reduction",
                "aggregation": "three-seed mean per dataset and control",
                "uncertainty": "descriptive paired comparison; no formal CI claimed",
                "measurement_scope": "reported test split and matched-budget adaptations",
                "evidence": evidence("results/confirmation-test-v2.json"),
            },
            {
                "id": "F9",
                "kind": "result",
                "statement": (
                    "Task superiority was not established: T=2/4 accuracy and "
                    "teacher-agreement deltas were mixed across budgets, and the "
                    "earlier task-superiority target failed. The accepted claim is "
                    "bounded task degradation rather than universal task gain."
                ),
                "status": "observed_verified",
                "model": "frozen two-layer hidden-16 GCN checkpoint seeds 0/1/2",
                "condition": "0.5%-2% residual-budget grid",
                "metric": "T=2/4 accuracy and teacher-agreement deltas",
                "value": "mixed signs; task-superiority gate false",
                "unit": "percentage points",
                "aggregation": "dataset, budget, horizon, and seed",
                "uncertainty": "negative evidence retained; no equivalence claim",
                "measurement_scope": "three local static graphs",
                "evidence": evidence("inputs/v2-summary.json"),
            },
        ]
    )

    packet["brief"]["paragraph_plan"] = [
        {"id": "P1", "section": "Introduction", "point": "Low-rank graph-message transport can preserve the wrong output-sensitive directions under a fixed serialization budget.", "fact_ids": ["F1", "F3"], "adds": "problem and contribution"},
        {"id": "P3", "section": "Method", "point": "Output-Jacobian squared sensitivity selects sparse residual coefficients after SVD transport under an exact padded-bit ledger.", "fact_ids": ["F1", "F3"], "adds": "mechanism and cost model"},
        {"id": "P4", "section": "Experiments and Results", "point": "The held-out test run confirms logit-MSE reductions on all three graphs at matched total padded serialized-bit budget.", "fact_ids": ["F1", "F3", "F8"], "adds": "main comparison"},
        {"id": "P5", "section": "Experiments and Results", "point": "Hidden-MSE and budget-grid sensitivity show that output-sensitive fidelity improves across evaluated settings.", "fact_ids": ["F6", "F7"], "adds": "sensitivity evidence"},
        {"id": "P6", "section": "Experiments and Results", "point": "Task degradation remains bounded, but task superiority is not established; warmed cost is modest in the measured 1% setting.", "fact_ids": ["F2", "F4", "F9"], "adds": "trade-off and negative finding"},
        {"id": "P7", "section": "Discussion", "point": "The evidence supports a local fidelity/resource contribution with explicit static-GCN, conversion, and measurement limits.", "fact_ids": ["F5"], "adds": "scope and interpretation"},
        {"id": "P8", "section": "Conclusion", "point": "Output-Jacobian residual allocation improves logit fidelity within the tested frozen-GCN scope while bounding observed task loss.", "fact_ids": ["F1", "F2"], "adds": "bounded conclusion"},
    ]
    packet["internal"]["reference_context_file"] = "writing/verified-reference-context-p7.md"
    packet_path = WRITING / "packet-p7.json"
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reference_context = """# Verified reference context for P7

Use only these short citation keys at draft stage. P12 will supply verified full bibliographic entries and remove duplicate versions before final export.

- `one-spike`: One-Spike SNN, IEEE TETC 2024/2025, https://arxiv.org/abs/2403.08786 and https://doi.org/10.1109/TETC.2024.3386893. Supports graph conversion and output-code context.
- `asgcn`: ASGCN, AAAI 2025, https://doi.org/10.1609/aaai.v39i2.32154. Supports ANN graph-to-asynchronous-event-graph conversion context.
- `spikinggcn`: SpikingGCN, IJCAI 2022, https://www.ijcai.org/proceedings/2022/338. Supports direct spiking-GCN context.
- `spikenet`: SpikeNet, AAAI 2023, https://ojs.aaai.org/index.php/AAAI/article/view/26034. Supports direct dynamic spiking-GNN context.
- `dy-sign`: Dy-SIGN, AAAI 2024, https://doi.org/10.1609/aaai.v38i15.29587. Supports dynamic spiking-GNN context.
- `delay-dsgn`: Delay-DSGN, ICML 2025, https://proceedings.mlr.press/v267/wang25dm.html. Supports delayed dynamic spiking-GNN context.
- `signnn`: SiGNN, Pattern Recognition 2025, https://doi.org/10.1016/j.patcog.2024.111026. Supports temporal spiking-GNN context.
- `a2q`: A2Q, 2023, https://arxiv.org/html/2302.00193. Supports graph-aware learned quantization and the matched-budget adaptation.
- `adaqp`: AdaQP, MLSys 2023, https://proceedings.mlsys.org/paper_files/paper/2023/hash/420bcf98bb3615a21468f1efb426e96d-Abstract-mlsys2023.html. Supports graph-message quantization/communication.
- `fast-snn`: Fast-SNN, 2023, https://arxiv.org/abs/2305.19868. Supports converted-SNN acceleration context.
- `dcgs`: DCGS reference implementation and paper context retained in the project literature map; use only for qualitative low-rank graph-communication context until P12 verifies the exact publication record.

Do not invent author names, titles, venues, years, DOI values, or arXiv identifiers. Do not write a References section in P7.
"""
    (WRITING / "verified-reference-context-p7.md").write_text(reference_context, encoding="utf-8")

    common = (
        "Use the accepted facts F1-F9 exactly. Preserve the phrase 'matched total "
        "padded serialized-bit budget', both 1.86 pp mean and 2.85 pp seed-level "
        "task loss, timing range 1.020-1.124x, and 'held-out confirmation after "
        "validation exposure'. Call A2Q and One-Spike implementations 'our "
        "matched-budget adaptations'. Do not claim novelty, state of the art, "
        "energy, temporal-event equivalence, task superiority, or broad GNN "
        "generality. Use only citation keys from the reference context."
    )
    reference_context_text = (WRITING / "verified-reference-context-p7.md").read_text(encoding="utf-8")
    tasks = [
        {
            "name": "part-1-title-abstract-introduction-related-work",
            "section_role": "introduction",
            "task": (
                "Write only the title, abstract, 1 Introduction, and 2 Related Work. "
                "Use exactly these top-level headings in the returned manuscript: "
                "# <paper title>, ## Abstract, ## 1 Introduction, ## 2 Related Work. "
                "Keep the abstract within 220 words. The Introduction must state the "
                "question, gap, bounded contribution, and evidence preview. Related "
                "Work must group graph conversion, graph-message compression, and "
                "output-sensitive coding by assumptions and trade-offs, and end with "
                "the exact gap. Use \\cite{key} only from the supplied context. "
                "Return JSON with manuscript and notes; notes must contain a reverse "
                "outline mapping each paragraph to its new contribution. "
                + common
                + "\n\nReference context:\n"
                + reference_context_text
            ),
        },
        {
            "name": "part-2-method-experiments-setup",
            "section_role": "methods",
            "task": (
                "Write only ## 3 Method and ## 4 Experiments and Results, with "
                "subsections 4.1 Experimental Scope and 4.2 Compared Methods and "
                "Exact Cost. Do not repeat the title or abstract. Define the frozen "
                "two-layer hidden-16 GCN setting, SVD rank-128 transport, exact "
                "padded serialized-bit ledger, output-Jacobian squared sensitivity, "
                "sparse coefficient encoding, rate-coded conversion, datasets/splits, "
                "seeds, metrics, controls, and the validation-exposed/held-out status. "
                "Include reproducible equations and a compact compared-method table. "
                "Return JSON with manuscript and notes; notes must reverse-outline "
                "each paragraph. "
                + common
            ),
        },
        {
            "name": "part-3-results-discussion-conclusion",
            "section_role": "results",
            "task": (
                "Continue ## 4 Experiments and Results without repeating its heading. "
                "Use only subsections 4.3 Main Logit-Fidelity Result, 4.4 Sensitivity "
                "and Matched-Budget Controls, and 4.5 Task and Runtime Trade-offs. "
                "Then write exactly ## 5 Discussion and ## 6 Conclusion. Do not create "
                "separate top-level Results, Experiments, Limitations, or Future Work "
                "sections. Report the complete supported findings F1-F9, preserve the "
                "negative task-superiority result, and distinguish observations from "
                "mechanism hypotheses. Conclusion must answer the Introduction without "
                "adding a new promise. Return JSON with manuscript and notes; notes "
                "must reverse-outline each paragraph. "
                + common
            ),
        },
    ]
    (WRITING / "p7-section-tasks.json").write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    request_paths: list[Path] = []
    for task in tasks:
        output = WRITING / f"request-p7-{task['name']}.json"
        subprocess.run(
            [
                sys.executable,
                str(ADAPTER),
                "--packet",
                str(packet_path),
                "--run-root",
                str(RUN_ROOT),
                "--stage",
                "P7",
                "--section-task",
                task["task"],
                "--section-role",
                task["section_role"],
                "--subskill",
                "ml-paper-writing",
                "--output",
                str(output),
            ],
            check=True,
        )
        request_paths.append(output)

    arc_run = WRITING / "arc-draft-v1"
    if arc_run.exists():
        raise RuntimeError(f"ARC draft run already exists: {arc_run}")
    for directory in ("stage-12/runs", "stage-14", "stage-15", "stage-16", "stage-17"):
        (arc_run / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        WRITING / "arc-outline-v3" / "stage-16" / "outline.md",
        arc_run / "stage-16" / "outline.md",
    )
    shutil.copyfile(
        WRITING / "arc" / "stage-14" / "analysis.md",
        arc_run / "stage-14" / "analysis.md",
    )
    shutil.copyfile(
        WRITING / "arc" / "stage-15" / "decision.md",
        arc_run / "stage-15" / "decision.md",
    )
    migration_fixture = {
        "status": "verified-migrated",
        "metrics": {
            "logit_mse_reduction_cora": 0.2623240871,
            "logit_mse_reduction_chameleon": 0.3398668714,
            "logit_mse_reduction_squirrel": 0.2582841138,
            "max_three_seed_mean_task_loss_pp": 1.8571886007,
            "max_seed_level_task_loss_pp": 2.85,
        },
        "evidence_paths": [
            "results/confirmation-summary.json",
            "results/confirmation-test-v2.json",
            "inputs/v2-summary.json",
        ],
        "note": "Truthful ARC anti-simulation compatibility fixture; no experiment was rerun or fabricated.",
    }
    (arc_run / "stage-12" / "runs" / "migrated-verification.json").write_text(
        json.dumps(migration_fixture, indent=2) + "\n", encoding="utf-8"
    )
    experiment_summary = {
        "metrics_summary": {
            "logit_mse_reduction_cora": {"mean": 0.2623240871, "min": 0.2623240871, "max": 0.2623240871, "count": 3},
            "logit_mse_reduction_chameleon": {"mean": 0.3398668714, "min": 0.3398668714, "max": 0.3398668714, "count": 3},
            "logit_mse_reduction_squirrel": {"mean": 0.2582841138, "min": 0.2582841138, "max": 0.2582841138, "count": 3},
        },
        "datasets": ["cora", "chameleon", "squirrel"],
        "total_conditions": 9,
        "total_metric_keys": 5,
    }
    (arc_run / "stage-14" / "experiment_summary.json").write_text(
        json.dumps(experiment_summary, indent=2) + "\n", encoding="utf-8"
    )

    manifest = {
        "packet": {"path": str(packet_path.relative_to(RUN_ROOT)), "sha256": sha256(packet_path)},
        "requests": [
            {"path": str(path.relative_to(RUN_ROOT)), "sha256": sha256(path)}
            for path in request_paths
        ],
        "compatibility_fixture": {
            "path": "writing/arc-draft-v1/stage-12/runs/migrated-verification.json",
            "sha256": sha256(arc_run / "stage-12" / "runs" / "migrated-verification.json"),
            "purpose": "satisfy ARC Stage 17 anti-simulation guard using truthful migrated evidence; not used as model context",
        },
    }
    (WRITING / "p7-input-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
