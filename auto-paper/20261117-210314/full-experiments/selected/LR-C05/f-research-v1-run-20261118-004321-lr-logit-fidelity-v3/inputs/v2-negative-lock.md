# P5 v2 strong-result lock

- LR-A at the main 1% budget fails the ≥20% hidden/logit MSE target. At the predeclared 2% budget, logit MSE reductions are 28.18/30.40/25.85%, but budget selection is outcome-informed and cannot retroactively validate the old task-superiority claim.
- LR-B task-superiority target fails: the Jacobian method does not beat the strongest exact-bit control by ≥1 pp on two graphs.
- LR-D warmed cost passes: overall p95 ratio 1.122× and peak memory ≤218.23 MB.
- Decision: preserve v2 as a negative/repair experiment and start guidance-v3 with a genuinely revised logit-fidelity/ bounded-task-loss claim.

Verdict: **blocked for v2 writing; supersede via guidance-v3**.
