from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "writing/arc-export-v3/stage-22"
DEST = ROOT / "writing/p13-final-v4/stage-22"


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
    lines = tex.read_text(encoding="utf-8").splitlines()
    repaired = []
    geometry_removed = False
    labels_removed = 0
    for line in lines:
        if line.startswith("% WARNING: Compilation failed") or line.startswith("% !"):
            continue
        if line.strip() == "\\usepackage{geometry}" and not geometry_removed:
            geometry_removed = True
            continue
        if re.fullmatch(r"\\label\{[^}]+\}", line.strip()):
            labels_removed += 1
            continue
        repaired.append(line)
    text = "\n".join(repaired) + "\n"
    text = text.replace("\\_", "_")
    text = text.replace("\\section{References}", "\\section*{References}")
    table = r"""\begin{table}[ht]
\centering
\caption{Bound definitions and roles}
\begin{tabular}{p{0.20\linewidth}p{0.56\linewidth}p{0.18\linewidth}}
\toprule
\textbf{Bound or control} & \textbf{Exact definition} & \textbf{Role} \\
\midrule
\(B_{\mathrm{abs}}\) & \(\sum_q G_{iq}\sum_h \Delta_{qh}\lvert W_{1,hk}\rvert\), where \(G=\lvert A\rvert\lvert A\rvert\) & proposed deterministic interval \\
\(B_{\mathrm{mink}}\) & \(\left(\sum_q G_{iq}\lVert\Delta_{q,:}\rVert_2\right)\lVert W_{1,:,k}\rVert_2\) & valid analytic upper comparator \\
\(B_{\mathrm{global}}\) & \(c_i\max(\Delta)\lVert W_{1,:,k}\rVert_1\), where \(c_i=\sum_qG_{iq}\) & matched global-radius ablation \\
Scalar reference & \(c_i\max(\Delta)\lVert W_1\rVert_{1,1}\) & deliberately loose context \\
\bottomrule
\end{tabular}
\end{table}"""
    text = re.sub(
        r"\\begin\{table\}\[ht\].*?\\end\{table\}",
        lambda _: table,
        text,
        count=1,
        flags=re.S,
    )
    tex.write_text(text, encoding="utf-8")

    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"],
        cwd=DEST,
        capture_output=True,
        text=True,
    )
    log = DEST / "repair-latexmk.log"
    log.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
    pdf = DEST / "paper.pdf"
    problems = []
    if result.returncode != 0:
        problems.append(f"latexmk return code {result.returncode}")
    if not pdf.exists():
        problems.append("paper.pdf missing")
    text = tex.read_text(encoding="utf-8")
    if "\\usepackage{geometry}" in text:
        problems.append("duplicate geometry remains")
    if re.search(r"\\label\{[^}]*\\_", text):
        problems.append("escaped underscore label remains")
    if text.count("\\bibliography{") != 1:
        problems.append("bibliography command count is not one")
    audit = {
        "schema_version": 1,
        "stage": "P13/generic-export-repair",
        "status": "passed" if not problems else "failed",
        "source": str(SOURCE.relative_to(ROOT)),
        "destination": str(DEST.relative_to(ROOT)),
        "geometry_removed": geometry_removed,
        "labels_removed": labels_removed,
        "latexmk_returncode": result.returncode,
        "problems": problems,
        "tex_sha256": sha256(tex),
        "pdf_sha256": sha256(pdf) if pdf.exists() else "",
        "bib_sha256": sha256(DEST / "references.bib") if (DEST / "references.bib").exists() else "",
    }
    (ROOT / "writing/p13-final-v4/repair-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
