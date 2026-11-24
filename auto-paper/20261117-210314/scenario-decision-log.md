# Scenario decision log

Date: 2026-11-17.

## Chosen discovery setting

Frozen ANN/GNN→SNN conversion on real graph tasks, with graph-level SuperPixel MNIST/CIFAR10 as the main cross-domain smoke pair and citation/heterophilic graphs for signed-message candidates. This is preferred over direct spiking-GNN training because it uses the project's verified strong teachers and isolates conversion mechanisms rather than trading away teacher quality.

## Alternatives

| Scenario | Decision | Reason |
|---|---|---|
| Dynamic/temporal graph conversion | Needs evidence | Literature and directly accessible local temporal data not yet verified; no automatic admission |
| Fly connectome temporal vision | Defer | Different scientific task and data pipeline; cannot use it as a cheap tenth variant |
| Optical-flow membrane transfer | Defer | Historical distinct project, not necessarily GNN→SNN conversion; no duplicate packaging |
| New SNN training on Cora/Citeseer | Defer | Not the requested conversion focus; teacher/training improvements confound conversion |
| Large OGB/ImageNet/ViT conversion | Reject for smoke | Missing local OGB dependency/data or exceeds a rapid 12 GiB screen; can be future full validation only |

Candidates that fail their novelty or smoke gate will be added below with specific sources/results, never silently removed.
