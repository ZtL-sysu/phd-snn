# Magnitude-Weighted Output-Jacobian Residual Coding of \(M_0=\hat{A}X\) for Matched-Budget GNN-to-SNN Logit Fidelity

## Abstract

Frozen GNN-to-SNN conversion can require repeated transport of the first-layer input message \(M_0=\hat{A}X\). Under a fixed serialization budget, low-rank coding may omit residual directions that matter to the frozen model's logits. We therefore ask whether magnitude-weighted output-Jacobian allocation of sparse exact residual coefficients improves logit fidelity at matched total padded serialized bits while limiting observed task degradation. On the reported test split, rank-128 transport with a 2% residual budget reduced the ratio of three-seed mean split-specific logit MSE relative to the strongest evaluated matched-budget residual control by 26.23%, 33.99%, and 25.83% on Cora, Chameleon, and Squirrel; all nine dataset-seed comparisons improved. Against our matched-budget A2Q-style and One-Spike-style adaptations, the reductions were 28.93%, 36.19%, and 35.24%, and 42.83%, 47.61%, and 34.03%, respectively. Across \(T=2/4\) accuracy and teacher agreement, the maximum observed three-seed-mean degradation was 1.86 percentage points and the maximum seed-level degradation was 2.85 percentage points relative to the best matched-budget non-proposed control for each dataset and task metric. These are descriptive maxima, not equivalence results or population bounds. Compared methods used identical total padded serialized bits within each dataset at rank 128 and 2%. A separate rank128/1% warmed benchmark measured paired p95 full-pipeline runtime ratios of 1.020-1.124 versus SVD-only and peak CUDA allocation of 218.23 MB; it measures wall-clock cost, not energy or focal 2% timing. The evidence is held-out confirmation after validation-exposed setting selection, not preregistered or independent replication, and the contribution is limited to logit-fidelity coding of \(M_0=\hat{A}X\).

## 1 Introduction

Frozen GNN-to-SNN compression repeatedly transports high-dimensional first-layer graph messages. Low-rank transport can preserve large message components while omitting residual directions that influence the frozen model's outputs. This creates a specific output-sensitive coding problem: under a fixed serialization budget, which sparse residual coefficients should be retained to improve logit fidelity without exceeding the transport cost?

We study this question for the transported input message \(M_0=\hat{A}X\) only. The evaluated method retains an operator-aligned rank-128 basis and allocates a 2% sparse residual budget using the composite score \(s_i=r_i^2\lVert J_i\rVert_2^2\), where \(r_i\) is the residual coefficient and \(J_i\) is the analytic derivative of the frozen ANN logits with respect to the corresponding transported message entry under the ReLU hidden mask. Selection is global for each dataset and checkpoint seed over the full transductive graph and does not use labels. The sparse coefficients are exact message residual values with explicit indices; they are not temporal spikes. The second aggregation \(\hat{A}H^{(1)}\) and output layer are not compressed by this method.

The reported test run confirms lower logit MSE on all three graphs at matched total padded serialized bits. At rank 128 and 2%, the ratio of three-seed means fell by 26.23%, 33.99%, and 25.83% on Cora, Chameleon, and Squirrel relative to the strongest evaluated matched-budget residual control. Task superiority was not established: task deltas were mixed across the evaluated budget grid, and the earlier task-superiority target failed. The supported task statement is instead a descriptive maximum observed degradation of 1.86 percentage points across three-seed means and 2.85 percentage points at seed level under per-metric matched-budget comparisons.

## 2 Related Work

Graph neural networks provide the frozen message-passing substrate for this study. Graph convolution, neighborhood sampling, attention, expressive message passing, depth, and higher-order mixing are established by a broad line of work \cite{kipf2017gcn,hamilton2018graphsage,velickovic2018gat,xu2019gin,li2019deepgcn,abu2019mixhop,chen2020gcnii,li2018deeper,wu2021gnnsurvey}. These papers motivate the normalized input message \(M_0=\hat{A}X\), but they do not study exact serialized-bit allocation for frozen conversion. The present paper therefore compresses one concrete operator output rather than proposing a new graph architecture.

