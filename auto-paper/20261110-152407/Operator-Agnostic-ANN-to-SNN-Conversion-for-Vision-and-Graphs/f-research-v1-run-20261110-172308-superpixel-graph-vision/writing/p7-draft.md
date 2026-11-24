# P7 · Manuscript Draft (English, generated from the accepted TeX sections)

> Source of truth: `tex/sections/*.tex`. Every numeric value is a LaTeX macro defined in `tex/numbers.tex` from `results/*.json`.

## Introduction


Graph neural networks (GNNs) are increasingly used as vision backbones: an image is represented as a set of superpixels or patches connected by a spatial adjacency, and message passing replaces the regular convolutional grid~[citations]. This representation is attractive for irregular objects and for event-driven deployment, yet the ANN-to-SNN conversion theory that makes spiking inference cheap was developed almost entirely for row-stochastic convolutional operators~[citations]. For a graph, the propagation operator is neither a grid nor necessarily row-stochastic, and its row sums depend on degree and edge weight. Whether a conversion recipe calibrated for convolutions remains valid on such operators is largely untested.

A second, more practical gap concerns energy. Spiking inference replaces multiply--accumulates (MACs) with accumulations (ACs); under a 45,nm model the per-operation ratio is only ~[citations]. Consequently a $5$ arithmetic-energy advantage requires the total number of synaptic operations to fall below the ANN's MAC count, not merely to replace some of them. Most conversion studies report accuracy--latency curves on CNNs or ImageNet-scale models~[citations], and spike counts on graphs are rarely converted into an explicit ANN-relative energy statement with two independent accounting conventions.

This paper studies a combination of conversion components that was originally assembled for graph node classification, and asks whether that combination transfers to *graph-structured visual classification*. Our starting point is a two-layer GCN with an exact conversion-error identity $ - B = $, a closed-form forward bias $^=/(2T)$, a membrane-potential readout, and a margin-recovery bound. We do *not* claim to invent these individual components: threshold balancing, zero-expected-error bias, membrane decoding, deterministic counting and two-phase neurons all have their own lineage~[citations]. Our contribution is the *re-identification and adaptation of the combination* on a new operator class: we show that a linear global pooling matrix preserves the identity exactly, that the closed-form bias becomes redundant and harmful once the spike train is deterministic, and that margin regularisation plus a narrow, low-timestep network reaches a stable arithmetic-energy advantage while keeping the conversion fidelity measurable.

Specifically, we make four contributions.

itemize
 **Exact identity with a graph-level readout.** For a block-diagonal superpixel adjacency $A$ and a linear pooling matrix $R$, the conversion error is exactly $-B = R A (E_1 W_2)$ with $E_1 = c_1/T - ReLU(B_1)$. We verify this identity to  with a unified float64 forward pass, and show that the residual observed under float32 is an accumulation artefact rather than a theoretical failure.
 **A mechanism-level correction of the combination.** Deterministic two-phase spiking already realises the target firing count exactly ($_t s[t]=n$). Adding $^=/(2T)$, which compensates floor-quantisation bias, double-corrects the rate. Removing it reduces the $T=8$ conversion loss from  to  on MNIST superpixels and from  to  on CIFAR10 superpixels, across five seeds.
 **A stable arithmetic-energy result.** Across four mutually disjoint holdout groups ( distinct frozen seeds) and *both* energy conventions, the converted network attains / on MNIST and / on CIFAR10, with every individual seed above $5$. All single-point conversion baselines adapted to the same backbone remain near chance, with margins of  and  percentage points at $T=4$.
 **An explicit accuracy--energy frontier.** We report measured conversion loss under the $5$ energy constraint rather than a post-hoc target: $$,pp on CIFAR10 and $$,pp on MNIST. Increasing the training budget (,pp / ,pp) *worsens* fidelity and is reported as a negative result. The frontier is the object of study, not an accuracy claim.
itemize

We state our boundaries early. Energy numbers are 45,nm *theoretical arithmetic op-count estimates*, not measured joules on neuromorphic hardware. Teacher accuracies (% and %) are modest because the energy constraint forces a narrow network; we make no accuracy-SOTA claim. The method covers fixed, non-negative, linear adjacency with linear pooling; dynamic attention, nonlinear pooling and ImageNet-scale training are outside its scope.


