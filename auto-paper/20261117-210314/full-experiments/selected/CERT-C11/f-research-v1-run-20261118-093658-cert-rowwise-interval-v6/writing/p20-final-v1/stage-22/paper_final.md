# Rowwise Layerwise Interval Certificates for Quantized Messages in Frozen Two-Layer GNN-to-SNN Conversion

## Abstract

Finite-precision message transport can change the final logits of a frozen graph neural network along a conversion path. We study a narrow but auditable certificate for one exact frozen two-layer graph-convolution chain. A rowwise uniform quantizer assigns each node a deterministic half-step error radius; these radii are propagated through two normalized-adjacency operations, a non-expansive ReLU, and the frozen downstream weight matrix. The resulting interval is compared with a valid norm upper bound and a matched global-radius outputwise ablation. Across Cora, Chameleon and Squirrel, three frozen checkpoint seeds, 4/8 quantization levels, and global/rowwise uniform quantizers, all 36 measured final-logit errors are contained and all proposed bounds are analytically no looser than the norm comparator. The 18 global-uniform cells provide an equality control. In the 18 rowwise cells, the proposed interval reduces median bound width relative to the matched global-radius ablation by 74.26% to 82.12%, with a standard median tightening of 79.65%. Absolute width relative to realized RMS error remains large, with a median of 30.68 and a maximum of 36.91. The supported contribution is therefore deterministic final-logit containment plus relative tightening over a matched radius-granularity ablation, not statistical coverage, broad SNN superiority, robustness, or an absolute-width guarantee.

## 1 Introduction

Finite-precision conversion of a frozen graph neural network changes the numerical path from input features to output logits. Quantized messages are aggregated by the graph operator, passed through nonlinearities, aggregated again, and transformed by frozen downstream weights. A small elementwise message error can therefore be amplified by graph connectivity and weight magnitude. Generic quantization metrics such as bit count, message error, or average task accuracy do not tell a user whether the final logits remain inside a computable worst-case envelope.

Interval and norm bounds offer a natural certificate language, but their usefulness depends on preserving the structure of the actual operator chain. A scalar global norm bound is easy to state but can merge all nodes, hidden channels, and output classes into a single loose radius. Conversely, a bound estimated from observed errors can become tautological if the same errors are used to construct the certificate. For frozen conversion, a useful target is a deterministic bound whose radius comes from the quantizer definition, not labels, logits, or realized residuals.

This paper examines the exact chain

\\[
M=XW_0,\\qquad \\widehat M=Q_{\\mathrm{row}}(M),\\qquad
H=\\operatorname{relu}(AM+b_0),\\qquad
Z=AHW_1+b_{\\mathrm{out}},
\\]

and its quantized counterpart. Each row of \\(M\\) is quantized with a rowwise uniform lattice. The quantizer step determines a half-step radius before any actual error is inspected. ReLU non-expansiveness and two applications of the normalized adjacency operator yield a componentwise interval for the final logits.

The main question is: can this rowwise deterministic interval contain every measured final-logit error while materially tightening a matched global-radius ablation? We answer this question within a fixed frozen two-layer GCN scope. The empirical contribution is relative tightening under deterministic containment. We explicitly do not claim that the absolute worst-case width is small.

The remainder of the paper is organized as follows. Section 2 relates the study to graph-message quantization, frozen ANN-to-SNN conversion, and interval certificates. Section 3 defines the exact computation, quantizer, bounds and numerical policy. Section 4 reports the complete 36-cell matrix and its negative width evidence. Section 5 separates analytic validity from empirical utility and states limitations. Section 6 concludes.

## 2 Related Work

Frozen ANN-to-SNN conversion studies accuracy-latency trade-offs, offset correction, grouped neurons, early exit, quantized conversion, transformer conversion and post-training calibration \\cite{one-spike,hao2023offset,lv2024group,bu2023optimal,li2023seenn,hu2023fast,you2024spikezip,zhao2025ttfs,huang2025ecmt,li2024erroraware}. These works address temporal rate conversion or output representation, but they do not provide the rowwise final-logit interval studied here. Broader SNN learning surveys distinguish conversion from direct spike-based training and clarify temporal assumptions \\cite{dampfhoffer2023snnlearning,nunes2022snnsurvey,wang2022taxonomicsnn}.

