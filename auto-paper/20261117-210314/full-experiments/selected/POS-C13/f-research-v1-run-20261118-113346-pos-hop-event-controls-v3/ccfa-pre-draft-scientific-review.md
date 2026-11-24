# CCFA Pre-Draft Scientific Review

review_execution: independent-agent

## Verdict

**PROCEED**

**Score: 7.8/10**  
**Confidence: medium-high**

The POS-C13 package supports a narrow but coherent representation-coding and control study. The method is technically sound, the negative evidence is preserved, and the claims remain within a frozen positional-message scope. The contribution is application-specific rather than a new general quantizer or graph-transformer-to-SNN result.

## Evidence Reviewed

- `pre-draft-evidence-dossier.md`
- `results/pos-representation.json`
- `results/pos-task-rows.json`
- `results/pos-representation-summary.json`
- `results/pos-task-summary.json`
- `strong-result-lock.md`
- `experiment-traceability.md`
- `corrections/pos-task-leaky-probe-v1.json`

No experiment was run and no evidence was modified.

## Scientific Assessment

### Novelty

**6.2/10** Lloyd codebooks, escape coding, multi-hop features and permutation equivariance are established ingredients. The defensible novelty is their combined serialization and control protocol for frozen graph positional messages: exact conservative bit accounting, training-only task fitting, node-permutation audit, and ordered-codebook mismatched-shuffle testing.

### Soundness

**8.8/10** The representation, quantizer, bit ledger and controls are coherent. The mismatched-shuffle result measures codebook-order compatibility; the fixed raw probe adds descriptive task-level order sensitivity without being promoted to a causal claim.

### Baseline Fairness

**8.2/10** Raw, uniform, Lloyd-only and hybrid methods share the same representation and task protocol. Hybrid is not claimed to be the best accuracy method; it claims bounded loss versus raw while reducing storage. The fixed raw probe is appropriately separated from retrained probes.

### Evidence Strength

- Hybrid errors: 3.95% and 4.88%.
- Conservative storage: 7.49x and 7.60x.
- Permutation error: `2.22e-16`.
- Mismatched-shuffle means: 3.72x and 3.63x.
- Retrained hybrid loss: 0.083 pp on Chameleon and a 0.768 pp gain on Squirrel.
- Fixed-probe ordered/shuffled gap: 9.57 pp and 9.08 pp.

The five-seed results support task retention and descriptive order sensitivity. They do not establish broad transformer conversion, energy savings or deployment performance.

## Claim Scope

The dossier correctly distinguishes:

- deterministic permutation audit from novel equivariance theory;
- codebook mismatch from causal hop reasoning;
- fixed-probe transfer from retrained-probe performance;
- conservative serialization cost from full deployment runtime metadata;
- two-graph evidence from broad graph-transformer generality.

## Planned Figures

- **Figure 1:** supported by the exact hop construction and escape serialization.
- **Figure 2:** error, storage and retrained accuracy rows are available; avoid implying accuracy superiority.
- **Figure 3:** permutation and shuffle controls are supported; label the shuffle as ordered-codebook mismatch and fixed-probe gaps as descriptive.
- **Table 1:** bit ledger and method definitions are complete.
- **Table 2:** 40 task rows and 90 fixed-probe rows support a complete seed/control table.

## Reviewer Risks

1. Standard quantization ingredients may limit novelty.
2. Two graphs and five seeds do not support broad generality.
3. No real graph-transformer-to-SNN, spike, energy or hardware system is tested.
4. Mismatched-shuffle error is order sensitivity, not proof of positional reasoning.
5. The bit ledger excludes deployment metadata outside symbol/payload/codebook costs.

**Recommendation:** proceed to drafting with these boundaries and a verified related-work comparison.