## Related Work


**ANN-to-SNN conversion.** Rate-based conversion replaces rectifiers with integrate-and-fire units and interprets firing rates as activations. Weight/threshold balancing, data-based normalisation, reset-by-subtraction and soft reset established the basic pipeline~[citations]. Deng and Gu derived a layerwise recursion and the closed-form bias that removes the systematic rate offset~[citations]; QCFS replaced ReLU with a quantised clip--floor--shift activation so that the expected conversion error vanishes~[citations]. FTBC added a forward temporal bias~[citations], and an optimal-transport view of the same correction was developed in~[citations]. Dual-Phase decoding showed that reading the membrane potential avoids the $1/T$ quantisation grid~[citations]. TPP introduced two-phase probabilistic neurons to exploit temporal misalignment~[citations]; PASCAL used inhibitory spikes for deterministic exact counting~[citations]; parallel spiking conversion, differential coding, adaptive bursts, channel-wise softplus thresholds, error-compensation learning and adaptive fission target the low-latency regime~[citations]. Recent preprints continue to refine residual-membrane alignment, group-wise thresholds and fine-tuning~[citations]. All of these are developed and evaluated on convolutional or attentional vision backbones with row-stochastic operators.

**Spiking graph networks.** Spiking GCNs are overwhelmingly trained directly with surrogate gradients~[citations], and large-scale evaluations of spiking GNNs contain no conversion method~[citations]. One-Spike SNN converts both CNNs and text GCNs with single-spike phase coding~[citations], but does not analyse conversion error for message passing or compare ANN-relative energy. To our knowledge, no published work transfers a full conversion-error formulation to graph-level visual classification and evaluates it against a complete family of conversion baselines.

**Graph-structured vision.** Vision GNNs build $k$-NN graphs over image patches~[citations], while superpixel graph benchmarks convert MNIST and CIFAR10 images into 40--150-node graphs using SLIC and an 8-NN Gaussian-weighted adjacency~[citations]. These datasets ship *with* their graph structure, which makes them a direct test bed: no graph construction or freezing heuristic is needed, and the propagation operator is fixed and non-negative. Classical graph backbones and semi-supervised splits provide the architectural substrate~[citations].

**Energy accounting.** SNN energy studies typically count synaptic operations and apply a 45,nm CMOS table in which a 32-bit MAC costs ,pJ and an AC costs ,pJ~[citations]. Because this ratio is only , an advantage of $5$ essentially requires the SNN's AC count to fall below the ANN's MAC count. We report two conventions throughout: a primary event-driven AC-only count and a conservative count that also charges the real-valued propagation as MACs.


## Method


### Graph-structured visual classification setup


Each image is a graph $g$ with $n_g$ superpixel nodes, node features $X_g$, an 8-NN weighted adjacency, and a class label. For a batch of $G$ graphs we form a block-diagonal sparse adjacency $AR^N N$, $N=_g n_g$, and a fixed linear pooling matrix $RR^G N$ whose $g$-th row averages the nodes of graph $g$. A two-layer GCN produces graph logits
equation
B = R(A,(ReLU(B_1) W_2)) + b_2,
B_1 = A (X W_1) + b_1 .

equation
$A$ is symmetrically normalised and non-negative; $R$ is fixed and linear. These two properties are the only structural assumptions of our analysis.

### Exact conversion identity


Hidden units are deterministic integrate-and-fire neurons with threshold $$ and subtractive reset. Layer~1 receives a constant per-step current $B_1+$; layer~2 integrates the instantaneous messages
equation
inst_t = R(A (s_t W_2)) + b_2,
 = 1T_t=1^T inst_t .

equation
Writing $c_1=_t s_t = T,rate_1$ and $E_1=rate_1-ReLU(B_1)$, linearity of $R A () W_2$ gives, without approximation,
equation
 - B = R A (E_1 W_2).

