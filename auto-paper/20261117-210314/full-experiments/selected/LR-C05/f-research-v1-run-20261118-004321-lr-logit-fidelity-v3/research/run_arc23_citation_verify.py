from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
ARC_ROOT = Path(r"C:\code\AutoResearchClaw")
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-citation-v1"
SOURCE_PAPER = RUN_ROOT / "writing" / "p12" / "paper-with-verified-references.md"
SOURCE_BIB = RUN_ROOT / "references.bib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if OUTPUT_ROOT.exists():
        raise RuntimeError(f"ARC citation output already exists: {OUTPUT_ROOT}")
    for directory in ("stage-12/runs", "stage-14", "stage-22", "stage-23"):
        (OUTPUT_ROOT / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_PAPER, OUTPUT_ROOT / "stage-22" / "paper_final.md")
    shutil.copyfile(SOURCE_BIB, OUTPUT_ROOT / "stage-22" / "references.bib")
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-draft-v1" / "stage-12" / "runs" / "migrated-verification.json",
        OUTPUT_ROOT / "stage-12" / "runs" / "migrated-verification.json",
    )
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-draft-v1" / "stage-14" / "experiment_summary.json",
        OUTPUT_ROOT / "stage-14" / "experiment_summary.json",
    )

    sys.path.insert(0, str(ARC_ROOT))
    from researchclaw.config import RCConfig
    from researchclaw.pipeline.stage_impls._review_publish import _execute_citation_verify

    config = RCConfig.load(RUN_ROOT / "config.arc.yaml", check_paths=False)
    result = _execute_citation_verify(
        OUTPUT_ROOT / "stage-23",
        OUTPUT_ROOT,
        config,
        adapters=None,
        llm=None,
        prompts=None,
    )
    report_path = OUTPUT_ROOT / "stage-23" / "verification_report.json"
    verified_bib = OUTPUT_ROOT / "stage-23" / "references_verified.bib"
    paper_verified = OUTPUT_ROOT / "stage-23" / "paper_final_verified.md"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
    summary = report.get("summary", {})
    bib_text = verified_bib.read_text(encoding="utf-8") if verified_bib.exists() else ""
    bib_count = len(re.findall(r"^@", bib_text, re.M))
    problems = []
    if summary.get("hallucinated", 0) != 0:
        problems.append(f"hallucinated citations: {summary.get('hallucinated')}")
    if bib_count != 41:
        problems.append(f"verified bibliography count is {bib_count}, expected 41")
    if not paper_verified.exists():
        problems.append("paper_final_verified.md missing")
    if summary.get("total", 0) != 41:
        problems.append(f"citation verifier total is {summary.get('total')}, expected 41")
    if summary.get("suspicious", 0) != 0:
        problems.append(f"suspicious citations remain: {summary.get('suspicious')}")

    audit = {
        "schema_version": 1,
        "stage": "P14/AutoResearchClaw-23-CITATION_VERIFY",
        "status": "passed" if not problems else "failed-validation",
        "context": {
            "paper_sha256": sha256(SOURCE_PAPER),
            "bib_sha256": sha256(SOURCE_BIB),
            "independent_audit": "CITATION_AUDIT_INDEPENDENT_FINAL.md",
        },
        "verification_summary": summary,
        "bibliography_entries": bib_count,
        "problems": problems,
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
        print(json.dumps({"status": "failed-validation", "problems": problems, "summary": summary}, indent=2))
        return 2
    print(json.dumps({"status": "passed", "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
