# G2 — Task and evaluation validity

## Task

- Input: Fashion-MNIST 28x28 grayscale image, split into a 7x7 grid of 4x4 patches (49 nodes).
- Output: one of 10 apparel classes.
- Teacher: a locally trained small ViG-style classifier with a patch embedding layer, several Grapher blocks using per-layer kNN over patch features and max aggregation over signed neighbor-minus-center differences, followed by global pooling and a classifier.
- Why valid: the dataset supplies labels and official splits; the teacher contains the exact discrete operations whose preservation is claimed; no external checkpoint is needed.

## Splits and isolation

- Official train/test from the MIT-licensed parquet files.
- Fixed 5,000-image calibration subset sampled from train with seed 0.
- Model-development validation subset of 5,000 images from the remaining train set; final hyperparameters frozen before test.
- Three teacher training seeds and three conversion calibration seeds. Test identities are recorded by SHA-256 of sorted sample indices and never used for tuning.
- Any test-driven design change marks that test as exposed and opens a versioned replacement contract.

## Metrics

Primary:
- Layerwise neighbor-set Jaccard versus the teacher, averaged over all Grapher blocks and samples.
- Layerwise signed-max winner agreement versus the teacher, matched by channel and node.

Secondary:
- Top-1 accuracy and teacher-student logit agreement.
- Event count per scalar (graded-pulse count) and warmed CPU/GPU latency.
- Accuracy recovery from teacher-neighbor, teacher-winner, and both-oracle interventions.

## Evaluation protocol

- T in {2,4,8}.
- Nominal signed coding levels matched across signed uniform quantization and signed multi-threshold coding.
- All methods use the same teacher weights and calibration data.
- Report every seed, mean, sample SD, failures, and non-finite events.
- Statistical comparison: paired differences over identical examples/seeds with descriptive bootstrap confidence intervals on the primary structure metrics; no unadjusted significance claim.

Gate verdict: `pass`. The dataset, task, splits, primary/secondary metrics, and isolation rules are explicit and reproducible.
