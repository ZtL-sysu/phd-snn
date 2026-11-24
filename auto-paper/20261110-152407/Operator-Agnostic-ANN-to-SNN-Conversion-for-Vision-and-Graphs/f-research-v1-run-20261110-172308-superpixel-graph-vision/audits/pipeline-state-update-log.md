# Pipeline State Update Log

由 `protocols/update_state.py` 实跑；P0–P3 以本机 smoke 真实证据逐门接受，P3A 起保持 pending（全量在 novix 20049 在途）。

| 校验 | rc | stdout |
|---|---:|---|
| `P1` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  |
| `P1A` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  |
| `P1B` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  |
| `P2` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  |
| `P3` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  |
| `P3A` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  |
| `--workflow-complete (expected FAIL)` | 1 | ERROR: citation_gate: exactly one report file/hash record required for completion |

## 当前状态

- P0 / P1 / P1A / P1B / P2 / P3：`passed`
- P3A → P21：`pending`（全量实验在 4090 在途，结果未回收）
- `--workflow-complete` 预期 rc=1：本地工作流**未**完成，不得进 P6 写作
- `submission_ready = false`
