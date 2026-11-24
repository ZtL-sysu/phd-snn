# P2 evidence migration check

- V2 baseline, exact-Jacobian method and warmed timing files are copied into `inputs/` with SHA256 in `input-manifest.json`.
- Data, split identities, seeds, code semantics, CUDA/Conda environment and metric definitions match guidance-v3. No rerun is needed for unchanged evidence.
- V2 failed task-superiority evidence is retained and is not reused as a success claim.
- ARC stage map/config and local TeX availability are verified.

Verdict: **pass**.
