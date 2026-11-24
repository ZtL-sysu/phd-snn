# NOVIX ALERT · STEPS_STALL

- time: 2026-11-11T14:30:42.233023
- task: `21247`
- detail: steps frozen at 201 for >20 min; backend=processing placement=submitted

Action required before any resubmission: inspect `novix_watch.jsonl`, `novix --json debug task 21247` and the workspace listing. This watcher never resubmits automatically.