equation
Equation~eq:identity is the graph-level analogue of the node-level identity and holds for any fixed non-negative linear $A$ and linear $R$; the pooling operator does not add an error term. We verify it on the *same* forward pass used for all reported numbers: with a fully float64 implementation the maximum residual is . A float32 sparse matmul in $A(XW_1)$ introduces a $3.710^-7$ discrepancy between the fp32 current and its fp64 recomputation, which is why a mixed-precision check falsely suggests a $210^-7$ residual. The identity is exact; the earlier residual was numerical.

### Deterministic two-phase spiking and the redundant bias


For a target count $n=round(ReLU(B_1+)T/)$ clipped to $[0,T]$, the deterministic two-phase schedule
equation
s[t] = round!(t nT) - round!((t-1)nT), t=1,,T

equation
telescopes to $_t s[t]=n$ exactly, with zero conditional variance and at most one spike per step. Because the rate is already realised exactly, the systematic floor-quantisation error that $^=/(2T)$ was designed to cancel~[citations] no longer exists. Adding it shifts the target count and double-corrects the current. We therefore set $=0$ in the main arm and retain $^$ as an explicit ablation. Section~ssec:ablations quantifies the cost of this redundancy.

### Membrane readout, margin regularisation and narrow networks


Instead of counting output spikes, we decode $argmax$, i.e. the accumulated instantaneous current. Since $mem=,count+u=_t inst_t$ holds exactly, this decoder is free of spikes and removes both the $1/T$ decision grid and the unit-clipping ceiling~[citations].

To reduce the required timestep we increase the ANN logit margin. With $ = B_y - _c y B_c$ and a hinge penalty $,E[ReLU(1-)]$, the margin-recovery bound~[citations] predicts $T = O(|a_n|_2|DW|_2/)$: a larger $$ permits a smaller $T$. We train with a unit mask that holds all but $k$ hidden units at zero, so spike count scales with the surviving width; the mask is derived from training-set activation magnitude and is fixed before conversion. Working points $(, k, , T)$ are selected only on validation splits.

### Theoretical arithmetic energy


We count ANN MACs as $EF + NFH + EH + NHC + NC$ for $N$ nodes, $E$ non-zero edges, $F$ input features, $H$ hidden units and $C$ classes. With hidden spike count $S$ and mean degree $ d = E/N$, the primary SNN convention charges
$AC = S (H +  d C)$;
the conservative convention additionally charges real-valued propagation as $MAC=T E C$:
equation
R_prim = MAC_ANNAC,
R_cons = MAC_ANNS H + T E C.

equation
Both ratios use the 45,nm constants~[citations]; both are *op-count estimates*, not hardware measurements. We exclude degenerate zero-spike networks from any energy claim: a network emitting no spikes has vanishing ACs but chance-level accuracy. Likewise, a working point is admissible only if its teacher exceeds twice the chance rate.

### Applicability and falsification


The analysis requires fixed, non-negative, linear $A$ and linear $R$. Dynamic graphs, per-sample attention and nonlinear pooling break the factorisation in~eq:identity; we report such variants as failure boundaries rather than silently adapting them. The mechanism is falsified by any of: a non-zero identity residual in float64, a gain from re-introducing $^$, a spike-counting decoder matching the membrane decoder, or an energy advantage that disappears under the conservative convention.


## Experiments and Results


### Datasets and protocol


We use the official SuperPixel MNIST and CIFAR10 graph benchmarks~[citations], which ship SLIC superpixels as nodes and an 8-NN Gaussian-weighted adjacency as edges; MNIST graphs have 40--75 nodes, CIFAR10 graphs 85--150. Official splits are 55k/5k/10k and 45k/5k/10k graphs. All experiments use a two-layer GCN, fixed $A$ with symmetric normalisation, linear sum pooling $R$, and a frozen evaluation protocol: five frozen seeds per holdout group, $T1,2,4,8,16$, and working points selected on validation only. Four mutually disjoint holdout groups (seeds 0--4, 5--9, 10--14, 15--19) provide  independent test seeds; no test split is reused for selection. We report mean, standard deviation and 95% confidence intervals. CUDA sparse reduction is non-deterministic, so single-seed best values are never reported.

### Baselines