Graph-model compression changes what is communicated or stored. Quantization-aware GNN training, vector-quantized node representations, tensor-core-oriented quantized execution, aggregation-aware mixed precision, distributed message quantization, quantized conversion, general quantization, and low-rank neural compression cover complementary cost models \cite{tailor2021degreequant,ding2021vqgnn,wang2022qgtc,zhu2023a2q,wan2023adaqp,hu2023fast,gholami2022quantization,cherukuri2025lowrank}. These methods differ in learned codebooks, bitwidth allocation, communication primitives, training objectives, and hardware assumptions. Our matched-budget A2Q-style and One-Spike-style adaptations are evaluated only under the present padded serialized-bit ledger; they are not direct reproductions of the published systems.

ANN-to-SNN conversion studies accuracy-latency trade-offs, offset and group-neuron corrections, early exit, transformer conversion, and post-training calibration \cite{one-spike,hao2023offset,lv2024group,bu2023optimal,li2023seenn,you2024spikezip,zhao2025ttfs,huang2025ecmt,li2024erroraware}. Broader SNN learning surveys distinguish conversion from direct spiking training and clarify temporal and hardware assumptions \cite{dampfhoffer2023snnlearning,nunes2022snnsurvey,wang2022taxonomicsnn}. One-Spike supplies output-code context \cite{one-spike}, while the conversion literature above does not establish the present exact-cost, output-sensitive residual allocation rule.

Direct and dynamic spiking graph models address spiking graph convolution, dynamic graph representation, delayed evolution, manifold geometry, signed conversion, graph attention, large-scale evaluation, contrastive learning, and geometric applications \cite{spikinggcn,spikenet,dy-sign,delay-dsgn,signnn,msg,negative-spike,sun2024spikegraphormer,zhang2025sgnnbench,li2023graph1bit,chaurasia2026sgspose}. Asynchronous spiking processing has also been applied to event-based visual inputs \cite{asgcn}; that work constrains event-processing terminology but is not a matched graph-message compression baseline. Collectively, these lines leave a narrower question: for frozen graph messages, can magnitude-weighted output-Jacobian residual allocation improve logit fidelity at matched total padded serialized-bit cost? The present contribution is limited to that question on \(M_0=\hat{A}X\) for frozen two-layer hidden-16 GCN checkpoints on Cora, Chameleon, and Squirrel.

## 3 Method

We consider frozen two-layer hidden-16 GCN checkpoints with parameters \(\theta\) and checkpoint seeds 0, 1, and 2. Let \(\hat{A}\) denote the normalized adjacency operator. The first-layer input message is

$$M_0=\hat{A}X\in\mathbb{R}^{N\times F},$$

and the frozen network computes

$$H^{(1)}=\sigma(M_0W^{(1)}), \qquad Z=\hat{A}H^{(1)}W^{(2)}.$$

Only \(M_0\) is transported with the proposed coding method. The second aggregation \(\hat{A}H^{(1)}\) and the output transformation are outside its compression scope. The message dimensions are \(N=2708,F=1433\) for Cora, \(N=2277,F=2325\) for Chameleon, and \(N=5201,F=2089\) for Squirrel. Thus \(F>128\) on every dataset and rank 128 is valid for the first-layer message. The normalized adjacency and its column norms remain part of the operator-aligned message construction rather than an additional post-hoc score factor.

For each dataset and checkpoint seed, transport retains a rank-128 SVD representation over the full transductive graph message:

$$M_{0,128}=U_{128}\Sigma_{128}V_{128}^{T}, \qquad R=M_0-M_{0,128}.$$

