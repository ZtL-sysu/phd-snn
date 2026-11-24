# CCFA Pre-Experiment Integrity Review

review_execution: independent-agent

## Integrity Verdict

**BLOCK PENDING CONTRACT CORRECTION**

**Score: 5.6/10**  
**Confidence: high**

The v2 package improves evidence discipline and preserves negative controls. Its storage and shuffle contracts are not precise enough to prevent an unsupported strong claim or a tautological order result.

## Claim-Evidence Alignment

| Claim | Evidence contract | Integrity judgment |
|---|---|---|
| Hybrid fidelity ≤5% | Frobenius error on two graphs | Well-defined if denominator and reconstruction payload are frozen |
| Storage ≥4x | Average bits/value | Underdefined; cannot reproduce prior 10.17x |
| Permutation equivariance | Two graphs x five seeds, raw/hybrid | Structurally sound; standard algebraic property |
| Hop-order information | POS-E and fixed-probe control | POS-E potentially tautological |
| Task retention ≤2 pp | Five paired split/probe seeds | Fair if probe/splits are identical across methods |
| Scope | Two static graphs, frozen messages | Appropriate |

## Mathematical And Design Checks

### Representation

`H=[X,AX,A^2X,A^3X]` is dimensionally consistent for `X∈R^(N×F)` and row-normalized `A∈R^(N×N)`. Under `X→PX`, `A→PAP^T`, the hop representation transforms as `H→PH`, so the inverse-permutation audit is a valid implementation check but not a novel theorem.

### Hybrid reconstruction

The error claim requires an exact decoder definition: centroid lookup, escape identification, float32/float64 precision, per-channel codebook fitting, and treatment of constant channels. The 0.5% escape rule must identify escapes from the declared data scope without using labels or task results.

### Fixed probe

The raw-trained probe must be paired across methods. Retrained probes answer a different question and cannot be substituted into the fixed-probe claim. Report paired raw-hybrid accuracy differences per seed, not only independent means.

## Numeric-Policy Gaps

1 Storage denominator is not specified as bits per original scalar or serialized file size.
2 Codebook centroid storage is not amortized in the current `3.145` figure.
3 Escape marker/index storage is absent.
4 Escape payload precision is unstated.
5 Relative Frobenius error denominator and zero-denominator policy are unstated.
6 Shuffled/ordered error references are unstated.
7 Contract matrix mixes five split/probe seeds and five permutation/shuffle seeds without a row-count table.

## Strong-Gate Integrity

- Fidelity and accuracy thresholds are falsifiable and plausible from prior data.
- Permutation error is a deterministic implementation audit.
- Storage `≥4x` may remain plausible under conservative accounting, but the reported strength is not yet auditable.
- POS-E `≥1.25x` is not acceptable until its reference construction is non-tautological.
- POS-F is correctly descriptive and must not be promoted to a binding result.

## Required Corrections

1 Publish a symbolic bit ledger covering symbol width, escape flag/index, payload bits, codebook bits and amortization rule.
2 Recompute expected bits under the chosen format before locking the 4x gate.
3 Define within-node/global shuffle semantics and ordered/shuffled target matrices.
4 State the exact row matrix and paired seed relationships.
5 Freeze codebook/escape fitting data scope and decoder precision.
6 Keep fixed-probe and retrained-probe results separate.

**Recommendation:** block. The core multi-seed design is credible, but integrity cannot be signed while storage and shuffle gates are underdefined.
