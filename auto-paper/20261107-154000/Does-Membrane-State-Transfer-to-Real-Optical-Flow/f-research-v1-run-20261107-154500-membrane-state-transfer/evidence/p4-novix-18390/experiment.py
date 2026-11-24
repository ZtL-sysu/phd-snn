#!/usr/bin/env python3
"""f-research-v1 P4 C1 correction-loop-v3 attempt #4 full experiment.

This is the sole experiment orchestrator.  It consumes only official archived
files plus project-local code, executes all registered seeds and diagnostic
matrices, preserves per-condition raw NPZs, and writes *working* evidence.  The
separate finalization step writes result.json/config.json last, after tests and
validation, so a failed run cannot masquerade as a complete deliverable.
"""
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
import sklearn
import scipy
from scipy import stats as scipy_stats
import torch

ROOT = Path("/home/novix/workspace/project")
EVIDENCE = ROOT / "evidence"
RAW = EVIDENCE / "raw"
LOGS = ROOT / "logs"
DATA = ROOT / "data"
for directory in (EVIDENCE, RAW, LOGS, DATA):
    directory.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))
from src.data_pipeline import build_davis, build_sintel, file_record, make_synthetic
from src.graph_pipeline import build_graph_bundle, sha256_file
from src.metrics import (
    add_yoked_noise,
    benjamini_hochberg,
    bootstrap_mean_ci,
    exact_paired_sign_flip,
    feature_dispersion,
    fisher_scatter,
    group_stratified_split,
    measure_split,
    paired_bootstrap_delta,
    pca_train_only,
    gaussian_random_projection,
    stratified_split,
    to_jsonable,
)
from src.models import DirectInputModel, ResolvedGraphModel


GRIND_BLOCK = {
    "上一轮失败点": "18273 有效跑完全量、有真实方法数值，但两真实域 unavailable、预注册强信号 +0.0117 << +0.15、一因子消融全 0；biological LIF KC 方差严格 0，identity/A=0 LIF 方差非零 → round-006「整体旁路」假设被部分否证；且 `project/result.json` / `config.json` 第三次未落在可 pull workspace。",
    "本轮假设": "塌缩不是整体旁路、也不必是唯一动力学不动点，而是 **hard-spike 门控工作点失配**：在 15,091,983 边、谱半径 504.30 的 biological graph 上，`syn = index_add · 8/fan_in · 8` 的扇入归一化把 hop-3 resolved KC 的膜电位分布整体压到固定阈值 θ=0.15 之下，于是 KC 从不发放（KC hard-spike rate = 0），soft feature 退化为常量 `sigmoid(−θ·slope)`；identity / A=0 图的有效增益不同所以能发放（方差非零）。可证伪推论：(i) 若把 θ 降到 0（无门控纯模拟态）或按训练集标定到目标发放率，biological KC std 应恢复 >0；(ii) 若 θ=0 下仍严格 0，则塌缩在门控**之前**（drive→syn→v），本假设被否证，转向逐环节 instrumentation + 两室状态拆解；(iii) 即便方差恢复，若 probe_acc 仍 ≈chance 而 A=0=1.0，则「方差塌缩」与「标签信息丢失」是可分离的两个现象，必须分别报告，不得混为一谈。",
    "具体改动": [
        "1.【新增·核心】**等发放率 yoked 标定**：在**仅训练集**上把 biological / degree-null / identity / A=0 四类图的 θ 分别标定到同一预注册目标 KC hard-spike rate `r* ∈ {0.02, 0.10}`，再在**发放率相等**条件下重跑 4 图 × {stateless, LIF} 的 2×2。attempt #3 的 2×2 用固定 θ=0.15、没有 yoked 标定，无法把「结构」与「工作点」解耦。",
        "2.【新增·核心】**门控工作点网格 + 逐跳膜电位分布**：固定其余一切，扫 `θ ∈ {0, 0.01, 0.05, 0.15, 0.3}` × `fan_in_gain ∈ {1, 8, 32}`，每格逐跳落盘膜电位的 min/max/mean/std、超过 θ 的比例、hard-spike rate、KC 特征跨样本 std / 非常数维 / probe_acc(h)。θ=0 是「无门控上界」决定性对照。attempt #3 的 λ×K 相图扫的是传播算子缩放与步数，**从未扫脉冲门控 θ / 扇入增益**。",
        "3.【新增·核心】**方差塌缩与标签信息丢失分开测量**：每个条件每 hop 分别落盘 (a) `feature_std` / 非常数维，(b) 类间/类内散度 Fisher 比 `S_B/S_W` 与类条件均值距离，(c) 只在训练集拟合的 ridge `probe_acc(h)` + 5-seed bootstrap CI，(d) **方差匹配噪声注入**：对塌缩成常量的 KC 特征注入各向同性高斯噪声，使 `feature_std` 数值等于 identity-LIF 实测的 0.2075（噪声 seed 预注册），再看 probe_acc 是否从 chance 回升；另加标签置换阴性对照。attempt #3 只测了 feature_std 轨迹与 probe_acc(h)，**从未把二者分开、也从未注入 yoked 噪声**。",
        "4.【新增】**读出状态变量选择**：等维数 / 等参数量、同一 split、同一 5 seeds，只换送进同一个 ridge 的内部量：`v_raw` / `hard_spike` / `soft_sigmoid`（现口径）/ `spike_count` / `threshold_crossing_time`。检验常量塌缩是否只是「读错了内部量」。另加 yoked 等维随机投影对照（排除「只是维数变了」）。attempt #3 只读 8 帧 soft-sigmoid 均值。",
        "5.【新增·协议修复】**真实域预注册协议更换（训练前写死，禁止 post-hoc）**：DAVIS 改用 trainval-480p ZIP 内**官方 GT 分割 mask 的质心逐帧位移方向**作标签（不是 full-frame 帧差运动能量；18228 的 post-hoc v2 教训），Sintel 改用 **HTTP Range 分块 + 断点续传 + 每块校验**（18228 已验证该策略可拿全 178,853,187 B 边表），并把 ROI / margin / 像素处理规则 / 类别平衡规则在 `config_preregistered.json` 里**训练前冻结并哈希锁定**。仍维持：任一真实域 5-seed ceiling < 0.70 即标 `unavailable`；两个真实域都 unavailable 时**不得作迁移主张**，只报告 SYNTHETIC 侧机制结果。**不许在看到 v1 结果后再注册 v2**。",
        "6.【新增·实现修复，针对第三次缺陷】产物持久化**不依赖 git commit**：在全部计算结束的最后一步，用 Python 直接 `open(path,'wb').write(...)` 写出 **`project/result.json` 与 `project/config.json` 两个主文件**，再写 byte-identical 的 `project/evidence/result_snapshot.json` 与 `project/evidence/config_snapshot.json`；随后立即执行 `os.path.exists` / `os.path.getsize` / `sha256` 自检并把**实测输出原样**贴进最终回复；另写 `project/MANIFEST.txt` 列出每个预期文件的存在性与字节数。最终回复还必须给出 `ls -l project/result.json project/config.json` 的**真实命令输出**。**不许只在回复里声称写了却没有文件**；不许只写 snapshot 而漏掉主文件。",
        "7.【沿用·已验证有效】完整边表 178,853,187 B（`prefix=false`、Range 分块拼接 + gzip 校验）、eye→KC exact-hop 自检并按冻结回退规则取 K=3 / 2,544 annotated KC、SYNTHETIC ceiling 1.0、训练前 invariant checks、5 固定 seeds [1,2,3,4,5]、2000 次 paired-seed bootstrap 95% CI、exact paired sign-flip p、BH-FDR q=0.05、自适应阈值 / 不应期 / E-I 符号各一因子移除消融、打乱帧序 + flash 阴性对照、A=0（明确定义为输入信息上界，不得写成生物接线优势）、保度零模型（保 in/out 度序列 / 权重集合 / nnz / 互反边对）、identity 图、每条件每 seed 一个 raw NPZ、完整原始日志与硬件报告。",
        "8.【不变】`minimum` / `expected_strong` 一律沿用 C1 `guidance.md` §Expected Results（real-domain `delta >= +0.15` / `>= +0.25` + 迁移裁决 + 一因子消融），**不静默下调**；`runtime_hours` 只是可行性估算，**不是超时参数**；提交命令不带 `--max-turns` / `--timeout`、不阻塞 `watch`。",
    ],
    "预期信号_若失败下一步": "预期：存在 (θ, gain) 使 biological KC std > 0 且 KC hard-spike rate > 0；等发放率 yoked 2×2 下四图 `delta` 两两 CI 跨 0（结构效应可由工作点解释）；`v_raw` 或 `hard_spike` 读出的 probe_acc 高于 `soft_sigmoid` 且 CI 下界 > 0；Fisher 比与 probe_acc 一致，方差匹配噪声注入**不能**让 probe_acc 回到 A=0 水平（证明方差与信息可分离）；两真实域至少一个 ceiling >= 0.70。若失败（θ=0 下仍严格 0 / 五种读出全 ≈chance / yoked 后四图仍可区分）：本假设被否证，塌缩位于门控之前；下一步转向逐环节 drive→syn→v 全张量 instrumentation 与两室（树突/胞体）状态拆解，继续死磕同一 C1，按 §3.6(4) 保留全部失败证据，**不换题、不放弃**（当前 `abandon_allowed=False`）。两真实域仍 unavailable：如实标 unavailable、不做迁移主张，**不把「实验跑完」写成「结果达标」**。",
}