The residual \(R\) is represented by selected exact coefficients with explicit serialized positions. For residual coefficient \(r_i\) at position \(i\), let \(J_i\) be the analytic derivative of the frozen ANN logits with respect to the corresponding transported message entry under the current ReLU hidden mask. The evaluated magnitude-weighted output-Jacobian score is

$$J_i=\frac{\partial z_{\theta}}{\partial m_{0,i}}, \qquad s_i=r_i^2\lVert J_i\rVert_2^2.$$

Given a residual-entry budget \(B\), the selector transmits the set \(S=\operatorname{TopB}(s_i)\). Selection is global per dataset and checkpoint seed over all entries of the transductive graph message and uses no labels. This composite score is a heuristic allocation rule; the evaluated comparisons do not identify a causal contribution from the Jacobian term alone.

The serialization ledger explicitly charges each selected index-value pair 64 padded bits. For the rank-128 basis, the charged cost is

$$C_{\mathrm{basis}}=(N\cdot128+128+128\cdot F)\cdot32\ \mathrm{bits},$$

and the total padded cost is

$$C_{\mathrm{total}}=C_{\mathrm{basis}}+64|S|.$$

At the focal 2% budget, \(|S|=\operatorname{round}(0.02NF)\). The resulting totals are 21,932,736 bits for Cora, 25,630,208 bits for Chameleon, and 43,771,008 bits for Squirrel. Within each dataset, seed, rank, and budget comparison, methods are matched by total padded serialized bits even when their payload lengths or coefficient counts differ. Full-float transport and SVD-only transport are reference rows rather than matched residual-budget controls.

Rate-coded conversion represents each nonnegative post-activation value as a finite firing rate over \(T\in\{2,4\}\) bins, with the decoded scalar equal to the spike count divided by \(T\). Frozen parameters, adjacency, features, and serialized-cost conditions are held fixed across conversion comparisons. Sparse residual coefficients are exact message residual values with explicit indices and are not temporal SNN events. The measurement scope excludes hardware energy and does not establish temporal-event equivalence or broad GNN generality.

![Exact-cost output-Jacobian residual transport](../../../figures/figure1-architecture.png)

**Figure 1.** Exact-cost residual coding of \(M_0=\hat{A}X\) for frozen GNN-to-SNN conversion. A rank-128 basis and global sparse exact residual records selected by \(s_i=r_i^2\lVert J_i\rVert_2^2\) are serialized under an exact padded-bit ledger before rate-coded conversion. The figure represents input-message coding only and not temporal-event or energy behavior.

## 4 Experiments and Results

### 4.1 Experimental Scope

We evaluate Cora, Chameleon, and Squirrel using the reported split protocol and frozen two-layer hidden-16 GCN checkpoints with seeds 0, 1, and 2. Validation exposed ranks 16, 32, 64, and 128 and residual budgets 0.5%, 1%, and 2%. Guidance-v3 fixed rank 128 and the 2% focal budget after validation exposure and before the confirmation test run. The reported test is therefore held-out confirmation after validation-exposed reframing and setting selection, not preregistered or independent replication. No focal-setting selection based on the test results is claimed.

We report split-specific logit MSE, hidden-state MSE, \(T=2/4\) accuracy, and teacher agreement. For logits \(z_s\) on split \(s\), the split-specific metric is

$$\operatorname{MSE}_{\operatorname{logit}}(s)=\frac{1}{|s|C}\sum_{n\in s}\lVert z_n^{\operatorname{converted}}-z_n^{\operatorname{frozen}}\rVert_2^2,$$

and hidden-state MSE is defined analogously on the hidden representation. Accuracy is measured at \(T=2\) and \(T=4\); teacher agreement is the fraction of converted predictions matching the frozen GCN prediction. Task comparisons are descriptive and do not establish equivalence.

### 4.2 Compared Methods and Exact Cost

All compared encodings use the same rank-128 transport and exact total padded serialized-bit ledger within each dataset, seed, rank, and budget condition. The residual-budget controls use alternative allocation or coefficient-coding rules while allowing payload lengths and coefficient counts to differ.

