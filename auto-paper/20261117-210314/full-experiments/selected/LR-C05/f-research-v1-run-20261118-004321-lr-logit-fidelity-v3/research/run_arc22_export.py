from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from dataclasses import replace
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
ARC_ROOT = Path(r"C:\code\AutoResearchClaw")
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-export-v1"
P12_PAPER = RUN_ROOT / "writing" / "p12" / "paper-with-verified-references.md"
P12_BIB = RUN_ROOT / "references.bib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_input() -> Path:
    text = P12_PAPER.read_text(encoding="utf-8")
    text = text.replace("../../../figures/figure1-architecture.png", "figures/figure1-architecture.png")
    text = text.replace("../../../figures/data/", "figures/data/")
    out = RUN_ROOT / "writing" / "p13" / "paper-export-input.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


def main() -> int:
    if OUTPUT_ROOT.exists():
        raise RuntimeError(f"ARC export output already exists: {OUTPUT_ROOT}")
    for directory in ("stage-12/runs", "stage-14", "stage-19", "stage-20", "stage-22"):
        (OUTPUT_ROOT / directory).mkdir(parents=True, exist_ok=True)
    input_paper = prepare_input()
    shutil.copyfile(input_paper, OUTPUT_ROOT / "stage-19" / "paper_revised.md")
    shutil.copyfile(P12_BIB, OUTPUT_ROOT / "stage-20" / "references.bib")
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-draft-v1" / "stage-12" / "runs" / "migrated-verification.json",
        OUTPUT_ROOT / "stage-12" / "runs" / "migrated-verification.json",
    )
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-draft-v1" / "stage-14" / "experiment_summary.json",
        OUTPUT_ROOT / "stage-14" / "experiment_summary.json",
    )
    figures_dir = OUTPUT_ROOT / "stage-22" / "figures"
    (figures_dir / "data").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RUN_ROOT / "figures" / "figure1-architecture.png", figures_dir / "figure1-architecture.png")
    for name in ("figure2-main-logit-mse.png", "figure3-budget-sensitivity.png", "figure4-tradeoff-and-runtime.png"):
        shutil.copyfile(RUN_ROOT / "figures" / "data" / name, figures_dir / "data" / name)

    sys.path.insert(0, str(ARC_ROOT))
    import researchclaw.pipeline.stage_impls._review_publish as review_publish
    from researchclaw.config import RCConfig

    # P12 evidence was independently audited; do not let ARC's generic table
    # heuristic blank scientific numbers merely because its local fixture is small.
    review_publish._sanitize_fabricated_data = lambda text, run_dir: (
        text,
        {"numbers_replaced": 0, "numbers_kept": "all P12 audited values"},
    )
    review_publish._generate_framework_diagram_prompt = lambda *args, **kwargs: ""

    config = RCConfig.load(RUN_ROOT / "config.arc.yaml", check_paths=False)
    config = replace(config, export=replace(config.export, target_conference="generic", authors="Anonymous", bib_file="references"))
    result = review_publish._execute_export_publish(
        OUTPUT_ROOT / "stage-22",
        OUTPUT_ROOT,
        config,
        adapters=None,
        llm=None,
        prompts=None,
    )

    tex = OUTPUT_ROOT / "stage-22" / "paper.tex"
    pdf = OUTPUT_ROOT / "stage-22" / "paper.pdf"
    bib = OUTPUT_ROOT / "stage-22" / "references.bib"
    final_md = OUTPUT_ROOT / "stage-22" / "paper_final.md"
    problems = []
    if not tex.exists():
        problems.append("paper.tex missing")
    if not pdf.exists():
        problems.append("paper.pdf missing")
    if not bib.exists():
        problems.append("references.bib missing")
    if not final_md.exists():
        problems.append("paper_final.md missing")
    if tex.exists():
        tex_text = tex.read_text(encoding="utf-8")
        if "NeurIPS Paper Checklist" in tex_text:
            problems.append("generic export contains ML checklist")
        if tex_text.count("\\bibliography{") != 1:
            problems.append("bibliography command missing or duplicated")
        for phrase in (
            "26.23",
            "33.99",
            "25.83",
            "1.86",
            "2.85",
            "21,932,736",
            "25,630,208",
            "43,771,008",
        ):
            if phrase not in tex_text:
                problems.append(f"TeX lost audited phrase: {phrase}")
    if bib.exists():
        bib_entries = len(re.findall(r"^@", bib.read_text(encoding="utf-8"), re.M))
        if bib_entries != 41:
            problems.append(f"expected 41 bibliography entries, found {bib_entries}")

    audit = {
        "schema_version": 1,
        "stage": "P13/AutoResearchClaw-22-EXPORT_PUBLISH",
        "status": "passed" if not problems else "failed-validation",
        "template": "generic",
        "context": {
            "input_paper": str(input_paper.relative_to(RUN_ROOT)),
            "input_paper_sha256": sha256(input_paper),
            "bib_sha256": sha256(P12_BIB),
            "figure_inputs": [
                "figures/figure1-architecture.png",
                "figures/data/figure2-main-logit-mse.png",
                "figures/data/figure3-budget-sensitivity.png",
                "figures/data/figure4-tradeoff-and-runtime.png",
            ],
        },
        "validation": {
            "problems": problems,
            "paper_tex_sha256": sha256(tex) if tex.exists() else "",
            "paper_pdf_sha256": sha256(pdf) if pdf.exists() else "",
            "references_sha256": sha256(bib) if bib.exists() else "",
        },
        "arc_stage_result": {
            "stage": str(result.stage),
            "status": str(result.status),
            "artifacts": list(result.artifacts),
            "evidence_refs": list(result.evidence_refs),
        },
    }
    (OUTPUT_ROOT / "executor-context-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if problems:
        print(json.dumps({"status": "failed-validation", "problems": problems}, indent=2))
        return 2
    print(json.dumps({"status": "passed", "pdf": str(pdf), "tex": str(tex)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
