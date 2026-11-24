# 技能自带校验器的真实输出（round-000）

> 用户 2026-11-07 14:45 提醒：`f-guidance-builder-v1` / `f-research-v1` 是用户自研科研流水线，
> 必须严格按其中的规则与脚本执行。本文件记录**对齐后**用技能自带校验器实跑的结果。
> 命令中的 python 为本机 conda `dyg-cold`。

## 第一次（对齐前，如实保留）

```
validate_guidance.py --strict --packet <packet> <guidance.md>   -> exit 1
  missing required section: Title / Topic / Core Idea / Paper Story / Paper Outline /
  Experiment Plan / Expected Results / Traceability Checklist / Citation Scope /
  Figure and Table Plan or Figure/Table Decision Rules
  missing required guidance element: Secondary metrics / Failure signal /
  Runtime / Hardware Budget / Must appear in paper?
  paper outline must include canonical section 1..6
  strict mode found unresolved placeholder pattern: /:\s*$/
  invalid feasibility packet: feasibility-contract.json not found
pipeline_state.py <state> --before CCFA-startup -> exit 1
  ERROR: contract: nonempty file/hash list required
pipeline_state.py <state> --complete            -> exit 1
  ERROR: contract / readiness / workflow completion requires every stage passed
```

结论：此前按「概括版流程」生成的包**不满足技能契约**。已用
`fly-connectome-cvpr2027/scripts/align_round000_to_skill.py` 按校验器规则修复。

## 第二次（对齐后，当前有效）

```
C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe \
  C:/Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/validate_guidance.py \
  --strict --packet <ROOT>/ccfa-startup-packet <ROOT>/guidance.md
-> "Guidance structure is valid."   exit 0   PASS

C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe \
  C:/Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py \
  <ROOT>/pipeline-state.json --before CCFA-startup
-> "PASS: ordered local workflow evidence and readiness-record checks;
    submission readiness is a separate recorded fact; scientific validity is not inferred."
   exit 0   PASS

C:/Users/xhf/miniconda3/envs/dyg-cold/python.exe \
  C:/Users/xhf/.workbuddy/skills/f-guidance-builder-v1/scripts/pipeline_state.py \
  <ROOT>/pipeline-state.json --complete
-> ERROR: readiness: exactly one file/hash record required for completion
   ERROR: workflow completion requires every stage passed
   exit 1   FAIL (EXPECTED)
```

## 为什么 `--complete` 失败是正确状态而不是缺陷

`guidance-pipeline-state.md` 如实记录 G8 故事门、validation、handoff 仍为 **pending**：
这是实验阶段契约，论文级强结果与 ≥36 篇一手文献尚未产生。技能明确规定
「只有所有 canonical 阶段 passed 才能交付」，因此 `--complete` 必须失败。
**不得**为了让它通过而伪造 stage passed、伪造 readiness 记录或下调 expected_strong。

## 对齐时补齐的技能要求

- `guidance.md`：精确 H2 标题（`## Title / Topic` 等）、`1. Introduction:` …
  `6. Conclusion:` 六节格式、新增 `## Traceability Checklist`（含 `Must appear in paper?`）、
  补齐 `Secondary metrics` / `Failure signal` / `Runtime / Hardware Budget`、
  消除 strict 模式的行尾冒号占位符。
- `ccfa-startup-packet/feasibility-contract.json`：schema 1、`decision: proceed`、
  2 条 claim（19 个实质字符串字段 + `metric_direction` + 4 个数值字段）、
  7 个 startup 文件的 SHA-256 绑定。
- `execution-contract-v1.md`：immutable run-local 契约，记录用户三条指令
  （多机制、无预算异步跨轮、严格按技能）以及「契约里的 runtime_hours 只是可行性估算，
  绝不作为 novix 任务超时参数」这一关键区分。
- `pipeline-state.json` 的 `contract`：10 个文件 + SHA-256 清单，由技能脚本 `--init` 生成的
  ledger 填充，未手编 history、未标记任何 stage passed。

## 结构校验 ≠ 科学有效性

`validate_guidance.py` 只检查结构与占位符；`pipeline_state.py` 只是有序性一致性守卫。
两者通过**不证明**新颖性、结果真实性或图表正确性。P5/P5A/P9/P12 等实质门仍必须靠真实证据。
