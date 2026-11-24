# NOVIX ALERT · STEPS_STALL

- time: 2026-11-11T14:30:42.233023
- task: `21247`
- detail: steps frozen at 201 for >20 min; backend=processing placement=submitted

Action required before any resubmission: inspect `novix_watch.jsonl`, `novix --json debug task 21247` and the workspace listing. This watcher never resubmits automatically.

## 复盘结论（14:35）

**误报**。steps 201→203、`project/` 目录 mtime 从 05:07 推进到 06:05、MNIST_v2.zip 完整 192378381 B、无 backend error。
steps 是 agent 对话轮次，单条全量训练命令不会使其增长；已把判据改为「workspace 产物 mtime + steps 双冻结 45 min」，见 `watch_novix_v3.py`。
