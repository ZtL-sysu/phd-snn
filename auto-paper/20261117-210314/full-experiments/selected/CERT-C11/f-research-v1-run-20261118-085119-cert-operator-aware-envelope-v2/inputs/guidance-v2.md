# Research Guidance File

## Title / Topic

- Working title: Operator-Aware Affine Error Envelopes for Quantized Graph Messages in Frozen GNN-to-SNN Conversion
- Target field: verified graph-message compression and frozen ANN-to-SNN conversion
- Target venue: Q2+ journal / IEEE TNNLS-style conversion-verification scope
- Technique/method: deterministic output-column interval envelopes propagated through normalized adjacency, ReLU's 1-Lipschitz property, and frozen downstream weights
- Selected application scenario: frozen two-layer GCN checkpoints on Cora, Chameleon, and Squirrel

## Core Idea

For a frozen two-layer GCN, quantization of the first-layer pre-activation message changes the final logits. A deterministic certificate can propagate the known quantizer rounding interval through normalized adjacency and the downstream weight matrix without labels at inference. The useful contribution is not a statistical coverage claim; it is an output-aware, operator-aware worst-case envelope whose width is substantially tighter than a scalar global norm bound.

### Mechanism-Level Rationale

- Domain bottleneck: generic norm bounds merge all output coordinates and ignore the graph operator and quantizer granularity.
- Mechanism: for message error matrix `E`, ReLU is non-expansive, so `abs(A @ relu(M) - A @ relu(M_hat))` is bounded by `abs(A) @ abs(E)`. Propagating the componentwise quantizer interval through `abs(A)` and `abs(W2)` yields a per-node, per-logit interval.
- Required adaptation: global-uniform and per-channel-uniform rounding bounds, normalized adjacency, frozen `W1/W2`, exact float64 bound arithmetic, and a global scalar comparator.
- Novelty boundary: this is a certificate for one post-aggregation affine message followed by ReLU and one frozen downstream linear map. It is not a general multi-layer, nonlinear, temporal-spike, energy, or robustness theorem.

## Paper Story

- Central scientific question: can an operator-aware output-column interval certificate remain valid while being materially tighter than a global scalar bound for quantized graph messages?
- Intended reader: graph compression, verified ML, and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → choice: loose generic bounds → propagate known local rounding intervals through `A` and `W2` → output-aware certificate with auditable width.
- Expected contribution type: deterministic certificate plus matched quantizer/bound study.
- planned_claim: all measured post-aggregation logit errors are contained, with width/RMS at most 10 and at least 25% tighter than the global scalar bound across the fixed matrix.
- observed_finding: pending corrected operator-aware confirmation.
- Main claim: valid and tighter output-column envelopes for the stated two-layer frozen-GCN scope.
- Boundary: three graphs, checkpoint seeds 0/1/2, 4/8 quantization levels, global/per-channel uniform rounding, no label use, no causal claim, no energy claim.

## Paper Outline

1. Introduction: why certified conversion error needs operator- and output-aware bounds.
2. Related Work: ANN-to-SNN conversion error, quantized GNN communication, robust/certified SNNs, interval and norm bounds.
3. Method: frozen two-layer GCN, quantizer interval, ReLU propagation, output-column envelope, global scalar and Euclidean comparators.
4. Experiments and Results: coverage audit, width/RMS, tightening, quantizer granularity, seed/graph/level sweep, failure diagnostics.
5. Discussion: what the deterministic certificate proves, why coverage is a validity audit rather than independent statistical evidence, and scope limits.
6. Conclusion: operator-aware affine envelopes can make finite-precision graph-message certificates substantially tighter in the tested frozen-GCN setting.

## Experiment Plan

### Datasets and splits

Cora, Chameleon, and Squirrel public graph data from the existing local project snapshots; frozen checkpoint seeds 0, 1, and 2. No labels are used by the certificate. Dataset loading and model snapshots are hash-tracked; no test selection is performed.

### Baselines