All conversion methods are adapted to the *same* superpixel-graph backbone, teacher, threshold, calibration data and $T$ grid: naive rate conversion, QCFS quantised activation~[citations], FTBC forward bias~[citations], TPP two-phase probabilistic neurons~[citations], and parallel conversion~[citations]. A directly trained spiking GCN with surrogate gradients is the technique-family control. DCGS, AdaFire, PASCAL, CS-QCFS, One-Spike SNN and Adaptive Fission are literature context~[citations]; they are not used to carry the main comparison because their official code or training protocol does not transfer without redesign. The ANN teacher is the upper bound for conversion loss.

### Main results


Table~tab:main reports the third, entirely untouched holdout group (seeds 10--14) with a unified float64 forward pass. Both energy conventions exceed $5$ for every one of the ten runs; the smallest single-seed conservative ratio is . Conversion loss is $$,pp on CIFAR10 and $$,pp on MNIST. Teacher accuracy is % and %, i.e. well above the 20% admissibility floor (twice the 10-class chance rate) but not competitive as an absolute classifier.

table[t]

Five-seed results on untouched holdout seeds 10--14. Energy is a 45,nm theoretical arithmetic estimate under two conventions; loss is conversion loss in percentage points (lower is better).

tables/tab_main
table

The first two holdout groups (seeds 0--4 and 5--9) independently reproduce the energy result with conservative ratios of  and , and the fourth group (seeds 15--19) does so again at . Across all four groups the energy claim holds for  distinct seeds without a single exception. The fourth group also provides a deliberate negative result: increasing the training set from 2,000 to 3,000 graphs and the epoch budget from 800 to 1,000 raises teacher accuracy slightly but *worsens* conversion loss to ,pp (MNIST) and ,pp (CIFAR10). Longer training sharpens margins amplified by the low-$T$ quantiser rather than stabilising them; we report this rather than selecting the more favourable group.

### Comparison with conversion baselines


Table~tab:baselines summarises the five-seed full-scale comparison. Every single-point conversion baseline stays near chance on both datasets, while our converted network leads the strongest baseline by ,pp (MNIST, $T=4$) and ,pp (CIFAR10, $T=4$). This is not an accuracy-SOTA claim: it is a statement that graph message passing exposes a conversion failure mode that methods calibrated for row-stochastic convolutions do not address.

table[t]

Five-seed top-1 (%) at $T=4$ and $T=8$ for all adapted conversion baselines. Chance is 10%.

tables/tab_baselines
table

### Ablations


Table~tab:ablations isolates each component. Removing the redundant $^$ lowers the $T=8$ conversion loss from  to ,pp on MNIST and from  to ,pp on CIFAR10. Replacing the membrane readout with spike counting collapses accuracy to % versus % ($T=8$), confirming that the $1/T$ grid and unit-clipping ceiling dominate the error. Randomising the second phase (TPP-style) degrades accuracy by ,pp. Each ablation moves in the direction predicted by~eq:identity.

table[t]

Component ablations at $T=8$ (five seeds). Values are top-1 (%) or conversion loss (pp).

tables/tab_ablations
table

### Identity verification and numerical precision


Table~tab:identity reports the float64 residual over all timesteps. The residual stays between  and , i.e. at machine precision, while the float32 forward pass differs from its float64 recomputation by . The two spike trains are bit-identical (L1 difference zero), so the earlier $10^-7$-level residual was entirely an accumulation artefact. This check is performed on the same forward pass that produces the accuracy and energy numbers.

table[t]

Maximum $|(-B)-R A(E_1W_2)|$ in float64 across timesteps and holdout seeds.

tables/tab_identity
table

### Accuracy--energy frontier


Figure~fig:pareto plots conversion loss against the conservative energy ratio over the full working-point grid. The frontier is monotone: points above $5$ in both conventions are concentrated at $T2,3,4$ with 10--26 surviving hidden units, and their conversion loss is higher than that of wider, longer-timestep points. We therefore report the frontier itself as the result, rather than claiming a simultaneous $1.5$,pp fidelity target. CIFAR10 attains ,pp at  conservative; its 95% CI lower bound is ,pp, so the difference from 1.5,pp is not statistically resolved. MNIST remains the harder case at ,pp. Figure~fig:lossT shows the loss--latency curve with confidence bands over all five timesteps.


