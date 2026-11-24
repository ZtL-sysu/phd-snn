#!/usr/bin/env python3
"""S7 layout revision. Works ONLY on revised/ copies; sources/ stays read-only.
Repairs the seven concrete visual defects found in audits/visual/*.png.
"""
from __future__ import annotations

import shutil
from pathlib import Path

S = Path(__file__).resolve().parent
SRC = S / "sources"
REV = S / "revised"
(REV / "sections").mkdir(parents=True, exist_ok=True)
(REV / "tables").mkdir(parents=True, exist_ok=True)

for f in ["main.tex", "preamble.tex", "cvpr.sty", "ieeenat_fullname.bst",
          "references.bib", "numbers.tex"]:
    shutil.copyfile(SRC / f, REV / f)
for p in (SRC / "sections").glob("*.tex"):
    shutil.copyfile(p, REV / "sections" / p.name)
for p in (SRC / "tables").glob("*.tex"):
    shutil.copyfile(p, REV / "tables" / p.name)

# ---- D1: ruler line numbers overlapping body text + D2: backref digits in references
p = REV / "main.tex"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "\\usepackage[pagebackref,breaklinks,colorlinks,allcolors=cvprblue]{hyperref}",
    "\\usepackage[breaklinks,colorlinks,allcolors=cvprblue]{hyperref}")
s = s.replace("\\input{numbers}\n",
              "\\input{numbers}\n"
              "% The author-kit review ruler is drawn by lineno into the gutter in\n"
              "% two-column mode and overlaps body text. Keep the review/confidential\n"
              "% header but suppress the intrusive line numbers for readability.\n"
              "\\AtBeginDocument{\\nolinenumbers}\n")
# ---- D3: two figures stacked in one column
s = s.replace("\\includegraphics[width=\\linewidth]{../figures/pareto.pdf}",
              "\\includegraphics[width=\\linewidth]{../figures/pareto.pdf}")
s = s.replace("\\begin{figure}[t]\n\\centering\n\\includegraphics[width=\\linewidth]{../figures/loss_T.pdf}",
              "\\begin{figure}[b]\n\\centering\n\\includegraphics[width=\\linewidth]{../figures/loss_T.pdf}")
p.write_text(s, encoding="utf-8")

# ---- D4: over-wide Eq.(5) -> two aligned rows
p = REV / "sections" / "3_method.tex"
s = p.read_text(encoding="utf-8")
old = r"""\begin{equation}
\mathcal{R}_{\mathrm{prim}} = \frac{\mathrm{MAC}_{\mathrm{ANN}}\cdot\MACPJ}{\mathrm{AC}\cdot\ACPJ},\qquad
\mathcal{R}_{\mathrm{cons}} = \frac{\mathrm{MAC}_{\mathrm{ANN}}\cdot\MACPJ}{S H\cdot\ACPJ + T E C\cdot\MACPJ}.
\label{eq:energy}
\end{equation}"""
new = r"""\begin{align}
\mathcal{R}_{\mathrm{prim}} &= \frac{\mathrm{MAC}_{\mathrm{ANN}}\cdot\MACPJ}{\mathrm{AC}\cdot\ACPJ},
\label{eq:energy}\\
\mathcal{R}_{\mathrm{cons}} &= \frac{\mathrm{MAC}_{\mathrm{ANN}}\cdot\MACPJ}{S H\cdot\ACPJ + T E C\cdot\MACPJ}.
\notag
\end{align}"""
assert old in s, "eq:energy block not found"
s = s.replace(old, new)
# ---- D5: subsection headings wrapping awkwardly
s = s.replace("\\subsection{Deterministic two-phase spiking and the redundant bias}",
              "\\subsection{Two-phase spiking and bias redundancy}")
s = s.replace("\\subsection{Membrane readout, margin regularisation and narrow networks}",
              "\\subsection{Readout, margin, and network width}")
p.write_text(s, encoding="utf-8")

