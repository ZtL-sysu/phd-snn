# execution-contract-v2 (immutable, round 023)

- Created: 2026-11-09 (GMT+8), automation round 023.
- Supersedes: `execution-contract-v1` binding in `pipeline-state.json`.
- Defect: `contract` bound the MUTABLE append-only file `experiment-traceability.md` to immutable sha256 `34b498f3e124221882d10a6f02ddef988f0589f9efbce3ca6fe428e82c35d14e`, while its live hash was `dafea5c70e9cf4cc0aa8a845fa7ef8a01988005e23ebf22d2714a000d2358ba0`. Every `--before`/`--complete`/`--submission-ready` returned rc=1 (`contract: stale hash experiment-traceability.md`) for rounds 021, 022, 023.
- Repair: contract v2 binds the FROZEN versioned snapshot `experiment-traceability-frozen-v2.md` (sha256 `dafea5c70e9cf4cc0aa8a845fa7ef8a01988005e23ebf22d2714a000d2358ba0`) instead of the mutable log. The mutable log remains append-only and live; it is no longer hash-bound.
- Failure evidence preserved: `pipeline-state.json.bak-pre-contract-v2-round023`, this document, and the per-round validator logs under `fly-connectome-cvpr2027/rounds/`.
- Integrity: NO stage status changed (all 26 remain `pending`); NO `pass` event appended; `workflow_complete` and `submission_ready` remain false; only one REAL `reopen` history event records the contract-version change.
- This is a LOCAL structural repair ONLY. It does not advance any scientific gate, does not start P0, and does not pull or judge any novix result.
