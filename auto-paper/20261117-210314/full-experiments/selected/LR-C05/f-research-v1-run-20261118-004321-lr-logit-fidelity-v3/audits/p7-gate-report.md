# P7 gate report

## Decision

**PASS after one structural merge.** The accepted draft is `writing/arc-draft-v3/stage-17/paper_draft.md`; the external reverse outline is `writing/arc-draft-v3/reverse-outline.md`.

## Execution

- AutoResearchClaw Stage 17 `PAPER_DRAFT` control flow was executed from the installed ResearchClaw 0.3.1 checkout.
- The external writer was Codex CLI 0.169.0-alpha.11.1 through `acpx` 0.19.2 and the ACP-compatible agent interface.
- Three bounded `writing_adapter.py` calls supplied the clean title/introduction, method/setup, and results/discussion/conclusion tasks.
- ARC historical context, raw logs, and the anti-simulation compatibility fixture were not sent to the external model.
- The only non-writing availability probe asked the agent to reply `OK`; it contained no research content.

## Evidence checks

| Check | Result |
|---|---|
| Exactly six canonical numbered sections | pass |
| Complete Method and Experiments and Results | pass |
| F1-F9 evidence present with units, aggregation, and scope | pass |
| Matched total padded serialized-bit wording | pass |
| 1.86 pp mean and 2.85 pp seed-level task loss | pass |
| Timing range 1.020-1.124x and 218.23 MB | pass |
| Held-out confirmation after validation exposure | pass |
| Negative task-superiority result preserved | pass |
| No novelty, SOTA, energy, temporal-event, or broad-GNN claim | pass |
| Reverse outline and paragraph-purpose map | pass |
| No placeholders or generated References section | pass |

## Structural repair

The initial model draft repeated the detailed result inventory in subsection 4.2 before reporting it again in 4.3-4.5. The repeated paragraphs were merged out of 4.2 without changing scientific facts. The repair is recorded in `writing/p7-structural-revision.md`.

## Length judgment

The final draft is approximately 2,020 words after removing duplicated results. With no target journal or author numeric length requirement, the workflow requires completeness and proportionality rather than a default page threshold. The draft contains the complete question, method, protocol, main and supporting results, negative finding, limitations, and bounded conclusion; it is accepted as a complete first draft for figure insertion and review.