| Method | Representation and allocation | Comparison role | Citation |
|---|---|---|---|
| Full-float | Uncompressed message reference | Reference, not a matched residual-budget control | — |
| SVD-only | Rank-128 basis without residual coefficients | Reference, not a matched residual-budget control | — |
| Output-Jacobian sparse residual | Rank-128 basis plus globally selected top-\(B\) exact residual pairs | Proposed method | — |
| Top-absolute residual | Rank-128 basis plus largest-magnitude residual pairs | Matched-budget residual control | — |
| Random residual indices | Rank-128 basis plus randomly indexed residual pairs | Matched-budget residual control | — |
| Dense uniform residual quantization | Uniform quantization of the residual under the same ledger | Matched-budget residual control | — |
| A2Q-style node-budget adaptation | Graph-aware node-budget allocation adapted to the same ledger | Matched-budget adapted control | \cite{zhu2023a2q} |
| One-Spike-style coefficient adaptation | Coefficient-coding allocation adapted to the same ledger | Matched-budget adapted control | \cite{one-spike} |


The validation grid also evaluated random-projection rank-$k$ bases with top-absolute, random, and A2Q-style residual controls across the rank and budget sweep. Because guidance-v3 fixed the operator-aligned SVD basis before the test run, random projection is retained as a validation diagnostic rather than a focal test comparator. Message MSE, hidden MSE, logit MSE, accuracy, teacher agreement, exact bit totals, coefficient counts, and warmed latency/memory were all recorded; the focal tables below expose the previously implicit message-MSE, coefficient-count, and exact-cost evidence.

For logit-MSE comparisons, the strongest evaluated residual control is selected post hoc, separately for each dataset, as the non-proposed matched-budget residual method with the lowest three-seed mean logit MSE. For task metrics, the comparator is the best matched-budget non-proposed control separately for each dataset and task metric. Together, the raw controls compare the complete composite selector with magnitude-only, random, dense-uniform, node-budget, and coefficient-coding alternatives; they do not constitute a Jacobian-only interaction ablation or a causal decomposition. All differences are descriptive, and no formal confidence interval is claimed.

### 4.3 Main Logit-Fidelity Result

At rank 128 and a 2% sparse residual budget on the reported test split, output-Jacobian selection reduced the ratio of three-seed mean split-specific logit MSE versus the strongest evaluated matched-budget residual control by 26.23% on Cora, 33.99% on Chameleon, and 25.83% on Squirrel. All nine dataset-seed comparisons improved. Each comparison used identical total padded serialized bits within the corresponding dataset

**Table 1. Fidelity decomposition and observed task trade-off.** Values are three-seed means ± sample SD (n=3); reductions are versus the top-absolute residual control, and task loss is the maximum three-seed-mean degradation across T=2/4 accuracy and teacher agreement. Message MSE is a diagnostic: the proposed method trades higher message MSE for lower hidden and logit MSE. Lower MSE is better; task loss is a descriptive maximum, not an equivalence bound.

| Dataset | Proposed logit MSE | Top-absolute logit MSE | Message MSE reduction | Hidden MSE reduction | Max observed task loss (pp) | Selected coefficients |
|---|---:|---:|---:|---:|---:|---:|
| Cora | 0.005666 ± 0.001975 | 0.007680 ± 0.002734 | -65.65% | 16.13% | 0.53 | 77611 |
| Chameleon | 0.033725 ± 0.007106 | 0.051088 ± 0.011935 | -31.90% | 10.85% | 1.17 | 105880 |
| Squirrel | 0.032645 ± 0.003495 | 0.044012 ± 0.004664 | -26.54% | 11.22% | 1.86 | 217298 |
, although payload lengths and coefficient counts could differ. No formal confidence interval is claimed.

