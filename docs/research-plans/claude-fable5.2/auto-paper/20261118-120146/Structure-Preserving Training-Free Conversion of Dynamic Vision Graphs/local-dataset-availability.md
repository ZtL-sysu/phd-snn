# Local dataset availability log

Access/inspection date: 2026-11-18.

## Finding

The user pointed to existing datasets inside `C:\code\phd-snn`. Inspection found the following directly reusable local assets:

| Asset | Local path | Content verified | License/source evidence | Constraint |
|---|---|---|---|---|
| SuperPixel MNIST + CIFAR10 graph datasets | `C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\data\pyg_bench` | 12 files, 4,380,659,876 bytes. Loaded `MNIST/processed/train_data.pt` as a tuple of dicts with `x`, `edge_index`, `edge_attr`, `pos`, `y`; train 55,000 graphs, test 10,000. CIFAR10 train has 45,000 graphs with 3-channel node features. Files are PyG batch-level dicts, not model weights. | Local `public_baselines/LICENSE.benchmarking-gnns` is MIT, and `SOURCES.md` names `graphdeeplearning/benchmarking-gnns` as upstream. Teacher metadata records split counts and processed-file SHA-256s. | Official test is marked historically exposed in all teacher result files. It cannot be reused as unseen final test evidence. |
| Full teacher runs | `C:\code\phd-snn\archive-gnn2snn\gnn2snn-main\research\visual-graphs\takeover_20261112\full_teacher_runs` | 9 runs with `done.json`/`metadata.json` and test JSON. Gated CIFAR10 teachers reach 0.6920 / 0.6839 / 0.6872; plain CIFAR10 teachers about 0.55; MNIST teachers about 0.91. | Metadata records model class, seeds, splits, source hashes, processed-data hashes, device, and PyTorch/PyG versions. | Test exposure is explicitly recorded. Also, architecture is fixed-graph GatedGCN, not the dynamic-kNN/max operator needed for the primary claim. |
| Citation graph datasets | `C:\code\phd-snn\third_party\SpikeGraphormer\datasets` | Cora/Citeseer/Pubmed raw and processed files exist. | Dataset terms not verified in this gate. | Not visual graphs; not a valid substitute for the primary mechanism. |

## Decision

- Keep Fashion-MNIST and MNIST as license-clear, unexposed-data routes for the binding final test.
- Use the local SuperPixel graph datasets and teacher metadata as a pre-existing resource for method prototyping, split diagnostics, and architecture/code reuse, with test results labeled historically exposed.
- Do not claim new unseen-test performance from the historical official test files.
- Do not switch the primary teacher to the fixed-graph GatedGCN checkpoints, because that would remove the dynamic-kNN/signed-max mechanism under study.
