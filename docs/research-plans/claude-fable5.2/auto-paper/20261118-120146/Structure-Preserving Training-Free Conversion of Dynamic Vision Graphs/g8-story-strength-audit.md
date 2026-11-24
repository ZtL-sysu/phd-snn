# G8 — Story strength for target tier

## Skeptical-reviewer case

- Why care: training-free conversion promises to reuse trained vision models, but graph conversion has stopped at fixed topology or source retraining; dynamic visual graphs force continuous errors through discrete neighbor and max-winner decisions.
- Prior-work threat: DCGS may already make low-step errors small enough that topology decisions are stable; One-Spike/PMSM/point-cloud work may cover the graph case; local fixed-graph results may show conversion is already solved.
- Distinguishing experiment: measure neighbor and signed-winner disagreement at matched events, then use teacher-neighbor/winner oracles to test whether those discrete errors explain accuracy loss. Matching or beating DCGS-family conversion at the same event budget while recovering structure disagreement is the decisive method result.
- Strong threshold: at least 50% recovery of baseline structure-disagreement loss and at least half of both-oracle accuracy recovery, with <=1 pp teacher accuracy gap and no higher event count.
- Honest lower story: if structure is naturally stable, report the negative diagnostic and pivot to the streaming-graph or fair-energy direction under a versioned replacement contract; do not repackage it as a weak method paper.

## Top-tier fit

- The contribution is a mechanism and method for discrete structure preservation, not a dataset substitution.
- Evidence tests the causal chain from quantization error to neighbor/winner flip to accuracy loss.
- Baselines and falsifiers are explicit.
- Local resources can complete the first discriminating experiment.

Gate verdict: `pass`, conditional on observed evidence meeting the strong-result lock before drafting.
