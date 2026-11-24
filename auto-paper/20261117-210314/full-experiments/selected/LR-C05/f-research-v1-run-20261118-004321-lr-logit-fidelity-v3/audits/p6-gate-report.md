# P6 gate report

## Decision

**PASS.** The accepted P6 output is `writing/arc-outline-v3/stage-16/outline.md`.

## Gate checks

| Check | Result | Evidence |
|---|---|---|
| P5/P5A predecessors passed | pass | `pipeline-state.json` |
| Clean manuscript packet built | pass | `writing/packet.json` |
| Writing adapter request built | pass | `writing/request-p6.json` |
| AutoResearchClaw Stage 16 executed | pass | `writing/arc-outline-v3/stage-16/outline.md` |
| Exactly six canonical numbered sections | pass | `writing/arc-outline-v3/executor-context-audit.json` |
| Section-purpose and fact-ID map present | pass | `writing/arc-outline-v3/stage-16/outline.md` |
| Core evidence and qualifiers preserved | pass | F1-F5 in `writing/packet.json` and outline |
| Output complete and not truncated | pass | `finish_reason=stop`, `truncated=false` in executor audit |
| External context isolated from ARC history | pass | `writing/arc-outline-v3/executor-context-audit.json` |

## Accepted outline

The numbered body is exactly:

1. `Introduction`
2. `Related Work`
3. `Method`
4. `Experiments and Results`
5. `Discussion`
6. `Conclusion`

The outline uses the required phrase **matched total padded serialized-bit budget**, preserves the 1.86 percentage-point three-seed-mean and 2.85 percentage-point seed-level task losses, reports timing as `1.020-1.124x`, and identifies the official-test run as held-out confirmation after validation exposure.

## Executor and context boundary

- AutoResearchClaw checkout: `C:\code\AutoResearchClaw`
- ResearchClaw version: `0.3.1`
- Stage implementation: `researchclaw/pipeline/stage_impls/_paper_writing.py`
- External model: configured `deepseek-v4-pro`; response model `deepseek-v4-pro`
- Boundary status: verified clean external boundary
- The installed Stage 16 control flow was executed, while the external model call consumed only `writing/request-p6.json` messages plus one format-only correction.
- ARC analysis, decision, history, raw experiment logs, and its historical context preamble were not sent to the external model.

## Preserved failed attempts

- `writing/arc/stage-16/outline.md`: first CLI output, truncated and lacking the canonical outline.
- `writing/arc-outline-v2/`: isolated Stage 16 output, complete JSON but rejected because P6 requires a Markdown canonical six-section outline.
- `writing/arc-outline-v3/`: corrected format-only rerun and accepted P6 evidence.

## Remaining boundary

P6 establishes structure and evidence mapping only. The 36-reference authenticity, relevance, placement, and duplicate-version audit remains mandatory before any novelty or state-of-the-art language.