Graph-model compression changes what message is communicated or stored. Degree-aware and graph-aware quantization, vector-quantized node representations, tensor-oriented quantized execution, generic low-rank neural compression, and mixed-precision message compression provide important cost and codebook baselines \\cite{tailor2021degreequant,ding2021vqgnn,wang2022qgtc,zhu2023a2q,wan2023adaqp,cherukuri2025lowrank,gholami2022quantization,jacob2018quantization,nagel2021white}. These methods optimize quantization or execution; the present work instead certifies the final-logit effect of a fixed rowwise lattice.

Spiking graph models directly address spiking graph convolution, dynamic graphs, delayed evolution, compact graph representations and graph attention \\cite{spikinggcn,spikenet,dy-sign,delay-dsgn,signnn,msg,li2023graph1bit,chaurasia2026sgspose,sun2024spikegraphormer,zhang2025sgnnbench}. Asynchronous event-based processing provides additional context \\cite{asgcn}. Their published outcomes are not direct matched comparisons for the exact frozen two-layer chain used in this paper. We therefore treat them as domain context rather than state-of-the-art baselines.

Interval bound propagation and ReLU network verification supply the mathematical ingredients \\cite{gowal2018ibp,wong2018provable,mirman2018diffai,katz2017reluplex}. Componentwise ReLU is non-expansive, and interval arithmetic propagates local coordinate radii through affine maps. The application-specific step here is to retain the two graph-operator magnitudes and the rowwise message radius before applying the frozen output weight. Nearby conversion-error work studies corrections and temporal/output behavior \\cite{li2024erroraware,huang2025ecmt}; it does not establish the deterministic finite-precision message certificate evaluated here.

The differentiation is therefore narrow: interval propagation itself is standard; the application-specific contribution is retaining rowwise message radii through two graph operators and isolating their effect with a matched global-radius ablation. We do not claim a new general interval theorem or broad SNN robustness.

## 3 Method

### 3.1 Frozen graph computation

Let \\(X\\in\\mathbb R^{N\\times F}\\) be the node-feature matrix and \\(A\\in\\mathbb R^{N\\times N}\\) the normalized adjacency matrix. The frozen first-layer matrix and bias are \\(W_0\\in\\mathbb R^{F\\times H}\\) and \\(b_0\\in\\mathbb R^H\\). The hidden-width message is \\(M=XW_0\\in\\mathbb R^{N\\times H}\\). The frozen output matrix and bias are \\(W_1\\in\\mathbb R^{H\\times C}\\) and \\(b_{\\mathrm{out}}\\in\\mathbb R^C\\). All nine frozen model snapshots have \\(H=16\\); their tensor shapes are recorded in `results/model-shapes.json` and linked to model hashes in the run provenance. The reference logits are

\\[
Z=A\\operatorname{relu}(AM+b_0)W_1+b_{\\mathrm{out}}.
\\]

Stored graph and model snapshots are float32, but all quantized values, dequantized values, reconstructions and certificate arithmetic are evaluated in float64. This removes an unmodelled float32 reconstruction term from the radius.

### 3.2 Rowwise uniform quantizer

For node \\(i\\), let \\(m_i=\\min_h M_{ih}\\) and \\(r_i=\\max_h M_{ih}\\). For \\(L\\in\\{4,8\\}\\) levels, the step is

\\[
s_i=\\frac{r_i-m_i}{L-1}.
\\]

Rounding uses \\(\\lfloor (M_{ih}-m_i)/s_i+0.5\\rfloor\\), so ties move upward. Minima and maxima are represented exactly. If \\(s_i=0\\), row \\(i\\) is copied exactly and receives zero radius. Endpoint clipping is only a safeguard; an out-of-range source value beyond tolerance fails the cell. The deterministic radius matrix is

\\[
\\Delta_{ih}=s_i/2.
\\]

It is computed from the quantizer range before actual errors are inspected. No label, logits, realized residual or held-out error is used to set \\(\\Delta\\).

### 3.3 Layerwise interval certificate

Let \\(E=M-\\widehat M\\). Componentwise ReLU satisfies

\\[
|\\operatorname{relu}(x)-\\operatorname{relu}(y)|\\le |x-y|.
\\]

Because \\(|E|\\le\\Delta\\), the first aggregation and nonlinearity give

\\[
|H-\\widehat H|\\le |A|\\Delta.
\\]

The second aggregation and frozen weight give the proposed absolute interval