The proposed composite selector also improved on the top-absolute residual control in all nine dataset-seed logit-MSE comparisons. Relative to our matched-budget A2Q-style adaptation, its three-seed mean logit MSE reductions were 28.93%, 36.19%, and 35.24% on Cora, Chameleon, and Squirrel. Relative to our matched-budget One-Spike-style adaptation, the reductions were 42.83%, 47.61%, and 34.03%. These paired descriptive comparisons use matched total padded serialized-bit budgets and the frozen two-layer GCN checkpoints.

**Table 2. Matched-budget adapted controls.** Values are three-seed means ± sample SD of logit MSE; reductions are relative to our matched-budget A2Q-style and One-Spike-style adaptations, not direct reproductions of the published systems.

| Dataset | Proposed | A2Q-style | Reduction vs A2Q-style | One-Spike-style | Reduction vs One-Spike-style |
|---|---:|---:|---:|---:|---:|
| Cora | 0.005666 ± 0.001975 | 0.007972 ± 0.002816 | 28.93% | 0.009910 ± 0.003744 | 42.83% |
| Chameleon | 0.033725 ± 0.007106 | 0.052852 ± 0.012665 | 36.19% | 0.064376 ± 0.016545 | 47.61% |
| Squirrel | 0.032645 ± 0.003495 | 0.050410 ± 0.005209 | 35.24% | 0.049482 ± 0.006139 | 34.03% |


![Matched-budget logit MSE for the proposed selector and controls](../../../figures/data/figure2-main-logit-mse.png)

**Figure 2.** Matched-budget logit fidelity on Cora, Chameleon, and Squirrel at rank 128 and a 2% residual budget. Bars show three-seed means and sample SD; lower logit MSE is better. Full-float and SVD-only are reference rows rather than matched residual-budget controls.

### 4.4 Sensitivity and Matched-Budget Controls

At rank 128 and the 2% residual budget, hidden-state MSE fell by 16.88%, 12.86%, and 10.63% relative to the strongest matched-budget control on Cora, Chameleon, and Squirrel. These three-seed mean reductions are descriptive sensitivity measurements without formal confidence intervals and were obtained in the validation-grid analysis preceding held-out confirmation of the focal setting.

Across the evaluated 0.5%, 1%, and 2% residual budgets and three graphs, logit MSE was below the strongest corresponding matched-budget residual control in all nine dataset-budget cells, with reductions from 2.98% to 30.40%. This validation-grid sensitivity analysis shows a consistent direction across the evaluated cells; it does not replace the separately reported held-out confirmation at the focal 2% setting.

![Logit-MSE reduction across residual budgets](../../../figures/data/figure3-budget-sensitivity.png)

**Figure 3.** Logit-MSE reduction over the evaluated 0.5%, 1%, and 2% residual-budget grid. The focal 2% setting later received held-out confirmation after validation exposure.

The matched-budget control set further shows that the result is not specific to comparison with a single encoding rule. The proposed composite selector outperformed top-absolute residual selection in all nine dataset-seed logit-MSE comparisons and was also compared with random indices, dense uniform residual quantization, and our A2Q-style and One-Spike-style adaptations. These comparisons evaluate the complete allocation rule against alternative rules; because no Jacobian-only or interaction ablation was performed, they do not isolate the causal contribution of the Jacobian factor.

### 4.5 Task and Runtime Trade-offs

Task superiority was not established. Across \(T=2/4\) accuracy and teacher agreement, deltas were mixed over the 0.5%-2% residual-budget grid, and the earlier task-superiority target failed. The accepted task statement is therefore limited to observed degradation rather than universal task gain.

Using the best matched-budget non-proposed control separately for each dataset and task metric, the maximum three-seed-mean observed degradations were 0.53, 1.17, and 1.86 percentage points on Cora, Chameleon, and Squirrel. Across all metrics and seeds, the largest observed single-seed degradation was 2.85 percentage points. These are descriptive maxima under per-metric comparators, not bounds, equivalence results, or evidence of population-level task preservation.

