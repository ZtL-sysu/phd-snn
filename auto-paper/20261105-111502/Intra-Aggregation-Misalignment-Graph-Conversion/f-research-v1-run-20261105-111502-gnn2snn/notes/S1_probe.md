# S1 — mechanism separation

Branch **A** selected from measured data.

| quantity | value (pp) |
|---|---|
| inter-layer permutation delta | +0.542 |
| intra-aggregation phase delta | -11.877 |
| ours minus TPP at T=4 | 4.238 |
| ours T=4 / TPP T=4 | 0.7537 / 0.7113 |

The 2x2 design separates the two mechanisms physically, not by definition. The faithful L=3
replay shows that a permuted train can matter when it drives another spiking layer, while the
two-layer membrane accumulator is exactly order-invariant. The two-phase TPP neuron was
re-implemented from Eqs. (8)-(13) of arXiv:2502.14487 because the official codebase is
unreleased; a membrane-proportional Bernoulli variant is reported as a robustness arm.

GP: PASS.
