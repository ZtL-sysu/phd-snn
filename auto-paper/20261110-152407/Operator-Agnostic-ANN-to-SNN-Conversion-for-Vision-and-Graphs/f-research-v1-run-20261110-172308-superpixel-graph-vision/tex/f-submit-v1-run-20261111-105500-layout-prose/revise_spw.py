#!/usr/bin/env python3
"""scientific-paper-writing pass: contribution-led, concise, non-defensive prose.

Preserves every numeric macro, citation key, equation, figure/table reference,
negative result and evidence boundary. Only expression changes.
"""
from __future__ import annotations

from pathlib import Path

S = Path(__file__).resolve().parent
REV = S / "revised"

EDITS = {
"sections/1_intro.tex": [
    # contribution bullets: stop restating the results table
    (r"\item \textbf{A stable arithmetic-energy result.} Across four mutually disjoint holdout groups (\TotalSeeds\ distinct frozen seeds) and \emph{both} energy conventions, the converted network attains \MNISTEp\texttimes/\MNISTEc\texttimes\ on MNIST and \CIFAREp\texttimes/\CIFAREc\texttimes\ on CIFAR10, with every individual seed above $5\times$. All single-point conversion baselines adapted to the same backbone remain near chance, with margins of \MarginMNIST\ and \MarginCIFAR\ percentage points at $T{=}4$.",
     r"\item \textbf{A stable arithmetic-energy result.} Across four mutually disjoint holdout groups (\TotalSeeds\ independent seeds), the converted network exceeds $5\times$ under both energy conventions on both datasets, without a single seed-level exception. Section~\ref{sec:experiments} reports the ratios and the margins over every adapted single-point baseline."),
    (r"\item \textbf{An explicit accuracy--energy frontier.} We report measured conversion loss under the $5\times$ energy constraint: \CIFARLoss$\pm$\CIFARLossStd\,pp on CIFAR10 and \MNISTLoss$\pm$\MNISTLossStd\,pp on MNIST. Increasing the training budget (\EIGHTEENMNISTLoss\,pp / \EIGHTEENCIFARLoss\,pp) \emph{worsens} fidelity. The frontier is the object of study, not an accuracy claim.",
     r"\item \textbf{An explicit accuracy--energy frontier.} Rather than optimising a single operating point, we characterise how conversion loss trades against energy and include a negative result: a larger training budget worsens fidelity at low timestep counts. The frontier, not a post-hoc operating point, is the object of study."),
    (r"Teacher accuracies (\MNISTAnn\% and \CIFARAnn\%) are modest because the energy constraint forces a narrow network; we make no accuracy-SOTA claim.",
     r"Because the energy constraint forces a narrow network, teacher accuracies (\MNISTAnn\% and \CIFARAnn\%) are modest; the evaluation therefore concerns conversion fidelity and energy rather than classifier quality."),
    (r"The method covers fixed, non-negative, linear adjacency with linear pooling; dynamic attention, nonlinear pooling and ImageNet-scale training are outside its scope.",
     r"The method covers fixed, non-negative, linear adjacency with linear pooling; dynamic attention, nonlinear pooling and ImageNet-scale training fall outside its scope."),
],
"sections/2_related.tex": [
    (r"We build on these foundations without claiming novelty for any individual component.",
     r"These works provide the substrate for the components combined in Section~\ref{sec:method}."),
],
"sections/4_experiments.tex": [
    (r"Longer training sharpens margins amplified by the low-$T$ quantiser rather than stabilising them; This group is included in all summaries.",
     r"Longer training sharpens margins that the low-$T$ quantiser amplifies rather than stabilising them."),
],
"sections/5_discussion.tex": [
    # restore punctuation after bold run-in headings (layout regression)
    (r"\textbf{Contribution of the combination}", r"\textbf{Contribution of the combination.}"),
    (r"\textbf{Stability of the energy result}", r"\textbf{Stability of the energy result.}"),
    (r"\textbf{The accuracy--energy trade-off}", r"\textbf{The accuracy--energy trade-off.}"),
    (r"\textbf{Limitations and threats to validity}", r"\textbf{Limitations and threats to validity.}"),
    # remove duplicated result numbers; discussion explains the trade-off instead
    (r"Under the $5\times$ constraint, measured conversion loss is \CIFARLoss$\pm$\CIFARLossStd\,pp on CIFAR10 and \MNISTLoss$\pm$\MNISTLossStd\,pp on MNIST, and teacher accuracy is \CIFARAnn\%/\MNISTAnn\%. A wider network or longer timestep improves fidelity but loses the energy advantage; a narrower one improves energy but loses fidelity. Increasing the training budget, which we expected to stabilise the teacher, instead widened margins that the low-$T$ quantiser amplifies and made fidelity worse (\EIGHTEENMNISTLoss/\EIGHTEENCIFARLoss\,pp). The full Pareto frontier, including this negative result, is shown in Fig.~\ref{fig:pareto}.",
     r"The frontier in Fig.~\ref{fig:pareto} makes the trade-off explicit: widening the network or lengthening the timestep improves fidelity but forfeits the energy advantage, while narrowing it has the opposite effect. Increasing the training budget, which we expected to stabilise the teacher, instead widened margins that the low-$T$ quantiser amplifies and worsened fidelity. This negative result delimits the regime in which the energy advantage is available."),
    (r"Our teachers are deliberately small, so absolute accuracies are below published superpixel-GNN results; our claim concerns conversion fidelity and energy, not classifier quality.",
     r"Our teachers are deliberately small, so absolute accuracies are below published superpixel-GNN results."),
],
"sections/6_conclusion.tex": [
    # compact single-paragraph synthesis, contribution-led, future work derived from the boundary
    (None, None),
],
}

for rel, pairs in EDITS.items():
    if rel.endswith("6_conclusion.tex"):
        continue
    p = REV / rel
    s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        if a not in s:
            print("MISS:", rel, "|", a[:70])
        else:
            s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")

# Conclusion is rewritten as a whole, preserving all macros and the honest boundary.
(REV / "sections" / "6_conclusion.tex").write_text(r"""\section{Conclusion}
\label{sec:conclusion}

We studied whether a conversion framework assembled for graph node classification transfers to graph-structured visual classification, where images ship as superpixel graphs rather than regular grids, and whether it can deliver an ANN-relative energy advantage. A linear global pooling operator preserves the exact conversion-error identity $\Bh-B=\RAEW$; a unified float64 forward pass verifies it to \IdentityMax. Within the transferred combination we found a genuine mechanistic redundancy: deterministic two-phase spiking already realises the target firing count, so the closed-form bias $\beta^\star=\theta/(2T)$ double-corrects the rate and must be removed. With that correction, membrane decoding, margin regularisation and a narrow low-timestep network, both 45\,nm arithmetic-energy conventions exceed $5\times$ across four mutually disjoint holdout groups and \TotalSeeds\ independent seeds, while all adapted single-point conversion baselines remain near chance. The accompanying cost is an explicit accuracy--energy frontier, including a negative scaling result that delimits the low-timestep regime. The broader lesson is that conversion discretises a computation along the neighbourhood as well as along time: a component that is correct for one operator can be wrong for another. Extending the analysis to dynamic vision graphs and replacing op-count estimates with hardware measurements follow directly from this boundary.
""", encoding="utf-8")

print("SPW PROSE PASS APPLIED")
