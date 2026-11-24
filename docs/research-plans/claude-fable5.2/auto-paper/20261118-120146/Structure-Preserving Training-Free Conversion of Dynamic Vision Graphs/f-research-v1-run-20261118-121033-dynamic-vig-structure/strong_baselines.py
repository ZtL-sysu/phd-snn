import json
import statistics
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

run = Path(__file__).resolve().parent
sys.path.insert(0, str(run / "src"))
sys.path.insert(0, str(run))
from structure_conversion import load_images, matrix_knn_indices, signed_multilevel_encode
from train_teacher import SmallViGTeacher
from v2_message_calibration import forward_with_codes, graph_message

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
seeds = (41, 42, 43)
levels = 16
calibration_count = 5000
test_limit = 2000
scales = (5.0, 7.0, 9.0, 11.0, 15.0)
offsets = (0.0, 0.05, 0.10)
dcgs_threshold_scales = (0.5, 0.75, 1.0, 1.25)
dcgs_budget_threshold_scales = (1.4, 1.6, 1.8, 2.0, 2.25, 2.5, 3.0, 4.0)


def load_teacher(seed):
    state = torch.load(run / f"teacher_seed{seed}.pt", map_location=device, weights_only=False)
    model = SmallViGTeacher().to(device)
    model.load_state_dict(state["state_dict"])
    model.eval()
    return model


def teacher_features(model, images):
    nodes = images.unfold(1, model.patch, model.patch).unfold(2, model.patch, model.patch)
    nodes = nodes.contiguous().view(images.size(0), model.grid * model.grid, model.patch * model.patch)
    return F.normalize(F.relu(model.embed(nodes)), dim=-1).detach()


def encode(values, scale, offset):
    centered = (values + offset).clamp(-1, 1)
    quantized = torch.round(((centered + 1) / 2) * scale) / scale
    return 2 * quantized - 1 - offset


def message_mse(features, codes, model, batch_size=256):
    total = 0.0
    count = 0
    for start in range(0, len(features), batch_size):
        stop = start + batch_size
        target = graph_message(model, features[start:stop])
        pred = graph_message(model, codes[start:stop])
        total += float(((target - pred) ** 2).sum())
        count += target.numel()
    return total / count


def feature_mse(features, codes):
    return float(((features - codes) ** 2).mean())


def logit_mse(features, codes, model, images, batch_size=256):
    total = 0.0
    count = 0
    for start in range(0, len(features), batch_size):
        stop = start + batch_size
        teacher_logits, _ = forward_with_codes(model, images[start:stop], features[start:stop])
        converted_logits, _ = forward_with_codes(model, images[start:stop], codes[start:stop])
        total += float(((teacher_logits - converted_logits) ** 2).sum())
        count += teacher_logits.numel()
    return total / count


def dcgs_encode(values, threshold_scale):
    codes, events, unit = signed_multilevel_encode(values, levels=levels, threshold_scale=threshold_scale)
    return codes, events, float(unit)


def dcgs_gamma_encode(values, gamma):
    codes, events, unit = signed_multilevel_encode(values, levels=levels, threshold_scale=0.75)
    return codes * gamma, events, float(unit)


def choose_uniform_parameters(features, images, model, objective):
    best = None
    for scale in scales:
        for offset in offsets:
            codes = encode(features, scale, offset)
            if objective == "feature_mse":
                loss = feature_mse(features, codes)
            elif objective == "message_mse":
                loss = message_mse(features, codes, model)
            elif objective == "logit_mse":
                loss = logit_mse(features, codes, model, images)
            else:
                raise ValueError(objective)
            candidate = {"scale": scale, "offset": offset, "loss": loss}
            if best is None or loss < best["loss"]:
                best = candidate
    return best


def choose_dcgs_parameters(features, model):
    best = None
    for threshold_scale in dcgs_threshold_scales:
        codes, _, unit = dcgs_encode(features, threshold_scale)
        loss = message_mse(features, codes, model)
        candidate = {"threshold_scale": threshold_scale, "unit": unit, "loss": loss}
        if best is None or loss < best["loss"]:
            best = candidate
    return best