CONFIG_DIFF_18273 = GRIND_BLOCK["具体改动"]


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(message: str) -> None:
    line = f"[{utc_now()}] {message}"
    print(line, flush=True)
    with (LOGS / "experiment.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config() -> tuple[dict[str, Any], str]:
    path = ROOT / "config_preregistered.json"
    expected = (ROOT / "config_preregistered.sha256").read_text().split()[0]
    actual = sha256_file(path)
    if actual != expected:
        raise RuntimeError(f"preregistration hash mismatch {actual} != {expected}")
    with path.open(encoding="utf-8") as f:
        return json.load(f), actual


def hardware_report() -> dict[str, Any]:
    query = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
        capture_output=True, text=True, check=False,
    )
    devices = []
    for i in range(torch.cuda.device_count()):
        p = torch.cuda.get_device_properties(i)
        devices.append({"index": i, "name": p.name, "total_memory_bytes": int(p.total_memory)})
    return {
        "nvidia_smi_query_stdout": query.stdout.strip(),
        "nvidia_smi_returncode": query.returncode,
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "cudnn_version": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None,
        "devices": devices,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "pandas_version": pd.__version__,
        "sklearn_version": sklearn.__version__,
        "torch_deterministic_algorithms_enabled": torch.are_deterministic_algorithms_enabled(),
        "torch_deterministic_warn_only": torch.is_deterministic_algorithms_warn_only_enabled(),
    }


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")


def write_raw_npz(domain: str, condition: str, seed: int, metrics: dict[str, Any],
                  labels_test: np.ndarray, predictions: np.ndarray, test_indices: np.ndarray,
                  extra_arrays: dict[str, np.ndarray] | None = None) -> str:
    path = RAW / f"{safe_name(domain)}__{safe_name(condition)}__seed-{seed}.npz"
    scalar_metadata = {k: v for k, v in metrics.items()
                       if k not in {"predictions", "test_indices"} and not isinstance(v, np.ndarray)}
    arrays: dict[str, Any] = {
        "labels_test": np.asarray(labels_test, dtype=np.int64),
        "predictions": np.asarray(predictions, dtype=np.int64),
        "test_indices": np.asarray(test_indices, dtype=np.int64),
        "accuracy": np.array(float(metrics["accuracy"]), dtype=np.float64),
        "feature_std": np.array(float(metrics.get("feature_std", 0.0)), dtype=np.float64),
        "nonconstant_dimensions": np.array(int(metrics.get("nonconstant_dimensions", 0)), dtype=np.int64),
        "Fisher_ratio": np.array(np.nan if metrics.get("Fisher_ratio") is None else metrics["Fisher_ratio"], dtype=np.float64),
        "metadata_json": np.array(json.dumps(to_jsonable(scalar_metadata), ensure_ascii=False, separators=(",", ":"))),
    }
    if extra_arrays:
        arrays.update({k: np.asarray(v) for k, v in extra_arrays.items()})
    np.savez_compressed(path, **arrays)
    return str(path.relative_to(ROOT))


def csv_write(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("status\nno_rows\n", encoding="utf-8")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key); seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(to_jsonable(v), ensure_ascii=False, separators=(",", ":"))
                             if isinstance(v, (dict, list, tuple, np.ndarray)) else to_jsonable(v)
                             for k, v in row.items()})


def compact_metric(metric: dict[str, Any]) -> dict[str, Any]:
    return to_jsonable({k: v for k, v in metric.items() if k not in {"predictions", "test_indices"}})


def summarize_seed_metrics(per_seed: dict[int, dict[str, Any]], bootstrap: int, bootstrap_seed: int) -> dict[str, Any]:
    acc = [per_seed[s]["accuracy"] for s in sorted(per_seed)]
    stds = [per_seed[s].get("feature_std", 0.0) for s in sorted(per_seed)]
    spikes = [per_seed[s].get("kc_hard_spike_rate", 0.0) for s in sorted(per_seed)]
    fisher = [per_seed[s].get("Fisher_ratio") for s in sorted(per_seed)]
    finite_fisher = [float(v) for v in fisher if v is not None and np.isfinite(v)]
    return {
        "accuracy": bootstrap_mean_ci(acc, bootstrap, bootstrap_seed),
        "feature_std": bootstrap_mean_ci(stds, bootstrap, bootstrap_seed + 1),
        "kc_hard_spike_rate": bootstrap_mean_ci(spikes, bootstrap, bootstrap_seed + 2),
        "Fisher_ratio_mean_finite": float(np.mean(finite_fisher)) if finite_fisher else None,
        "per_seed": {str(k): compact_metric(v) for k, v in per_seed.items()},
    }