A separate secondary benchmark measures warmed full variant construction and evaluation cost at rank128/1%, not the focal 2% condition. The timed operation includes basis construction, residual construction and selection, reconstruction, rate conversion, and evaluation, while the frozen model, adjacency, and features are precomputed. Each method-dataset-seed p95 is the 0.95 quantile of seven measured elapsed times after three warmups, with CUDA synchronization before and after each call. Across nine dataset-seed pairs, paired p95 full-pipeline runtime ratios versus SVD-only ranged from 1.020 to 1.124, and the maximum recorded peak CUDA allocation was 218.23 MB. This is a wall-clock pipeline measurement and does not measure hardware energy.

**Table 3. Exact serialized-cost ledger at rank 128 and the 2% residual budget.** Each selected index-value pair is charged 64 bits. The total padded budget is basis bits plus residual padded bits; full-float is shown only as an uncompressed reference.

| Dataset | Basis bits | Residual target bits | Total padded bits | Selected coefficients | Full-float bits |
|---|---:|---:|---:|---:|---:|
| Cora | 16,965,632 | 4,967,104 | 21,932,736 | 77,611 | 124,178,048 |
| Chameleon | 18,853,888 | 6,776,320 | 25,630,208 | 105,880 | 169,408,800 |
| Squirrel | 29,863,936 | 13,907,072 | 43,771,008 | 217,298 | 347,676,448 |


![Task trade-off and warmed runtime overhead](../../../figures/data/figure4-tradeoff-and-runtime.png)

**Figure 4.** Observed task trade-off and warmed runtime overhead. Panel a reports reported-test logit-fidelity gains against the maximum observed three-seed-mean task degradation relative to the per-metric matched-budget control; its dashed line is the earlier 3 pp task-loss reference, not an observed equivalence threshold. Panel b reports paired p95 full-pipeline runtime ratios at rank128/1% and does not represent focal 2% timing or energy.

## 5 Discussion

Within the reported static-graph setting, the evidence supports a local fidelity-resource result for coding \(M_0=\hat{A}X\): magnitude-weighted output-Jacobian residual allocation reduced logit MSE under matched total padded serialized bits, and the maximum observed task degradation remained limited in the evaluated comparisons. The improvements over the strongest evaluated residual control, our matched-budget A2Q-style and One-Spike-style adaptations, and the nine positive dataset-seed comparisons against top-absolute selection are descriptive observations. Squared output-Jacobian sensitivity may preferentially retain residual directions that influence frozen-model outputs, but this explanation remains a mechanism hypothesis rather than an identified causal mechanism.

The evidence is restricted to frozen two-layer hidden-16 GCN checkpoints on Cora, Chameleon, and Squirrel. The focal setting and logit-fidelity reframing were fixed after validation exposure and before the test run; the test run is held-out confirmation, not preregistered or independent replication. Sparse residual coefficients are exact transported-message values rather than temporal SNN events. The study does not establish formal equivalence, hardware-energy savings, broad GNN generality, downstream utility beyond the reported metrics, or focal 2% runtime cost. These boundaries constrain both the logit-fidelity interpretation and the task trade-off.

## 6 Conclusion

For frozen two-layer hidden-16 GCN checkpoints on Cora, Chameleon, and Squirrel, magnitude-weighted output-Jacobian coding of the first-layer input message \(M_0=\hat{A}X\) improved logit fidelity at matched total padded serialized bits. At rank 128 and a 2% residual budget, the ratio of three-seed mean split-specific logit MSE fell by 26.23%, 33.99%, and 25.83% relative to the strongest evaluated matched-budget residual control. Task superiority was not established; the maximum observed three-seed-mean degradation was 1.86 percentage points and the maximum seed-level degradation was 2.85 percentage points under per-metric matched-budget comparisons. The result is held-out confirmation after validation exposure within the evaluated static graphs, not preregistered or independent replication.
