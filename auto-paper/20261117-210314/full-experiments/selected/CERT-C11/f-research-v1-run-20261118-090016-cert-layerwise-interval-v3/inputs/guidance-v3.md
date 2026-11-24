# Research Guidance File

## Title / Topic

- Working title: Layerwise Interval Certificates for Quantized Messages in Frozen Two-Layer GNN-to-SNN Conversion
- Target field: verified graph-message compression and frozen ANN-to-SNN conversion
- Target venue: Q2+ journal / IEEE TNNLS-style conversion-verification scope
- Technique/method: deterministic layerwise absolute-value interval propagation through two normalized-adjacency applications, one ReLU, and frozen weights
- Selected application scenario: frozen two-layer GCN checkpoints on Cora, Chameleon, and Squirrel

## Core Idea

Quantize the pre-aggregation first-layer channel message, then certify the resulting frozen two-layer GCN logits with an operator-aware interval bound. The exact computation is

`M = X W0`, `M_hat = Q(M)`, `H = relu(A M + b0)`, `H_hat = relu(A M_hat + b0)`, `Z = A H W1 + b_out`, and `Z_hat = A H_hat W1 + b_out`.

For `E = M - M_hat` and a deterministic coordinatewise radius `Delta >= abs(E)`, ReLU non-expansiveness gives `abs(H-H_hat) <= abs(A) abs(E)`. The second aggregation and frozen weight give

`abs(Z-Z_hat) <= B_prop = abs(A) abs(A) Delta abs(W1)`.

Under independent coordinate intervals, `B_prop` is the exact worst-case absolute-value interval envelope before interval-dependence tightening. The empirical contribution is its measured width and tightening relative to correctly defined Euclidean and global scalar references.

### Mechanism-Level Rationale

- Domain bottleneck: generic scalar or norm bounds ignore output coordinates, graph-operator magnitude, and quantizer granularity.
- Mechanism: propagate the known rounding radius through both normalized-adjacency applications, the 1-Lipschitz ReLU, and the frozen downstream matrix.
- Required adaptation: explicit tensor shapes, deterministic uniform/per-channel quantizers, float64 bound arithmetic, clipping-aware radius, rowwise Euclidean comparator, global scalar reference, and all-cell audit.
- Novelty boundary: a tailored deterministic envelope and tightness study for the exact frozen two-layer chain above; not a new general interval theorem, multilayer nonlinear certificate, temporal SNN result, robustness guarantee, or energy claim.

## Paper Story

- Central scientific question: for the exact frozen two-layer message path, how much tighter is the layerwise absolute interval envelope than standard norm/scalar references while retaining deterministic containment?
- Intended reader: graph compression, verified ML, and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → choice: finite-precision graph messages → propagate known local radii through graph operators and weights → auditable outputwise certificate.
- Expected contribution type: application-specific deterministic certificate plus matched quantizer/bound study.
- planned_claim: all 36 corrected cells have deterministic containment, median width/RMS ≤10, every cell ≤15, and per-cell tightening ≥25% versus the global scalar reference.
- observed_finding: pending corrected v3 confirmation.
- Main claim: valid and tighter layerwise interval envelopes for the exact frozen two-layer chain.
- Boundary: three graphs, checkpoint seeds 0/1/2, 4/8 levels, global/per-channel uniform rounding, no labels or actual errors in bound construction.

## Paper Outline

1. Introduction: why finite-precision graph-message certificates need exact operator and metric contracts.
2. Related Work: ANN-to-SNN conversion error, quantized GNN communication, certified/robust SNNs, interval propagation and norm bounds.
3. Method: exact tensor chain, quantizer radius, ReLU and adjacency propagation, `B_prop`, rowwise Euclidean bound, global scalar reference.
4. Experiments and Results: 36-cell deterministic containment audit, width/RMS, tightening, quantizer granularity, seed/graph dispersion and failures.
5. Discussion: theorem/implementation interpretation, comparator fairness, and strict scope limitations.
6. Conclusion: layerwise interval propagation yields auditable finite-precision envelopes in the tested frozen two-layer GNN message path.

## Experiment Plan

### Datasets and splits

Cora, Chameleon, and Squirrel public graph data from existing local project snapshots. Frozen checkpoint seeds 0, 1, and 2. The certificate uses no labels and performs no split selection. Dataset/model hashes and dimensions are recorded.

### Exact tensors and quantizers

- `X ∈ R^(N×F)`, normalized `A ∈ R^(N×N)`, `W0 ∈ R^(F×H)`, `b0 ∈ R^H`, `W1 ∈ R^(H×C)`, `b_out ∈ R^C`.
- `M = X W0` is quantized before first-layer adjacency aggregation; `b0` is not quantized.
- Global-uniform quantizer: one min/max range and step `s = (max(M)-min(M))/(L-1)`.
- Per-channel-uniform quantizer: one min/max range and step `s_j` per channel of `M`.
- Rounding is deterministic `floor((m-min)/s + 0.5)` with ties upward, then clipped to the finite level grid; exact min/max endpoints are represented.
- Radius is `Delta_ij = s/2` or `s_j/2`, with `Delta=0` for a constant channel. Clipping/saturation outside the declared range is not allowed; any such event fails the cell.
- Model/message computation is float32; bounds, RMS, ratios and comparisons are computed in float64.