class ExperimentRunner:
    def __init__(self, config: dict[str, Any], prereg_hash: str, graph: dict[str, Any]) -> None:
        self.config = config
        self.prereg_hash = prereg_hash
        self.graph = graph
        self.seeds = [int(x) for x in config["reproducibility"]["seeds"]]
        self.bootstrap = int(config["reproducibility"]["bootstrap_replicates"])
        self.bootstrap_seed = int(config["reproducibility"]["bootstrap_seed"])
        self.alpha = float(config["reproducibility"]["ridge_l2"])
        self.mi_bins = int(config["condition_matrix"]["variance_information"]["mi_bins"])
        self.main_rows: list[dict[str, Any]] = []
        self.gate_rows: list[dict[str, Any]] = []
        self.yoked_rows: list[dict[str, Any]] = []
        self.variance_rows: list[dict[str, Any]] = []
        self.readout_rows: list[dict[str, Any]] = []
        self.probe_hop_rows: list[dict[str, Any]] = []
        self.variance_trajectory_rows: list[dict[str, Any]] = []
        self.trace_rows: list[dict[str, Any]] = []
        self.raw_files: list[str] = []
        self.condition_counter = 0

    def splits(self, y: np.ndarray, groups: np.ndarray | None = None) -> dict[int, tuple[np.ndarray, np.ndarray]]:
        result = {}
        for seed in self.seeds:
            result[seed] = (group_stratified_split(y, groups, seed) if groups is not None
                            else stratified_split(y, seed))
        return result

    def evaluate_simulation(self, domain: str, condition: str, sim: dict[str, Any], y: np.ndarray,
                            splits: dict[int, tuple[np.ndarray, np.ndarray]],
                            selected_seeds: list[int] | None = None,
                            row_extras: dict[str, Any] | None = None,
                            record_hops: bool = True) -> dict[int, dict[str, Any]]:
        selected = self.seeds if selected_seeds is None else selected_seeds
        per_seed: dict[int, dict[str, Any]] = {}
        features = sim["primary_features"]
        sample_spike = np.mean(sim["state_features"]["hard_spike"], axis=1)
        for seed in selected:
            train, test = splits[seed]
            metric = measure_split(features, y, train, test, alpha=self.alpha, mi_bins=self.mi_bins)
            metric["kc_hard_spike_rate"] = float(np.mean(sample_spike[test]))
            metric["runtime_seconds_shared_simulation"] = float(sim["runtime_seconds"])
            metric["peak_gpu_mib"] = int(sim["peak_gpu_mib"])
            metric["theta"] = float(sim["theta"])
            metric["fan_in_gain"] = float(sim["fan_in_gain"])
            metric["condition"] = condition
            metric["domain"] = domain
            extra_arrays: dict[str, np.ndarray] = {}
            if record_hops and sim.get("hop_features"):
                hop_std, hop_acc, hop_fisher, hop_nonconst = [], [], [], []
                for hop, hop_x in enumerate(sim["hop_features"]):
                    if hop_x.shape[1] == 0:
                        continue
                    full_dimensions = hop_x.shape[1]
                    probe_cap = int(self.graph["resolved_kc_count"])
                    if full_dimensions > probe_cap:
                        probe_indices = np.linspace(0, full_dimensions - 1, probe_cap, dtype=np.int64)
                        probe_x = hop_x[:, probe_indices]
                    else:
                        probe_x = hop_x
                    hm = measure_split(probe_x, y, train, test, alpha=self.alpha, mi_bins=self.mi_bins)
                    # Dispersion and scatter describe the complete layer, while
                    # the supervised probe has the frozen equal-parameter cap.
                    hm.update(feature_dispersion(hop_x[test]))
                    hm.update(fisher_scatter(hop_x[test], y[test]))
                    hm["full_layer_dimensions"] = int(full_dimensions)
                    hm["probe_input_dimensions"] = int(probe_x.shape[1])
                    hm["probe_dimension_selection"] = "all" if full_dimensions <= probe_cap else "root_id_ordered_even_spacing"
                    hop_std.append(hm["feature_std"]); hop_acc.append(hm["accuracy"])
                    hop_fisher.append(np.nan if hm["Fisher_ratio"] is None else hm["Fisher_ratio"])
                    hop_nonconst.append(hm["nonconstant_dimensions"])
                    base_row = {
                        "domain": domain, "condition": condition, "seed": seed, "hop": hop,
                        "feature_std": hm["feature_std"], "nonconstant_dimensions": hm["nonconstant_dimensions"],
                        "S_B": hm["S_B"], "S_W": hm["S_W"], "Fisher_ratio": hm["Fisher_ratio"],
                        "class_conditional_mean_distance": hm["class_conditional_mean_distance"],
                        "mutual_information_nats": hm["mutual_information_nats"],
                        "probe_accuracy": hm["accuracy"], "dimensions": hm["dimensions"],
                        "full_layer_dimensions": hm["full_layer_dimensions"],
                        "probe_input_dimensions": hm["probe_input_dimensions"],
                        "probe_dimension_selection": hm["probe_dimension_selection"],
                        "mi_bins": hm["bins_requested"], "mi_estimator": hm["estimator"],
                    }
                    if hop < len(sim.get("hop_voltage_stats", [])):
                        base_row["voltage_stats"] = sim["hop_voltage_stats"][hop]
                    if row_extras: base_row.update(row_extras)
                    self.variance_rows.append(base_row)
                    self.probe_hop_rows.append({k: base_row[k] for k in base_row if k in {
                        "domain", "condition", "seed", "hop", "probe_accuracy", "Fisher_ratio",
                        "feature_std", "nonconstant_dimensions", "dimensions"}})
                    self.variance_trajectory_rows.append({
                        "domain": domain, "condition": condition, "seed": seed, "hop": hop,
                        "feature_std": hm["feature_std"], "nonconstant_dimensions": hm["nonconstant_dimensions"],
                    })
                extra_arrays.update({
                    "hop_feature_std": np.asarray(hop_std, dtype=np.float64),
                    "hop_probe_accuracy": np.asarray(hop_acc, dtype=np.float64),
                    "hop_Fisher_ratio": np.asarray(hop_fisher, dtype=np.float64),
                    "hop_nonconstant_dimensions": np.asarray(hop_nonconst, dtype=np.int64),
                })
            raw = write_raw_npz(domain, condition, seed, metric, y[test], metric["predictions"],
                                metric["test_indices"], extra_arrays)
            self.raw_files.append(raw)
            metric["raw_npz"] = raw
            per_seed[seed] = metric
            row = {
                "domain": domain, "condition": condition, "seed": seed,
                "accuracy": metric["accuracy"], "feature_std": metric["feature_std"],
                "nonconstant_dimensions": metric["nonconstant_dimensions"],
                "Fisher_ratio": metric["Fisher_ratio"],
                "kc_hard_spike_rate": metric["kc_hard_spike_rate"],
                "theta": metric["theta"], "fan_in_gain": metric["fan_in_gain"],
                "peak_gpu_mib": metric["peak_gpu_mib"], "runtime_seconds": metric["runtime_seconds_shared_simulation"],
                "raw_npz": raw,
            }
            if row_extras: row.update(row_extras)
            self.main_rows.append(row)
        self.condition_counter += 1
        return per_seed

    def evaluate_features(self, domain: str, condition: str, x: np.ndarray, y: np.ndarray,
                          splits: dict[int, tuple[np.ndarray, np.ndarray]],
                          selected_seeds: list[int] | None = None,
                          row_extras: dict[str, Any] | None = None,
                          train_label_provider: Callable[[int, np.ndarray], np.ndarray] | None = None) -> dict[int, dict[str, Any]]:
        selected = self.seeds if selected_seeds is None else selected_seeds
        per_seed = {}
        for seed in selected:
            train, test = splits[seed]
            train_labels = train_label_provider(seed, train) if train_label_provider else None
            metric = measure_split(x, y, train, test, alpha=self.alpha, mi_bins=self.mi_bins,
                                   train_labels=train_labels)
            metric.update({"condition": condition, "domain": domain, "kc_hard_spike_rate": 0.0,
                           "theta": None, "fan_in_gain": None, "peak_gpu_mib": 0,
                           "runtime_seconds_shared_simulation": 0.0})
            raw = write_raw_npz(domain, condition, seed, metric, y[test], metric["predictions"], metric["test_indices"])
            self.raw_files.append(raw); metric["raw_npz"] = raw; per_seed[seed] = metric
            row = {"domain": domain, "condition": condition, "seed": seed,
                   "accuracy": metric["accuracy"], "feature_std": metric["feature_std"],
                   "nonconstant_dimensions": metric["nonconstant_dimensions"],
                   "Fisher_ratio": metric["Fisher_ratio"], "kc_hard_spike_rate": 0.0,
                   "raw_npz": raw}
            if row_extras: row.update(row_extras)
            self.main_rows.append(row)
        self.condition_counter += 1
        return per_seed

    def summarize(self, per_seed: dict[int, dict[str, Any]]) -> dict[str, Any]:
        return summarize_seed_metrics(per_seed, self.bootstrap, self.bootstrap_seed)

    def contrast(self, first: dict[int, dict[str, Any]], second: dict[int, dict[str, Any]],
                 name: str) -> dict[str, Any]:
        seeds = sorted(set(first) & set(second))
        a = [first[s]["accuracy"] for s in seeds]
        b = [second[s]["accuracy"] for s in seeds]
        delta = paired_bootstrap_delta(a, b, self.bootstrap, self.bootstrap_seed)
        p = exact_paired_sign_flip(delta["paired_differences"])
        delta.update({"name": name, "exact_p_two_sided": p, "seeds": seeds,
                      "minimum_possible_two_sided_p_n5": 0.0625})
        return delta

    def run_ceiling(self, domain: str, frames: np.ndarray, y: np.ndarray,
                    groups: np.ndarray | None = None) -> dict[str, Any]:
        splits = self.splits(y, groups)
        x = frames.reshape(frames.shape[0], -1)
        per_seed = self.evaluate_features(domain, "ceiling_flattened_pixels", x, y, splits)
        summary = self.summarize(per_seed)
        summary["available"] = summary["accuracy"]["mean"] >= (0.9 if domain == "SYNTHETIC" else 0.7)
        summary["threshold"] = 0.9 if domain == "SYNTHETIC" else 0.7
        summary["split_type"] = "stratified" if groups is None else "sequence_group_stratified"
        return {"splits": splits, "per_seed": per_seed, "summary": summary}

    def calibration_candidates(self, model: Any, frames: np.ndarray, splits: dict[int, tuple[np.ndarray, np.ndarray]],
                               targets: list[float], dynamics: str = "LIF", parameter: str = "theta",
                               fixed_theta: float = 0.15, fixed_gain: float = 8.0) -> dict[tuple[int, float], dict[str, float]]:
        if parameter == "theta":
            coarse = [0.0, 0.0025, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.3, 0.5, 1, 2, 4, 8, 16, 32, 64]
        elif parameter == "gain":
            coarse = [0.0, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 32, 64]
        else:
            raise ValueError(parameter)
        rates: dict[float, np.ndarray] = {}

        def run_candidate(value: float) -> None:
            if value in rates: return
            theta = value if parameter == "theta" else fixed_theta
            gain = value if parameter == "gain" else fixed_gain
            sim = model.simulate(frames, dynamics=dynamics, theta=theta, fan_in_gain=gain,
                                 batch_size=64, capture_hops=False)
            rates[value] = np.mean(sim["state_features"]["hard_spike"], axis=1)
            del sim; gc.collect()

        for value in coarse:
            run_candidate(float(value))
        refine: set[float] = set()
        for seed, (train, _) in splits.items():
            for target in targets:
                errs = [abs(float(rates[v][train].mean()) - target) for v in coarse]
                i = int(np.argmin(errs)); lo = coarse[max(0, i-1)]; hi = coarse[min(len(coarse)-1, i+1)]
                refine.update(float(v) for v in np.linspace(lo, hi, 9))
        for value in sorted(refine): run_candidate(value)
        all_values = sorted(rates)
        selected: dict[tuple[int, float], dict[str, float]] = {}
        for seed, (train, _) in splits.items():
            for target in targets:
                # Ties choose the larger threshold/gain as frozen.
                best = min(all_values, key=lambda v: (abs(float(rates[v][train].mean()) - target), -v))
                selected[(seed, target)] = {
                    parameter: float(best),
                    "train_rate": float(rates[best][train].mean()),
                    "target": float(target),
                    "absolute_error": abs(float(rates[best][train].mean()) - target),
                    "candidate_count": len(all_values),
                    "calibration_fit": "training_only",
                }
        return selected


