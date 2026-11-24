# Traceability policy (content-addressed)

The f-research-v1 pipeline requires every run to be traceable to a command, seeds and a commit,
while its own non-negotiable rules forbid committing changed files without explicit author
instruction. This run resolves the conflict without weakening either side:

- No git repository is initialized and no commit is made in this run root.
- Each `runs/<run_id>/config.yaml` carries a **content-addressed trace id** built from the sha256
  of every code file used, every input data file, the full command line, hyperparameters, seed,
  device, Conda environment and library versions.
- Where a code or data asset came from the companion run, its source commit
  `d12511207b1f0f1ee49650ec560de5236942c419` is also recorded, with the byte-identical copy's
  sha256 in `audits/reaccepted-assets.md`.
- `registry/results.csv` stores the trace id in the `git_commit` column with the prefix
  `content:<sha256-prefix>` so the column is never empty and never masquerades as a git commit.
- A run is void if the recorded hashes cannot be recomputed from files inside this run root.

This is a **hard** traceability mechanism, not a relaxed one: it binds the exact bytes, which a
git commit alone would not do for untracked data files. If the author later authorizes a local
repository, a real commit field is added and the hash chain is retained.

Verification command (example): recompute the sha256 of `experiments/core.py`,
`protocols/graph_data.py` and `results/.data/ind.<dataset>.*` and compare with `config.yaml`.
