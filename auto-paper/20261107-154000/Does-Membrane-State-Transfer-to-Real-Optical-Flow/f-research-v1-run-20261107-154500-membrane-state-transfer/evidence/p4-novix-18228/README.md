# f-research-v1 P4 / C1 correction loop v3

Self-contained implementation and measured artifacts for the C1 second grind attempt.

## Reproduce

```bash
/home/novix/workspace/project/entrypoint.sh
```

Optional cache reuse in the same sandbox:

```bash
/home/novix/workspace/project/entrypoint.sh --reuse-features --skip-download
```

Exit codes:

- `0`: full method batch completed and independently validated (the scientific verdict may still be `REJECT_FAILURE`).
- `2`: a registered pre-training invariant failed; `result.json` is `design_invalid`, downstream readout fitting was stopped, and the partial evidence was independently validated.
- `1`: runtime or artifact-validation failure.

## Current measured terminal state

The clean final run ended intentionally with `status=design_invalid` at the KC feature-variance invariant. It is not a runtime crash and is not evidence that any method is superior.

- Complete graph: 178,853,187-byte edge archive, 138,639 nodes, 15,091,983 deduplicated edges.
- Exact-length eye→KC counts for hops 1..8: `0, 15, 2559, 2559, 2559, 2559, 2559, 2559`; selected `K=5`.
- SYNTHETIC five-seed flattened ceiling mean: `1.0`.
- Registered DAVIS v2 five-seed flattened ceiling mean: `0.72`.
- Biological-graph LIF variants had zero across-sample KC feature variance and zero KC hard-spike rate; the invariant therefore stopped the batch before Ridge fitting.
- No method accuracy, paired bootstrap CI, sign-flip p-value, or BH result was fabricated for unrun conditions.

The first full-frame DAVIS protocol obtained `0.685` and was marked unavailable. The fixed-ROI v2 preprocessing is explicitly post-hoc: GT masks select one fixed eight-frame union ROI (+10% margin), but mask values never multiply or replace grayscale input pixels. This history is retained in both `config.json` and `result.json`.

## Artifact map

- `result.json`: crash-safe authoritative result and invariant measurements.
- `validation.json`: independent numerical and structural validation, including the result byte count and SHA-256.
- `evidence/main_table.csv`: partial ceiling-only table because no method readout was trained.
- `evidence/raw/*.npz`: five raw ceiling records for SYNTHETIC and five for DAVIS.
- `evidence/features/*.npz`: eight pre-readout synthetic feature caches used to verify the feature-std invariant.
- `experiment-traceability.csv`: requirement-to-evidence map.
- `command_history.log`: acquisition and execution command history.
- `config.json`: complete registered protocol plus transparent preflight history.
- `test_pipeline.py`: protocol/unit tests.
- `validate_results.py`: terminal-state-aware validator.

Five paired seeds imply a minimum tie-free two-sided exact sign-flip p-value of `0.0625`; the design has limited inferential power. Because the feature invariant failed before readout fitting, this limitation is disclosed but no paired test was run.
