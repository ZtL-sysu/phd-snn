# Failure diagnostics — novix task 17788 (round 002 recovery)

- Recorded at: 2026-11-07T21:34:40+08:00
- Recorded by: 6-hour automation round 002, Step 0/1 (`POLL_NOVIX` → `FAILED`)
- Task: `17788`, idea `C1` ("Real optical flow external validity of membrane-state gain"),
  resource pool `exp-4090`, submitted 2026-11-07T16:10:25+08:00 (no `--max-turns`, no `--timeout`).
- Guidance dir: `C:/code/phd-snn/auto-paper/20261107-154000/Does-Membrane-State-Transfer-to-Real-Optical-Flow`
- f-research run root: `f-research-v1-run-20261107-154500-membrane-state-transfer` (`pipeline_stage=P4`)

## Verdict of this check

`FAILED` — a **platform-side backend failure terminal state**, NOT a running task, NOT a
scientific negative result, NOT `REJECT_INVALID`, and NOT a `rc=4` transport error.
No result files exist, so no `acceptance-verdict.md` may be written and no science claim
may be derived. Evidence is preserved; nothing is fabricated.

## Cross-checked evidence (three independent novix commands, all consistent)

1. `novix --json task result 17788` → parsed JSON terminal state:
   - `status: "error"`, `errorCode: "1"`, `steps: 2`,
     `finalReply: "API Error: stream error: stream disconnected before completion: stream closed before response.completed"`.
   - Note: the CLI exit code is `1` for a task in the `error` terminal state. This is **not** `rc=4`
     (transport read timeout). `scripts/check_inflight.py` conservatively records any `rc != 0` as
     `transport_error_retry`, which is why its 21:20:09 poll was logged that way; the retry below
     re-parsed an explicit JSON `status` field, which is the authoritative terminal signal per the
     playbook ("only a parsed JSON status decides a terminal state").
2. Retry (independent invocation, parsed with a JSON reader):
   - `rc=1`, `PARSED status = error`, `steps = 2`, `errorCode = 1`, `finalReply` identical.
   - Confirms a stable terminal state, not a transient read failure.
3. `novix --json task get 17788` → top-level `"status": "error"`, `createdAt 16:10:25`,
   `updatedAt 16:28:24`, `version 2`, two step records: the user trajectory (16:11:11) and an
   assistant message (16:27:57) whose entire content is the same `API Error: stream error ...`.
4. `novix debug task 17788 --logs` →
   - `backend.status: "error"`, `error_code: "1"`; `task.status: "failed"`.
   - `placement.state: "released"`, `pool: "exp-4090"`, `gpu: 1`, `node: aliyun-hz-exp-4090-2`,
     `dispatch_phase: "invoking"`, `pool_status.dispatch_paused: false`, `eligible_nodes: 2`.
   - `runtime_failure.exit_code: 143` (SIGTERM), `oom_killed: false`, disk healthy (~1.01 TB free).
   - `diagnosis: "ALLOCATION_EVIDENCE_UNAVAILABLE"`, `next_step: "Nomad 暂不可达或历史记录已回收；保留任务记录，不要直接重新派发。"`.
   - `runtime_logs.stderr` shows the container started normally, then shut down; the SDK runner
     raised `Unknown SDK error (subtype=success)` with
     `[claude-code:unrecognized_model] {"model":"gpt-5.6-sol(max)","query_source":"generate_session_title"}`
     — i.e. the platform's own session-title model is unrecognized and the LLM stream closed before
     completion. The remote agent never reached experiment code.

## Why the experiment never ran

- `steps: 2` and the single assistant message consist only of the API error string. The task died
  at the platform's session-title / first-response stage, ~18 minutes after submission.
- `novix debug pull task:17788 <pull_dir>` was attempted at 21:2x and returned
  `novix: track-ops ... does not answer /healthz; set NOVIX_TRACK_OPS_URL ...` — the platform's
  artifact-tracking service is unreachable. No `pulled/` workspace was produced.
