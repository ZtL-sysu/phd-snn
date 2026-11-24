# P10 post-revision correction

AutoResearchClaw Stage 19 returned a complete revised manuscript. Automated validation initially reported two formatting-only failures:

1. The manuscript used the mathematically equivalent LaTeX notation `\(M_0=\hat{A}X\)` rather than the literal ASCII string `A_hat X`.
2. The Figure 4 caption did not explain the dashed 3 pp reference line.

No scientific fact was changed. The notation check now accepts the implemented normalized-adjacency notation, and the Figure 4 caption explicitly states that the dashed line is the earlier 3 pp task-loss reference rather than an observed equivalence threshold.
