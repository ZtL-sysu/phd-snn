# Reviewer 2 (empirical/reproducibility lens)

Strengths: four mutually disjoint holdout groups with 20 distinct frozen seeds is unusually thorough for a conversion study; both energy conventions are reported; all single-point conversion baselines are adapted to the same backbone rather than quoted from papers. Zero-spike and degenerate-teacher exclusion rules are explicit.

Concerns: (1) narrow networks with 10-26 hidden units are unusual and may limit generality; (2) the working points were selected on validation with several seeds, and the test gap should be quantified (it is); (3) figure quality is schematic.

Verdict: the empirical protocol is sound. The authors should keep the val-vs-test distinction explicit and avoid claiming the method transfers to ImageNet-scale data (they do). Minor revision recommended.