- Local `novix/` contains only `query.txt` (6114 bytes) and `create-response.json` (70 bytes);
  **no `experiment.py`, no `result.json`, no staged result, no raw logs**.

## Classification relative to the inherited failure (task 17682)

| | task 17682 (round 000) | task 17788 (this round) |
|---|---|---|
| Platform status | `finish` (nominally successful) | `error` (explicit backend failure) |
| Remote artifacts | empty `project/`, only hardware report | none; agent never started |
| Root cause | remote run produced no experiment/results | platform SDK stream disconnect + unrecognized model |
| Verdict | `REJECT_INVALID` (guidance §6) | `FAILED` / `RECORD_FAILURE` (playbook Step 1) |
| Hardened query applied? | legacy v1 budget params | yes: staged `result.json` + `experiment.py`-first requirements were in `query.txt` |

The 17682-style hardening in `query.txt` was never exercised, because the platform failed before
any user code could run. **This failure cannot be attributed to the query, the experiment design,
or the science.** It must not be recorded as a negative finding.

## Decision for this round (per WORKFLOW-PLAYBOOK.md v2)

- Step 0/1: status `SUBMITTED` → `FAILED`; `next_action` `RECORD_FAILURE`.
- Step 3: rewrite `IN-FLIGHT-TASKS.md`, append one `WORKFLOW-INDEX.md` line, write
  `rounds/round-002.md`.
- Step 5 serial constraint: the C1 primary line is **not qualified** (no `**Overall:** >= 8.0`
  paper, no P21). Therefore this round's five new candidates are **scored for ranking only and
  appended to `candidate_pool` as backups**; no new paper/guidance/novix submission is started.
- Playbook §5 ("平台返回超时类终态"): "如实记录；视为 `FAILED` 证据，下一轮按**新设计**重提，
  不重复同一实验". So the replacement of the P4 full-experiment batch is **deferred to the next
  round's Step 0**, and must use a NEW hardened design — never a verbatim resubmission of 17788.
- `pipeline_stage` stays `P4`; the f-research run root is untouched (no `--before P5`, no P5
  strong-result lock, no writing stages). No `acceptance-verdict.md` is written.

## Next round's first action (recorded, not executed now)

1. Re-check platform health (`track-ops /healthz`, `pool_status`, a cheap probe task) before
   spending another `exp-4090` slot; if the backend is still broken, record and stop again.
2. Once healthy, submit the C1 P4 **full experiment batch** under a **new design** that reduces
   single-session length (split stage A / B / C into separate short tasks, each writing its own
   `experiment.py` + staged `result.json` immediately), still with **no** `--max-turns`,
   `--timeout`, or blocking `watch`.
3. Keep all of this file, `query.txt`, `create-response.json`, and the two earlier failures as
   preserved evidence. Do not delete or rewrite them.

## Honesty statement

No experiment numbers, accuracies, CIs, scores, or `Overall` values were produced by this task.
Nothing in this file is a scientific result. No credentials appear here.

## Appendix — round 003 re-check (2026-11-08 04:1x GMT+8), append-only

**Platform health is RECOVERED.** Four independent signals this round:

1. Direct HTTPS `GET /track-ops/healthz` → **HTTP 200**, body begins
   `{"ok":true,"version":"2026-10-23.1","ws_root":"/mnt/novix-k8s-workspace-root","ws_root_mounted":true...}`.
   (Note: `novix track curl /healthz` still fails with a CLI traceback; that is a CLI path issue,
   not a server failure. The `/docs` and root `/healthz` paths return 404 and `/api/healthz` returns
   401 as expected for those endpoints. Only `/track-ops/healthz` is the relevant probe.)
2. `novix debug ls task:17788 -L 1` → **rc=0**, lists the workspace tree (`.claude`, `.runtime_data`,
   `project`, `search_results`, `user_data`, `writing_space`). track-ops artifact service is readable.
3. `novix --json debug task 17788 --logs` → `pool_status.dispatch_paused = False`,
   `pool_status.eligible_nodes = 2`, `placement.pool = exp-4090`. Resource pool is dispatching.