### Baselines

- Proposed layerwise absolute interval: `B_prop = abs(A) @ abs(A) @ Delta @ abs(W1)`.
- Correct rowwise Euclidean bound: `B_euc[i,k] = sqrt(sum_j((abs(A)@abs(A))[i,j] * Delta[j])^2) * ||W1[:,k]||_2`.
- Deliberately loose global scalar reference: `B_global[i,k] = rowsum(abs(A)@abs(A))[i] * max(Delta) * sum(abs(W1))`.
- Actual error `abs(Z-Z_hat)` is diagnostic only and cannot construct `Delta`, select a range after observing errors, or tune a bound.

### Required experiments

| ID | Matrix | Primary metric | Minimum | Binding expected-strong |
|---|---|---|---|---|
| CERT-A | 3 graphs × 3 seeds × 2 levels × 2 quantizers | deterministic containment | all 36 finite | 36/36 cells pass; any violation fails |
| CERT-B | same matrix, proposed bound | width/RMS | reported per cell | median ≤10 and every cell ≤15 |
| CERT-C | proposed versus global scalar | per-cell tightening | reported per cell | every cell ≥25%; report median/range |
| CERT-D | proposed versus rowwise Euclidean | elementwise bound comparison | no violation | `B_prop <= B_euc + tol` in all cells |
| CERT-E | quantizer granularity | radius/step audit | exact | no observed-error-derived radius, clipping, NaN or Inf |

### Metrics and numerical policy

- Actual RMS is `sqrt(mean(abs(Z-Z_hat)^2))` over all `N×C` logits in a cell.
- Proposed width/RMS is `median(B_prop)/actual_RMS`; global and Euclidean use the same denominator and median rule.
- Per-cell tightening is `1 - proposed_width_over_rms / global_width_over_rms`.
- If actual RMS is zero, a zero actual error with zero bounds passes with ratio 0; any nonzero bound/zero RMS case is `+inf` and fails.
- Comparisons use elementwise `atol=1e-10`, `rtol=1e-12` in float64. NaN/Inf is an explicit failed cell.
- Containment is called deterministic theorem/implementation containment, never statistical coverage or a confidence interval.
- Report every row, all dispersion, the worst width/RMS cell, minimum tightening cell, and all negative/failure diagnostics.

### Runtime / hardware budget

RTX3060 12GB or CPU fallback; Conda `dyg-cold`; 36 cells and fixed matrix; target under 15 minutes and under 2 GB peak memory; no remote compute.

## Expected Results

- Minimum: complete 36-cell corrected matrix with explicit derivation and reproducible numerical policy.
- Strong: CERT-A through CERT-E pass with 36/36 deterministic containment, median width/RMS ≤10, maximum ≤15, per-cell tightening ≥25%, and proposed no looser than Euclidean.
- Failure: any containment violation, clipping event, non-finite result, width/RMS above 15, tightening below 25%, or ambiguity in the operator chain blocks the strong claim.
- Writing gate: corrected raw rows, derivation, code and tests must be frozen first; all v1/v2 experiments and CCFA reviews remain preserved background.

## Figure/Table Decision Rules

Figure 1 shows the exact quantize → aggregate → ReLU → aggregate → frozen-weight chain. Figure 2 shows per-cell width/RMS and tightening. Figure 3 compares global-uniform and per-channel-uniform radii. Table 1 defines the three bounds and numerical policy. Table 2 reports the complete 36-cell result and worst cases.

## Traceability Checklist

Every number maps to `results/cert-confirmation.json`, `results/cert-confirmation.csv`, `results/cert-theorem-audit.json`, `research/cert_confirmation.py`, and `input-manifest.json`. Record dataset/model hashes, dimensions, seed, quantizer, step/radius, tolerance, clipping count, and every failed row. Preserve `f-research-v1-run-20261118-085119-cert-operator-aware-envelope-v2` as the CCFA-revised negative attempt.

## Citation Scope

At least 30 unique verified references, majority 2022–2026. Must cite frozen ANN-to-SNN conversion, graph-message quantization/communication, certified or robust SNNs, interval bound propagation, ReLU 1-Lipschitz/non-expansive arguments, matrix norm bounds, and the three graph benchmarks. Literature-only context must remain separate from direct bound comparisons.

## Constraints and Preferences

English paper, Chinese logs; complete TeX/PDF/source package; one final PDF; no commit, push, submission, remote compute, or credential writes; all run artifacts under the v3 run root; retain all prior versions, CCFA reviews and failures as negative evidence.
