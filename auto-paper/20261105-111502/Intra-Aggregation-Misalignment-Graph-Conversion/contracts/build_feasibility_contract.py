"""Build feasibility-contract.json with real SHA-256 bindings for the CCFA packet.

Run with the project's local Conda Python. This script writes no scientific claims of its own:
the claim text is a machine-readable index into strong-result-feasibility-contract.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1] / "ccfa-startup-packet"

REQUIRED = [
    "startup-stage-plan.md",
    "idea-cards.md",
    "prior-art-opportunity-map.md",
    "idea-red-team-review.md",
    "claim-evidence-matrix.md",
    "strong-result-feasibility-contract.md",
    "startup-decision.md",
]

URL = "https://github.com/kimiyoung/planetoid/raw/master/data"
SPLIT = "Planetoid public split (Cora 140/500/1000, CiteSeer 120/500/1000, PubMed 60/500/1000); 7 fixed seeds 0-6; T grid 2,4,8,16,32; test identities frozen before fitting"

CLAIMS = [
    {
        "id": "C1-mechanism-separation",
        "claim": "Graph conversion error is generated inside one neighbourhood aggregation as a deterministic rho_n-amplified phase error; the ICML 2025 cross-layer stochastic rearrangement is a distinct phenomenon and does not remove it.",
        "mechanism": "The exact identity B_hat_l - B_l = (1-alpha) A_hat (E_{l-1} M_l) contains the aggregation operator inside the error; randomising firing times changes E but not the systematic bias transported by A_hat.",
        "assumptions": "Rate-coded IF/TPP neurons, static graph, fixed normalized A_hat, shared weights, identical backbone and seeds across arms, no test-time adaptation.",
        "falsifying_ablation": "2x2 crossed probe (inter-layer permutation on/off x intra-aggregation phase randomisation on/off) plus the four-way neuron control IF / IF+beta* / TPP / TPP+beta*.",
        "dataset_url": URL,
        "split_protocol": SPLIT,
        "primary_metric": "Node-classification accuracy, reported as pp difference against the matched control.",
        "metric_direction": "higher",
        "minimum": "S1 lands in branch A or B; TPP transplant at least 1.5 pp behind IF+beta* at T=4 on at least 2/3 graphs; crossed-probe directions differ by more than 2x the 0.4 pp noise floor.",
        "expected_strong": "Branch B on all three graphs over 7 seeds: cross-layer permutation effect below the noise floor, intra-aggregation randomisation significantly worse, and TPP+beta* at least TPP so the correction is neuron-orthogonal.",
        "failure": "Branch C (TPP >= ours) or D (phase randomisation helps), a seed-level direction reversal, or a TPP unit test missing the frozen T=8 values by more than 0.5 pp.",
        "simple_baseline": "IF conversion without bias correction.",
        "strong_baseline": "TPP neuron re-implemented from ICML 2025 equations (8)-(13) under identical aggregation, backbone, seeds and hyperparameter budget.",
        "matched_control": "IF+beta* versus TPP+beta* at the same T, isolating the neuron model.",
        "implementation_path": "Adapt the companion L-layer core.py (record source commit d125112 and sha256) and add probes.py plus tpp_neuron.py; store the diff under runs/.",
        "prototype_check": "Single-cell T=8 Cora TPP re-implementation reproduces 0.7756 within 0.5 pp before the full probe grid starts.",
        "calibration_evidence": "Task book section 2 T=8 ablation: ours 0.8021/0.6880/0.7684 versus TPP 0.7756/0.6457/0.7427, margins 2.65/4.23/2.57 pp, all above the 0.8 pp decision threshold; ICML 2025 Figure 1 verified in notes/G0_literature_map.md.",
        "test_isolation": "Held-out graphs untouched; probe seeds fixed and separate from any model-selection decision.",
        "stop_return_condition": "Prototype failure or branch C/D stops the campaign, writes notes/, reports to the author under GP, and returns to mechanism design; no target rescaling and no progression to S3.",
        "runtime_hours": 24,
        "memory_gb": 8,
        "seeds": 7,
        "search_trials": 120,
    },
    {
        "id": "C2-rho-weighted-L-layer-bound",
        "claim": "An exact per-layer identity yields a rho_n-weighted L-layer error bound with a mandatory beta* system term and an explicit T_L dependence; the multiplier involves neighbourhood geometry rather than only a weight norm.",
        "mechanism": "Recursion of E_l through A_hat makes the row sum rho_n enter multiplicatively per hop, while the uncorrected system term accumulates linearly in rho_n.",
        "assumptions": "Bounded activations, fixed A_hat, ReLU homogeneity, known spectral norms, no train-time renormalisation of the absolute threshold scale.",
        "falsifying_ablation": "L in {2,3,4} counterexample search over the fixed 30-cell-style grid, with spectral-norm-constrained training and adaptive-threshold controls closing the two escape routes.",
        "dataset_url": URL,
        "split_protocol": SPLIT,
        "primary_metric": "Number of bound violations (target 0); secondary bound/measured conservatism ratio.",
        "metric_direction": "lower",
        "minimum": "Zero counterexamples at L=2 and L=3, conservatism reported for every cell, and an explicit failure-depth condition if L=4 fails.",
        "expected_strong": "Zero counterexamples for all L<=4, mean conservatism between 3x and 8x, and a closed-form T_L exponent matching the measured depth scaling within the pre-registered tolerance.",
        "failure": "Any bound violation not attributable to a stated assumption, or conservatism above 20x (true but unusable).",
        "simple_baseline": "The image-domain form ||W||_inf * theta / T applied naively to graph weights.",
        "strong_baseline": "Companion empirical G^0.95 law (r=0.990 over 9 cells), reaccepted as external calibration evidence with hashes and commits.",
        "matched_control": "The same networks with beta* removed, measuring the system term directly.",
        "implementation_path": "bound.py implementing the recursion, the L-layer closed form and the violation scan; proof and symbol table in the appendix.",
        "prototype_check": "Numerical residual of the exact identity at most 1e-5 on a 30-cell grid before any theorem claim is written.",
        "calibration_evidence": "Companion measured ||E_L||/||E_1|| proportional to G^0.948 at r=0.990, a 21 pp four-layer loss at T=8, and an identity residual at most 2e-6; the earlier latency bound was conservative by 3.2-6.7x.",
        "test_isolation": "The counterexample grid is fixed before fitting any bound constant; held-out graphs are not used.",
        "stop_return_condition": "A violation with no stated failure condition returns to theory design; substituting an empirical characterisation requires a versioned contract correction.",
        "runtime_hours": 18,
        "memory_gb": 8,
        "seeds": 7,
        "search_trials": 60,
    },
    {
        "id": "C3-bound-derived-latency-allocation",
        "claim": "Inverting the C2 closed form predicts each model's minimum T* for a target error epsilon=1.5 pp, and a per-layer allocation reaches that target with fewer total timesteps than a matched uniform-T budget on graphs unused for constant fitting.",
        "mechanism": "T_L is an explicit function of rho_n, G, theta and the margin distribution; inversion yields a per-model/per-layer step budget computable from trained weights without running the full T grid.",
        "assumptions": "C2 assumptions hold; the margin proxy is computable from the trained ANN alone; epsilon is fixed before measurement; all constants are frozen in a committed pre-registration.",
        "falsifying_ablation": "Uniform-T matched-budget control, shuffled-rho_n control, full grid-search oracle, and an L=3 per-layer schedule negative control.",
        "dataset_url": URL,
        "split_protocol": SPLIT + "; constants fitted on the three fitted Planetoid graphs only; held-out evaluation on ogbn-arxiv and chameleon, with squirrel as a stress cell excluded from claims if its budget is exceeded.",
        "primary_metric": "Total timesteps needed to reach epsilon=1.5 pp; secondary prediction hit rate within one T-grid step and achieved ANN gap.",
        "metric_direction": "lower",
        "minimum": "On at least 2/3 held-out graphs the predicted T* actually reaches epsilon without under-provisioning, the shuffled-rho_n control is worse, and L<=4 has zero bound counterexamples.",
        "expected_strong": "On at least 3/3 held-out graphs the predicted T* is within one T-grid step of the grid-searched minimum and reaches epsilon; total timesteps fall by at least 25 percent versus uniform-T at matched accuracy; the matched-budget uniform control fails to reach epsilon on at least 2/3 graphs.",
        "failure": "Any held-out graph under-provisioned by more than 2x the noise floor (gap above epsilon+0.8 pp), hit rate below 2/3, savings below 0 percent, or the shuffled-rho_n control matching the real allocation.",
        "simple_baseline": "Uniform T equal to the largest T required across the panel; task book section 2 shows T=4 already reaches 1.17/1.02/0.18 pp so a single uniform budget wastes steps.",
        "strong_baseline": "Full T-grid search per model (oracle), costing 5 conversions per model and representing exactly the cost the method avoids.",
        "matched_control": "Uniform-T allocation with the same total timestep budget as the predicted allocation, so savings cannot come from spending less compute.",
        "implementation_path": "latency_alloc.py uses the C2 closed form and a margin proxy from the trained ANN; one ANN per (graph, seed) is trained (7 per graph, not 49), removing the earlier budget overrun; constants and the held-out list committed before measurement.",
        "prototype_check": "On the three fitted graphs only, closed-form prediction lands within one T-grid step for at least 6/9 (graph x L) cells before held-out evaluation is unlocked.",
        "calibration_evidence": "Task book section 2 shows graph-dependent minimum T (Cora/PubMed/CiteSeer T=4 gaps 1.17/0.18/1.02 pp), so a uniform budget is wasteful in the frozen data; companion G^0.95 law at r=0.990 supports predictability of error scale from weights. A 25 percent saving over a 5-step grid is roughly one grid step.",
        "test_isolation": "Held-out graph identities, epsilon, the T grid and fitting constants are frozen in a committed pre-registration; no held-out result may re-fit a constant.",
        "stop_return_condition": "Prototype below 6/9 or any held-out failure returns to C2 before C3; no tuning on held-out graphs; persistent failure enters the autonomous correction loop and the within-family model-selection pivot.",
        "runtime_hours": 30,
        "memory_gb": 10,
        "seeds": 7,
        "search_trials": 90,
    },
    {
        "id": "C4-low-latency-pareto-and-hosts",
        "claim": "At T<=4 the conversion is not dominated by reproduced direct-training SNNs on (accuracy, spike/SynOps proxy, retrain count), and the correction plugs into mean, sum and symmetric-normalized aggregation without neuron changes.",
        "mechanism": "Conversion needs one ANN training for the entire T grid whereas direct training retrains per T; the bias correction is an affine offset independent of the aggregation kernel.",
        "assumptions": "Identical hyperparameter search budgets for both arms; spike/SynOps stated as proxies; protocol differences for external arms labelled explicitly.",
        "falsifying_ablation": "Remove beta*, swap to count decoding, and rerun with a 512-wide published architecture (the unfavourable row is retained).",
        "dataset_url": URL,
        "split_protocol": SPLIT,
        "primary_metric": "Accuracy (higher) paired with spikes per node, SynOps proxy and retrain count (lower); dominance judged on the (accuracy, cost) pair.",
        "metric_direction": "higher",
        "minimum": "At least 2 direct-training arms reproduce under the frozen protocol, no T<=4 conversion point is dominated, and H1/H2/H3 rows have no blank cell.",
        "expected_strong": "At least 3 arms reproduce; conversion is never dominated on (accuracy, cost) at T<=4; H1-H3 differ by less than 1 pp at T=8; Table 1 has zero blanks including T=2.",
        "failure": "A direct-training arm dominates a T<=4 conversion point on both accuracy and cost, or fewer than 2 arms reproduce with no honest labelled substitute.",
        "simple_baseline": "IF no-bias conversion.",
        "strong_baseline": "At least 3 SGNNBench direct-training implementations (SpikingGCN, SpikeGCL or SpikeGraphormer, DRSGNN/SiGNN) with the task book's 5-working-day stop-loss.",
        "matched_control": "Same-width and same-propagation-order conversion versus direct training.",
        "implementation_path": "hosts.py for the three normalizations, pareto.py for dominance scanning, tables.py generating Tables 1-3 from results.csv.",
        "prototype_check": "H3 symmetric normalization runs end-to-end on Cora for one seed before the full grid starts.",
        "calibration_evidence": "Companion four-arm Pareto found conversion never dominated at T<=4 with 2-23x fewer SOPs, while its 512-wide published architecture was more accurate on two graphs; both facts including the unfavourable one are retained. Task book section 2 gives T=4 gaps 1.17/1.02/0.18 pp.",
        "test_isolation": "The dominance rule and T grid are frozen before any arm is measured; external protocol rows are labelled and cannot carry the main comparison.",
        "stop_return_condition": "An arm that cannot run within 5 working days triggers the labelled stop-loss; a reproduced arm that dominates is recorded and the claim is narrowed through a versioned correction, never by deleting the row.",
        "runtime_hours": 36,
        "memory_gb": 12,
        "seeds": 7,
        "search_trials": 200,
    },
]


def main() -> None:
    evidence = []
    for name in REQUIRED:
        path = PACKET / name
        if not path.is_file() or not path.stat().st_size:
            raise SystemExit("missing or empty packet artifact: " + name)
        evidence.append(
            {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        )
    data = {"schema_version": 1, "decision": "proceed", "claims": CLAIMS, "evidence": evidence}
    out = PACKET / "feasibility-contract.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", out, "claims:", len(CLAIMS), "evidence:", len(evidence))


if __name__ == "__main__":
    main()
