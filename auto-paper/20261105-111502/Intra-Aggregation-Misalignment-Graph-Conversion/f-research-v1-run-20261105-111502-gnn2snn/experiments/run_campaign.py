#!/usr/bin/env python3
"""Run the real experimental campaign for the new manuscript.

Stages (each writes its own JSON under results/ and appends rows to registry/results.csv):

  models  : train and cache one ANN per (graph, host, seed) with ANN-only diagnostics.
  s1      : S1 mechanism probes (2x2, faithful L=3 inter-layer replay, four-way neuron control).
  table1  : Table 1 method-by-T grid plus the three aggregation hosts.
  c3      : bound-derived latency allocation, fitted graphs -> frozen c -> held-out graphs.
  all     : the four stages in order.

Run with the local Conda `base` Python on CPU (frozen device). No remote compute.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
sys.path.insert(0, str(ROOT / "protocols"))

import core  # noqa: E402
import graph_data  # noqa: E402
import snn_probe  # noqa: E402

FITTED = ["cora", "citeseer", "pubmed"]
HELDOUT = ["chameleon", "squirrel", "ogbn-arxiv"]
T_GRID = [2, 4, 8, 16, 32]
SEEDS = list(range(7))
EPS_PP = 1.5
DATA_ROOT = str(ROOT / "results" / ".data")
MODELS = ROOT / "results" / "models"
FIELDS = [
    "run_id", "date", "stage", "probe", "dataset", "host", "method_family", "method",
    "is_transplant", "neuron", "bias_correction", "t_steps", "hidden", "seed", "ann_ref",
    "acc", "std", "gap_pp", "spikes_per_node", "sop_est", "train_seconds",
    "retrain_count", "perm_seed", "git_commit", "notes", "device",
]
ROWS_DEFS = [
    ("if_nobias", "if", False, "membrane"),
    ("no_bias_count", "if", False, "count"),
    ("count_decoding", "if", True, "count"),
    ("tpp_transplant", "tpp_faithful", False, "membrane"),
    ("tpp_plus_beta", "tpp_faithful", True, "membrane"),
    ("tpp_simple", "tpp_simple", False, "membrane"),
    ("tpp_simple_beta", "tpp_simple", True, "membrane"),
    ("ours", "if", True, "membrane"),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def make_data(name: str, host: str = "H3_sym"):
    d = graph_data.load_ds(name, DATA_ROOT)
    adj = sp.csr_matrix(d["adj"], dtype=np.float32)
    deg = np.asarray(adj.sum(1)).ravel()
    if host == "H1_mean":
        norm = sp.diags(np.power(np.maximum(deg, 1e-12), -1.0).astype(np.float32)) @ adj
    elif host == "H2_sum":
        norm = adj
    else:
        dinv = np.power(np.maximum(deg, 1e-12), -0.5).astype(np.float32)
        norm = sp.diags(dinv) @ adj @ sp.diags(dinv)
    norm = norm.astype(np.float32).tocsr()
    X = np.asarray(d["features"], dtype=np.float32).copy()
    if d.get("row_normalize"):
        rs = X.sum(1)
        rs[rs == 0] = 1.0
        X = X / rs[:, None]
    labels = np.asarray(d["labels"], np.int64)
    return dict(name=name, X=X, y=labels, adj=norm,
                train=np.asarray(d["train_mask"], bool),
                val=np.asarray(d["val_mask"], bool),
                test=np.asarray(d["test_mask"], bool),
                N=int(X.shape[0]), F=int(X.shape[1]), C=int(labels.max()) + 1,
                E=int((adj.nnz - adj.shape[0]) // 2), host=host)


def trace_id() -> str:
    h = hashlib.sha256()
    for p in [ROOT / "experiments/core.py", ROOT / "experiments/snn_probe.py",
              ROOT / "experiments/run_campaign.py", ROOT / "protocols/graph_data.py"]:
        h.update(p.read_bytes())
    return "content:" + h.hexdigest()[:16]


def append_rows(rows: list[dict]) -> None:
    if not rows:
        return
    path = ROOT / "registry" / "results.csv"
    with path.open("a", encoding="utf-8", newline="") as stream:
        csv.DictWriter(stream, fieldnames=FIELDS).writerows(rows)


def row(stage, name, host, method, T, seed, ann_ref, acc, gap, spikes, sop,
        seconds, probe="none", neuron="if", bias="beta_star", perm_seed="",
        method_family="conversion", is_transplant=0, notes=""):
    return {
        "run_id": "%s-%s-%s-T%d-s%d" % (stage, name, method, T, seed),
        "date": datetime.now().strftime("%Y-%m-%d"), "stage": stage, "probe": probe,
        "dataset": name, "host": host, "method_family": method_family, "method": method,
        "is_transplant": is_transplant, "neuron": neuron, "bias_correction": bias,
        "t_steps": T, "hidden": 16, "seed": seed, "ann_ref": round(float(ann_ref), 6),
        "acc": round(float(acc), 6), "std": "", "gap_pp": round(float(gap), 4),
        "spikes_per_node": round(float(spikes), 6), "sop_est": int(sop),
        "train_seconds": round(float(seconds), 3), "retrain_count": 1,
        "perm_seed": perm_seed, "git_commit": trace_id(), "notes": notes,
        "device": "cuda" if name == "ogbn-arxiv" else "cpu",
    }


def save_model(name, host, seed, model, diag, seconds):
    MODELS.mkdir(parents=True, exist_ok=True)
    path = MODELS / ("%s__%s__s%d.npz" % (name, host, seed))
    payload = dict(
        Ms0=model["Ms"][0], Ms1=model["Ms"][1],
        bs0=model["bs_layers"][0], b_out=model["b_out"],
        acc_test=float(model["acc_test"]), n_layers=2, alpha=0.0, hidden=16, seed=seed,
        kappa=float(diag["kappa"]), margin=float(diag["margin"]), rho=float(diag["rho"]),
        epochs_run=int(model["epochs_run"]), train_seconds=float(seconds),
    )
    np.savez_compressed(path, **payload)
    return path


def load_model(name, host, seed):
    path = MODELS / ("%s__%s__s%d.npz" % (name, host, seed))
    if not path.exists():
        return None, None
    z = np.load(path)
    model = dict(Ms=[z["Ms0"], z["Ms1"]], bs_layers=[z["bs0"]], b_out=z["b_out"],
                 acc_test=float(z["acc_test"]), n_layers=2, alpha=0.0, hidden=16,
                 seed=int(z["seed"]), epochs_run=int(z["epochs_run"]))
    diag = dict(kappa=float(z["kappa"]), margin=float(z["margin"]),
                rho=float(z["rho"]), ann_acc=float(z["acc_test"]))
    meta = dict(train_seconds=float(z["train_seconds"]))
    return (model, diag), meta


def stage_models(args):
    out = {}
    for name in args.graphs:
        epochs = 150 if name == "ogbn-arxiv" else 400
        for host in args.hosts:
            data = make_data(name, host)
            for seed in args.seeds:
                t0 = time.perf_counter()
                # Only the 169k-node graph uses CUDA. It is a held-out graph, never pooled with
                # CPU accuracy rows; pre-registration-c3 v4 records the device check.
                device = "cuda" if name == "ogbn-arxiv" else "cpu"
                model = core.train_ann(data, hidden=16, n_layers=2, seed=seed,
                                       device=device, epochs=epochs)
                diag = snn_probe.ann_diagnostics(data, model)
                elapsed = time.perf_counter() - t0
                save_model(name, host, seed, model, diag, elapsed)
                key = "%s__%s__s%d" % (name, host, seed)
                out[key] = dict(**diag, train_seconds=elapsed, epochs=epochs)
                log("models %s: ANN %.4f kappa %.4g margin %.4g rho %.3f %.1fs"
                    % (key, model["acc_test"], diag["kappa"], diag["margin"],
                       diag["rho"], elapsed))
    (ROOT / "results" / "models_index.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def stage_s1(args):
    out = {"probe_2x2": {}, "l3_interlayer": {}, "four_way": {}, "branch": "undetermined"}
    rows = []
    # 2x2 crossed probe on the three fitted graphs
    for name in FITTED:
        data = make_data(name)
        for ip in (False, True):
            for ap in (False, True):
                for T in [2, 4, 8]:
                    vals = []
                    for seed in SEEDS:
                        loaded, _ = load_model(name, "H3_sym", seed)
                        if loaded is None:
                            continue
                        model, diag = loaded
                        for k in range(5):
                            r = snn_probe.simulate_l2(
                                data, model, T, bias=True, neuron="if",
                                intra_phase=ap, inter_perm=ip,
                                perm_seed=seed * 10 + k, phase_seed=k)
                            vals.append(r["acc"])
                            rows.append(row("S1", name, "H3_sym", "ours_probe", T, seed,
                                            diag["ann_acc"], r["acc"],
                                            (r["acc"] - diag["ann_acc"]) * 100,
                                            r["spikes_per_node"], r["sop_est"], 0.0,
                                            probe=("inter+intra" if ip and ap else
                                                   "inter" if ip else "intra" if ap else "none"),
                                            perm_seed=k, notes="2x2 S1 probe K=5"))
                    key = "%s_ip%d_ap%d_T%d" % (name, int(ip), int(ap), T)
                    out["probe_2x2"][key] = dict(mean=float(np.mean(vals)),
                                                 std=float(np.std(vals)), n=len(vals))
                    log("S1 2x2 %s: %.4f" % (key, np.mean(vals)))
    # faithful L=3 inter-layer replay (Cora, 3 seeds)
    data = make_data("cora")
    for seed in range(3):
        model3 = core.train_ann(data, hidden=16, n_layers=3, seed=seed, device="cpu")
        for T in [2, 4, 8]:
            base = snn_probe.simulate_l3_interlayer(data, model3, T, permute=False,
                                                    perm_seed=seed)
            perm = [snn_probe.simulate_l3_interlayer(data, model3, T, permute=True,
                                                     perm_seed=seed * 10 + k)["acc"]
                    for k in range(5)]
            key = "cora_s%d_T%d" % (seed, T)
            out["l3_interlayer"][key] = dict(base=base["acc"], perm_mean=float(np.mean(perm)),
                                             delta_pp=(np.mean(perm) - base["acc"]) * 100)
            log("S1 L3 %s: base %.4f perm %.4f delta %+.3f pp"
                % (key, base["acc"], np.mean(perm), (np.mean(perm) - base["acc"]) * 100))
    # four-way neuron x bias control
    for name in FITTED:
        data = make_data(name)
        for T in [2, 4, 8, 16]:
            for neuron in ["if", "tpp_faithful"]:
                for bias in (False, True):
                    vals = []
                    for seed in SEEDS:
                        loaded, _ = load_model(name, "H3_sym", seed)
                        if loaded is None:
                            continue
                        model, diag = loaded
                        r = snn_probe.simulate_l2(data, model, T, bias=bias,
                                                  neuron=neuron, perm_seed=seed)
                        vals.append(r["acc"])
                        rows.append(row("S1", name, "H3_sym",
                                        "%s_bias%d" % (neuron, int(bias)), T, seed,
                                        diag["ann_acc"], r["acc"],
                                        (r["acc"] - diag["ann_acc"]) * 100,
                                        r["spikes_per_node"], r["sop_est"], 0.0,
                                        neuron=neuron,
                                        bias="beta_star" if bias else "none",
                                        is_transplant=int(neuron != "if"),
                                        notes="four-way control"))
                    key = "%s_%s_b%d_T%d" % (name, neuron, int(bias), T)
                    out["four_way"][key] = dict(mean=float(np.mean(vals)),
                                                std=float(np.std(vals)), n=len(vals))
                    log("S1 four-way %s: %.4f" % (key, np.mean(vals)))

    # branch decision from data, not expectation
    t4 = {}
    for key, v in out["four_way"].items():
        if key.endswith("_T4"):
            t4[key] = v["mean"]
    ours_t4 = np.mean([v for k, v in t4.items() if "_if_b1_" in k])
    tpp_t4 = np.mean([v for k, v in t4.items() if "_tpp_faithful_b0_" in k])
    inter_deltas = [v["delta_pp"] for k, v in out["l3_interlayer"].items()]
    intra_deltas = []
    for name in FITTED:
        for T in [2, 4, 8]:
            a = out["probe_2x2"]["%s_ip0_ap0_T%d" % (name, T)]["mean"]
            b = out["probe_2x2"]["%s_ip0_ap1_T%d" % (name, T)]["mean"]
            intra_deltas.append((b - a) * 100)
    out["decision_evidence"] = dict(ours_T4=float(ours_t4), tpp_T4=float(tpp_t4),
                                    tpp_gap_pp=float((ours_t4 - tpp_t4) * 100),
                                    inter_layer_delta_pp=float(np.mean(inter_deltas)),
                                    intra_agg_delta_pp=float(np.mean(intra_deltas)))
    d = out["decision_evidence"]
    if d["tpp_gap_pp"] < 1.5:
        out["branch"] = "C"
    elif d["intra_agg_delta_pp"] > 0.8:
        out["branch"] = "D"
    elif abs(d["inter_layer_delta_pp"]) < 0.4:
        out["branch"] = "B"
    else:
        out["branch"] = "A"
    log("S1 BRANCH = %s | %s" % (out["branch"], json.dumps(d)))
    (ROOT / "results" / "s1_probe.json").write_text(json.dumps(out, indent=2) + "\n",
                                                     encoding="utf-8")
    append_rows(rows)
    return out


def stage_table1(args):
    out = {"method_grid": {}, "hosts": {}}
    rows = []
    for name in FITTED:
        data = make_data(name)
        for label, neuron, bias, readout in ROWS_DEFS:
            for T in T_GRID:
                vals, spk = [], []
                for seed in SEEDS:
                    loaded, meta = load_model(name, "H3_sym", seed)
                    if loaded is None:
                        continue
                    model, diag = loaded
                    r = snn_probe.simulate_l2(data, model, T, bias=bias, neuron=neuron,
                                              readout=readout, perm_seed=seed)
                    vals.append(r["acc"])
                    spk.append(r["spikes_per_node"])
                    rows.append(row("S3", name, "H3_sym", label, T, seed,
                                    diag["ann_acc"], r["acc"],
                                    (r["acc"] - diag["ann_acc"]) * 100,
                                    r["spikes_per_node"], r["sop_est"], 0.0,
                                    neuron=neuron,
                                    bias="beta_star" if bias else "none",
                                    is_transplant=int("tpp" in neuron),
                                    notes="Table 1 row " + label))
                key = "%s_%s_T%d" % (name, label, T)
                out["method_grid"][key] = dict(mean=float(np.mean(vals)),
                                               std=float(np.std(vals)), n=len(vals),
                                               spikes=float(np.mean(spk)))
                log("Table1 %s: %.4f" % (key, np.mean(vals)))
    # plug-in hosts, each with its own trained ANN
    for host in ["H1_mean", "H2_sum", "H3_sym"]:
        for name in FITTED:
            data = make_data(name, host)
            for T in T_GRID:
                vals = []
                for seed in SEEDS:
                    loaded, meta = load_model(name, host, seed)
                    if loaded is None:
                        continue
                    model, diag = loaded
                    r = snn_probe.simulate_l2(data, model, T, bias=True, neuron="if",
                                              perm_seed=seed)
                    vals.append(r["acc"])
                    rows.append(row("S3", name, host, "ours", T, seed,
                                    diag["ann_acc"], r["acc"],
                                    (r["acc"] - diag["ann_acc"]) * 100,
                                    r["spikes_per_node"], r["sop_est"], 0.0,
                                    notes="host plug-in " + host))
                key = "%s_%s_T%d" % (name, host, T)
                out["hosts"][key] = dict(mean=float(np.mean(vals)),
                                         std=float(np.std(vals)), n=len(vals))
                log("hosts %s: %.4f" % (key, np.mean(vals)))
    (ROOT / "results" / "table1.json").write_text(json.dumps(out, indent=2) + "\n",
                                                   encoding="utf-8")
    append_rows(rows)
    return out


def stage_c3(args):
    out = {"curves": {}, "fit": {}, "heldout": {}, "controls": {}}
    rows = []
    allnames = FITTED + HELDOUT
    for name in allnames:
        data = make_data(name)
        curves = []
        kappas = []
        for seed in SEEDS:
            loaded, meta = load_model(name, "H3_sym", seed)
            if loaded is None:
                log("C3 WARNING missing model %s s%d" % (name, seed))
                continue
            model, diag = loaded
            # Recompute kappa from the frozen weights with the current (pre-registered)
            # definition; cached values from an earlier margin convention are never trusted.
            fresh = snn_probe.ann_diagnostics(data, model)
            kappa = float(fresh["kappa"])
            kappas.append(kappa)
            per_T = {}
            for T in T_GRID:
                r = snn_probe.simulate_l2(data, model, T, bias=True, neuron="if",
                                          perm_seed=seed)
                gap_pp = (diag["ann_acc"] - r["acc"]) * 100
                per_T[str(T)] = dict(acc=r["acc"], gap_pp=gap_pp)
                rows.append(row("S5", name, "H3_sym", "ours_Tgrid", T, seed,
                                diag["ann_acc"], r["acc"], gap_pp,
                                r["spikes_per_node"], r["sop_est"], 0.0,
                                notes="C3 T-grid; gap=ANN-acc in pp"))
            valid = [T for T in T_GRID if per_T[str(T)]["gap_pp"] <= EPS_PP]
            curves.append(dict(seed=seed, kappa=kappa,
                               T_grid_min=min(valid) if valid else None, per_T=per_T))
        out["curves"][name] = dict(rows=curves, kappa_mean=float(np.mean(kappas)))
        log("C3 curves %s: kappa %.4g Tmin %s"
            % (name, np.mean(kappas),
               [c["T_grid_min"] for c in curves]))

    # fit c on fitted graphs only; freeze before any held-out evaluation
    pairs = []
    for name in FITTED:
        for c in out["curves"][name]["rows"]:
            if c["T_grid_min"] is not None and c["kappa"] > 0:
                pairs.append((c["T_grid_min"], c["kappa"]))
    if not pairs:
        raise SystemExit("C3 fit failed: no fitted graph reaches epsilon")
    c_val = float(np.median([t / k for t, k in pairs]))
    out["fit"] = dict(c=c_val, n_pairs=len(pairs), epsilon_pp=EPS_PP,
                      fitted_graphs=FITTED,
                      pearson_r=float(np.corrcoef([p[0] for p in pairs],
                                                  [p[1] for p in pairs])[0, 1])
                      if len(pairs) > 2 else None)
    (ROOT / "results" / "c3_fit.json").write_text(json.dumps(out["fit"], indent=2) + "\n",
                                                   encoding="utf-8")
    log("C3 FROZEN c=%.6g over %d fitted rows (r=%s)"
        % (c_val, len(pairs), out["fit"]["pearson_r"]))

    def snap(v):
        for T in T_GRID:
            if T >= v:
                return T
        return T_GRID[-1]

    pred_all, true_all = [], []
    for name in HELDOUT:
        curves = out["curves"][name]["rows"]
        preds = [snap(max(1.0, np.ceil(c_val * c["kappa"]))) for c in curves]
        trues = [c["T_grid_min"] for c in curves]
        usable = [(p, t, c) for p, t, c in zip(preds, trues, curves)
                  if t is not None and str(t) in c["per_T"]]
        if not usable:
            out["heldout"][name] = dict(status="infeasible-with-evidence",
                                        reason="no grid T reaches epsilon")
            continue
        hit = [abs(np.log2(p / t)) <= 1.0 for p, t, _ in usable]
        gap_at_pred = [c["per_T"][str(p)]["gap_pp"] for p, _, c in usable
                       if str(p) in c["per_T"]]
        mean_pred = float(np.mean([p for p, _, _ in usable]))
        mean_true = float(np.mean([t for _, t, _ in usable]))
        out["heldout"][name] = dict(
            status="complete", n=len(usable),
            T_pred_mean=mean_pred, T_grid_min_mean=mean_true,
            hit_rate=float(np.mean(hit)),
            gap_at_pred_pp=float(np.mean(gap_at_pred)) if gap_at_pred else None,
            max_gap_at_pred_pp=float(np.max(gap_at_pred)) if gap_at_pred else None,
            underprovisioned=int(sum(1 for g in gap_at_pred if g > EPS_PP + 0.8)),
        )
        pred_all.extend([p for p, _, _ in usable])
        true_all.extend([t for _, t, _ in usable])
        log("C3 heldout %s: %s" % (name, json.dumps(out["heldout"][name])))

    uniform_T = max(true_all) if true_all else T_GRID[-1]
    saving = 1.0 - (np.mean(pred_all) / uniform_T) if true_all else 0.0
    out["controls"] = dict(uniform_T=int(uniform_T),
                           mean_predicted_T=float(np.mean(pred_all)) if pred_all else None,
                           timestep_saving=float(saving),
                           grid_oracle_mean_T=float(np.mean(true_all)) if true_all else None)
    # shuffled-kappa control: reassign kappa across graphs, keep the frozen c
    all_k = [c["kappa"] for name in allnames for c in out["curves"][name]["rows"]
             if c["T_grid_min"] is not None]
    all_t = [c["T_grid_min"] for name in allnames for c in out["curves"][name]["rows"]
             if c["T_grid_min"] is not None]
    rng = np.random.default_rng(20261105)
    errs_real, errs_shuf = [], []
    for k, t in zip(all_k, all_t):
        errs_real.append(abs(np.log2(max(snap(np.ceil(c_val * k)), 1) / t)))
    for _ in range(20):
        kk = np.array(all_k)[rng.permutation(len(all_k))]
        errs_shuf.append(float(np.mean([abs(np.log2(max(snap(np.ceil(c_val * k)), 1) / t))
                                        for k, t in zip(kk, all_t)])))
    out["controls"]["shuffled_kappa"] = dict(
        real_mean_log2_error=float(np.mean(errs_real)),
        shuffled_mean_log2_error=float(np.mean(errs_shuf)),
        control_strictly_worse=bool(np.mean(errs_shuf) > np.mean(errs_real)))

    n_ok = sum(1 for v in out["heldout"].values()
               if v.get("status") == "complete" and v["hit_rate"] >= 2 / 3
               and v.get("underprovisioned", 1) == 0
               and (v.get("gap_at_pred_pp") or 99) <= EPS_PP)
    out["verdict"] = dict(
        heldout_passed=n_ok, heldout_total=len(HELDOUT),
        saving=saving, saving_target=0.25,
        expected_strong=bool(n_ok >= 3 and saving >= 0.25
                             and out["controls"]["shuffled_kappa"]["control_strictly_worse"]),
        minimum=bool(n_ok >= 2 and saving > 0))
    log("C3 VERDICT: %s" % json.dumps(out["verdict"]))
    (ROOT / "results" / "c3_allocation.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    append_rows(rows)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=["models", "s1", "table1", "c3", "all"])
    ap.add_argument("--graphs", nargs="*", default=FITTED + HELDOUT)
    ap.add_argument("--hosts", nargs="*", default=["H1_mean", "H2_sum", "H3_sym"])
    ap.add_argument("--seeds", nargs="*", type=int, default=SEEDS)
    args = ap.parse_args()
    log("run_campaign stage=%s python=%s numpy=%s device=cpu at %s"
        % (args.stage, platform.python_version(), np.__version__,
           datetime.now().isoformat(timespec="seconds")))
    if args.stage in ("models", "all"):
        stage_models(args)
    if args.stage in ("s1", "all"):
        stage_s1(args)
    if args.stage in ("table1", "all"):
        stage_table1(args)
    if args.stage in ("c3", "all"):
        stage_c3(args)
    log("stage %s done" % args.stage)


if __name__ == "__main__":
    main()
