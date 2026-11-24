"""Structural dry-run: create temporary neutral assets, compile, and report TeX errors.

Real assets from make_paper_assets.py overwrite these files before the accepted build.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "tex"
TABLES = TEX / "tables"
FIGS = TEX / "figures"
TABLES.mkdir(exist_ok=True)
FIGS.mkdir(exist_ok=True)

MACROS = ["annCora", "annCite", "annPub", "oursTfour", "oursTeight", "tppTfour",
          "tppGapTfour", "soneInter", "soneIntra", "soneTppGap", "soneBranch",
          "cthreeC", "cthreeR", "cthreeSaving", "cthreeUniform", "cthreePred",
          "cthreeOracle", "cthreeShufReal", "cthreeShuf", "cthreePass", "hostSpread"]
(TEX / "numbers.tex").write_text(
    "% DRY-RUN PLACEHOLDER - overwritten by make_paper_assets.py before delivery\n"
    + "".join("\\newcommand{\\%s}{0.00}\n" % m for m in MACROS), encoding="utf-8")

for name in ["table1", "table_std", "table_s1", "table_c3", "table_hosts"]:
    p = TABLES / (name + ".tex")
    if not p.exists():
        p.write_text("\\begin{table}[h]\\centering\\caption{Dry-run placeholder.}"
                     "\\label{tab:dry}\\begin{tabular}{ll}\\toprule a & b \\\\\\bottomrule"
                     "\\end{tabular}\\end{table}\n", encoding="utf-8")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    for name in ["fig_s1", "fig_tstar", "fig_pareto"]:
        p = FIGS / (name + ".pdf")
        if not p.exists():
            fig, ax = plt.subplots(figsize=(3.4, 2.5))
            ax.text(0.5, 0.5, "dry-run", ha="center", va="center")
            fig.savefig(p, bbox_inches="tight")
            plt.close(fig)
except ImportError:
    print("matplotlib unavailable; figures omitted")

env = None
for i in range(2):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                        "main.tex"], cwd=TEX, capture_output=True, text=True, env=env)
    print("pdflatex pass", i + 1, "rc", r.returncode)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        print("\n".join(tail[-25:]))
        break
r = subprocess.run(["bibtex", "main"], cwd=TEX, capture_output=True, text=True)
print("bibtex rc", r.returncode, (r.stdout + r.stderr).strip()[:400])
