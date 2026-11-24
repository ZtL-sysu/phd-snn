# Permutation-Equivariant Hybrid Hop-Event Coding for Frozen Graph Positional Messages

## Abstract

Multi-hop positional messages preserve graph structure but are expensive to communicate in frozen graph-to-spiking conversions. We study a narrow representation-coding problem on Chameleon and Squirrel: concatenate raw node features with one-, two- and three-hop normalized messages, quantize each channel using eight Lloyd centroids plus one escape symbol, and account for four-bit symbols, 32-bit escape payloads and per-channel codebooks. Across five split/probe seeds, hybrid reconstruction error is 3.952% and 4.879%, while the conservative ledger reduces storage by 7.49× and 7.60×. Recomputation after node permutation agrees to `2.22e-16`. A codec-consistent shuffled-hop control, which quantizes globally permuted hop blocks with unchanged ordered-channel codebooks, produces 3.72× and 3.63× mean error ratios. Retrained hybrid probes lose 0.083 percentage points on Chameleon and gain 0.768 points on Squirrel relative to raw features. Fixed raw-trained probes favor ordered over shuffled hybrid representations by 9.57 and 9.08 points. The contribution is a conversion-level multi-hop coding and order-control protocol, not a general graph-transformer-to-SNN method.

## 1 Introduction

Graph positional information often appears as multi-hop propagation of features or structural identifiers. Concatenating hop-wise messages increases feature width and communication cost, while simple global quantization can distort channel distributions and rare values. Frozen conversion settings make the problem more specific: the graph representation is fixed, and the goal is to serialize a positional message without changing its node-permutation behavior.

Compression error alone is not sufficient evidence. A useful study must also show whether the canonical hop order matters, whether the representation is equivariant to node relabeling, and whether downstream predictions survive without representation-specific retraining. These controls distinguish a structured hop code from a generic high-dimensional quantizer.

This paper evaluates the representation

\\[
H = [X, AX, A^2X, A^3X],
\\]

where `A` is a row-normalized graph operator. Each channel is encoded with eight Lloyd centroids and one escape symbol. Escaped values are stored exactly as float32 payloads. The serialization cost is deliberately conservative:

\\[
b_{\\mathrm{avg}} = 4 + 32 f_{\\mathrm{escape}} + \\frac{256}{N},
\\]

where four bits encode one of eight centroid identifiers or the escape marker, `f_escape` is the escaped fraction, and `256/N` amortizes eight float32 centroids over `N` nodes.

The central question is whether this hybrid code preserves ordered multi-hop messages at useful storage reduction while remaining node-permutation equivariant and sensitive to hop order. We answer this within two static graphs and explicitly separate three forms of evidence: representation fidelity/storage, retrained linear-probe performance, and fixed raw-probe ordered/shuffled controls.

## 2 Related Work

Positional encodings and graph transformers represent structure through random walks, Laplacian eigenvectors, distances, hop features or attention biases \\cite{vaswani2017attention,dwivedi2021graph,kreuzer2021rethinking,bouritsas2023transformers,li2023graphpos}. These methods motivate the importance of ordered structural channels, but they do not provide the exact serialization ledger evaluated here.

Graph-model compression studies degree-aware quantization, vector-quantized node representations, aggregation-aware mixed precision and communication compression \\cite{tailor2021degreequant,ding2021vqgnn,wang2022qgtc,zhu2023a2q,wan2023adaqp,gholami2022quantization,jacob2018quantization,nagel2021white}. Our method uses standard Lloyd centroids and exact escapes; the contribution is their combined hop-message accounting and order controls, not a new general quantizer.

ANN-to-SNN conversion work addresses output codes, offsets, grouped neurons, early exit and transformer conversion \\cite{one-spike,hao2023offset,lv2024group,bu2023optimal,li2023seenn,hu2023fast,zhao2025ttfs,huang2025ecmt,li2024erroraware}. Spiking graph models address spiking graph convolution, dynamic graphs and graph transformers \\cite{spikinggcn,spikenet,dy-sign,delay-dsgn,signnn,sun2024spikegraphormer,zhang2025sgnnbench}. These systems are adjacent context; the present paper does not train a spiking graph transformer or measure temporal energy.

The differentiation is therefore narrow. The work combines multi-hop positional messages, a conservative codebook/escape format, exact node-permutation recomputation and a non-tautological codebook-order mismatch control for frozen graph representations. It does not claim a new positional encoding, a direct graph-transformer conversion result or broad SNN superiority.