\\[
B_{\\mathrm{abs}}=|A||A|\\Delta|W_1|.
\\]

Every measured error satisfies \\(|Z-\\widehat Z|\\le B_{\\mathrm{abs}}\\) if the implementation and quantizer radius are correct. Containment is therefore a theorem/implementation audit, not an estimated coverage probability.

### 3.4 Comparators and numerical policy

Let \\(G=|A||A|\\), \\(c=G\\mathbf 1\\), and \\(\\Delta_{i,:}\\) denote row \\(i\\) of the radius matrix. We report three additional quantities:

\\[
B_{\\mathrm{mink}}[i,k]
=\\left(\\sum_q G_{iq}\\|\\Delta_{q,:}\\|_2\\right)\\|W_{1,:,k}\\|_2,
\\]

\\[
B_{\\mathrm{global}}[i,k]
=c_i\\max(\\Delta)\\|W_{1,:,k}\\|_1,
\\]

and a collapsed full-matrix scalar reference. \\(B_{\\mathrm{mink}}\\) is a valid norm upper comparator; its ordering relative to \\(B_{\\mathrm{abs}}\\) is analytic and is not counted as an empirical improvement. \\(B_{\\mathrm{global}}\\) is a matched global-radius ablation, not a state-of-the-art compression baseline. Global-uniform quantization makes \\(\\Delta\\) constant and therefore yields \\(B_{\\mathrm{abs}}=B_{\\mathrm{global}}\\) as a structural equality control.

For each cell, actual RMS is computed over all \\(N\\times C\\) final-logit errors. Width/RMS is the median of all bound entries divided by this RMS. Per-cell tightening is

\\[
1-\\frac{\\operatorname{median}(B_{\\mathrm{abs}})/\\mathrm{RMS}}
{\\operatorname{median}(B_{\\mathrm{global}})/\\mathrm{RMS}}.
\\]

Elementwise comparisons use \\(v\\le b+10^{-10}+10^{-12}|b|\\). NaN or infinity fails the row. If RMS is zero, zero ratio is allowed only when the corresponding median bound is also zero. All rows and diagnostics are retained.

![Exact rowwise interval certificate chain](figures/data/figure1-certificate-chain.png)

**Figure 1.** Exact rowwise interval certificate chain. Rowwise uniform radii are set before error inspection, propagated through both normalized-adjacency operations and ReLU, and transformed by the frozen output weight.

## 4 Experiments and Results

### 4.1 Experimental matrix

We evaluate Cora, Chameleon and Squirrel with frozen two-layer hidden-16 GCN checkpoints at seeds 0, 1 and 2 \\cite{yang2016planetoid,pei2020geomgnn,platonov2023heterophily}. The fixed matrix contains three graphs, three seeds, two levels and two quantizers, for 36 cells. Global-uniform quantization is the constant-radius control; rowwise uniform quantization supplies the proposed variable-radius condition. The certificate uses no labels or data splits. Dataset and model snapshots, code and outputs are hash-tracked.

| Bound or control | Exact definition | Role |
|---|---|---|
| \\(B_{\\mathrm{abs}}\\) | \\(\\sum_q G_{iq}\\sum_h\\Delta_{qh}|W_{1,hk}|\\), where \\(G=|A||A|\\) | proposed deterministic interval |
| \\(B_{\\mathrm{mink}}\\) | \\(\\left(\\sum_q G_{iq}\\|\\Delta_{q,:}\\|_2\\right)\\|W_{1,:,k}\\|_2\\) | valid analytic upper comparator |
| \\(B_{\\mathrm{global}}\\) | \\(c_i\\max(\\Delta)\\|W_{1,:,k}\\|_1\\), where \\(c_i=\\sum_qG_{iq}\\) | matched global-radius ablation |
| Scalar reference | \\(c_i\\max(\\Delta)\\|W_1\\|_{1,1}\\) | deliberately loose context |

**Table 1.** Bounds and roles. Analytic ordering is separated from empirical tightening.

### 4.2 Deterministic containment and comparator validity

All 36 measured final-logit errors lie within \\(B_{\\mathrm{abs}}\\), and all 36 proposed bounds satisfy \\(B_{\\mathrm{abs}}\\le B_{\\mathrm{mink}}\\) under the fixed tolerance. No cell contains NaN or infinity. The largest actual-minus-proposed excess is negative in every row, so no observed error crosses the certificate. These findings validate the deterministic derivation and its implementation; they are not statistical coverage estimates.