def choose_dcgs_budget_match(features, target_events_per_element):
    best = None
    for threshold_scale in dcgs_budget_threshold_scales:
        _, events, unit = dcgs_encode(features, threshold_scale)
        event_rate = events / features.numel()
        gap = abs(event_rate - target_events_per_element)
        candidate = {"threshold_scale": threshold_scale, "unit": unit, "event_rate": event_rate, "gap": gap}
        if best is None or gap < best["gap"]:
            best = candidate
    return best


def choose_dcgs_gamma(features, images, model, objective, threshold_scale=0.75):
    codes, _, _ = dcgs_encode(features, threshold_scale)
    best = None
    for gamma in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0):
        scaled = codes * gamma
        if objective == "feature_mse":
            loss = feature_mse(features, scaled)
        elif objective == "message_mse":
            loss = message_mse(features, scaled, model)
        elif objective == "logit_mse":
            loss = logit_mse(features, scaled, model, images)
        else:
            raise ValueError(objective)
        candidate = {"gamma": gamma, "threshold_scale": threshold_scale, "loss": loss}
        if best is None or loss < best["loss"]:
            best = candidate
    return best


def evaluate_codes(model, images, targets, features, codes, method, adaptation, parameters, events=None):
    with torch.no_grad():
        logits, _ = forward_with_codes(model, images, codes)
        accuracy = float((logits.argmax(1) == targets).float().mean())
        mse = message_mse(features, codes, model)
        if events is None:
            events = int((codes != 0).sum())
    return {
        "method": method,
        "adaptation_label": adaptation,
        "accuracy": accuracy,
        "message_mse": mse,
        "events": int(events),
        "levels": levels,
        "parameters": parameters,
    }


def evaluate_seed(seed, train_images, test_images, test_labels):
    model = load_teacher(seed)
    cal_images = train_images[:calibration_count].to(device)
    images = test_images[:test_limit].to(device)
    targets = test_labels[:test_limit].to(device)
    with torch.no_grad():
        cal_features = teacher_features(model, cal_images)
        features = teacher_features(model, images)
        teacher_logits, _ = forward_with_codes(model, images, features)
        teacher_accuracy = float((teacher_logits.argmax(1) == targets).float().mean())

    message_best = choose_uniform_parameters(cal_features, cal_images, model, "message_mse")
    feature_best = choose_uniform_parameters(cal_features, cal_images, model, "feature_mse")
    logit_best = choose_uniform_parameters(cal_features, cal_images, model, "logit_mse")
    dcgs_best = choose_dcgs_parameters(cal_features, model)
    uniform_event_rate = int((encode(cal_features, 9.0, 0.0) != 0).sum()) / cal_features.numel()
    dcgs_budget_best = choose_dcgs_budget_match(cal_features, uniform_event_rate)
    dcgs_feature_gamma_best = choose_dcgs_gamma(cal_features, cal_images, model, "feature_mse")
    dcgs_logit_gamma_best = choose_dcgs_gamma(cal_features, cal_images, model, "logit_mse")
    dcgs_message_gamma_best = choose_dcgs_gamma(cal_features, cal_images, model, "message_mse")

    uniform_objectives = {
        "v1_scale_uniform_reference": {"scale": 9.0, "offset": 0.0, "selection": "fixed_v1_protocol"},
        "v2_message_mse_uniform_reference": message_best,
        "activation_feature_mse_uniform": feature_best,
        "logit_mse_uniform": logit_best,
    }
    uniform_codes = {name: encode(features, params["scale"], params["offset"])
                     for name, params in uniform_objectives.items()}

    methods = [
        ("v1_scale_uniform_reference", "internal_control", uniform_codes["v1_scale_uniform_reference"], None, uniform_objectives["v1_scale_uniform_reference"]),
        ("v2_message_mse_uniform_reference", "internal_control", uniform_codes["v2_message_mse_uniform_reference"], None, uniform_objectives["v2_message_mse_uniform_reference"]),
        ("activation_feature_mse_uniform", "faithful_adaptation", uniform_codes["activation_feature_mse_uniform"], None, uniform_objectives["activation_feature_mse_uniform"]),
        ("logit_mse_uniform", "proxy", uniform_codes["logit_mse_uniform"], None, uniform_objectives["logit_mse_uniform"]),
        ("dcgs_signed_multilevel_fixed", "faithful_adaptation",
         *dcgs_encode(features, 0.75)[:2], {"threshold_scale": 0.75, "unit_from_calibration": None, "selection": "fixed_dcgs_style_threshold"}),
        ("dcgs_signed_multilevel_message_selected", "proxy",
         *dcgs_encode(features, dcgs_best["threshold_scale"])[:2], dcgs_best),
        ("dcgs_signed_multilevel_budget_matched", "proxy",
         *dcgs_encode(features, dcgs_budget_best["threshold_scale"])[:2], dcgs_budget_best),
        ("dcgs_signed_multilevel_feature_mse_gamma", "faithful_adaptation",
         *dcgs_gamma_encode(features, dcgs_feature_gamma_best["gamma"])[:2], dcgs_feature_gamma_best),
        ("dcgs_signed_multilevel_logit_mse_gamma", "proxy",
         *dcgs_gamma_encode(features, dcgs_logit_gamma_best["gamma"])[:2], dcgs_logit_gamma_best),
        ("dcgs_signed_multilevel_message_mse_gamma", "proxy",
         *dcgs_gamma_encode(features, dcgs_message_gamma_best["gamma"])[:2], dcgs_message_gamma_best),
    ]

    rows = []
    for method, adaptation, codes, events, parameters in methods:
        rows.append({"seed": seed, "teacher_accuracy": teacher_accuracy,
                     **evaluate_codes(model, images, targets, features, codes, method, adaptation, parameters, events)})
    return rows


