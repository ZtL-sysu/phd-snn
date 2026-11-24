# Novelty and feasibility report — GNN→SNN idea portfolio

Date: 2026-11-17. Search scope: 2022–2026 public literature, with older conversion foundations retained. Source policy: official proceedings/publisher/arXiv/project pages; direct spiking training is separated from frozen ANN/GNN→SNN conversion.

## Verdict

Ten candidates pass their preregistered smoke gates and have no identified exact duplicate in the recorded search. Novelty confidence is **medium-high within scope**, not proof over unpublished/unindexed work. Each candidate retains a narrow positioning boundary; broad claims such as “first graph conversion”, “first signed SNN”, “first sparse event graph”, or “energy efficient” are rejected.

## Closest-work subtraction

| Candidate | Closest verified work | What it owns | Remaining novelty delta |
|---|---|---|---|
| DYN-C01 | ASGCN AAAI 2025; Delay-DSGN ICML 2025 | event-graph conversion / direct temporal SNN | causal state-residual conversion for graph rollouts |
| EQ-C02 | MSG NeurIPS 2024; GC-LIF 2026; SGSPose 2026 | direct/hybrid equivariant spiking models | frozen coordinate-GNN radial event conversion with rotation certificate |
| PERM-C03 | SpikeGraphormer 2024; graph-equivariance literature | permutation-equivariant graph models | conversion-level node-order certificate and scheduler test |
| SIGN-C04 | Negative-spike conversion IJCAI 2025; SpikingHAN | signed spikes / direct heterogeneous SNN | signed graph-message event banks with heterophily evidence |
| LR-C05 | A²Q; AdaQP; graph quantization | learned/mixed precision or training communication | operator-aligned low-rank message events during frozen conversion |
| EDGE-C06 | Fast-SNN; PTQ conversion; One-Spike; ASGCN | generic quantization/sparse event graphs | quantized biological weighted edge messages |
| CERT-C11 | SEENN; AdaFire; robust SNN literature | SNN confidence/robustness | affine graph-aggregation conversion error envelope |
| POS-C13 | SpikeGraphormer; SpikeZIP-TF; ECMT; TTFSFormer | direct graph transformer / generic transformer conversion | quantized hop-positional graph conversion with equivariance |
| DLY-C14 | SpikeNet; Dy-SIGN; SiGNN; ASGCN | temporal/event spiking graph models | delay-aligned frozen-conversion residual schedule |
| READ-C18 | One-Spike SNN; generic ANN→SNN output mapping | cross-GCN conversion / full output maps | certified top-two signed margin-pair graph readout |

## Search limitations

- Chinese databases, patents, non-indexed workshop manuscripts and anything after 2026-11-17 were not exhaustively searched.
- Generic transformer conversion is mature, so graph-specific claims require explicit attention/positional/operator controls.
- The literature includes direct spiking GNN training; it is not counted as frozen conversion prior art but constrains terminology and baselines.
- No exact match was found for the listed deltas; the final paper phase must rerun a fresh closest-work search before submission.

## Smoke feasibility

- All reusable mechanisms have failing-first unit tests; the final suite is 32/32 pass.
- Real local assets include DAVIS-2017 clips, MaleCNS coordinates, FlyWire edge weights, Chameleon/Squirrel/Planetoid/OGBN-Arxiv graphs, and frozen GCN checkpoints.
- Strong smoke means the exact predeclared mechanism gate passed, not publication-level accuracy superiority. Several candidates are correctness/compression/certificate mechanisms and require full downstream teacher-fidelity experiments before method-paper claims.
- Local RTX 3060 12 GiB / 32 GiB RAM is sufficient for these screens. No remote compute or test-set selection was used in accepted smoke evidence.