4. `novix --json task list` → **rc=0**, main API and login state (`track whoami`,
   `kind=platform`, user 637) are intact; recent sessions include several "please only reply OK"
   probes and a successfully executed, already-written GPU experiment script session, i.e. the
   backend agent is able to run scripts again.

**RETRY_PULL executed and the FAILED verdict is confirmed, not reversed.**

- First attempt into the original long `novix/pulled-recheck-003` path failed with
  `[WinError 206] 文件名或扩展名太长` (Windows MAX_PATH on a deep `.claude/plugins/...` path).
  This is a **local path-length issue, not a platform failure**.
- Retry into short path `C:/code/phd-snn/pull003` → **`done`, rc=0**, 1282 files pulled.
- Inventory: `project/` has **0 files**; `writing_space/`, `user_data/`, `search_results/` each
  have 0 files; **no `experiment.py` and no `result.json` anywhere outside `.claude/skills`
  plugin templates** (0 scientific artifacts).
- `agent.log` for `task_17788` ends at `Workspace runtime env prepared` (2026-11-07 08:11:08 UTC);
  there is no subsequent tool execution. The remote agent never reached experiment code.

Therefore the round-002 classification stands: `17788` is a **platform-side backend SDK
failure with zero experiment output**, NOT a scientific negative result, NOT `REJECT_INVALID`,
and NOT a `rc=4` transport error. No `acceptance-verdict.md` may be written (no `result.json`).
This round does not re-adjudicate it.

**Consequence for round 003** (per `WORKFLOW-PLAYBOOK.md` §5 "平台返回超时类终态" and the
round-002 handoff): with the platform healthy again, the correction loop's first step
"修当前方案" now proceeds by submitting the **C1 P4 full experiment batch under a NEW design**
(shorter separate sessions, each sub-task writes `experiment.py` + staged `result.json`
immediately, hardened query), with **no** `--max-turns`, **no** `--timeout`, and no blocking `watch`.
The original `17788` query is NOT resubmitted verbatim. All prior failure evidence is retained.

No experiment numbers, scores, or `Overall` values were produced by this re-check.
No credentials appear here.

## Appendix — round 011 (2026-11-08 21:28–22:0x GMT+8), append-only

**Task `18489`（C1 attempt #6，query-round010-attempt6.txt）在本轮执行期间发生状态跃迁：
`processing` → 平台终态 `error`。本段只追加新事实，不改动任何历史行。**

### 时间线与权威证据

| 时刻 (GMT+8) | 命令 | 结果 |
|---|---|---|
| 21:28–21:31 | `check_inflight.py` | `{"checks":[{"task_id":"18489","outcome":"still_running"}]}`，脚本只查+更新文档 |
| 21:29 | `novix --json task result 18489` | rc=0 `{"status":"processing","steps":0}` |
| 21:30 | `novix --json task get 18489` | rc=0 `status=processing`、`steps=null`、`createdAt=updatedAt 20:20:15`、`errorCode=null`、`errorInfo=null`、`version=2`、无 `finalReply` |
| 21:31 | `novix debug task 18489 --logs` | `backend.status=processing`；`task.status=provisioning` "creating sandbox claim"；`placement.state=reserved`、`pool=exp-4090`、`node=aliyun-hz-exp-4090-2`、`dispatch_phase=preparing`；`pool_status.dispatch_paused=false`、`eligible_nodes=1`；`runtime_logs.source=unavailable`；`diagnosis=ALLOCATION_EVIDENCE_UNAVAILABLE` |
| **21:34** | 收尾复核 `novix --json task get 18489` | **`status="error"`、`errorCode="1"`、`updatedAt 21:34:21`、`steps=null`**，`errorInfo`：`stale task auto-reconciled: sandbox became unhealthy before completion callback (novixlet claim failed: node release allocation identity is missing or changed; final synchronization not proven)` |
| 21:35 | 收尾复核 `novix --json task result 18489`（首次读超时，按 rc=4 传输错误规则重试一次） | 首次输出 `The read operation timed out`；**重试 rc=0 解析到 JSON**：`{"status":"error","errorCode":"1","steps":0,"errorInfo":"stale task auto-reconciled: ..."}` — **不是把传输错误误判为任务失败**，是重试后解析到明确 JSON 终态 |
| 21:36 | `novix debug task 18489 --logs` | `backend.status="error"`、`error_code="1"`、`task.status="failed"`、`message` 同上；`placement.state` 仍 `reserved` / `dispatch_phase` 仍 `preparing`（**从未进入 invoking**）；`runtime_logs.stdout=""`、`stderr=""`、`source="unavailable"`；`runtime_failure={}`；`artifact_sync=null`；`diagnosis=ALLOCATION_EVIDENCE_UNAVAILABLE` |
| 21:37 | `novix debug ls task:18489 -L 2` | `no session matches session_8ef44763296cb15e116f177f30481b13 under /mnt/novix-k8s-workspace-root` — **远端工作区根本不存在**，零产物 |