def summarize(rows):
    summary = {}
    for method in sorted({row["method"] for row in rows}):
        method_rows = [row for row in rows if row["method"] == method]
        summary[method] = {
            "accuracy_mean": statistics.fmean(row["accuracy"] for row in method_rows),
            "accuracy_sd": statistics.stdev(row["accuracy"] for row in method_rows),
            "message_mse_mean": statistics.fmean(row["message_mse"] for row in method_rows),
            "message_mse_sd": statistics.stdev(row["message_mse"] for row in method_rows),
            "events_mean": statistics.fmean(row["events"] for row in method_rows),
            "levels": sorted({row["levels"] for row in method_rows})[0],
        }
    return summary


def main():
    started = time.time()
    train_images, _ = load_images(run / "data/fashion_mnist_train.parquet")
    test_images, test_labels = load_images(run / "data/fashion_mnist_test.parquet")
    rows = []
    for seed in seeds:
        rows.extend(evaluate_seed(seed, train_images, test_images, test_labels))
        print(f"completed seed {seed}", flush=True)
    report = {
        "protocol": {
            "dataset": "Fashion-MNIST",
            "split": "official test, first 2000 examples per seed",
            "calibration": "official train, first 5000 examples per seed",
            "checkpoints": [f"teacher_seed{seed}.pt" for seed in seeds],
            "seeds": list(seeds),
            "levels": levels,
            "uniform_search_grid": {"scales": list(scales), "offsets": list(offsets), "candidates": len(scales) * len(offsets)},
            "dcgs_search_grid": {"threshold_scales": list(dcgs_threshold_scales), "candidates": len(dcgs_threshold_scales)},
            "dcgs_budget_search_grid": {"threshold_scales": list(dcgs_budget_threshold_scales), "candidates": len(dcgs_budget_threshold_scales), "target": "uniform-code event rate"},
            "dcgs_gamma_search_grid": {"gammas": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0], "candidates": 8},
            "forward": "unchanged teacher weights; converted codes drive kNN, winners, message, update, and readout",
        },
        "adaptation_labels": {
            "faithful_adaptation": "Algorithm transferred to the local Grapher; not the full external implementation.",
            "proxy": "External idea approximated with this benchmark's encoder/search; not a claim of reproducing published DCGS.",
            "internal_control": "Existing v1/v2 protocol recalculated for a like-for-like reference.",
        },
        "summary": summarize(rows),
        "rows": rows,
        "wall_seconds": time.time() - started,
    }
    path = run / "strong-baseline-results.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
