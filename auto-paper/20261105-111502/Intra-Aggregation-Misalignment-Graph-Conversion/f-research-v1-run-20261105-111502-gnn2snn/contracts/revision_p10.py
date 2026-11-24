"""P10 concern-to-action revision: remove the falsified inversion claim and reframe honestly.

Actions are KEEP/REWRITE only; no fact, number, citation or equation is altered.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "tex" / "main.tex"
t = p.read_text(encoding="utf-8")

REPL = [
    (r"""\item We \emph{invert} the bound. From the trained weights alone we compute a scalar $\kappa$ and
predict the smallest timestep $\Tstar$ that reaches a target error, then allocate timesteps per
model. This changes what a practitioner can compute: no timestep sweep is needed. A calibrated feasibility band derived from the bound screens all three held-out
graphs correctly and saves \cthreeSaving{} of timesteps on the evaluable ones; the exact
inversion of the sufficient bound is falsified. % run: S5-c3""",
     r"""\item We provide the first controlled \emph{physical} separation of the two misalignment
mechanisms, and use it to falsify the natural inversion of the bound. A linear bound-derived
timestep predictor over-provisions the budget (a $-88.9$\% saving) and fails on every held-out
graph; a conservatism-calibrated feasibility band instead screens reachability correctly on
$3/3$ held-out graphs and saves \cthreeSaving{} of timesteps on the evaluable ones, with an
explicit failure boundary. The negative result is reported with its mechanism. % run: S5-c3"""),
    (r"""present contribution is the mechanism separation, the $\rhon$-weighted bound and the
bound-derived latency rule.""",
     r"""present contribution is the mechanism separation, the $\rhon$-weighted bound and the
calibrated feasibility band with its stated failure boundary."""),
    (r"""Graph ANN-to-SNN conversion error is an exact algebraic object, not noise: the aggregation
operator and its row sum sit inside the identity, which explains both the deterministic bias and
its $\rhon$ amplification. A four-part theorem turns that identity into a usable bound, and
inverting the bound lets a practitioner choose the timestep budget from trained weights instead of
sweeping it. Controlled probes separate this mechanism from the cross-layer phenomenon addressed
by probabilistic spiking neurons, and the resulting closed-form correction is simple enough to
require no randomness and a single hyperparameter.""",
     r"""Graph ANN-to-SNN conversion error is an exact algebraic object, not noise: the aggregation
operator and its row sum sit inside the identity, which explains both the deterministic bias and
its $\rhon$ amplification. A four-part theorem makes that structure explicit, and a controlled
$2\times2$ probe separates it from the cross-layer phenomenon addressed by probabilistic spiking
neurons: their transplant trails the closed-form correction by \soneTppGap{} pp at $T{=}4$,
while perturbing neighbour arrival phases inside one aggregation costs \soneIntra{} pp.
The natural inversion of a sufficient bound is falsified; we replace it with a calibrated
feasibility band that screens unreachable graphs correctly on all three held-out datasets.
The resulting correction is deterministic, requires no randomness, and plugs into standard
aggregations with a single hyperparameter."""),
    (r"""criterion is \cthreePass{}. % run: S5-c3-verdict""",
     r"""criterion is \cthreePass{}. That negative outcome is itself a result: a sufficient
$\rhon$-weighted bound cannot be inverted into exact per-graph timesteps on heterogeneous
graphs, and we delimit where it can be used. % run: S5-c3-verdict"""),
    (r"""On held-out graphs the predicted $\Tstar$ is compared with the true smallest grid timestep""",
     r"""On held-out graphs the calibrated timestep band is compared with the true smallest grid timestep"""),
]

for old, new in REPL:
    if old not in t:
        print("WARN not found:", old[:80])
    t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("P10 revision applied; falsified-claim phrases left:",
      t.count("no timestep sweep is needed"), t.count("inverting the bound lets"))
