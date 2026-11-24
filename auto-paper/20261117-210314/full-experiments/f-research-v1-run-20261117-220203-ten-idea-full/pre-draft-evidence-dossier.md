# Pre-draft evidence dossier

## Portfolio claim

This campaign evaluates ten graph-conversion mechanisms under frozen local protocols. It does not claim that all ten become successful standalone papers. Nine meet their method-specific strong gate; SIGN-C04 is a falsified strong hypothesis.

## Evidence by idea

1. **DYN-C01**: initial+residual coding is lossless. Across five DAVIS splits, decoded accuracy equals raw exactly and repeated-state nonzero events fall 20.52%. Direct probing of the residual coordinates is unstable (−7.53 to +10.96 pp), so the supported claim is lossless coding/cost reduction, not representation-learning superiority. Dynamic-edge GNN evidence is absent.
2. **EQ-C02**: radial events on 8,000 typed MaleCNS coordinates have 3.78% relative error and 2.91e-11 rotation error. Mean balanced accuracy is 25.99% versus 24.35% raw and 24.49% component-uniform. Supported scope is coordinate-event equivariance, not a full E(3) GNN conversion.
3. **PERM-C03**: deterministic graph pooling is permutation-equivariant within 1.11e-16 on Cora/Chameleon/Squirrel×5 permutations; the deliberately order-naive control errs by 0.50–0.95. This is a correctness/system contribution and likely needs integration with a larger conversion method.
4. **SIGN-C04**: exact signed split preserves negative messages, but balanced-accuracy gains over the stronger unsigned control are only 0.46 pp (Chameleon) and 0.48 pp (Squirrel); Cora is slightly negative. The ≥2 pp strong hypothesis fails. Only exact inhibitory-message preservation is supported.
5. **LR-C05**: raw `A X` rank-128 SVD gives 7.32×/8.99×/11.64× compression on Cora/Chameleon/Squirrel and downstream logit errors 3.79–6.20× lower than equal-rank random projection. Strong compression/alignment evidence is present; generic low-rank novelty remains constrained by A²Q/AdaQP.
6. **EDGE-C06**: 6-bit log quantization of 385,946 FlyWire weights achieves 2.82% error and 5.33× bit reduction; error is 83.2% lower than uniform at the same bits. Supported scope is biological weighted-edge message coding, not hardware energy.
7. **CERT-C11**: the proposed affine envelope has 100% empirical coverage on 3 graphs×2 levels, width/RMS 3.06–6.72 and is 79.7–85.1% tighter than the global scalar bound. Supported claim is a useful operator-aware certificate under this quantizer.
8. **POS-C13**: an 8-level Lloyd hop codebook with 0.5% exact escapes reaches 2.46%/3.06% error and 10.17× storage reduction on Chameleon/Squirrel; balanced accuracy improves 2.13/2.20 pp over raw. Generic transformer conversion overlap remains high.
9. **DLY-C14**: delay-aligned residual decoding is exact and repeated-event reduction is 20.52%; the wrong-delay diagnostic error is 4.33%. As with DYN, the evidence is a temporal schedule/causality mechanism rather than dynamic-graph benchmark performance.
10. **READ-C18**: top-two pair readout preserves 100% of full-output argmax decisions over 6 graphs×3 seeds and reduces output slots by a median 63.33%. The claim must include near-margin limitations and does not reduce hidden message work.

## Main limitations

- DYN/DLY share DAVIS evidence and do not yet validate dynamic-edge GNNs.
- EQ lacks a full equivariant GNN teacher/task.
- Several exactness/compression results are method components, not end-to-end SNN energy/accuracy wins.
- SIGN is negative; generic signed-spike prior art is close.
- Local checkpoints/data bound generality; final publication would require broader external benchmarks and direct One-Spike/ASGCN/A²Q/AdaQP/SpikeZIP adaptations.