### 4.3 Radius-granularity ablation

The 18 global-uniform cells satisfy the expected equality control: \\(B_{\\mathrm{abs}}=B_{\\mathrm{global}}\\) within tolerance, and tightening is zero up to numerical precision. This equality confirms that the rowwise gain does not arise from comparing different formulas under constant radius.

In all 18 rowwise cells, the proposed interval is tighter than the matched global-radius ablation. Tightening ranges from 74.26% to 82.12%, with a standard median of 79.65%. The effect is consistent across graph, checkpoint seed and 4/8-level conditions. Figure 2 shows per-cell width/RMS and tightening; Figure 3 uses the same frozen rows to show the global equality control and rowwise tightening distribution.

![Width and tightening across the 36-cell matrix](figures/data/figure2-width-tightening.png)

**Figure 2.** Descriptive width/RMS and relative tightening across all cells. Lower width/RMS is visually better, but no absolute width threshold is claimed.

![Global equality and rowwise tightening](figures/data/figure3-equality-tightening.png)

**Figure 3.** Global-uniform equality control and rowwise tightening distribution. The plotted values are exported directly from the frozen 36-row result.

### 4.4 Absolute width is a negative result

Worst-case interval width relative to realized RMS is large. For rowwise quantization, width/RMS has a standard median of 30.68 and a maximum of 36.91. The global-uniform condition also ranges above ten in several cells. This negative evidence rejects an absolute-width claim. The result is instead a relative one: rowwise radii substantially tighten a matched global-radius envelope while retaining deterministic containment.

### 4.5 Failure audit

The run contains zero clipping events and zero non-finite rows. Constant rows receive identity reconstruction and zero radius. Every row records dataset, seed, level, quantizer and radius hash. The complete raw table is retained; no failed or unfavorable cell is omitted. The main empirical improvement is the rowwise tightening distribution, while absolute width remains an explicit limitation.

**Table 2. Complete 36-cell certificate summary.** `Yes` denotes deterministic containment or analytic comparator ordering. Global equality is a structural control; rowwise tightening is versus the matched global-radius ablation.

| Graph | Seed | Levels | Quantizer | Contained | $B_{abs}\\leq B_{mink}$ | Global equality | Width/RMS | Tightening (%) |
|---|---:|---:|---|---|---|---|---:|---:|
| chameleon | 0 | 4 | global | Yes | Yes | Yes | 19.73 | 0.00 |
| chameleon | 0 | 4 | rowwise | Yes | Yes | N/A | 27.66 | 81.36 |
| chameleon | 0 | 8 | global | Yes | Yes | Yes | 23.30 | 0.00 |
| chameleon | 0 | 8 | rowwise | Yes | Yes | N/A | 30.91 | 81.36 |
| chameleon | 1 | 4 | global | Yes | Yes | Yes | 20.33 | 0.00 |
| chameleon | 1 | 4 | rowwise | Yes | Yes | N/A | 30.65 | 78.55 |
| chameleon | 1 | 8 | global | Yes | Yes | Yes | 27.41 | 0.00 |
| chameleon | 1 | 8 | rowwise | Yes | Yes | N/A | 33.55 | 78.55 |
| chameleon | 2 | 4 | global | Yes | Yes | Yes | 19.42 | 0.00 |
| chameleon | 2 | 4 | rowwise | Yes | Yes | N/A | 30.71 | 79.65 |
| chameleon | 2 | 8 | global | Yes | Yes | Yes | 25.39 | 0.00 |
| chameleon | 2 | 8 | rowwise | Yes | Yes | N/A | 36.52 | 79.65 |
| cora | 0 | 4 | global | Yes | Yes | Yes | 9.99 | 0.00 |
| cora | 0 | 4 | rowwise | Yes | Yes | N/A | 15.84 | 80.97 |
| cora | 0 | 8 | global | Yes | Yes | Yes | 14.49 | 0.00 |
| cora | 0 | 8 | rowwise | Yes | Yes | N/A | 16.55 | 80.97 |
| cora | 1 | 4 | global | Yes | Yes | Yes | 7.26 | 0.00 |
| cora | 1 | 4 | rowwise | Yes | Yes | N/A | 15.49 | 74.26 |
| cora | 1 | 8 | global | Yes | Yes | Yes | 14.21 | 0.00 |
| cora | 1 | 8 | rowwise | Yes | Yes | N/A | 16.83 | 74.26 |
| cora | 2 | 4 | global | Yes | Yes | Yes | 8.43 | 0.00 |
| cora | 2 | 4 | rowwise | Yes | Yes | N/A | 15.44 | 82.12 |
| cora | 2 | 8 | global | Yes | Yes | Yes | 12.45 | 0.00 |
| cora | 2 | 8 | rowwise | Yes | Yes | N/A | 16.77 | 82.12 |
| squirrel | 0 | 4 | global | Yes | Yes | Yes | 12.53 | 0.00 |
| squirrel | 0 | 4 | rowwise | Yes | Yes | N/A | 34.89 | 78.38 |
| squirrel | 0 | 8 | global | Yes | Yes | Yes | 28.30 | 0.00 |
| squirrel | 0 | 8 | rowwise | Yes | Yes | N/A | 36.91 | 78.38 |
| squirrel | 1 | 4 | global | Yes | Yes | Yes | 21.75 | 0.00 |
| squirrel | 1 | 4 | rowwise | Yes | Yes | N/A | 36.28 | 76.14 |
| squirrel | 1 | 8 | global | Yes | Yes | Yes | 29.05 | 0.00 |
| squirrel | 1 | 8 | rowwise | Yes | Yes | N/A | 36.76 | 76.14 |
| squirrel | 2 | 4 | global | Yes | Yes | Yes | 20.81 | 0.00 |
| squirrel | 2 | 4 | rowwise | Yes | Yes | N/A | 30.61 | 79.96 |
| squirrel | 2 | 8 | global | Yes | Yes | Yes | 33.85 | 0.00 |
| squirrel | 2 | 8 | rowwise | Yes | Yes | N/A | 34.07 | 79.96 |