### 判定：`FAILED` / 平台侧沙箱故障（与 17788 同类）

- **不是**科学负结果 / 机制否证：**远程 agent 从未执行任何实验代码**
  （`steps=0`、无 `finalReply`、`runtime_logs` 全空、工作区未创建、
  `dispatch_phase` 停在 `preparing`）。没有任何 accuracy / delta / CI / p 值产出。
- **不是** `REJECT_INVALID`：那条需要平台 `finish` 且拉回工作区后缺
  `result.json`；此处平台自身报错 `error`、工作区不存在。
- **不是** `rc=4` 传输误判：首次读超时按规则**重试一次**，重试解析到
  明确的 JSON `status=error` 终态才判定。
- **不是** 达标、**不是** `design_invalid`、**不是** `INPUT_BOTTLENECK`、
  **不是** 阴性对照/实现层诊断结果（三项必修诊断一项都没跑）。
- 根因（平台原文）：stale task auto-reconciled — 沙箱在完成回调前变为
  unhealthy，novixlet claim 失败（节点释放时 allocation identity 缺失或变更），
  **final synchronization not proven**。平台调度/节点层问题，
  **不能归因于 query、实验设计或科学命题**。

### 后果（v3 §3.6 死磕）

1. attempt #6 的假设「梯度路径是未被检验的自变量」**仍然未被检验**
   （不是被否证）；`expected_strong(+0.25)` / `minimum(+0.15)` /
   真实域 ceiling 0.70 门槛**均不下调**，三项必修诊断继续有效，失败证据不删。
2. 本轮**不重提**：Step 0–7 全程按「在途」正确执行，本轮已交付一次实质优化
   （`query-round011-attempt7-DESIGN-DRAFT-NOT-SUBMITTED.txt`，
   四要素 + 与 attempt #6 的机制级 diff）。按 §3.6(2)「同一 idea 在途不重复提交」
   与 playbook §5「平台返回超时类终态 → 下一轮按**新设计**重提，不重复同一实验」，
   重提交 round-012 Step 0。
3. **平台故障不构成放弃理由**（§3.6(4) 明文）。
   `abandon_allowed=False` 不变：`(a) 6/6 尝试、(b) 0/2 kill、(c) 0/2 不可修复评审`。
   本次**不计入** kill criteria 独立命中（无有效实验、无科学数值）。
4. 不写 `acceptance-verdict-18489.md`（无 `result.json`）、不进 P5、
   不写论文、不标任何 stage passed（26 阶段仍全 pending、history 空）。
5. round-012 首动作：先查平台健康（`/track-ops/healthz`、
   `pool_status`、`debug ls` 可读性，参照 round-003 的四信号流程），
   健康后以**新设计**（不得原样重提 `query-round010-attempt6.txt`）
   无预算参数重提；仍 unhealthy 则如实记录收尾，不刷额度、不绕行。

### 诚实性声明

本段每个状态与字段均来自上面列出的 novix 命令输出，无推断、无补数、
无编造数值 / 分数 / Overall、无凭据。`18489` 未产出任何实验结果；
本文件不把平台故障写成科学结论、也不删改任何历史失败证据。

