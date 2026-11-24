# 20049 教训对照清单（21247 任务）

> 用户 13:03 指令：「盯着 novix 的跑，不要再犯 20049 那样的问题了」。逐条落实如下。

| # | 20049 的问题 | 本次对策 | 状态 |
|---|---|---|---|
| 1 | `queued / NO_ALLOCATION` 卡约 3 小时才发现 | 提交前先跑最小探针 `21224` 验证分配；加固盯梢每 **180 s** 探测，`queued/reserved` 持续 >15 min 立即 `NOVIX_ALERT.md` | ✅ 已落实 |
| 2 | 分配后执行撞 429 usage limit + `unrecognized_model` 失败，长时间未识别 | 盯梢每次解析 `backend.error_info`，命中 `429 / usage limit / unrecognized_model / request rejected / api error / sdk error / OOM` 或 `backend.status∈{error,failed}` 立即告警并**抢救 pull** | ✅ 已落实 |
| 3 | 主 API rc=4/503 与带外不一致，差点误判 | 每次同时查主通道与 `debug task`；主通道失败时以带外 `backend.status` 为权威，两者都写进 `novix_watch.jsonl` | ✅ 已落实 |
| 4 | 平台报 finish/processing 但零产物 | 终态判据写死为「解析到终态 status + `finalReply` + 可 pull 的 `project/result.json` + SHA-256」，缺一不算完成；失败终态也先抢救 pull | ✅ 已落实 |
| 5 | agent 卡住无提示 | `steps` 20 分钟不增长 → `STEPS_STALL` 告警 | ✅ 已落实 |
| 6 | 深 run-root 路径 pull 触发 `WinError 206` | 先 pull 到短路径 `C:/tmp/tp21247`，再用 `\\?\` 长前缀同步到 `novix_delivery/`；短路径 pull 已在 `21224` 实测成功 | ✅ 已落实 |
| 7 | `result.json` 写到 `/home/novix/workspace/` 而非可 pull 的 session workspace | v2 query 内置 `summarize.py`：生成顶层 `result.json`/`README`/`run.log` 并**自动同步**整个 `project/` 到 `/mnt/.../session_*/workspace`；盯梢终态再校验 `result.json` 存在 | ✅ 已落实 |
| 8 | 排队时反复查询却迟迟不决策 | 盯梢**从不自动重提**；任何异常只写告警并退出，由人判断。已取消的 `21237` 有明确取消记录 | ✅ 已落实 |

## 补充：本次已验证的实测证据

- `21224` 探针 `finish`（57 步）：Python 3.11.18 / torch 2.11.0+cu130 / CUDA true / RTX 4090，无 429、无 unrecognized_model。
- `21247` 已 `submitted` 到 `aliyun-hz-exp-4090-1`，`dispatch_phase=invoking`，`backend.status=processing`、error_code 空、pool `eligible_nodes=2 / dispatch_paused=False`。
- 代码载荷已还原到**可 pull 的** `project/protocols/`（vision_pipeline.py 19037 B、run_e17.py 8268 B）与 `project/teacher_probe/`（run_all.py、run_bcd.py、summarize.py、run_all.sh）。
- 运行时日志 `/call_agent_v2` 200 OK；stderr 只有 `autoresearch` skill 包为空与 FastAPI DeprecationWarning，非致命。

## 当前观察窗口（需继续盯）

13:03 时 `steps=27`，`project/data` 尚未出现 —— 可能处于数据下载（两个 zip 共约 509 MB）或脚本准备阶段。加固盯梢会在 20 分钟 steps 停滞时告警；同时每次探测记录 `artifact_sync`、`diagnosis`、`pool`，便于复盘。

## 判定纪律

- 只有「终态 + finalReply + `project/result.json` + SHA」四件套齐备才算完成。
- 任何告警先读 `novix_watch.jsonl` 与 `NOVIX_ALERT.md`，再决定，不盲目重提。
- 不把 `processing` 当成「在跑实验」的结论；以 workspace 产物（CSV/快照/result.json）为准。
