# NOVIX ALERT · PLATFORM_FAILURE

- time: 2026-11-11T18:13:04.105666
- task: `21524`
- detail: patterns=[]; backend=error; error_info=control-plane execute failed before agent completion: novixlet claim released: runtime exited with code=1, oom_killed=False; rescue_result_json=0

Inspect `novix_watch.jsonl`, `novix --json debug task 21247` and the workspace listing before any decision. This watcher never resubmits.