## round-012 附录（2026-11-08 23:5x GMT+8）：attempt #7 提交首次 rc=4 传输错误

- 命令 `novix task create --json <query-round012-attempt7.txt> --provider novixlet
  --resource-pool exp-4090 --gpu --gpu-count 1`（`CMD_ARGV_GUARD_OK argc=12`，
  **无** `--max-turns` / `--timeout` / `--watch`）首次返回 **rc=4**：
  `novix: POST https://novix-platform-test.8-233-45-156.sslip.io/api/chat_session/create
  -> The read operation timed out`。按 playbook §5「`novix` 读超时 rc=4 属传输错误，
  重试一次；绝不误判为任务失败」，**这不是平台拒绝、不是安全审核拒绝、不是任务失败**。
- 权威复核（避免重复提交）：
  · `novix --json task list` 的 `local` 最新条目仍为 `18489`（20:20:13），
    **无新 task_id / session_id 记录** → CLI 未完成 create 流程。
  · 服务端 `sessions` 出现 `b6631769bf9e23a51a4b29237580ca14`
    （created=updated `2026-11-08 23:55:13`、creatorUserId=637），
    `title` 正是本轮 attempt #7 query 全文 → POST 已在服务端创建 **chat_session**，
    但读响应超时使 CLI 未拿到返回。
  · `novix debug ls b6631769bf9e23a51a4b29237580ca14 -L 1` →
    `no session matches ... under /mnt/novix-k8s-workspace-root`
    → **无 sandbox workspace、无 task 派发、远程 agent 从未执行实验代码**。
  · 平台健康四信号在此前后均为健康（`/track-ops/healthz` 200
    `ws_root_mounted=true`、`whoami` user 637、`dispatch_paused=false`、
    `eligible_nodes=1`、`debug task` 可读）→ 属链路读超时，非服务端不健康。
- 结论：该 chat_session 是**孤儿会话，无关联 task、零产物**。
  按 §5 重试一次提交（新建 session + 派发 task），**不会造成重复实验**。
  同平台账号下 23:37 的两个 `R63-N10/N11` 会话属于另一条无关研究链，本任务不触碰。

### round-012 收尾更正（覆盖上方「孤儿会话、无 task」初步判断）

上方首次 rc=4 的核查结论需要**更正一处**：第二次提交（重试那一次）虽也返回
rc=4（这次超时点为 `POST /api/task/create_task`），但**服务端确已创建 task `18533`**。
权威证据链（全部 rc=0 / 可解析，非推断）：
- `novix --json task get 18533` → `status=processing` / `n_steps=27` /
  `createdBy=637` / `createdAt 2026-11-08 23:58:44` / `updatedAt 2026-11-09 00:05:24`
  （持续增长）/ `chatSessionId=005445c57cbb058aa667f9b55ae45ff7`。
- step 内容含 `attempt #7` / `measurement_identifiability` /
  `known_signal_injection` / `round-012` → **确认是本轮合并 query**。
- `novix debug ls 005445… -L 1` → workspace 存在，含 `project/`、`progress.md`、
  `.novix_run_identity.json` 等 → **远程 agent 已开始执行、正在跑**。
- `novix --json task result 18533` 首次 rc=4（传输错误）→ 按规则**重试一次**
  rc=0 解析到 `status=processing` / `steps=27` / `errorCode=None` / 顶层
  `finalReply` 为空 → **真在跑，不是终态、不是失败**。
- 精确单线程 `get_task` 扫描 18528–18555：23:55 时段无 createdBy=637 的 task，
  只有 `18533`（23:58:44, 637）。→ 首次 rc=4 只留孤儿 chat_session
  `b663…` **无 task**；重试那次留下 `18533` **唯一一个 task**。
  **没有重复提交、没有第三次提交**（playbook §5 的 rc=4 只重试一次已遵守）。
- `18533` 登记为 `SUBMITTED` / `POLL_NOVIX`，本轮**不等结果**，
  由 round-013 Step 0 异步回收。
