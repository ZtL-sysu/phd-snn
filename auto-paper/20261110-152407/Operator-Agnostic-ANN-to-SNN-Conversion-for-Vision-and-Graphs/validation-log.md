# Validation Log

所有命令由 `protocols/finalize_contracts.py` 在 `dyg-cold` 环境实跑，返回码如实记录。

| 命令 | rc | stdout |
|---|---:|---|
| `pipeline_state.py --init` | 0 | Initialized pending ledger; populate contract files and hashes before execution. |
| `--before G0` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G1` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G2` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G3` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G4` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G5` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G6` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G7` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before G8` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before validation` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--before handoff` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `--complete` | 0 | PASS: ordered local workflow evidence and readiness-record checks;  submission readiness is a separate recorded fact; scientific validity is not inferred. |
| `validate_guidance.py --strict --packet` | 0 | Guidance structure is valid. |
| `delivery_readiness.py` | 0 | {   "ok": true,   "delivery_mode": "preparation",   "submission_ready": false,   "deferred_items": 7,   "pending_items": 7,   "errors": [] } |
| `--submission-ready (expected FAIL)` | 1 | ERROR: --submission-ready requires state delivery_mode=submission-ready |

## 结论

- `guidance.md --strict --packet` 与 12 门 `--before` / `--complete` 全部为 rc=0。
- `--submission-ready` 预期为 rc=1（作者管理事实待决，`submission_ready=false`），不是失败。
- 校验器只证明结构与哈希一致性，不证明科学正确性；科学结论以三轮独立红队与 M0 实跑证据为准。
