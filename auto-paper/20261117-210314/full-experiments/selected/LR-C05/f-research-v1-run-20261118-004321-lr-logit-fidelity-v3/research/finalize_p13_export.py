from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
STAGE = RUN_ROOT / "writing" / "arc-export-v1" / "stage-22"
TEX = STAGE / "paper.tex"
PDF = STAGE / "paper.pdf"
LOG = STAGE / "paper.log"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=STAGE, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main() -> int:
    text = TEX.read_text(encoding="utf-8")
    text = re.sub(r"^% WARNING: Compilation failed\..*?\n(?:% .*\n)*", "", text, flags=re.M)
    text = text.replace("\\usepackage{geometry}\n", "", 1)
    if "\\usepackage[margin=1in]{geometry}" not in text:
        raise RuntimeError("expected margin geometry package not found")
    TEX.write_text(text, encoding="utf-8")

    run(["latexmk", "-C"])
    compile_result = run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"]
    )
    log_text = LOG.read_text(encoding="utf-8", errors="replace") if LOG.exists() else ""
    errors = [
        line
        for line in log_text.splitlines()
        if line.startswith("!") or "LaTeX Error" in line or "Emergency stop" in line
    ]
    undefined = re.findall(r"(?:Citation|Reference) `([^']+)'", log_text)
    if compile_result.returncode != 0 or errors:
        audit = {
            "status": "failed",
            "compile_returncode": compile_result.returncode,
            "errors": errors[:20],
            "stderr": compile_result.stderr[-2000:],
        }
        (STAGE / "p13-compile-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(audit, indent=2))
        return 2

    pdfinfo = run(["pdfinfo", "paper.pdf"])
    pdffonts = run(["pdffonts", "paper.pdf"])
    pdftotext = run(["pdftotext", "-layout", "paper.pdf", "-"])
    page_match = re.search(r"Pages:\s+(\d+)", pdfinfo.stdout)
    page_count = int(page_match.group(1)) if page_match else None
    embedded_font_failures = [
        line
        for line in pdffonts.stdout.splitlines()[2:]
        if line.strip() and not re.search(r"\byes\b", line, re.I)
    ]
    text_out = pdftotext.stdout
    normalized_text = re.sub(r"\s+", " ", text_out)
    problems = []
    if page_count is None or page_count < 5:
        problems.append(f"unexpected page count: {page_count}")
    if undefined:
        problems.append(f"undefined citations/references: {sorted(set(undefined))}")
    if "[?]" in text_out or "??" in text_out:
        problems.append("PDF text contains unresolved markers")
    headings = ("1 Introduction", "2 Related Work", "3 Method", "4 Experiments and Results", "5 Discussion", "6 Conclusion")
    for heading in headings:
        if heading not in normalized_text:
            problems.append(f"missing PDF heading: {heading}")
    if "NeurIPS Paper Checklist" in normalized_text:
        problems.append("PDF contains forbidden conference checklist")
    if embedded_font_failures:
        problems.append(f"non-embedded fonts: {embedded_font_failures[:8]}")

    audit = {
        "schema_version": 1,
        "status": "passed" if not problems else "failed-validation",
        "compile_returncode": compile_result.returncode,
        "compile_errors": errors,
        "undefined_citations_or_references": sorted(set(undefined)),
        "page_count": page_count,
        "pdf_text_checks": {
            "unresolved_markers": "[?]" in text_out or "??" in text_out,
            "six_sections_present": all(heading in normalized_text for heading in headings),
            "forbidden_checklist_absent": "NeurIPS Paper Checklist" not in normalized_text,
        },
        "font_embedding_failures": embedded_font_failures,
        "hashes": {
            "paper.tex": sha256(TEX),
            "paper.pdf": sha256(PDF),
            "paper.log": sha256(LOG),
            "references.bib": sha256(STAGE / "references.bib"),
        },
    }
    (STAGE / "p13-compile-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STAGE / "compilation_quality.json").write_text(
        json.dumps(
            {
                "page_count": page_count,
                "unresolved_refs": sorted(set(undefined)),
                "unresolved_cites": sorted(set(undefined)),
                "overfull_hboxes": len(re.findall(r"Overfull \\hbox", log_text)),
                "warnings": [
                    line for line in log_text.splitlines() if "Warning" in line or "warning" in line
                ][-20:],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (RUN_ROOT / "writing" / "arc-export-v1" / "executor-context-audit-final.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "stage": "P13/AutoResearchClaw-22-EXPORT_PUBLISH",
                "status": "passed" if not problems else "failed-validation",
                "arc_stage": "22",
                "template": "generic",
                "clean_compile": not problems,
                "validation": audit,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if problems:
        print(json.dumps({"status": "failed-validation", "problems": problems}, indent=2))
        return 2
    print(json.dumps({"status": "passed", "pages": page_count, "pdf": str(PDF)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
