"""Adapt downstream generators and manuscript wording to the repaired C3' result keys.

No number is changed here; only key names and the honest framing of a falsified claim.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(rel, pairs):
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in t:
            print("WARN not found in", rel, ":", old[:78])
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")
    print("patched", rel)


patch("experiments/make_paper_assets.py", [
    ('"cthreeC": "%.4g" % c3["fit"]["c"]',
     '"cthreeC": "%.4g" % c3["fit"]["delta"]'),
    ('"cthreeUniform": str(c3["controls"]["uniform_T"])',
     '"cthreeUniform": str(c3["controls"]["uniform_T_calibration"])'),
    ('"cthreeShufReal": "%.3f" % c3["controls"]["shuffled_kappa"]["real_mean_log2_error"]',
     '"cthreeShufReal": "%.2f" % c3["controls"]["shuffled_kappa"]["real_screening_accuracy"]'),
    ('"cthreeShuf": "%.3f" % c3["controls"]["shuffled_kappa"]["shuffled_mean_log2_error"]',
     '"cthreeShuf": "%.2f" % c3["controls"]["shuffled_kappa"]["shuffled_screening_accuracy"]'),
    ('"Uniform-$T$ budget & \\\\multicolumn{5}{r}{$T{=}%d$} \\\\\\\\" % ctrl["uniform_T"]',
     '"Uniform-$T$ budget & \\\\multicolumn{5}{r}{$T{=}%d$} \\\\\\\\" % ctrl["uniform_T_calibration"]'),
])

patch("experiments/make_audits.py", [
    ("fit['c']:.6g", "fit['delta']:.4g"),
    ("ctrl['uniform_T']", "ctrl['uniform_T_calibration']"),
    ("ctrl['shuffled_kappa']['real_mean_log2_error']:.3f",
     "ctrl['shuffled_kappa']['real_screening_accuracy']:.3f"),
    ("ctrl['shuffled_kappa']['shuffled_mean_log2_error']:.3f",
     "ctrl['shuffled_kappa']['shuffled_screening_accuracy']:.3f"),
    ("v['heldout_total']", "v['evaluable_graphs']"),
    ("| held-out graphs passing | {v['heldout_passed']} / {v['heldout_total']} | >= 3 |",
     "| evaluable held-out graphs passing | {v['heldout_passed']} / {v['evaluable_graphs']} | all |"),
])

patch("tex/main.tex", [
    ("and the bound-derived allocation\nreaches a $1.5$\\,pp target with \\cthreeSaving{} fewer timesteps than a uniform budget on held-out\ngraphs. % run: S5-c3",
     "and a calibrated feasibility band derived from the bound screens unreachable graphs\ncorrectly on all three held-out datasets and saves \\cthreeSaving{} of timesteps on the evaluable\nones. Exact per-graph inversion of the sufficient bound is falsified and reported. % run: S5-c3"),
    ("On held-out\ngraphs it saves \\cthreeSaving{} of timesteps against a uniform budget. % run: S5-c3",
     "A calibrated feasibility band derived from the bound screens all three held-out\ngraphs correctly and saves \\cthreeSaving{} of timesteps on the evaluable ones; the exact\ninversion of the sufficient bound is falsified. % run: S5-c3"),
    ("The fitted\nconstant is $c=\\cthreeC{}$ with a $\\Tmin$--$\\kappa$ correlation of $r=\\cthreeR{}$ on the fitted\ngraphs. % run: S5-c3-fit",
     "A sufficiency-calibrated fit\n$\\log_2\\Tstar=a+b\\log_2\\kappa+\\delta$ on the fitted graphs gives $\\delta=\\cthreeC{}$ with\n$r=\\cthreeR{}$. % run: S5-c3-fit"),
    ("The shuffled-$\\kappa$ control has a mean log$_2$ prediction error of \\cthreeShuf{} versus\n\\cthreeShufReal{} for the true geometric signal, so the gain is attributable to the bound's\n$\\rhon$ term rather than to a generic constant. The pre-registered \\texttt{expected\\_strong}\ncriterion is \\cthreePass{}. % run: S5-c3-verdict",
     "Shuffling the graph--$\\kappa$ assignment drops reachability-screening accuracy from\n\\cthreeShufReal{} to \\cthreeShuf{}, so the screening signal comes from the bound's calibration\nrange rather than from a generic constant. The pre-registered \\texttt{expected\\_strong}\ncriterion is \\cthreePass{}. % run: S5-c3-verdict\n\n\\paragraph{Falsification of exact inversion.} The first, linear inversion of\nTheorem~\\ref{thm:g1}(d) over-provisioned the budget and produced a negative timestep saving\n($-88.9$\\%); it is preserved in the result registry. Two repairs, both fitted on the calibration\ngraphs only, recovered in-sample hit rate $1.0$ and screening accuracy $3/3$, but the strict\nstrong criterion remains unmet: ogbn-arxiv cannot reach the $1.5$\\,pp target at any grid $T$ and\nis reported as \\texttt{unreachable-with-evidence}, and chameleon's gap at the predicted budget\nexceeds the target. We therefore report the capability as a calibrated feasibility band with a\nstated failure boundary, not as exact per-graph timestep prediction. % run: S5-c3-v1-v2"),
])
