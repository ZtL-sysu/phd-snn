from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "writing/arc-export-pos-v1/stage-22"
DEST = ROOT / "writing/p13-final-v1/stage-22"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if DEST.exists():
        raise RuntimeError(f"destination exists: {DEST}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, DEST)
    for pattern in ("*.aux", "*.bbl", "*.blg", "*.fls", "*.fdb_latexmk", "*.log", "*.out", "*.pdf"):
        for generated in DEST.glob(pattern):
            generated.unlink()
    tex = DEST / "paper.tex"
    text = tex.read_text(encoding="utf-8")
    text = "\n".join(line for line in text.splitlines() if not line.startswith("% WARNING") and not line.startswith("% !")) + "\n"
    text = text.replace("\\usepackage{geometry}\n", "", 1)
    text = re.sub(r"^\\label\{[^}]+\}\n?", "", text, flags=re.M)
    text = text.replace("\\section{References}", "\\section*{References}")
    replacements = [
        (r"\caption{Hybrid multi-hop event coding}", r"\caption{Ordered multi-hop construction and hybrid codebook/escape serialization. The lower panel shows the exact four-bit symbol, 32-bit escape payload and amortized codebook ledger.}"),
        (r"\textbf{Figure 1.} Ordered multi-hop construction and hybrid codebook/escape serialization. The right panel shows the exact symbol, payload and amortized codebook ledger.", ""),
        (r"\caption{Comparison of Quantity across Definition, Role}", r"\caption{Methods, controls and exact accounting.}"),
        (r"\textbf{Table 1.} Methods, controls and exact accounting.", ""),
        (r"\caption{Representation fidelity, storage and task trade-off}", r"\caption{Representation error, conservative storage and five-seed retrained balanced accuracy across methods. Task error bars are sample SD; lower error and storage are better.}"),
        (r"\textbf{Figure 2.} Representation error, conservative storage and retrained balanced accuracy across methods. Task results are paired five-seed summaries; lower error and lower storage are better, while accuracy direction depends on the comparison.", ""),
        (r"\caption{Permutation and shuffled-hop controls}", r"\caption{Node-permutation errors and codec-consistent shuffled-hop ratios. Dashed lines mark the \(10^{-10}\) permutation and \(1.25\times\) mismatch gates; every seed is plotted.}"),
        (r"\textbf{Figure 3.} Node-permutation errors and codec-consistent shuffled-hop ratios. Points show every permutation/shuffle seed; dashed lines mark the \texttt{1e-10} and \texttt{1.25$\times$} gates.", ""),
        (r"\caption{Comparison of Graph across Raw BA mean$\pm$SD, Hybrid BA mean$\pm$SD, Paired hybrid$-$raw pp mean$\pm$SD, Min/max pp}", r"\caption{Retrained paired balanced accuracy. Hybrid loss is 0.083 pp on Chameleon and a 0.768 pp gain on Squirrel; mixed paired differences are reported explicitly.}"),
        (r"\textbf{Table 2.} Retrained paired balanced accuracy. Hybrid loss is 0.083 pp on Chameleon and a 0.768 pp gain on Squirrel, both inside the $\leq$2 pp loss gate. The mixed paired differences are reported rather than collapsed into a universal gain.", ""),
    ]
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"missing replacement: {old[:80]}")
        text = text.replace(old, new, 1)
    text = "\n\n".join(part for part in text.split("\n\n") if part.strip())
    tex.write_text(text, encoding="utf-8")
    result = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=DEST, capture_output=True, text=True)
    (DEST / "repair-latexmk.log").write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
    problems = []
    if result.returncode != 0:
        problems.append(f"latexmk return code {result.returncode}")
    if not (DEST / "paper.pdf").exists():
        problems.append("paper.pdf missing")
    if "\\usepackage{geometry}\n\\usepackage" in text:
        problems.append("possible duplicate geometry")
    if text.count("\\bibliography{") != 1:
        problems.append("bibliography count mismatch")
    audit = {
        "schema_version": 1,
        "stage": "P13/generic-export-repair",
        "status": "passed" if not problems else "failed",
        "latexmk_returncode": result.returncode,
        "problems": problems,
        "tex_sha256": sha256(tex),
        "pdf_sha256": sha256(DEST / "paper.pdf") if (DEST / "paper.pdf").exists() else "",
        "bib_sha256": sha256(DEST / "references.bib"),
    }
    (ROOT / "writing/p13-final-v1/repair-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