## 3 Method

### 3.1 Multi-hop representation

For node features `X∈R^(N×F)` and row-normalized adjacency `A∈R^(N×N)`, the ordered representation is

\\[
H = [X, AX, A^2X, A^3X] \\in \\mathbb{R}^{N\\times 4F}.
\\]

The four blocks retain hop position. The task experiments use labeled nodes only; representation, bit and permutation audits use all graph nodes.

### 3.2 Hybrid Lloyd/escape encoding

For each channel, Lloyd quantization estimates eight centroids. Every value receives one four-bit symbol: one of eight centroid identifiers or an escape marker. Escaped values retain a 32-bit float payload. Each channel stores eight float32 centroids.

For representation rows, codebooks are fitted on all nodes and the largest reconstruction errors are escaped using a threshold and every tied value, avoiding row-order-dependent top-k selection. For task rows, codebooks and escape thresholds are fitted on training nodes only and reused unchanged on validation and test nodes. Escapes are selected at the source encoder; labels and test logits are never used.

The exact average ledger is

\\[
b_{\\mathrm{avg}} = 4 + 32 f_{\\mathrm{escape}} + \\frac{256}{N}.
\\]

Raw float32 uses 32 bits/value. The eight-centroid Lloyd baseline uses three-bit symbols and `256/N` codebook overhead. Uniform 8-level coding uses three-bit symbols plus two float32 range endpoints per channel.

### 3.3 Permutation and shuffled-hop controls

For node permutation `P`, features, adjacency and labels are permuted consistently, `H` and the hybrid code are recomputed, and the reconstruction is inverse-permuted before comparison. Deterministic sorted Lloyd fitting and threshold-plus-ties escape selection make the audit invariant to row order.

The shuffled-hop control uses one non-identity global permutation `S` of the four hop blocks. Ordered codebooks are fitted on `H`; the shuffled raw target `S H` is quantized with the same codebooks and the same escape-fraction policy. The error ratio is

\\[
\\rho_S = \\frac{\\|S H - Q_{\\mathrm{ord}}(S H)\\|_F/\\|S H\\|_F}{\\|H-Q_{\\mathrm{ord}}(H)\\|_F/\\|H\\|_F}.
\\]

This compares the same codec family and does not shuffle target and reconstruction together. Five shuffle seeds are aggregated as a graph-level mean; every individual row is retained.

### 3.4 Task probes

Two probe protocols are separated. The retrained protocol fits one linear probe per method, graph and split seed. The fixed protocol fits one raw-feature probe and reuses its weights, normalization, split and test nodes for raw, uniform, Lloyd, hybrid-ordered and hybrid-shuffled representations. Training uses split-train indices, epoch selection uses validation, and final metrics use test indices only.

![Hybrid multi-hop event coding](figures/figure1-hop-coding.png)

**Figure 1.** Ordered multi-hop construction and hybrid codebook/escape serialization. The right panel shows the exact symbol, payload and amortized codebook ledger.

## 4 Experiments and Results

### 4.1 Experimental matrix

Chameleon and Squirrel are evaluated with split/probe seeds 600-604 \\cite{pei2020geomgnn,platonov2023heterophily}. The accepted matrix contains four retrained methods per seed, one fixed raw probe with five ordered methods and five shuffled controls per seed, and separate representation/permutation audits.

| Quantity | Definition | Role |
|---|---|---|
| Hybrid | eight Lloyd centroids + escape | proposed code |
| Uniform | global 8-level rounding | simple baseline |
| Lloyd | eight centroids, no escapes | codebook-only baseline |
| Raw | float32 message | reference |
| `B_avg` | `4+32f_escape+256/N` | conservative proposed ledger |
| `ρ_S` | ordered-codebook shuffled/ordered error | order-mismatch diagnostic |

**Table 1.** Methods, controls and exact accounting.

### 4.2 Representation fidelity and storage

Hybrid reconstruction error is 3.952% on Chameleon and 4.879% on Squirrel. The actual escape fractions are approximately 0.5%, and the conservative average costs are 4.272 and 4.209 bits/value. Storage reductions are 7.490× and 7.602×. Both fidelity and storage satisfy the binding gates.

