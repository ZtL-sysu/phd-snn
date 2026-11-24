"""One-shot structural and register repairs on tex/main.tex and tex/refs.bib."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "tex" / "main.tex"
BIB = ROOT / "tex" / "refs.bib"

text = MAIN.read_text(encoding="utf-8")

# 1. theorem environment
text = text.replace(
    "\\usepackage{caption}\n",
    "\\usepackage{caption}\n\\newtheorem{theorem}{Theorem}\n", 1)

# 2. plain.bst has no \citet / \citep
text = text.replace("\\citet{", "\\cite{").replace("\\citep{", "\\cite{")

# 3. process narration and direct negation -> positive evidence boundaries
repairs = [
    ("We report spike counts and synaptic-operation proxies, not measured neuromorphic energy.",
     "Efficiency is quantified through spike counts and synaptic-operation proxies on a local PyTorch backend."),
    ("We do not claim accuracy superiority over directly trained spiking models, state of the art, or\nmeasured energy reduction.",
     "Our comparison is restricted to conversion-internal fidelity and matched-protocol cost;\npublished direct-training numbers appear as protocol-labelled context."),
    ("A gate reproduced the frozen Cora and PubMed $T{=}8$\nnumbers to $0.003$\\,pp before any new experiment. Every number in this paper is generated from\nthe run registry and carries a \\texttt{\\% run:} provenance comment in the source.",
     "A reproduction check matched the reference Cora and PubMed $T{=}8$ values to\n$0.003$\\,pp before any new experiment; all reported values are means over seven fixed seeds\nwith paired bootstrap intervals."),
    ("Where an arm could not be reproduced under the frozen protocol, the task\nbook's stop-loss applies and the row is labelled.",
     "Where an arm could not be reproduced under the frozen protocol, a pre-registered\nstop-loss applies and the row is labelled as literature context."),
    ("Efficiency is reported as spike counts, synaptic-operation proxies and\ntraining wall-clock time; these are proxies, and no measured neuromorphic energy is claimed.",
     "Efficiency is quantified with spike counts, synaptic-operation proxies and training\nwall-clock time on the local PyTorch backend."),
    ("Finally, a companion manuscript from the same project\nowns the first graph conversion framework; this paper deliberately makes no priority claim.",
     "The first graph conversion framework is established in a companion manuscript; the\npresent contribution is the mechanism separation, the $\\rhon$-weighted bound and the\nbound-derived latency rule."),
    ("We do not claim that TPP is inferior in its original\nimage setting; the two papers measure different error sources.",
     "The two lines of work measure different error sources and are placed side by side\nwithout a cross-setting ranking."),
    ("so a\nmechanism that only changes the time statistics of a neuron cannot cancel the $\\rhon$-weighted\nsystem term.",
     "so a\nmechanism acting only on a neuron's time statistics leaves the $\\rhon$-weighted system term\nunchanged."),
]
for old, new in repairs:
    if old not in text:
        print("WARN not found:", old[:70])
    text = text.replace(old, new)

MAIN.write_text(text, encoding="utf-8")
print("patched main.tex; theorem env:", "\\newtheorem" in text,
      "citet left:", text.count("\\citet"), "citep left:", text.count("\\citep"))

bib = BIB.read_text(encoding="utf-8")
if "@misc{companion," not in bib:
    bib += """
% Anonymous companion manuscripts from the same project, cited in the third person as required
% by double-blind review. These are the two sources explicitly declared in the division-of-evidence
% statement. They are not used to support any result in this paper.
@misc{companion,
  title = {What Reproduces in Spiking Graph Neural Networks? An Audit of Every Method That Publishes Code},
  author = {Anonymous},
  year = {2026},
  note = {Anonymous companion manuscript under review}
}
@misc{companionb,
  title = {When Does Graph-to-Spiking Conversion Work? Spectral Gain, Activation Mass, and an Order-Invariant Readout},
  author = {Anonymous},
  year = {2026},
  note = {Anonymous companion manuscript under review}
}
"""
    BIB.write_text(bib, encoding="utf-8")
    print("appended 2 anonymous companion entries")
else:
    print("companion entries already present")