- Proposed output-column interval envelope: `B_prop[i,k] = (abs(A) @ Delta @ abs(W2))[i,k]`, where `Delta` contains the deterministic rounding half-step per message coordinate.
- Global scalar L1 envelope: `B_global[i,k] = rowsum(abs(A))[i] * max(Delta) * sum(abs(W2))`.
- Output-column Euclidean envelope: `rowsum(abs(A))[i] * ||Delta_row||_2 * ||W2[:,k]||_2`.
- Actual absolute error `abs(Z - Z_hat)` is a diagnostic lower-scale reference, never used to construct the proposed bound.

### Required experiments

| ID | Matrix | Primary metric | Minimum | Binding expected-strong |
|---|---|---|---|---|
| CERT-A | 3 graphs × 3 seeds × 2 levels × 2 quantizers | empirical containment | all 36 cells finite | 100% coverage in all 36 cells; any violation fails |
| CERT-B | same matrix, proposed versus global scalar | width/RMS | reported per cell | median width/RMS ≤10 and every cell ≤15 |
| CERT-C | same matrix, proposed versus global scalar | tightening | reported per cell | minimum tightening ≥25%; report median and range |
| CERT-D | same matrix, proposed versus Euclidean | bound width | no violation | proposed never exceeds Euclidean by more than numerical tolerance |
| CERT-E | quantizer granularity | rounding half-step and actual error | exact | per-channel bounds are valid and not constructed from labels or logits |

### Metrics and statistics

Report coverage fraction, maximum violation, width/RMS, median width/RMS, tightening `1 - median(B_prop)/median(B_global)`, per-cell values, and the finite-precision arithmetic tolerance. Use float64 for certificate arithmetic and float32 only for model/message computation. Coverage is a deterministic implementation/theorem audit, not a confidence interval. Report all 36 rows and preserve any failed cell.

### Runtime / hardware budget

RTX3060 12GB or CPU fallback; project Conda `dyg-cold`; three graphs, three checkpoint seeds, two levels, two quantizers; target under 15 minutes and under 2 GB peak memory. No remote compute.

## Expected Results

- Minimum: complete 36-cell matrix, all coverage checks pass, and width/tightness tables are auditable.
- Strong: CERT-A through CERT-E pass, with 100% containment, median width/RMS ≤10, every cell ≤15, and minimum tightening ≥25% versus the global scalar bound.
- Failure: any uncovered error, non-finite bound, width/RMS above 15, tightening below 25%, or an unavailable model/data snapshot triggers a correction or a narrowed claim before writing.
- Writing gate: corrected operator-aware raw rows, derivation, and tests must be frozen before manuscript drafting; old single-affine rows are background only and cannot support the main claim.

## Figure/Table Decision Rules

Figure 1 shows message quantization → interval propagation → output-column certificate. Figure 2 shows per-cell width/RMS and tightening. Figure 3 compares global-uniform and per-channel-uniform quantizers. Table 1 states the three bounds. Table 2 reports the 36-cell summary and worst-case diagnostics.

## Traceability Checklist

Every manuscript number maps to `results/cert-confirmation.json`, `results/cert-confirmation.csv`, `results/cert-bound-derivation.json`, and the frozen model/data input manifest. Include code hashes, model seed, quantizer level, adjacency normalization, tolerance, and all failed or negative diagnostics. Preserve the prior full-experiment result as `inputs/prior-cert-v1.json` with its limitation record.

## Citation Scope

At least 30 unique verified references, with a majority from 2022–2026. Must cite frozen ANN-to-SNN conversion, graph-message quantization/communication, robust or certified SNNs, interval bound propagation, Lipschitz/non-expansive ReLU arguments, and graph benchmark datasets. Include a title/DOI/URL duplicate audit and mark literature-only context separately from direct baselines.

## Constraints and Preferences

English paper, Chinese logs; complete TeX/PDF/source package; one final PDF; no commit, push, submission, remote compute, or credential writes; all run artifacts under this guidance directory; retain old v1 results and all failures as negative evidence.
