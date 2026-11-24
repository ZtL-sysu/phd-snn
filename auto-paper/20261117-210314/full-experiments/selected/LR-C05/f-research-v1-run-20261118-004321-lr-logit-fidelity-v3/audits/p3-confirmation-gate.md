# P3 confirmation gate

The official test masks were not used in v1/v2 selection. After guidance-v3 froze the 2% focal claim, a 63-row test confirmation compared the Jacobian method with top-absolute, A2Q-style, One-Spike-style, uniform and random controls plus full float.

- Logit-MSE reductions: Cora 26.23%, Chameleon 33.99%, Squirrel 25.83%.
- Worst task losses versus the strongest control: 0.47, 1.17 and 1.86 pp, all within the 3 pp bound.
- Same exact padded-bit rows are used.

Verdict: **pass**.
