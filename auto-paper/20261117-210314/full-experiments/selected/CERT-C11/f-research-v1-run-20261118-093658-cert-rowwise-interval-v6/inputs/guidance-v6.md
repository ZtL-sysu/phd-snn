# Research Guidance File

## Title / Topic

- Working title: Rowwise Layerwise Interval Certificates for Quantized Messages in Frozen Two-Layer GNN-to-SNN Conversion
- Target field: verified graph-message compression and frozen ANN-to-SNN conversion
- Target venue: Q2+ journal / IEEE TNNLS-style conversion-verification scope
- Technique/method: deterministic layerwise absolute-value interval propagation through two normalized-adjacency applications, one ReLU, and frozen weights
- Selected application scenario: frozen two-layer GCN checkpoints on Cora, Chameleon, and Squirrel

## Core Idea

The only certified computation is

`M=XW0`, `M_hat=Q(M)`, `H=relu(A M+b0)`, `H_hat=relu(A M_hat+b0)`, `Z=A H W1+b_out`, and `Z_hat=A H_hat W1+b_out`.

All source arrays are loaded from stored float32 snapshots and immediately cast to float64. The quantizer, dequantizer, model reconstruction, bounds and metrics are evaluated in float64; no unmodelled float32 reconstruction error remains.

For `E=M-M_hat`, ReLU non-expansiveness gives `abs(H-H_hat) <= abs(A)abs(E)`. The second aggregation and frozen weight give

`abs(Z-Z_hat) <= B_abs = (abs(A)abs(A)Delta)abs(W1)`.

Let `C=abs(A)abs(A)`, `c=C 1_N`, `delta_(i,h)` be the deterministic rowwise quantizer radius, and `Delta` the `N×H` radius matrix. Under independent coordinate intervals, the componentwise interval envelope is

`B_abs = abs(A) abs(A) Delta abs(W1)`.

The empirical contribution is deterministic containment and relative tightening over a fair global-radius outputwise comparator for rowwise quantization. Absolute width/RMS is descriptive only. Global-uniform quantization is an equality control.

### Mechanism-Level Rationale

- Domain bottleneck: generic scalar bounds lose channelwise radius and output-column structure.
- Mechanism: propagate the deterministic channel radius through both graph operators, the 1-Lipschitz ReLU and the frozen downstream weight.
- Comparator policy: use a valid Minkowski upper bound and a global-radius outputwise L1 comparator; report the collapsed full-matrix scalar only as a loose context reference.
- Novelty boundary: a tailored deterministic envelope and quantizer-granularity study for the exact frozen two-layer chain; not a general interval theorem, multilayer nonlinear certificate, robustness guarantee, temporal SNN result, or energy claim.

## Paper Story

- Central scientific question: for the exact frozen two-layer chain, does rowwise radius propagation give deterministic containment and useful tightening over a fair global-radius outputwise comparator when node radii differ?
- Intended reader: graph compression, verified ML, and neuromorphic conversion researchers.
- Domain/theory problem → design requirement → choice: finite-precision graph messages → propagate known channel radii through graph operators and weights → exact componentwise interval envelope.
- Expected contribution type: application-specific deterministic certificate plus matched quantizer-granularity study.
- planned_claim: 36/36 deterministic containment; `B_abs` is no looser than the valid Minkowski comparator; global-uniform equality control passes; every rowwise cell tightens by ≥25% versus the global-radius outputwise comparator.
- observed_finding: pending corrected v6 confirmation.
- Main claim: valid rowwise interval envelopes with substantial relative tightening when nodewise radii differ; no absolute-width promise.
- Boundary: three graphs, checkpoint seeds 0/1/2, 4/8 levels, global/rowwise uniform rounding, no labels or actual errors in bound construction.

## Paper Outline

1. Introduction: why finite-precision graph-message certificates require exact operator, radius and comparator contracts.
2. Related Work: ANN-to-SNN conversion error, quantized GNN communication, certified/robust SNNs, interval propagation and norm bounds.
3. Method: exact chain, float64 quantizer radius, `B_abs`, valid Minkowski comparator, global-radius outputwise comparator, collapsed scalar reference.
4. Experiments and Results: 36-cell containment audit, equality control, rowwise tightening, descriptive width/RMS and full failures.
5. Discussion: deterministic interpretation, comparator fairness, expected equality under constant radius, strict scope.
6. Conclusion: rowwise interval propagation is valid and substantially tightens the global-radius outputwise envelope in the tested rowwise quantizers.

## Experiment Plan

### Datasets and frozen models

Cora, Chameleon and Squirrel public graphs from local snapshots; frozen two-layer GCN checkpoints with seeds 0, 1 and 2. The certificate uses no labels or splits. Record data/model hashes and tensor shapes.

### Exact tensors and quantizers

