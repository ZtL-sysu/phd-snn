# Public-safe opportunity map

## Source status

- The imported GitHub/Notion materials are a source snapshot, not independent verification. They identify candidate gaps but do not by themselves satisfy G0-G4.
- Direct API checks on 2026-11-18 confirmed the arXiv records for DCGS (`2503.00301`), ViG (`2206.00272`), and DeltaCNN (`2203.03996`) and their official code links in the abstracts.
- GitHub API checks confirmed `h-z-h-cell/ANN-to-SNN-DCGS` exists, was pushed 2025-05-29, has 17 stars, and declares no license. `huawei-noah/Efficient-AI-Backbones` exists with ViG code and no detected license. Unlicensed code cannot be copied into deliverables; independent reimplementation from公开 papers is required.
- Hugging Face dataset tree API confirmed `uoft-cs/cifar10` exposes direct parquet files under `plain_text/`: test 23,940,850 bytes and train 119,705,255 bytes. This is a direct public path for G1 evidence.

## Closest-work clusters

1. Training-free ANN-to-SNN conversion: DCGS (2025) is the current strong low-step method for CNN/ViT; it introduces differential coding and multi-threshold neurons but no graph operators.
2. Graph conversion: One-Spike SNN (2025) converts fixed-text GCN with linear aggregation; PMSM (2025) requires a specially trained quantized source; point-cloud conversion replaces max pooling and retrains. None directly matches dynamic-kNN/signed-max training-free visual graph conversion in the locally imported evidence.
3. Vision graph backbones: ViG (NeurIPS 2022) constructs kNN from patch features in every Grapher block and uses max over signed neighbor differences; official PyTorch code exists in Efficient-AI-Backbones.
4. Delta/incremental inference: DeltaCNN (CVPR 2022) gives training-free sparse frame differences with up to 7x practical CNN speedup; AEGNN/DAGr/InkStream give exact or event-driven graph updates. The imported audit says approximate per-layer thresholding on visual graphs was not found.
5. Energy accounting: Horowitz-based op-only estimates omit memory and low-bit comparators; prior analyses favor quantized networks on static images. Graph-specific fair comparison was not found in the imported evidence.

## Current public data and code route

- CIFAR-10 direct parquet files: `https://huggingface.co/datasets/uoft-cs/cifar10/tree/main/plain_text`, license to be read from the dataset card before any use.
- DCGS source: `https://github.com/h-z-h-cell/ANN-to-SNN-DCGS`; no detected license, so use as algorithmic reference only, not source-copy dependency.
- ViG source: `https://github.com/huawei-noah/Efficient-AI-Backbones`; no detected license, so reproduce only the documented kNN/max graph operator from the paper unless a license file is found in the repository.
- Strong baseline gap: official CIFAR-10 ViG weights may not exist; if unavailable, use a locally trained teacher as an internal evidence route, while keeping literature-only DCGS/ViG numbers as context. This gap must be explicit in G0/G6.

## Differentiation routes

- Prefer a method paper if calibration can recover structure agreement and accuracy at T<=4 with fewer events than competing conversions.
- Prefer an analysis paper only if conversion is naturally faithful and structure decisions are robust; then the finding can guide conversion design but must still include strong baselines and interventions.
- Energy-only papers are low priority because hardware constants can dominate the conclusion.