The uniform and Lloyd-only rows show that the hybrid's contribution is not raw compression alone. The exact escapes reduce tail error while the codebook overhead and escape symbols remain visible in the ledger.

![Representation fidelity, storage and task trade-off](figures/figure2-method-tradeoff.png)

**Figure 2.** Representation error, conservative storage and retrained balanced accuracy across methods. Task results are paired five-seed summaries; lower error and lower storage are better, while accuracy direction depends on the comparison.

### 4.3 Permutation and shuffled-hop controls

Raw and hybrid inverse-permutation errors are `2.22e-16`, below the `1e-10` gate. The earlier top-k escape implementation was row-order-sensitive; threshold-plus-all-ties selection removed that defect.

All five shuffle seeds per graph are non-identity. Under the codec-consistent ordered-codebook control, mean error ratios are 3.725× on Chameleon and 3.626× on Squirrel, with a minimum of 3.310×. Thus the strong ratio gate passes without comparing different codec families.

![Permutation and shuffled-hop controls](figures/figure3-order-controls.png)

**Figure 3.** Node-permutation errors and codec-consistent shuffled-hop ratios. Points show every permutation/shuffle seed; dashed lines mark the `1e-10` and `1.25×` gates.

### 4.4 Five-seed task results

| Graph | Raw BA mean±SD | Hybrid BA mean±SD | Paired hybrid−raw pp mean±SD | Min/max pp |
|---|---:|---:|---:|---:|
| Chameleon | 62.88±2.97 | 62.80±1.86 | −0.08±1.20 | −1.28 / +1.69 |
| Squirrel | 45.99±0.84 | 46.76±0.48 | +0.77±1.02 | −0.49 / +2.21 |

**Table 2.** Retrained paired balanced accuracy. Hybrid loss is 0.083 pp on Chameleon and a 0.768 pp gain on Squirrel, both inside the ≤2 pp loss gate. The mixed paired differences are reported rather than collapsed into a universal gain.

For fixed raw probes, ordered hybrid balanced accuracy is 62.99±2.66% on Chameleon and 45.49±0.82% on Squirrel. Shuffled hybrid means are 53.43±7.67% and 36.41±7.23%, giving ordered-minus-shuffled gaps of 9.57 and 9.08 pp. These gaps are descriptive order-sensitivity evidence, not proof of causal positional reasoning.

### 4.5 Leakage audit and negative evidence

The first task implementation fitted probes on all labels and produced implausibly high accuracy near 99%. That run is preserved but excluded. The corrected implementation trains only on split-train indices, selects checkpoints on validation and evaluates once on test. Representation values are unchanged, while task accuracies fall to the accepted range above. No accepted row depends on the leaky run.

## 5 Discussion

The evidence supports three scoped statements. First, the conservative hybrid format preserves the tested multi-hop representation with 3.95–4.88% error and 7.49–7.60× storage reduction. Second, node permutation is reproduced to machine precision after deterministic codebook and escape handling. Third, ordered codebooks degrade under non-identity hop-block mismatch, and fixed raw probes prefer ordered over shuffled hybrid features.

The method does not establish that hop order causes a particular graph-transformer computation. Fixed probes show compatibility with the raw ordering, while mismatched-codebook error measures channel-order sensitivity. Retrained probes can compensate for some transformations, and their mixed accuracy differences should not be promoted to general task superiority.

The conservative ledger includes symbol, escape payload and centroid costs, but deployment metadata, packet framing and runtime energy may add overhead. The study uses two heterophilic graphs and five probe seeds. It does not include a complete graph-transformer model, temporal spikes, dynamic graphs, adversarial perturbations or hardware measurements.

The prior-art overlap is substantial because Lloyd quantization, exact escapes and permutation equivariance are established ingredients. The contribution is the combined frozen positional-message format and its paired order controls. A stronger future claim would require real graph-transformer-to-SNN conversion, broader graph families and energy-aware event timing.

## 6 Conclusion

Hybrid hop-event coding preserves ordered multi-hop graph messages at substantially lower conservative storage in the tested frozen setting. All binding representation, storage, permutation and shuffled-hop gates pass. Five-seed retrained task loss is bounded, and fixed raw probes show clear ordered-versus-shuffled gaps. The result is a scoped conversion-level message-coding study, not a general graph-transformer-to-SNN or temporal SNN claim.

## References

BibTeX source: `references.bib`.

\\bibliography{references}
