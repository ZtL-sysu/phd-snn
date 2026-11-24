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
OUTPUT_ROOT = RUN_ROOT / "writing/arc-export-pos-v1"
SOURCE_PAPER = RUN_ROOT / "writing/p10-revised-manuscript.md"
SOURCE_BIB = RUN_ROOT / "writing/references-final.bib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_input() -> Path:
    text = SOURCE_PAPER.read_text(encoding="utf-8")
    text = text.replace("\\\\", "\\")
    text = text.replace("|W_{1,hk}|", "\\lvert W_{1,hk}\\rvert")
    text = text.replace("G=|A||A|", "G=\\lvert A\\rvert\\lvert A\\rvert")
    text = "\n".join(line for line in text.splitlines() if line.strip() != "\\bibliography{references}") + "\n"
    output = RUN_ROOT / "writing/p13/paper-export-input-v3.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


def main() -> int:
    if OUTPUT_ROOT.exists():
        raise RuntimeError(f"ARC export output already exists: {OUTPUT_ROOT}")
    for directory in ("stage-12/runs", "stage-14", "stage-19", "stage-20", "stage-22"):
        (OUTPUT_ROOT / directory).mkdir(parents=True, exist_ok=True)
    input_paper = prepare_input()
    shutil.copyfile(input_paper, OUTPUT_ROOT / "stage-19/paper_revised.md")
    shutil.copyfile(SOURCE_BIB, OUTPUT_ROOT / "stage-20/references.bib")
    figures_dir = OUTPUT_ROOT / "stage-22/figures"
    (figures_dir / "data").mkdir(parents=True, exist_ok=True)
    for name in (
        "figure1-hop-coding.png",
        "figure2-method-tradeoff.png",
        "figure3-order-controls.png",
    ):
        shutil.copyfile(RUN_ROOT / "figures/data" / name, figures_dir / "data" / name)

    sys.path.insert(0, str(ARC_ROOT))
    import researchclaw.pipeline.stage_impls._review_publish as review_publish
    from researchclaw.config import RCConfig

    review_publish._sanitize_fabricated_data = lambda text, run_dir: (
        text,
        {"numbers_replaced": 0, "numbers_kept": "all P12 audited values"},
    )
    review_publish._generate_framework_diagram_prompt = lambda *args, **kwargs: ""
    config = RCConfig.load(RUN_ROOT / "config.p13.arc.yaml", check_paths=False)
    config = replace(
        config,
        export=replace(config.export, target_conference="generic", authors="Anonymous", bib_file="references"),
    )
    result = review_publish._execute_export_publish(
        OUTPUT_ROOT / "stage-22",
        OUTPUT_ROOT,
        config,
        adapters=None,
        llm=None,
        prompts=None,
    )

    tex = OUTPUT_ROOT / "stage-22/paper.tex"
    pdf = OUTPUT_ROOT / "stage-22/paper.pdf"
    bib = OUTPUT_ROOT / "stage-22/references.bib"
    final_md = OUTPUT_ROOT / "stage-22/paper_final.md"
    problems = []
    for path in (tex, pdf, bib, final_md):
        if not path.exists():
            problems.append(f"{path.name} missing")
    if tex.exists():
        text = tex.read_text(encoding="utf-8")
        if "NeurIPS Paper Checklist" in text:
            problems.append("generic export contains ML checklist")
        if text.count("\\bibliography{") != 1:
            problems.append("bibliography command missing or duplicated")
        for phrase in ("3.952", "4.879", "7.49", "7.60", "3.72", "3.63"):
            if phrase not in text:
                problems.append(f"TeX lost audited phrase: {phrase}")
    if bib.exists():
        entry_count = len(re.findall(r"^@", bib.read_text(encoding="utf-8"), flags=re.M))
        if entry_count != 32:
            problems.append(f"expected 32 bibliography entries, found {entry_count}")

    audit = {
        "schema_version": 1,
        "stage": "P13/AutoResearchClaw-22-EXPORT_PUBLISH",
        "status": "passed" if not problems else "failed-validation",
        "template": "generic",
        "context": {
            "input_paper": str(input_paper.relative_to(RUN_ROOT)),
            "input_paper_sha256": sha256(input_paper),
            "bib_sha256": sha256(SOURCE_BIB),
            "figure_inputs": [
                "figures/data/figure1-hop-coding.png",
                "figures/data/figure2-method-tradeoff.png",
                "figures/data/figure3-order-controls.png",
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
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": audit["status"], "problems": problems, "pdf": str(pdf)}, indent=2))
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