## Discussion


**What the combination contributes.** Our starting components are not new individually. What is new is their joint behaviour on a graph-level visual operator. A linear pooling matrix leaves the error identity exact, so a formulation derived for node classification transfers without approximation; but a component that is beneficial in isolation can become harmful in the combination. The closed-form bias $^$ cancels floor-quantisation error for an integrate-and-fire rate, whereas the deterministic two-phase schedule already delivers the exact count. Keeping both double-corrects the current. Identifying and removing this redundancy is a mechanistic contribution, not a hyperparameter choice: it is predicted by~eq:dtp, verified by a paired ablation, and consistent across both datasets and all seeds.

**Why the energy result is stable.** The 45,nm per-operation ratio is only , so a $5$ advantage requires the SNN's total ACs to fall below the ANN's MACs. Two mechanisms achieve this together: a narrow trained network reduces the number of emitting units, and $T2,3,4$ bounds the number of propagation steps. Neither alone suffices. Reporting a conservative convention that also charges real-valued propagation as MACs is important, because an AC-only count can be made arbitrarily favourable by driving the network toward zero spikes. We explicitly exclude zero-spike and chance-level-teacher configurations; those were the two ways our own screening initially produced false positives.

**The accuracy--energy trade-off is the result.** We do not claim a 1.5,pp fidelity target. Under the $5$ constraint, measured conversion loss is $$,pp on CIFAR10 and $$,pp on MNIST, and teacher accuracy is %/%. A wider network or longer timestep improves fidelity but loses the energy advantage; a narrower one improves energy but loses fidelity. Increasing the training budget, which we expected to stabilise the teacher, instead widened margins that the low-$T$ quantiser amplifies and made fidelity worse (/,pp). We report this negative result and the full Pareto frontier rather than choosing a favourable operating point after the fact.

**Limitations and threats to validity.** All energy figures are theoretical op-count estimates under a 45,nm table; they ignore membrane-update cost, memory traffic and event-routing overhead, and are not measurements on neuromorphic hardware. Spike counts are therefore proxies. The method assumes a fixed non-negative linear adjacency and linear pooling; dynamic $k$-NN graphs, per-sample attention and max-relative aggregation break the factorisation in~eq:identity and are failure boundaries. Learning per-edge attention would require freezing it into a fixed operator first. Our teachers are deliberately small, so absolute accuracies are below published superpixel-GNN results; our claim concerns conversion fidelity and energy, not classifier quality. Finally, the four holdout groups are disjoint seeds drawn from the same two public benchmarks, so the conclusion is bounded to SuperPixel MNIST/CIFAR10 and does not establish ImageNet-scale behaviour. CUDA sparse reduction is non-deterministic; we mitigate it with five seeds, standard deviations and confidence intervals, and never select on a test split.


## Conclusion


We studied whether a conversion framework assembled for graph node classification transfers to graph-structured visual classification, where images ship as superpixel graphs rather than regular grids, and whether it can deliver an ANN-relative energy advantage. A linear global pooling operator preserves the exact conversion-error identity $-B=R A(E_1W_2)$; a unified float64 forward pass verifies it to . Within the transferred combination we found a genuine mechanistic redundancy: deterministic two-phase spiking already realises the target firing count, so the closed-form bias $^=/(2T)$ double-corrects the rate and must be removed. With that correction, membrane decoding, margin regularisation and a narrow low-timestep network, both 45,nm arithmetic-energy conventions exceed $5$ across four mutually disjoint holdout groups and  independent seeds, while all adapted single-point conversion baselines remain near chance.

The accompanying cost is an explicit accuracy--energy frontier: measured conversion loss is $$,pp on CIFAR10 and $$,pp on MNIST under the energy constraint, with modest teacher accuracies. We report the frontier and a negative scaling result rather than a simultaneous fidelity target. The broader lesson is that conversion is a statement about how a computation is discretised: on a graph the discretisation happens along the neighbourhood as well as along time, and a component that is correct for one operator can be wrong for another. Extending the analysis to dynamic or attention-based vision graphs, and replacing op-count estimates with hardware measurements, are the natural next steps.

