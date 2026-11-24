# CCFA Full-Paper Review

review_execution: independent-agent

## Verdict

**REVISE**

**Score: 7.2/10**  
**Confidence: medium-high**

The manuscript is scientifically coherent, appropriately scoped, and numerically strong. It is not submission-ready because the bibliography is absent, and the novelty/probe-provenance boundaries require final tightening.

## Evidence Reviewed

- `writing/p8-manuscript-with-figures.md`
- `results/pos-representation.json`
- `results/pos-task-rows.json`
- `results/pos-representation-summary.json`
- `results/pos-task-summary.json`
- `results/pos-dispersion-summary.json`
- `strong-result-lock.md`
- `figure-table-insertion-audit.md`
- `corrections/pos-task-leaky-probe-v1.json`

No manuscript or evidence file was edited and no experiment was run.

## Scientific Assessment

### Novelty

**6.2/10** The paper correctly presents standard Lloyd quantization, escape coding, multi-hop features and permutation equivariance as ingredients. The contribution is the combined conservative serialization and control protocol for frozen positional messages. This is credible but narrow, and a verified related-work bibliography is essential.

### Soundness

**8.7/10** The formulas are consistent: `H=[X,AX,A^2X,A^3X]`, four-bit nine-symbol alphabet, 32-bit escape payloads, `256/N` codebook amortization, deterministic permutation audit and codec-consistent mismatched-shuffle ratio. The paper does not convert the descriptive fixed-probe gap into a causal hop-reasoning claim.

### Baseline And Evidence

Raw, uniform, Lloyd-only and hybrid comparisons are matched. Hybrid is not presented as universally best; it claims fidelity/storage with bounded paired task loss. Five-seed means, sample SD and paired min/max are reported. The corrected task run and preserved leaky run make the probe repair auditable.

## Numbered Reviewer Concerns

1. **Major — Missing bibliography.** The manuscript uses 31 unique citation keys and calls `references.bib`, but no `.bib` file exists in the run root. Add a verified bibliography and resolve every key.
2. **Medium — Novelty wording.** Keep “combined conversion-level coding/control protocol” explicit; do not imply that Lloyd, escapes or permutation equivariance are new individually.
3. **Medium — Probe provenance.** The prose says fixed weights, splits and normalization are reused, but the raw rows do not include fit-scope, split-index or probe-weight hashes. Link these before final packaging.
4. **Low — Event terminology.** “Hop-event coding” can suggest temporal spikes. Clarify in the title/abstract that “event” means escape/event symbols in the serialized hop code, not temporal SNN events.
5. **Low — Fixed-probe scope.** Preserve the current wording that ordered/shuffled gaps are descriptive order sensitivity, not causal positional reasoning.
6. **Low — Runtime cost boundary.** Retain the explicit exclusion of packet framing, deployment metadata and energy overhead.

## Required Actions

1. Add and verify `references.bib` for all 31 keys.
2. Add provenance hashes for task fit scope and fixed probe reuse.
3. Clarify event terminology and preserve the narrow novelty claim.
4. Keep the paired dispersion and leaky-run negative evidence visible.

**Recommendation:** revise before final paper approval. The scientific core is ready; citation completeness and provenance wording remain.
