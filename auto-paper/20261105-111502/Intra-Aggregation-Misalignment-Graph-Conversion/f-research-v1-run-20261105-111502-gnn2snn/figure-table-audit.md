# P18 — figure and table audit

| artifact | scientific question | evidence | placement |
|---|---|---|---|
| Table `tab:main` (Table 1) | do the method rows separate across the T grid? | `table1.json` | first discussion in Section 4 |
| Table `tab:s1` | are the two misalignments physically distinct? | `s1_probe.json` | Section 4.2 |
| Table `tab:c3` | does the bound predict a usable timestep? | `c3_allocation.json` | Section 4.3 |
| Table `tab:hosts` | does the correction plug into other aggregations? | `table1.json` hosts | Section 4.4 |
| Table `tab:contrast` | how does the bound differ from the image-domain form? | primary sources | Section 2 |
| Figure `fig:s1` | probe curves vs T | `s1_probe.json` | Section 4.2 |
| Figure `fig:tstar` | predicted vs measured T* | `c3_allocation.json` | Section 4.3 |
| Figure `fig:pareto` | accuracy/cost shape | `table1.json` | Section 4.4 |
| Appendix Table `tab:std` | seed uncertainty | `table1.json` | Appendix C |
| Appendix Table `tab:protocol` | frozen protocol | `protocols/protocol.md` | Appendix B |

Every artifact is cited and interpreted near its first discussion. Figure 1 (overall framework)
is generated as a TikZ schematic from verified components rather than through image generation:
`AutoResearchClaw`/image tooling is unavailable locally, and this substitution is recorded rather
than disguised. No per-subsection visual quota was applied.