# ---- D6: abrupt "Further foundations" paragraph at the end of related work
p = REV / "sections" / "2_related.tex"
s = p.read_text(encoding="utf-8")
import re
s = re.sub(r"\n\\paragraph\{Further foundations\.\}.*?\n", "\n", s, flags=re.S)
if not s.rstrip().endswith("We build on these foundations without claiming novelty for any individual component."):
    s = s.rstrip() + ("\n\nSpiking computation, graph representation learning and event-driven vision "
                      "rest on a broader body of work~\\cite{" + ",".join([
                          "maass1997", "krizhevsky2009", "lecun1998", "orchard2015",
                          "li2017cifardvs", "kugele2020", "liu2022spikeconverter",
                          "zhou2025edge", "ji2026gtdl", "xia2026neuro", "dualphase2024",
                          "bojkovic2024ot", "yang2025csqcfs", "jiang2025fission",
                          "sgnnbench2025", "hwang2025onespike"]) + "}. "
                      "We build on these foundations without claiming novelty for any individual component.\n")
p.write_text(s, encoding="utf-8")

# ---- D7: tables overflowing the column / crammed cells / truncated exponents
def wrap_table(raw, short_header=None):
    """Keep every numeric cell from the generated source; fix only geometry."""
    lines = [ln for ln in raw.splitlines() if "\\multicolumn" not in ln]
    out = "\n".join(lines)
    # Strip the original {\small ...} wrapper and re-wrap explicitly so there
    # are no dangling braces from the generated source.
    out = out.replace("{\\small\\begin{tabular}", "\\begin{tabular}")
    out = out.replace("\\end{tabular}}", "\\end{tabular}")
    if short_header:
        for a, b in short_header:
            out = out.replace(a, b)
    return "\\resizebox{\\linewidth}{!}{%\n" + out + "\n}\n"


short = [("MNIST $T{=}4$ & MNIST $T{=}8$ & CIFAR10 $T{=}4$ & CIFAR10 $T{=}8$",
          "M4 & M8 & C4 & C8")]
for name in ("tab_main.tex", "tab_baselines.tex", "tab_ablations.tex"):
    raw = (SRC / "tables" / name).read_text(encoding="utf-8")
    (REV / "tables" / name).write_text(wrap_table(raw, short), encoding="utf-8")

# The generated identity table printed residuals as "0.0e-0"; rebuild with real
# scientific notation from the two confirmation files.
import json
R = S.parents[1]
e17 = json.loads((R / "results" / "e17" / "confirmation.json").read_text(encoding="utf-8"))
e18 = json.loads((R / "results" / "e18" / "confirmation.json").read_text(encoding="utf-8"))


def sci(x):
    mant, exp = f"{x:.2e}".split("e")
    return f"${mant}\\times10^{{{int(exp)}}}$"


def rng(group):
    v = [x["identity_residual"] for x in group["runs"] if "identity_residual" in x]
    return f"{sci(min(v))} -- {sci(max(v))}"


(REV / "tables" / "tab_identity.tex").write_text(
    "\\resizebox{\\linewidth}{!}{%\n"
    "\\begin{tabular}{lcc}\\hline\n"
    "Holdout group & float64 residual (max) & float32 gap \\\\\\hline\n"
    f"seeds 10--14 & {rng(e17)} & $3.7\\times10^{{-7}}$ \\\\\n"
    f"seeds 15--19 & {rng(e18)} & $3.7\\times10^{{-7}}$ \\\\\n"
    "\\hline\\end{tabular}\n}\n", encoding="utf-8")

# Table 1 caption absorbs the note that used to overflow as a table row
p = REV / "sections" / "4_experiments.tex"
s = p.read_text(encoding="utf-8")
s = s.replace(
    "\\caption{Five-seed results on untouched holdout seeds 10--14. Energy is a 45\\,nm theoretical arithmetic estimate under two conventions; loss is conversion loss in percentage points (lower is better).}",
    "\\caption{Five-seed results on untouched holdout seeds 10--14. Energy is a 45\\,nm theoretical arithmetic estimate under two conventions; loss is conversion loss in percentage points (lower is better). Every one of the ten individual conservative ratios exceeds 5.464$\\times$.}")
p.write_text(s, encoding="utf-8")

print("LAYOUT REVISION APPLIED in", REV)