def add_bh(contrasts: list[dict[str, Any]]) -> None:
    qs = benjamini_hochberg([float(c["exact_p_two_sided"]) for c in contrasts])
    for contrast, q in zip(contrasts, qs): contrast["BH_q"] = q


def run() -> dict[str, Any]:
    wall_started = time.perf_counter()
    config, prereg_hash = load_config()
    log(f"preregistration verified sha256={prereg_hash}")
    np.random.seed(config["reproducibility"]["stimulus_seed"])
    torch.manual_seed(config["reproducibility"]["stimulus_seed"])
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(config["reproducibility"]["stimulus_seed"])
    # Request deterministic kernels globally. warn_only keeps the full registered
    # run executable if a sparse CUDA kernel lacks a deterministic alternative;
    # all stochastic arrays and split/calibration decisions remain seed-frozen.
    torch.use_deterministic_algorithms(True, warn_only=True)

    graph = build_graph_bundle(config, force=False)
    runner = ExperimentRunner(config, prereg_hash, graph)
    synthetic = make_synthetic(config)
    frames, y, flash = synthetic["frames"], synthetic["labels"], synthetic["flash_frames"]
    synth_ceiling = runner.run_ceiling("SYNTHETIC", frames, y)
    synth_splits = synth_ceiling["splits"]
    log(f"SYNTHETIC ceiling mean={synth_ceiling['summary']['accuracy']['mean']:.6f}")

    real_data: dict[str, Any] = {}
    real_ceiling: dict[str, Any] = {}
    for domain, builder in (("DAVIS", build_davis), ("SINTEL", build_sintel)):
        try:
            ds = builder(config)
            ceiling = runner.run_ceiling(domain, ds["frames"], ds["labels"], ds["groups"])
            real_data[domain] = ds; real_ceiling[domain] = ceiling
            log(f"{domain} protocol n={len(ds['labels'])} ceiling={ceiling['summary']['accuracy']['mean']:.6f} available={ceiling['summary']['available']}")
        except Exception as exc:
            archive_key = "davis" if domain == "DAVIS" else "sintel"
            archive = DATA / config["data"][archive_key]["archive"]
            real_ceiling[domain] = {
                "summary": {"available": False, "threshold": 0.7, "accuracy": {"mean": None},
                            "reason": f"{type(exc).__name__}: {exc}", "observed_archive_bytes": archive.stat().st_size if archive.exists() else 0}
            }
            log(f"{domain} unavailable: {type(exc).__name__}: {exc}")

    width, K = int(graph["resolved_kc_count"]), int(graph["actual_K"])
    device = "cuda" if torch.cuda.is_available() else "cpu"
    bio = ResolvedGraphModel(graph["paths"]["biological_layers"], graph["paths"]["biological_retina_xy"], config, device)
    null = ResolvedGraphModel(graph["paths"]["degree_null_layers"], graph["paths"]["degree_null_retina_xy"], config, device)
    identity = DirectInputModel(width, K, config, "identity", device)
    a0 = DirectInputModel(width, K, config, "A0", device)
    models = {"biological": bio, "degree_null": null, "identity": identity, "A0": a0}

    # A. Base conditions.
    base_specs = {
        "stateless": (bio, {"dynamics": "stateless", "theta": 0.15, "fan_in_gain": 8.0}),
        "lif_homeostasis": (bio, {"dynamics": "LIF", "theta": 0.15, "fan_in_gain": 8.0}),
        "lif_combo": (bio, {"dynamics": "LIF", "theta": 0.15, "fan_in_gain": 8.0, "combo": True}),
        "degree_null_lif": (null, {"dynamics": "LIF", "theta": 0.15, "fan_in_gain": 8.0}),
        "A0": (a0, {"dynamics": "LIF", "theta": 0.15, "fan_in_gain": 8.0}),
    }
    base_results: dict[str, dict[int, dict[str, Any]]] = {}
    retained: dict[str, dict[str, Any]] = {}
    for name, (model, kwargs) in base_specs.items():
        log(f"base condition {name}")
        sim = model.simulate(frames, batch_size=64, capture_hops=True, **kwargs)
        base_results[name] = runner.evaluate_simulation("SYNTHETIC", name, sim, y, synth_splits)
        if name in {"lif_homeostasis", "A0", "lif_combo"}: retained[name] = sim
        else: del sim; gc.collect()
    base_summaries = {name: runner.summarize(values) for name, values in base_results.items()}
    base_contrasts = [runner.contrast(values, base_results["stateless"], f"{name}-stateless")
                      for name, values in base_results.items() if name != "stateless"]
    add_bh(base_contrasts)

    # Identity fixed-threshold negative/control condition.
    identity_sim = identity.simulate(frames, dynamics="LIF", theta=0.15, fan_in_gain=8.0, batch_size=64)
    identity_result = runner.evaluate_simulation("SYNTHETIC", "identity_lif", identity_sim, y, synth_splits)
    identity_summary = runner.summarize(identity_result)

    # B. Complete theta x fan-in-gain operating grid.
    gate_grid: list[dict[str, Any]] = []
    grid_results: dict[tuple[float, float], dict[int, dict[str, Any]]] = {}
    for theta in config["condition_matrix"]["gate_grid"]["theta"]:
        for gain in config["condition_matrix"]["gate_grid"]["fan_in_gain"]:
            condition = f"gate_theta-{theta:g}_gain-{gain:g}"
            log(f"gate grid {condition}")
            if float(theta) == 0.15 and float(gain) == 8.0:
                sim = retained["lif_homeostasis"]
            else:
                sim = bio.simulate(frames, dynamics="LIF", theta=float(theta), fan_in_gain=float(gain), batch_size=64)
            per = runner.evaluate_simulation("SYNTHETIC", condition, sim, y, synth_splits,
                                             row_extras={"matrix": "gate_grid", "theta_grid": theta, "gain_grid": gain})
            grid_results[(float(theta), float(gain))] = per
            cell = {"theta": float(theta), "fan_in_gain": float(gain), "summary": runner.summarize(per),
                    "hop_voltage_stats": sim["hop_voltage_stats"]}
            gate_grid.append(cell)
            for seed, metric in per.items():
                runner.gate_rows.append({"theta": theta, "fan_in_gain": gain, "seed": seed,
                    "feature_std": metric["feature_std"], "nonconstant_dimensions": metric["nonconstant_dimensions"],
                    "kc_hard_spike_rate": metric["kc_hard_spike_rate"], "probe_accuracy": metric["accuracy"],
                    "Fisher_ratio": metric["Fisher_ratio"], "peak_gpu_mib": metric["peak_gpu_mib"],
                    "runtime_seconds": metric["runtime_seconds_shared_simulation"],
                    "hop_voltage_stats": sim["hop_voltage_stats"], "raw_npz": metric["raw_npz"]})
            if sim is not retained.get("lif_homeostasis"): del sim; gc.collect()

    # C. Train-only firing-rate-yoked 4 graph x 2 dynamics.
    targets = [float(v) for v in config["condition_matrix"]["yoked_firing_rate"]["targets"]]
    calibration: dict[str, dict[tuple[int, float], dict[str, float]]] = {}
    yoked_results: dict[float, dict[str, dict[str, dict[int, dict[str, Any]]]]] = {
        target: defaultdict(dict) for target in targets}
    for graph_name, model in models.items():
        log(f"yoked threshold calibration graph={graph_name}")
        selected = runner.calibration_candidates(model, frames, synth_splits, targets, dynamics="LIF", parameter="theta")
        calibration[graph_name] = selected
        for target in targets:
            for dynamics in ("stateless", "LIF"):
                by_seed: dict[int, dict[str, Any]] = {}
                unique_theta = sorted({selected[(seed, target)]["theta"] for seed in runner.seeds})
                for theta in unique_theta:
                    chosen_seeds = [s for s in runner.seeds if selected[(s, target)]["theta"] == theta]
                    sim = model.simulate(frames, dynamics=dynamics, theta=theta, fan_in_gain=8.0,
                                         batch_size=64, capture_hops=True)
                    condition = f"yoked_r-{target:g}_{graph_name}_{dynamics}"
                    evaluated = runner.evaluate_simulation(
                        "SYNTHETIC", condition, sim, y, synth_splits, selected_seeds=chosen_seeds,
                        row_extras={"matrix": "yoked_2x2", "target_rate": target,
                                    "graph": graph_name, "dynamics": dynamics},
                    )
                    for seed, metric in evaluated.items():
                        cal = selected[(seed, target)]
                        metric["calibration_train_rate"] = cal["train_rate"]
                        metric["calibration_absolute_error"] = cal["absolute_error"]
                        tolerance = max(0.01, 0.25 * target)
                        metric["yoked_tolerance"] = tolerance
                        metric["heldout_yoke_achieved"] = abs(metric["kc_hard_spike_rate"] - target) <= tolerance
                        by_seed[seed] = metric
                        runner.yoked_rows.append({
                            "target_rate": target, "graph": graph_name, "dynamics": dynamics, "seed": seed,
                            "calibrated_theta": theta, "train_rate": cal["train_rate"],
                            "heldout_rate": metric["kc_hard_spike_rate"],
                            "absolute_heldout_error": abs(metric["kc_hard_spike_rate"]-target),
                            "yoke_achieved": metric["heldout_yoke_achieved"],
                            "feature_std": metric["feature_std"], "probe_accuracy": metric["accuracy"],
                            "Fisher_ratio": metric["Fisher_ratio"], "raw_npz": metric["raw_npz"],
                        })
                    del sim; gc.collect()
                yoked_results[target][graph_name][dynamics] = by_seed
    yoked_summaries: dict[str, Any] = {}
    yoked_contrasts: list[dict[str, Any]] = []
    for target in targets:
        key = str(target)
        yoked_summaries[key] = {}
        reference = yoked_results[target]["biological"]["stateless"]
        for graph_name in models:
            yoked_summaries[key][graph_name] = {}
            for dynamics in ("stateless", "LIF"):
                r = yoked_results[target][graph_name][dynamics]
                yoked_summaries[key][graph_name][dynamics] = runner.summarize(r)
                c = runner.contrast(r, reference, f"r={target}:{graph_name}:{dynamics}-biological:stateless")
                yoked_contrasts.append(c)
                for seed in runner.seeds:
                    # Fill delta column in the already accumulated CSV rows.
                    for row in reversed(runner.yoked_rows):
                        if row["target_rate"] == target and row["graph"] == graph_name and row["dynamics"] == dynamics and row["seed"] == seed:
                            row["delta_vs_biological_stateless"] = r[seed]["accuracy"] - reference[seed]["accuracy"]
                            break
    add_bh(yoked_contrasts)

    # D. Variance-information separation controls on the observed biological LIF readout.
    collapse_x = retained["lif_homeostasis"]["primary_features"]
    noise_results: dict[str, dict[int, dict[str, Any]]] = {"variance_matched": {}, "variance_mismatched": {}}
    for label, target_std in (("variance_matched", 0.2075), ("variance_mismatched", 0.10375)):
        for seed, noise_seed in zip(runner.seeds, config["reproducibility"]["noise_seeds"]):
            train, _ = synth_splits[seed]
            # A variance-only control must not retain label geometry when the
            # observed reference happens not to be perfectly constant in this
            # run. Anchor every sample to the train-only per-feature mean, then
            # add preregistered isotropic noise at the exact training std.
            train_mean = collapse_x[train].mean(axis=0, keepdims=True)
            constant_reference = np.broadcast_to(train_mean, collapse_x.shape).copy()
            noisy, noise_meta = add_yoked_noise(constant_reference, train, target_std, int(noise_seed))
            noise_meta["constant_baseline"] = "training_feature_mean_broadcast_to_all_samples"
            noise_meta["test_features_not_used_for_baseline_or_scaling"] = True
            per = runner.evaluate_features("SYNTHETIC", f"{label}_noise", noisy, y, synth_splits,
                                           selected_seeds=[seed], row_extras=noise_meta)
            noise_results[label].update(per)
            del noisy
    def perm_provider(seed: int, train: np.ndarray) -> np.ndarray:
        pseed = config["reproducibility"]["label_permutation_seeds"][runner.seeds.index(seed)]
        rng = np.random.default_rng(int(pseed)); labels = y[train].copy(); rng.shuffle(labels); return labels
    label_perm = runner.evaluate_features("SYNTHETIC", "training_label_permutation", collapse_x, y, synth_splits,
                                          train_label_provider=perm_provider)
    variance_information = {
        "observed_reference": runner.summarize(base_results["lif_homeostasis"]),
        "variance_matched_noise_target_std": 0.2075,
        "variance_matched_noise": runner.summarize(noise_results["variance_matched"]),
        "variance_mismatched_noise_target_std": 0.10375,
        "variance_mismatched_noise": runner.summarize(noise_results["variance_mismatched"]),
        "training_label_permutation": runner.summarize(label_perm),
        "A0_input_information_upper_bound": base_summaries["A0"],
    }

    # E. Equal-dimensional/equal-parameter internal-state readout comparison.
    readout_state_results: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    state_source = retained["lif_homeostasis"]["state_features"]
    realized_dims: dict[int, int] = {}
    for seed in runner.seeds:
        train, _ = synth_splits[seed]
        for state_name in config["condition_matrix"]["readout_states"]["states"]:
            transformed, pca_meta = pca_train_only(state_source[state_name], train, 64)
            realized_dims[seed] = pca_meta["realized_components"]
            evaluated = runner.evaluate_features("SYNTHETIC", f"readout_state_{state_name}", transformed, y,
                                                 synth_splits, selected_seeds=[seed], row_extras=pca_meta)
            readout_state_results[state_name].update(evaluated)
            m = evaluated[seed]
            runner.readout_rows.append({"state": state_name, "seed": seed, "probe_accuracy": m["accuracy"],
                "feature_std": m["feature_std"], "Fisher_ratio": m["Fisher_ratio"], **pca_meta,
                "raw_npz": m["raw_npz"]})
        projected, rp_meta = gaussian_random_projection(state_source["soft_sigmoid"], realized_dims[seed],
                                                        config["reproducibility"]["random_projection_seeds"][runner.seeds.index(seed)])
        evaluated = runner.evaluate_features("SYNTHETIC", "readout_state_random_projection", projected, y,
                                             synth_splits, selected_seeds=[seed], row_extras=rp_meta)
        readout_state_results["random_projection"].update(evaluated)
        m = evaluated[seed]
        runner.readout_rows.append({"state": "random_projection", "seed": seed, "probe_accuracy": m["accuracy"],
            "feature_std": m["feature_std"], "Fisher_ratio": m["Fisher_ratio"], **rp_meta, "raw_npz": m["raw_npz"]})
    readout_summaries = {name: runner.summarize(result) for name, result in readout_state_results.items()}
    readout_contrasts = [runner.contrast(result, readout_state_results["soft_sigmoid"],
                                        f"{name}-soft_sigmoid")
                         for name, result in readout_state_results.items() if name != "soft_sigmoid"]
    add_bh(readout_contrasts)

    # F. One-factor combo ablations and one-factor gate/gain recalibration.
    ablation_specs = {
        "combo_minus_adaptive_threshold": {"remove_adaptive": True},
        "combo_minus_refractory": {"remove_refractory": True},
        "combo_minus_ei_sign": {"remove_ei": True},
    }
    ablation_results: dict[str, dict[int, dict[str, Any]]] = {}
    for name, removal in ablation_specs.items():
        sim = bio.simulate(frames, dynamics="LIF", theta=0.15, fan_in_gain=8.0, combo=True,
                           batch_size=64, **removal)
        ablation_results[name] = runner.evaluate_simulation("SYNTHETIC", name, sim, y, synth_splits)
        del sim; gc.collect()
    ablation_contrasts = [runner.contrast(result, base_results["lif_combo"], f"{name}-lif_combo")
                          for name, result in ablation_results.items()]
    add_bh(ablation_contrasts)
    # Gain-only recalibration at fixed theta=0.15 to r*=0.10.
    gain_selection = runner.calibration_candidates(bio, frames, synth_splits, [0.10], dynamics="LIF",
                                                   parameter="gain", fixed_theta=0.15)
    gain_recalibrated: dict[int, dict[str, Any]] = {}
    for gain in sorted({gain_selection[(s, 0.10)]["gain"] for s in runner.seeds}):
        chosen = [s for s in runner.seeds if gain_selection[(s, 0.10)]["gain"] == gain]
        sim = bio.simulate(frames, dynamics="LIF", theta=0.15, fan_in_gain=gain, batch_size=64)
        gain_recalibrated.update(runner.evaluate_simulation("SYNTHETIC", "fixed_theta_recalibrate_gain", sim, y,
            synth_splits, selected_seeds=chosen, row_extras={"target_rate": 0.10, "recalibrated_parameter": "gain"}))
        del sim
    theta_recalibrated = yoked_results[0.10]["biological"]["LIF"]
    gate_factor_contrast = runner.contrast(gain_recalibrated, theta_recalibrated,
                                           "fixed_theta_gain_recalibration-fixed_gain_theta_recalibration")
    add_bh([gate_factor_contrast])  # preregistered singleton gate-factor family

    # G. Remaining negative controls: per-seed frame shuffle, flash, frozen gain, label permutation already above.
    shuffled_results: dict[int, dict[str, Any]] = {}
    for seed in runner.seeds:
        rng = np.random.default_rng(seed + 9500)
        shuffled = frames.copy()
        for i in range(len(shuffled)):
            shuffled[i] = shuffled[i, rng.permutation(shuffled.shape[1])]
        sim = bio.simulate(shuffled, dynamics="LIF", theta=0.15, fan_in_gain=8.0, batch_size=64)
        shuffled_results.update(runner.evaluate_simulation("SYNTHETIC", "shuffled_frame_order", sim, y,
                                                           synth_splits, selected_seeds=[seed]))
        del sim, shuffled
    flash_sim = bio.simulate(flash, dynamics="LIF", theta=0.15, fan_in_gain=8.0, batch_size=64)
    flash_results = runner.evaluate_simulation("SYNTHETIC", "flash_control", flash_sim, y, synth_splits)
    frozen_gain_sim = bio.simulate(frames, dynamics="LIF", theta=0.15, fan_in_gain=1.0, batch_size=64)
    frozen_gain_results = runner.evaluate_simulation("SYNTHETIC", "frozen_gain_1", frozen_gain_sim, y, synth_splits)
    negative_controls = {
        "shuffled_frame_order": runner.summarize(shuffled_results),
        "flash_control": runner.summarize(flash_results),
        "frozen_gain_1": runner.summarize(frozen_gain_results),
        "training_label_permutation": runner.summarize(label_perm),
        "degree_null_lif": base_summaries["degree_null_lif"],
        "identity_lif": identity_summary,
    }

    # Real domains: fixed, preregistered A matrix only when the ceiling is available.
    real_method_results: dict[str, Any] = {}
    real_contrasts: list[dict[str, Any]] = []
    for domain in ("DAVIS", "SINTEL"):
        summary = real_ceiling[domain]["summary"]
        if not summary.get("available", False) or domain not in real_data:
            real_method_results[domain] = {"status": "unavailable", "reason": summary.get("reason", "ceiling_mean_below_0.70"),
                                           "ceiling_mean": summary.get("accuracy", {}).get("mean")}
            continue
        ds = real_data[domain]; splits = real_ceiling[domain]["splits"]
        methods: dict[str, dict[int, dict[str, Any]]] = {}
        for name, (model, kwargs) in base_specs.items():
            sim = model.simulate(ds["frames"], batch_size=64, capture_hops=True, **kwargs)
            methods[name] = runner.evaluate_simulation(domain, name, sim, ds["labels"], splits)
            del sim; gc.collect()
        summaries = {name: runner.summarize(v) for name, v in methods.items()}
        contrasts = [runner.contrast(v, methods["stateless"], f"{domain}:{name}-stateless")
                     for name, v in methods.items() if name != "stateless"]
        real_contrasts.extend(contrasts)
        real_method_results[domain] = {"status": "available", "conditions": summaries, "contrasts": contrasts}
    add_bh(real_contrasts)

    # Complete condition/seed index and a uniform delta-vs-stateless family.
    # This is generated from scalar rows only; it cannot alter any fit or
    # selection. It makes the main JSON independently cover every condition.
    indexed: dict[str, dict[str, dict[int, dict[str, Any]]]] = defaultdict(lambda: defaultdict(dict))
    for row in runner.main_rows:
        domain_name, condition_name, seed = str(row["domain"]), str(row["condition"]), int(row["seed"])
        if seed in indexed[domain_name][condition_name]:
            raise RuntimeError(f"duplicate condition/seed row: {domain_name}/{condition_name}/{seed}")
        indexed[domain_name][condition_name][seed] = row
    all_condition_summaries: dict[str, dict[str, Any]] = {}
    all_condition_contrasts: list[dict[str, Any]] = []
    row_delta_lookup: dict[tuple[str, str, int], float] = {}
    for domain_name, conditions in indexed.items():
        all_condition_summaries[domain_name] = {
            name: runner.summarize(per_seed) for name, per_seed in conditions.items()
            if set(per_seed) == set(runner.seeds)
        }
        reference = conditions.get("stateless")
        if reference is None or set(reference) != set(runner.seeds):
            continue
        for name, per_seed in conditions.items():
            if name == "stateless" or set(per_seed) != set(runner.seeds):
                continue
            contrast = runner.contrast(per_seed, reference, f"{domain_name}:{name}-stateless")
            all_condition_contrasts.append(contrast)
            for seed in runner.seeds:
                row_delta_lookup[(domain_name, name, seed)] = (
                    float(per_seed[seed]["accuracy"]) - float(reference[seed]["accuracy"])
                )
    add_bh(all_condition_contrasts)
    for row in runner.main_rows:
        key = (str(row["domain"]), str(row["condition"]), int(row["seed"]))
        row["delta_vs_stateless"] = row_delta_lookup.get(key, 0.0 if row["condition"] == "stateless" else None)

    # Three-state invariant classification from all 15 gate cells.
    any_variance = any(cell["summary"]["feature_std"]["mean"] > 1e-12 for cell in gate_grid)
    any_rate = any(cell["summary"]["kc_hard_spike_rate"]["mean"] > 0 for cell in gate_grid)
    informative = any(cell["summary"]["accuracy"]["ci95"][0] > 0.5 for cell in gate_grid
                      if cell["summary"]["feature_std"]["mean"] > 1e-12)
    if not any_variance:
        collapse_class = "COLLAPSE_UPSTREAM_OF_GATE"
    elif not informative:
        collapse_class = "VARIANCE_RESTORED_INFO_LOST"
    else:
        collapse_class = "VARIANCE_AND_INFORMATION_RESTORED"

    # Expected-signal checks are descriptive acceptance checks, never retuned.
    yoke_pairwise_ci_cross_zero = True
    pairwise_yoked: list[dict[str, Any]] = []
    for target in targets:
        lifs = {g: yoked_results[target][g]["LIF"] for g in models}
        names = list(lifs)
        for i in range(len(names)):
            for j in range(i+1, len(names)):
                c = runner.contrast(lifs[names[i]], lifs[names[j]], f"r={target}:{names[i]}-{names[j]}")
                pairwise_yoked.append(c)
                lo, hi = c["ci95"]
                yoke_pairwise_ci_cross_zero &= lo <= 0 <= hi
    add_bh(pairwise_yoked)
    readout_improved = any(c["name"].split("-")[0] in {"v_raw", "hard_spike"} and c["ci95"][0] > 0
                           for c in readout_contrasts)
    noise_below_a0 = (variance_information["variance_matched_noise"]["accuracy"]["ci95"][1]
                      < variance_information["A0_input_information_upper_bound"]["accuracy"]["mean"])
    # Operationalize the preregistered qualitative Fisher/probe agreement as a
    # positive Spearman association across gate cells. Infinite-only Fisher
    # summaries are excluded and fewer than two varying points cannot pass.
    fisher_probe_pairs = [
        (float(cell["summary"]["Fisher_ratio_mean_finite"]),
         float(cell["summary"]["accuracy"]["mean"]))
        for cell in gate_grid
        if cell["summary"]["Fisher_ratio_mean_finite"] is not None
    ]
    fisher_probe_rho: float | None = None
    if len(fisher_probe_pairs) >= 2:
        fvals, avals = map(np.asarray, zip(*fisher_probe_pairs))
        if np.ptp(fvals) > 0 and np.ptp(avals) > 0:
            fisher_probe_rho = float(scipy_stats.spearmanr(fvals, avals).statistic)
    fisher_agrees = fisher_probe_rho is not None and np.isfinite(fisher_probe_rho) and fisher_probe_rho > 0
    real_available = any(real_ceiling[d]["summary"].get("available", False) for d in real_ceiling)
    expected_checks = {
        "some_biological_gate_cell_feature_std_gt_zero": any_variance,
        "some_biological_gate_cell_hard_spike_rate_gt_zero": any_rate,
        "yoked_2x2_pairwise_delta_ci_crosses_zero": yoke_pairwise_ci_cross_zero,
        "v_raw_or_hard_spike_probe_above_soft_sigmoid_with_ci_lower_gt_zero": readout_improved,
        "fisher_agrees_with_probe": bool(fisher_agrees),
        "variance_matched_noise_does_not_recover_a0_probe": noise_below_a0,
        "at_least_one_real_ceiling_ge_0_70": real_available,
    }
    expected_signal_met = all(expected_checks.values())

    # Raw files and tables must exist before working result is serialized.
    csv_write(EVIDENCE / "main_table.csv", runner.main_rows)
    csv_write(EVIDENCE / "gate_operating_point.csv", runner.gate_rows)
    csv_write(EVIDENCE / "yoked_firing_rate_2x2.csv", runner.yoked_rows)
    csv_write(EVIDENCE / "variance_vs_information.csv", runner.variance_rows)
    csv_write(EVIDENCE / "readout_state_variables.csv", runner.readout_rows)
    csv_write(EVIDENCE / "probe_vs_hop.csv", runner.probe_hop_rows)
    csv_write(EVIDENCE / "variance_trajectory.csv", runner.variance_trajectory_rows)

    runner.trace_rows = [
        {"requirement": "complete biological edge table", "result_key": "graph.dense_graph", "evidence": "data/official_download_summary.json; data/graph_cache/dense_graph_meta.json"},
        {"requirement": "exact-hop KC self-check", "result_key": "invariants.kc_reachable_count", "evidence": "data/graph_cache/graph_bundle.json"},
        {"requirement": "15-cell gate grid", "result_key": "gate_operating_point_grid", "evidence": "evidence/gate_operating_point.csv"},
        {"requirement": "firing-rate-yoked 2x2", "result_key": "yoked_firing_rate_2x2", "evidence": "evidence/yoked_firing_rate_2x2.csv"},
        {"requirement": "variance-information separation", "result_key": "variance_information_separation", "evidence": "evidence/variance_vs_information.csv"},
        {"requirement": "five internal readouts", "result_key": "readout_state_variables", "evidence": "evidence/readout_state_variables.csv"},
        {"requirement": "one-factor ablations", "result_key": "one_factor_ablations", "evidence": "evidence/main_table.csv"},
        {"requirement": "raw NPZ per condition and seed", "result_key": "raw_artifacts", "evidence": "evidence/raw/*.npz"},
        {"requirement": "real protocol preregistration", "result_key": "preregistration", "evidence": "config_preregistered.json + config_preregistered.sha256"},
    ]
    csv_write(EVIDENCE / "experiment-traceability.csv", runner.trace_rows)
    # Keep byte-identical top-level table aliases for the explicit deliverable
    # filenames while evidence/ remains the canonical result namespace.
    table_names = [
        "main_table.csv", "gate_operating_point.csv", "yoked_firing_rate_2x2.csv",
        "variance_vs_information.csv", "readout_state_variables.csv", "probe_vs_hop.csv",
        "variance_trajectory.csv", "experiment-traceability.csv",
    ]
    for table_name in table_names:
        (ROOT / table_name).write_bytes((EVIDENCE / table_name).read_bytes())

    downloads = json.loads((DATA / "official_download_summary.json").read_text())
    data_files = {
        "connectome": file_record(DATA / "connections_biological.csv.gz"),
        "annotations": file_record(DATA / "neuron_annotations_flywire_v2.1.0.tsv.gz"),
        "retinal_positions": file_record(DATA / "right_visual_positions_all_neurons.csv"),
        "DAVIS": file_record(DATA / config["data"]["davis"]["archive"]),
        "SINTEL": file_record(DATA / config["data"]["sintel"]["archive"]),
    }
    real_ceiling_json = {d: to_jsonable(v["summary"]) for d, v in real_ceiling.items()}
    result = {
        "schema_version": "f-research-v1.p4.c1.attempt4.result.v1",
        "run_completed_utc": utc_now(),
        "run_status": "COMPUTATION_COMPLETE_PENDING_EXTERNAL_VALIDATION",
        "design_valid": None,
        "expected_signal_met": bool(expected_signal_met),
        "grind_block": GRIND_BLOCK,
        "configuration_diff_vs_18273": CONFIG_DIFF_18273,
        "preregistration": {"path": "config_preregistered.json", "sha256": prereg_hash,
                            "frozen_before_training": True, "posthoc_protocol_registered": False},
        "hardware": hardware_report(),
        "data_downloads": downloads,
        "data_files": data_files,
        "synthetic_metadata": synthetic["metadata"],
        "real_data_metadata": {d: to_jsonable(ds["metadata"]) for d, ds in real_data.items()},
        "graph": graph,
        "invariants": {
            "kc_reachable_count": graph["kc_reachable_count"],
            "actual_K": graph["actual_K"],
            "readout_layer_definition": graph["readout_layer_definition"],
            "resolved_kc_count": graph["resolved_kc_count"],
            "kc_feature_std_state": collapse_class,
            "synthetic_ceiling": synth_ceiling["summary"],
            "real_domain_ceiling": real_ceiling_json,
            "checks": {
                "kc_reachable_nonzero_at_selected_K": graph["kc_reachable_count"][str(graph["actual_K"])] > 0,
                "kc_feature_std_diagnostic_completed_without_early_stop": True,
                "synthetic_ceiling_ge_0_90": synth_ceiling["summary"]["accuracy"]["mean"] >= 0.90,
                "real_domain_availability_applied_at_0_70": True,
            },
        },
        "ceilings": {"SYNTHETIC": synth_ceiling["summary"], **real_ceiling_json},
        "base_conditions": base_summaries,
        "base_contrasts_vs_stateless": base_contrasts,
        "all_condition_summaries": all_condition_summaries,
        "all_condition_contrasts_vs_stateless": all_condition_contrasts,
        "identity_lif_control": identity_summary,
        "gate_operating_point_grid": gate_grid,
        "yoked_calibration": {g: {f"seed={s},target={t}": v for (s, t), v in vals.items()} for g, vals in calibration.items()},
        "yoked_firing_rate_2x2": yoked_summaries,
        "yoked_contrasts_vs_biological_stateless": yoked_contrasts,
        "yoked_pairwise_graph_contrasts_LIF": pairwise_yoked,
        "variance_information_separation": variance_information,
        "readout_state_variables": readout_summaries,
        "readout_state_contrasts_vs_soft_sigmoid": readout_contrasts,
        # Full scalar rows are embedded as well as written to CSV/NPZ so the
        # main result alone contains every condition/seed and per-hop probe.
        "condition_seed_measurements": runner.main_rows,
        "per_hop_measurements": runner.probe_hop_rows,
        "variance_trajectory_measurements": runner.variance_trajectory_rows,
        "one_factor_ablations": {name: runner.summarize(v) for name, v in ablation_results.items()},
        "one_factor_ablation_contrasts_vs_combo": ablation_contrasts,
        "gate_factor_recalibration": {
            "fixed_theta_recalibrate_gain": runner.summarize(gain_recalibrated),
            "fixed_gain_recalibrate_theta": runner.summarize(theta_recalibrated),
            "contrast": gate_factor_contrast,
        },
        "negative_controls": negative_controls,
        "real_domain_methods": real_method_results,
        "real_domain_contrasts": real_contrasts,
        "migration_verdict": ("AT_LEAST_ONE_REAL_DOMAIN_AVAILABLE_EVALUATE_FIXED_CONTRASTS" if real_available
                              else "NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE"),
        "statistical_protocol": {
            "seeds": runner.seeds, "bootstrap_replicates": runner.bootstrap,
            "bootstrap_ci": "paired-seed nonparametric percentile 95%",
            "exact_test": "two-sided exact paired sign-flip",
            "BH_FDR_q": 0.05, "minimum_two_sided_p_with_5_pairs": 0.0625,
            "power_limitation": "With five paired seeds, the smallest attainable two-sided exact sign-flip p is 0.0625; no contrast can individually attain p<0.05 under this test.",
        },
        "acceptance": {
            "fixed_minimum_real_delta": 0.15,
            "fixed_expected_strong_real_delta": 0.25,
            "thresholds_lowered": False,
            "fisher_probe_agreement_measurement": {
                "method": "Spearman correlation across finite gate-cell Fisher means and probe-accuracy means",
                "rho": fisher_probe_rho,
                "cell_count": len(fisher_probe_pairs),
                "pass_rule": "rho > 0 with at least two varying finite points",
            },
            "expected_signal_checks": expected_checks,
            "expected_signal_met": bool(expected_signal_met),
            "completion_is_acceptance": False,
        },
        "raw_artifacts": {"count": len(runner.raw_files), "files": sorted(runner.raw_files),
                          "one_npz_per_condition_seed": True},
        "tables": ["evidence/main_table.csv", "evidence/gate_operating_point.csv",
                   "evidence/yoked_firing_rate_2x2.csv", "evidence/variance_vs_information.csv",
                   "evidence/readout_state_variables.csv", "evidence/probe_vs_hop.csv",
                   "evidence/variance_trajectory.csv", "evidence/experiment-traceability.csv"],
        "runtime": {"wall_seconds": time.perf_counter() - wall_started,
                    "condition_groups_evaluated": runner.condition_counter},
        "interpretation_guardrails": {
            "A0": "input information upper bound, not a biological-wiring advantage",
            "synthetic": "controlled diagnostic only; never itself establishes transfer",
            "unavailable": "no transfer claim when both real ceilings are below 0.70 or construction fails",
            "measured_vs_inferred": "raw measurements are stored separately from acceptance/inference checks",
        },
    }
    working = EVIDENCE / "result_working.json"
    payload = (json.dumps(to_jsonable(result), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    working.write_bytes(payload)
    realized_config = {
        "schema_version": "f-research-v1.p4.c1.attempt4.config.realized.v1",
        "preregistered_sha256": prereg_hash,
        "preregistered": config,
        "realized": {
            "actual_K": graph["actual_K"], "resolved_kc_count": graph["resolved_kc_count"],
            "kc_reachable_count": graph["kc_reachable_count"],
            "yoked_threshold_calibration": result["yoked_calibration"],
            "gain_recalibration": {f"seed={s}": v for (s, _), v in gain_selection.items()},
            "device": device,
        },
    }
    (EVIDENCE / "config_working.json").write_bytes(
        (json.dumps(to_jsonable(realized_config), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    log(f"working result written bytes={working.stat().st_size}, raw_npz={len(runner.raw_files)}, expected_signal_met={expected_signal_met}")
    for model in models.values(): model.close()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="execute the full registered batch")
    args = parser.parse_args()
    if not args.run:
        parser.error("the production entrypoint requires --run (there is intentionally no demo/quick fallback)")
    with (EVIDENCE / "command_history.log").open("a", encoding="utf-8") as f:
        f.write(f"{utc_now()}\tpython3 experiment.py --run\n")
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