- `X∈R^(N×F)`, normalized `A∈R^(N×N)`, `W0∈R^(F×H)`, `b0∈R^H`, `W1∈R^(H×C)`, `b_out∈R^C`.
- Stored float32 inputs are cast to float64 before `M=XW0`; all subsequent computations and dequantized values remain float64.
- Global-uniform: one range `[min(M),max(M)]`, step `s=(max-min)/(L-1)`, radius `delta_j=s/2` for every channel.
- Rowwise-uniform: per-node range `[min_i,max_i]`, step `s_i=(max_i-min_i)/(L-1)`, radius `delta_(i,h)=s_i/2` for every hidden channel of node `i`.
- Rounding is `floor((m-min)/s+0.5)` with ties upward. Min/max endpoints are exact. Endpoint clipping is only a safeguard; any out-of-range value beyond `atol=1e-10` fails the cell.
- Constant row: `s_i=0`, `Q(m_i)=m_i`, dequantized value equals the source in float64, and `delta_(i,h)=0`.
- The full radius matrix `Delta∈R^(N×H)` is computed from quantizer parameters before actual errors are inspected.

### Bounds and comparators

Let `C=abs(A)abs(A)`, `c_i=sum_q C[i,q]`, and `Delta∈R^(N×H)`.

- Proposed independent-box interval: `B_abs = abs(A)abs(A)Delta abs(W1)`.
- Valid Minkowski upper comparator: `B_mink[i,k]=(C ||Delta_row||_2)[i] ||W1[:,k]||_2`.
- Global-radius outputwise comparator: `B_global_col[i,k]=c_i max(Delta) ||W1[:,k]||_1`.
- Collapsed full-matrix scalar context only: `B_scalar[i,k]=c_i max(Delta) ||W1||_(1,1)`; it is excluded from the strong fairness gate.
- Actual error `abs(Z-Z_hat)` is diagnostic only and cannot construct `delta`, select a range after observing errors, or tune any bound.

### Required experiments

| ID | Matrix | Primary metric | Binding expected-strong |
|---|---|---|---|
| CERT-A | 3 graphs × 3 seeds × 2 levels × 2 quantizers | deterministic containment | 36/36 cells pass; any violation fails |
| CERT-B | proposed bound | width/RMS | descriptive only; report median and worst cell, no absolute threshold |
| CERT-C1 | 18 global-uniform cells | equality control | `B_abs == B_global_col + tol`; zero tightening is expected |
| CERT-C2 | 18 rowwise cells | per-cell tightening | every cell ≥25%; report median/range |
| CERT-D | all cells | valid comparator check | `B_abs <= B_mink + tol` everywhere |
| CERT-E | all cells | radius/implementation audit | no error-derived radius, clipping, NaN or Inf |

### Metrics and numerical policy

- Actual RMS is `sqrt(mean(abs(Z-Z_hat)^2))` over all `N×C` logits in a cell.
- Width/RMS is `median(B)[all N×C elements]/actual_RMS` for each bound.
- Per-cell tightening is `1 - width_over_rms(B_abs)/width_over_rms(B_global_col)` and applies only to the 18 rowwise cells.
- The exact tolerance predicate is `value <= bound + 1e-10 + 1e-12*abs(bound)`.
- All arrays and reductions are float64. Quantizer step/radius and dequantized value precision are logged.
- If actual RMS is zero, ratio 0 is allowed only when the corresponding median bound is zero; otherwise the ratio is `+inf` and the cell fails. The same rule applies to comparator width/RMS.
- NaN/Inf is a failed row. Every cell is preserved with seed, graph, level, quantizer, step vector hash, radius hash, clipping count and bound diagnostics.
- Deterministic containment is theorem/implementation validation, never statistical coverage or a confidence interval.

### Runtime / hardware budget

RTX3060 12GB or CPU fallback; Conda `dyg-cold`; fixed 36-cell matrix; target under 15 minutes and under 2 GB peak memory; no remote compute.

## Expected Results

- Minimum: complete corrected 36-cell matrix with exact formulas and all negative diagnostics.
- Strong: CERT-A through CERT-E pass, including expected global-uniform equality and ≥25% tightening in every rowwise cell.
- Failure: any containment/comparator violation, clipping event, non-finite value, rowwise tightening below 25%, or unresolved numerical ambiguity blocks the strong claim.
- Writing gate: corrected raw rows, derivation, code and tests are frozen before manuscript drafting; all previous attempts remain background.

## Figure/Table Decision Rules

Figure 1 shows the exact quantize → aggregate → ReLU → aggregate → frozen-weight chain. Figure 2 compares per-cell width/RMS and rowwise tightening. Figure 3 shows the global-uniform equality control and rowwise radius heterogeneity. Table 1 defines bounds and numerical policy. Table 2 reports all 36 cells and worst cases.

## Traceability Checklist

Every number maps to `results/cert-confirmation.json`, `results/cert-confirmation.csv`, `results/cert-theorem-audit.json`, `research/cert_confirmation.py`, and `input-manifest.json`. Preserve all v1/v2/v3 runs and CCFA reviews as negative evidence.

## Citation Scope

At least 30 unique verified references, majority 2022–2026. Must cite frozen ANN-to-SNN conversion, quantized GNN communication, certified/robust SNNs, interval bound propagation, ReLU non-expansiveness, matrix norm bounds and graph benchmarks. Literature-only context stays separate from direct comparator results.

## Constraints and Preferences

English paper, Chinese logs; complete TeX/PDF/source package; one final PDF; no commit, push, submission, remote compute, or credential writes; all v6 artifacts under its run root.