## 5 Discussion

The experiment separates three logically different statements. First, the interval derivation and implementation yield deterministic containment for the specified chain. Second, the inequality \\(B_{\\mathrm{abs}}\\le B_{\\mathrm{mink}}\\) follows from norm ordering and serves as a validity check. Third, rowwise radius granularity produces an empirical 74.26% to 82.12% tightening over the matched global-radius ablation. Combining these statements into a generic “certified SNN improvement” would overstate the evidence.

The rowwise choice is appropriate for the tested message matrices because the quantizer range varies substantially across nodes. It is not claimed to dominate per-channel, learned, vector, or codebook quantizers. Those alternatives can reduce reconstruction error or adapt to data distributions, but they require different radius and cost assumptions. The present study holds the lattice family fixed to isolate the certificate effect of radius granularity.

The high absolute width/RMS is retained as negative evidence. It arises because a worst-case independent-coordinate interval allows all local errors to align adversarially, whereas realized quantization errors and graph paths partially cancel. A smaller absolute certificate may require distributional assumptions, calibration with independent data, correlation-aware bounds, or a multilayer abstraction. Such extensions would no longer be the deterministic unconditional certificate studied here.

The scope is limited to frozen two-layer hidden-16 GCN checkpoints on three static graphs and three seeds. The work does not measure temporal spikes, hardware energy, adversarial robustness, uncertainty calibration, learned quantizers, dynamic graphs, or multilayer nonlinear conversion. The global comparator is a matched radius-granularity ablation rather than a broad state-of-the-art baseline. Accordingly, the results support a narrow verification method and a controlled radius-granularity finding.

## 6 Conclusion

For the exact frozen two-layer chain studied in this paper, rowwise uniform message radii can be propagated through two normalized-adjacency operations, ReLU and the frozen output weight to form a deterministic final-logit interval. All 36 tested graph/seed/level/quantizer cells are contained, and the proposed interval is analytically no looser than a valid norm comparator. Global-uniform quantization provides an exact equality control. Rowwise radii tighten the matched global-radius ablation by 74.26% to 82.12%, with a median of 79.65%.

The result does not establish small absolute certificate width: rowwise width/RMS has a median of 30.68 and a maximum of 36.91. The supported contribution is therefore deterministic final-logit containment plus relative tightening over a matched global-radius ablation. Future work must address correlation-aware or multilayer bounds before claiming smaller absolute error envelopes or broader GNN-to-SNN robustness.

## References

BibTeX source: `references.bib`.

\\bibliography{references}

