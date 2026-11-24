# round-023 · 本机结构缺陷修复留痕（contract v1 → v2）

连续 3 轮（021/022/023）复现的缺陷：`contract` 把**可变追加型** `experiment-traceability.md` 绑为不可变 sha256，实际哈希漂移，使 `--before P0` / `--complete` / `--submission-ready` 全部 rc=1。

修复（严格按交接项 5）：
1. 备份原状态 `pipeline-state.json.bak-pre-contract-v2-round023`（不覆盖、保留失败证据）。
2. 冻结版本化快照 `contract-snapshots/experiment-traceability-frozen-v2.md`（当前可变日志的精确字节副本，sha256 `dafea5c70e9cf4cc0aa8a845fa7ef8a01988005e23ebf22d2714a000d2358ba0`）。
3. 不可变契约文件 `execution-contract-v2.md`（记录缺陷、修复、证据路径）。
4. `contract_version: v1 → v2`；contract[0] 改绑冻结快照；追加 v2 契约文件为第 11 条。
5. history 追加**一条真实 `reopen` 事件**（`pipeline_state.py` 认可的合法 action），不追加任何 `pass` 事件。
6. 26 个 stage 的 `contract_version` 同步为 v2，**status 一律保持 pending**；`readiness=[]` / `citation_gate=[]` / `delivery_mode=preparation` 未动。

**未做**：未标任何 passed、未启动 P0、未推进任何科学 gate、未 pull/判定任何 novix 结果、未修改可变日志本身、未下调任何 expected_strong。`workflow_complete` 与 `submission_ready` 仍为 false（本项目后者恒 false）。

修复后仍须实跑三个校验器并如实记录 rc（见 `rounds/round-023.md`）。结构校验通过**不等于**科学有效，也不等于 P0 已完成。
