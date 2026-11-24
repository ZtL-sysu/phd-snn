# Novelty and feasibility report

## Decision

Feasible as a top-conference method-plus-diagnosis project only if the pre-registered strong-result lock passes. Otherwise the next material-backed direction must be activated through a versioned replacement contract.

## Evidence summary

- Current strong conversion family: DCGS 2025, primary arXiv record verified; code exists but no detected license, so algorithmic reimplementation is required.
- Defining teacher: ViG NeurIPS 2022, primary record verified; dynamic kNN and Grapher/FFN are in the abstract; official code exists but no detected license.
- Closest graph conversion works: One-Spike SNN, PMSM, and point-cloud conversion. The imported audit separates them by fixed topology, source retraining, or max replacement.
- Search boundary: targeted arXiv queries found no paper combining spiking, dynamic graph, training-free conversion, kNN, and signed max. Final submission-stage novelty recheck remains mandatory.
- Data: Fashion-MNIST and MNIST are directly public with MIT dataset cards. CIFAR-10 was rejected for an unknown license. Existing local superpixel graph data and teacher metadata are usable for diagnostics only because official tests are historically exposed.
- Hardware: RTX 3060 12 GB, PyTorch 2.11+cu128, 12 CPUs, about 481 GiB free disk. Small patch-grid Grapher experiments fit within 24 hours and 8 GB under the declared trial budget.

## Main risks

1. Baseline conversion may produce negligible structure disagreement at T<=4, falsifying the mechanism.
2. Architecture calibration may not transfer from calibration subset to held-out examples.
3. The local dynamic teacher is small; scope claims must remain bounded by Fashion-MNIST/MNIST-style graphs.
4. Upstream code licenses prevent direct code reuse; implementation risk is mitigated by clean reimplementation and a 64-sample smoke test.

## Go/no-go rule

Go only if baseline disagreement reaches the pre-registered threshold and an oracle intervention explains accuracy loss. No-go returns to the streaming-graph rescue route with a new baseline-calibrated expected_strong target.
