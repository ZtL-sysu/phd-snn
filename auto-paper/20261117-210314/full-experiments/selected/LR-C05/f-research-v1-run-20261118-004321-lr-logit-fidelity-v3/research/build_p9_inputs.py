from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
WRITING = RUN_ROOT / "writing"
DRAFT = WRITING / "p8" / "paper-data-figures.md"
PACKET = WRITING / "packet-p7.json"
ARC_RUN = WRITING / "arc-review-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if ARC_RUN.exists():
        raise RuntimeError(f"ARC review output already exists: {ARC_RUN}")
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    draft = DRAFT.read_text(encoding="utf-8")
    evidence = {
        "facts": packet["facts"],
        "measurement_boundaries": [
            "Focal setting and logit-fidelity reframing were fixed after validation exposure and before the test run.",
            "The test run is held-out confirmation after validation exposure, not preregistered independent replication.",
            "Sparse residual coefficients are exact message residual values with explicit indices, not temporal SNN events.",
            "Runtime is wall-clock pipeline cost at rank128/1%; no hardware-energy claim is supported.",
            "Task superiority was not established; task loss is a bounded descriptive trade-off.",
        ],
        "figures": {
            "Figure 1": "Deterministic self-drawn SVG under explicit user fallback authorization after three GPT image-generation failures.",
            "Figure 2": "Three-seed mean logit MSE with sample SD at rank128/2%.",
            "Figure 3": "Validation-grid logit-MSE reductions at 0.5%, 1%, and 2%.",
            "Figure 4": "Official-test task trade-off and rank128/1% warmed runtime ratios.",
        },
        "known_late_gate": "A 36-reference authenticity/relevance/placement/duplicate audit is still scheduled at P12; reviewers must flag citation gaps without inventing references.",
    }
    evidence_path = WRITING / "p9-evidence-digest.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    common = (
        "Treat the manuscript and evidence as private research material. Do not "
        "rewrite the paper. Review only the supplied manuscript and evidence digest. "
        "Do not invent references, results, confidence intervals, significance tests, "
        "or external facts. Identify exact sections/passages by heading or quoted "
        "phrase. Distinguish fatal/major/minor concerns and give a concrete repair "
        "condition for each concern."
    )
    reviewer_tasks = {
        "reviewer-a": (
            "You are Reviewer A, a strict domain expert in graph neural networks, "
            "model compression, and ANN-to-SNN conversion. Evaluate scientific "
            "soundness, mechanism plausibility, novelty boundary, baseline adequacy, "
            "claim-evidence alignment, interpretation, and scope. Pay special attention "
            "to whether logit fidelity is a meaningful contribution without task "
            "superiority or energy evidence. Use this output structure exactly: "
            "# Reviewer A Report; ## Summary; ## Score; ## Confidence; ## Strengths; "
            "## Major Concerns; ## Minor Concerns; ## Required Revisions; ## Questions. "
            "Score 1-10 and confidence 1-5. Under Major/Minor Concerns, use numbered "
            "items with Severity, Evidence, Why it matters, and Repair condition."
        ),
        "reviewer-b": (
            "You are Reviewer B, a strict reproducibility, statistics, visualization, "
            "and research-integrity reviewer. Evaluate splits, seeds, aggregation, "
            "uncertainty, exact-cost accounting, timing boundary, validation exposure, "
            "figures/captions, table plans, terminology, and reproducibility. Check "
            "that all reported values and qualifiers agree with the evidence digest. "
            "Use this output structure exactly: # Reviewer B Report; ## Summary; "
            "## Score; ## Confidence; ## Strengths; ## Major Concerns; ## Minor "
            "Concerns; ## Required Revisions; ## Questions. Score 1-10 and confidence "
            "1-5. Under Major/Minor Concerns, use numbered items with Severity, "
            "Evidence, Why it matters, and Repair condition."
        ),
    }

    request_paths = []
    for name, role in reviewer_tasks.items():
        messages = [
            {"role": "system", "content": common},
            {
                "role": "user",
                "content": (
                    f"{role}\n\nMANUSCRIPT:\n{draft}\n\nEVIDENCE DIGEST:\n"
                    f"{json.dumps(evidence, ensure_ascii=False, indent=2)}"
                ),
            },
        ]
        request_path = WRITING / f"request-p9-{name}.json"
        request_path.write_text(
            json.dumps({"messages": messages}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        request_paths.append(request_path)

    for directory in ("stage-12/runs", "stage-17", "stage-18"):
        (ARC_RUN / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DRAFT, ARC_RUN / "stage-17" / "paper_draft.md")
    shutil.copyfile(
        WRITING / "arc-draft-v1" / "stage-12" / "runs" / "migrated-verification.json",
        ARC_RUN / "stage-12" / "runs" / "migrated-verification.json",
    )

    manifest = {
        "schema_version": 1,
        "draft": {"path": str(DRAFT.relative_to(RUN_ROOT)), "sha256": sha256(DRAFT)},
        "evidence_digest": {"path": str(evidence_path.relative_to(RUN_ROOT)), "sha256": sha256(evidence_path)},
        "requests": [
            {"path": str(path.relative_to(RUN_ROOT)), "sha256": sha256(path)}
            for path in request_paths
        ],
    }
    (WRITING / "p9-input-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
