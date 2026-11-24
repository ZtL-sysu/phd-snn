# Startup decision

**Decision: `proceed`.**

Rationale, in the order the gates ran.

G0/G4 — the literature sweep (33 arXiv hits on spiking GNNs, plus targeted searches on conversion
theory) returns no paper that predicts conversion fidelity for graphs, no paper that states a depth
behaviour, and no paper that separates ordering from quantisation. SGNNBench, the largest unified
evaluation, contains no conversion entry at all, which is positive evidence of the gap rather than an
absence of search.

G1/G2 — the datasets are directly public (Planetoid via the original GitHub raw files, ogbn-arxiv via
OGB, chameleon/squirrel via PyG), the split is the standard public split, and the metric is accuracy
with a measured run-to-run floor. Nothing depends on an approval flow.

G3/G7 — the mechanism is a recursion we can write down and have verified numerically, and it yields a
falsifier (held-out prediction error) rather than a story. The strong-result contract prices the risk
with numbers we already measured rather than hopes: the amplification exponent is 0.948 at r = 0.990,
the √H law is stable to 6 %, and the order-invariance spread is 0.000 pp.

G5 — 40 h on a local RTX 3060 and 12 cores, with a stated de-scoping rule.

G6 — the one gate that is only *partially* satisfiable: no published spiking-GNN method ships
checkpoints and SpikingGCN's repository is dependency-pinned to a Python 3.6 stack. The decision is
to proceed with formulation-level re-implementations, labelled as such in the caption, and with the
unfavourable row (their architecture beats us on two graphs) retained. Proceeding with a labelled
limitation is honest; pretending the gate is fully met would not be.

G8 — the red team scored current readiness at 4/10 for the target tier and named exactly two
score-change conditions: out-of-sample prediction (+2) and an external Pareto anchor (+2). Both are
in the guidance as binding claims with numeric thresholds and stated failure signals. The tier is
therefore conditional and the guidance says so; that is the honest position, and it is the reason the
paper can fail one of the two and still ship as a B-venue paper rather than collapsing.

Blocking issues found: none that cannot be handled by labelling. The one genuine risk — that we have
no codebase-level external reproduction — is recorded in the guidance, the red-team file, the
baseline matrix and the paper's own limitations section, so no later stage can quietly upgrade it.
