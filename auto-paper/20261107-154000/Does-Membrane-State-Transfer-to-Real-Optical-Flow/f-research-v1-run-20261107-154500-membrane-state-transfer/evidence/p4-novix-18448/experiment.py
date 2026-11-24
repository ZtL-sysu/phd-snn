#!/usr/bin/env python3
"""f-research-v1 P4 C1 attempt #5 full registered experiment.

This is the sole orchestration entry point.  It verifies the immutable
preregistration, ensures complete official public data, executes every frozen
condition, validates the assembled result in memory, then performs the required
last-step persistence of main files, byte-identical snapshots, and MANIFEST.
"""
from __future__ import annotations

import argparse
import copy
import csv
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import torch

from connectome import (
    audit_variant_trace,
    build_connectome_cache,
    build_exact_degree_null,
    build_pathway,
    exact_hop_layers,
    file_sha256,
    generate_synthetic,
    graph_statistics,
    power_spectral_radius,
    selected_kcs_for_hop,
)
from data_pipeline import file_digest as data_file_digest
from data_pipeline import run_downloads
from real_domains import (
    VARIANTS,
    assign_decidability_states,
    evaluate_real_ladder,
    prepare_real_domains,
)
from synthetic_experiment import (
    ALL_SYNTHETIC_CONDITIONS,
    build_drive_bundle,
    build_statistical_power_matrix,
    evaluate_real_domain_models_if_usable,
    evaluate_synthetic_ceiling,
    evaluate_synthetic_conditions,
)
from validate_results import validate_objects

PROJECT = Path("/home/novix/workspace/project")
EVIDENCE = PROJECT / "evidence"
RAW = EVIDENCE / "raw"
LOGS = PROJECT / "logs"
PREREG = PROJECT / "config_preregistered.json"
PREREG_LOCK = PROJECT / "config_preregistered.sha256"
DATA_INTEGRITY = EVIDENCE / "data_integrity.json"


GRIND_PREVIOUS_FAILURE = """18390 设计有效、跑完全量、主文件交付缺陷已修复，但两真实域 ceiling 0.691667 / 0.435714 仍 < 0.70 → `real_domain_contrasts=[]`、无 real-domain delta、不作迁移主张；预注册 7 项强信号 2 项失败；且 18273 的「KC 方差严格 0」在 18390 规范实现中未复现 → round-007「门控工作点失配」假设的观测前提被否证，前 3 轮围绕「修塌缩」的机制假说链观测基础不稳定；另有 5 paired seeds 下 exact sign-flip 最小双侧 p=0.0625 的结构性效力天花板，以及 18273/18390 谱半径 504.30 vs 292.415 的跨实现不一致。禁止继续沿「修复零方差塌缩」路线设计任何干预。"""

GRIND_HYPOTHESIS = """本轮假设（新，机制级不同；是假设不是结论）：连续 4 轮两真实域 unavailable 的根因不是模型容量、脉冲门控、方差塌缩或读出状态变量，而是真实域标签构造与可用输入表示之间的信息瓶颈——18390 已用训练前冻结的官方 GT mask 质心与官方 `.flo` 构造标签，ceiling 仍 0.691667 / 0.435714。可证伪推论：若在训练前一次性冻结并哈希锁定一组「真实域标签/特征构造阶梯」，并用官方 GT 直接构造的 oracle 特征测出该域标签的可分性上界 `oracle_upper_bound`，则三态判定必居其一且可由实测区分：(a) `LABEL_NOT_DECODABLE`：oracle 上界 < 0.70 → 该域在此协议下不可判定，瓶颈在标签/数据本身，必须收窄为诊断型负结果；(b) `INPUT_BOTTLENECK`：oracle 上界 ≥ 0.85 而现行像素/复眼特征 ceiling < 0.70 → 瓶颈在输入编码（可修），如实定位在哪一档丢失；(c) `DOMAIN_USABLE`：现行冻结口径 ceiling ≥ 0.70 → 真实域可用，只有此时才允许计算 real-domain `delta(LIF − stateless)` 并按 C1 guidance §Expected Results 判定 `minimum` / `expected_strong`。另两个可证伪子假设：(d) 18273 与 18390 的 `kc_feature_std` 0 vs 0.049855 翻变可由一个受控单因子（邻接 convention / 重复边合并 / 谱半径口径 / fan_in 定义 / 帧聚合 / 随机流 / 数据版本）解释；(e) 5 paired seeds 下结论不稳定的 contrast 在预注册增至 ≥11 paired seeds 后是否保持一致（统一应用、不选择性报告）。"""

GRIND_CHANGES = """具体改动（相对 `query-round007-attempt4.txt` 的 diff，均为机制/协议/测量层）：
1.【核心转向·新增】真实域预注册 ceiling 阶梯 + oracle 上界：训练前在 `config_preregistered.json` 里一次性冻结并哈希锁定全部档（(i) 现行 GT mask 质心位移 / `.flo` 平均方向；(ii) 多帧累积位移方向，时间窗 2/4/8；(iii) 空间多尺度池化后主方向；(iv) oracle 特征：官方 GT mask 质心轨迹 / GT 光流向量直方图，直接由 GT 构造、经同一 train-only ridge，作为标签可分性上界；(v) 按位移幅度分位的类别难度分层）。每档报 5-seed ceiling 均值 + bootstrap 95% CI、Fisher 比、离散化互信息（报 bin 数与估计量）、类别平衡、样本量。所有档全部落盘、全部报告，不许只报达标档；禁止看到 v1 结果后再注册 v2；0.70 门槛不下调、不改用 CI 上界判定、不挑 seed、不 post-hoc 换协议凑 0.70。attempt #4 只测了单一冻结协议（质心 / `.flo`）的 ceiling，从未测 oracle 上界，也从未把「标签构造」当受控自变量。
2.【新增·决定性】三态可判定性判定：把上面三态写成训练前冻结的判定规则，每域一个 `decidability_state`，并落盘判定依据（oracle 值、现行 ceiling 值、二者差值 CI）。无论落到哪一态都必须把全部条件跑完再落盘，禁止零信息终止；只有 `DOMAIN_USABLE` 才允许产出 real-domain delta 与迁移裁决。
3.【新增·跨实现一致性契约】把 18273→18390 的协议差异显式列为受控单因子：邻接 convention（二进制有向 vs `log1p(syn_count)` 加权）、重复有向对合并（1,756,014 行 on/off）、谱半径归一化口径（λ 估计量与收敛判据）、fan_in 定义（含/不含自环、in vs total degree）、帧聚合（8 帧 soft 均值 / 末帧 / 累积）、随机流与 gain 初值、数据文件 SHA-256 绑定。每档落盘逐环节张量指纹（drive/syn/v/soft/hard 的 min/max/mean/std/nonzero_frac）+ 图统计量（nnz、去重规则、谱半径、权重多重集、in/out 度、互反边对、自环），并加入「全 18273 口径 / 全 18390 口径」两端点对照。这是把前几轮失败证据变成可解释结果，不是删除或改写失败证据。
4.【新增·统计效力修复（协议层，不是凑显著）】训练前预注册把 paired seeds 从 5 增至 ≥11（同一刺激、同一 split，只增独立初始化 seed），使 exact sign-flip 最小可及双侧 p < 0.05；同时保留 5-seed 口径做可比性对照。检验族 exact sign-flip / paired bootstrap percentile / paired permutation 三族并列落盘，BH-FDR 族训练前冻结。输出「结论一致性矩阵」：每个预注册主 contrast 在 5-seed 与 ≥11-seed、三检验族下的 mean / CI / exact p / BH q / 效应量与「结论是否翻转」。全部条件统一应用、不做选择性报告、不事后挑显著对比、不改效应量与 CI 定义；强制标签置换与零效应注入阴性对照校准（应恒不显著）。这不是「只调超参凑显著」：它是修复 18390 实测暴露的结构性检验力缺陷，且预注册、统一、以结论一致性为输出，并带阴性对照；不得因 n 增大把任何 contrast 从「不显著」改写成「机制成立」。
5.【删除】不再重跑 18390 已完成的 15 格门控网格、等发放率 yoked 2×2 全网格、五种读出状态变量全网格、方差匹配噪声注入全表（结论已明确、观测前提被否证）。预算让给真实域阶梯 + 跨实现审计 + 效力修复。
6.【沿用·最小可比锚点】保留 SYNTHETIC 主表 5 条件（stateless / lif_homeostasis / lif_combo / degree_null_lif / A=0）× 两种子口径，作为与 18156/18228/18273/18390 可比的历史锚点；保留 `A=0`（明确定义为输入信息上界，不得写成生物接线优势）、精确保度零模型（in/out 度、权重多重集、nnz、互反边对、自环精确相等）、identity 图、自适应阈值/不应期/E-I 各一因子移除消融、打乱帧序 / flash / 冻结 gain / 标签置换阴性对照、每条件每 seed 一个 raw NPZ。
7.【沿用·已验证有效，禁止退化】完整边表 178,853,187 B（`prefix=false`、HTTP Range 分块拼接 + gzip 校验）、eye→KC exact-hop 自检并按冻结回退取 K、训练前 invariant checks、2000 次 paired-seed bootstrap 95% CI、BH-FDR q=0.05、PCA/scaler/ridge/MI 分位数一律 train-only；产物持久化沿用 18390 已实测有效的做法：全部计算结束后最后一步用 Python 直接写 `project/result.json` 与 `project/config.json` 两个主文件 + byte-identical 双 snapshot + `project/MANIFEST.txt`，立即 `os.path.exists` / `getsize` / `sha256` 自检。
8.【不变】`minimum` / `expected_strong` 一律沿用 C1 `guidance.md` §Expected Results（real-domain `delta >= +0.15` / `>= +0.25` + 迁移裁决 + 一因子消融），不静默下调；真实域 ceiling 冻结门槛 0.70 不下调；两域都 unavailable 时不得作迁移主张；`runtime_hours` 只是可行性估算，不是超时参数。"""

GRIND_EXPECTED_FAILURE = """预期信号 / 若失败下一步：预期：至少一档真实域 oracle 上界 ≥ 0.85；三态判定落 `INPUT_BOTTLENECK` 或 `DOMAIN_USABLE` 且判定依据 CI 完整；若 `DOMAIN_USABLE` 则 real-domain delta 与 CI 可计算并按 guidance 判定；跨实现审计定位到能把 `kc_feature_std` 从 0 翻到 0.049855 的具体单因子；结论一致性矩阵给出哪些 contrast 在 5→≥11 seeds 下稳定。若失败（所有档 oracle 上界 < 0.70，或现行 ceiling 仍全部 < 0.70）：落 `LABEL_NOT_DECODABLE` / `INPUT_BOTTLENECK`，如实报告「两个公开真实域在此训练前冻结的标签构造协议下不可判定 / 信息在输入编码丢失」——这是诊断型负结果，不是达标、不是机制否证、不是方法优越、不是科学结论反转。下一步转向 I2 端到端可训练膜状态（历史 4 次远程全部只用冻结特征 + train-only ridge 探针，从未训练脉冲动力学）与 I4 逐跳信息预算/残差修复，保留全部失败证据，继续死磕同一 C1，不换题、不放弃（`abandon_allowed=False`）。两真实域仍 unavailable：如实标注、不做迁移主张，不把「实验跑完」写成「结果达标」。"""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def canonical_json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def load_locked_config() -> tuple[dict[str, Any], str]:
    raw = PREREG.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    expected = PREREG_LOCK.read_text(encoding="ascii").split()[0]
    if digest != expected:
        raise RuntimeError(f"Preregistration lock mismatch: {digest} != {expected}")
    cfg = json.loads(raw)
    if not cfg.get("frozen_before_outcomes") or cfg.get("mutable_after_hash_lock"):
        raise RuntimeError("Preregistration is not immutable")
    return cfg, digest


def append_command(line: str) -> None:
    path = EVIDENCE / "command_history.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def hardware_report() -> dict[str, Any]:
    gpu: dict[str, Any] = {}
    try:
        query = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip().splitlines()[0]
        name, memory, driver = [x.strip() for x in query.split(",")]
        gpu = {"name": name, "memory_total_mib": int(memory), "driver_version": driver}
    except Exception as exc:
        gpu = {"name": None, "error": repr(exc)}
    return {
        "gpu": gpu,
        "torch_version": torch.__version__,
        "torch_cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "cudnn_version": torch.backends.cudnn.version(),
        "device_count": torch.cuda.device_count(),
        "python_version": sys.version,
        "platform": platform.platform(),
    }


def package_versions() -> dict[str, str | None]:
    names = ["numpy", "scipy", "pandas", "scikit-learn", "torch", "Pillow", "opencv-python-headless", "requests", "pytest"]
    out: dict[str, str | None] = {}
    for name in names:
        try:
            out[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            out[name] = None
    return out


def ensure_complete_data(config: dict[str, Any]) -> dict[str, Any]:
    expected = {x["id"]: x for x in config["downloads"]["files"]}
    valid = False
    if DATA_INTEGRITY.exists():
        try:
            existing = json.loads(DATA_INTEGRITY.read_text(encoding="utf-8"))
            by_id = {x["id"]: x for x in existing.get("files", [])}
            valid = set(by_id) == set(expected)
            for fid, spec in expected.items():
                rec = by_id.get(fid, {})
                path = PROJECT / "data" / spec["filename"]
                file_ok = (
                    rec.get("available") is True
                    and path.exists()
                    and path.stat().st_size == int(spec["expected_bytes"])
                    and rec.get("bytes") == int(spec["expected_bytes"])
                    and bool(rec.get("sha256"))
                )
                if file_ok:
                    # Do not trust only a previous evidence record: re-hash the
                    # exact bytes consumed by this run.  Matching the recorded
                    # digest also binds reuse to the archive-integrity pass that
                    # produced data_integrity.json.
                    measured_sha = data_file_digest(path, "sha256")
                    file_ok = measured_sha == rec["sha256"]
                    expected_md5 = spec.get("expected_md5")
                    if expected_md5:
                        file_ok = file_ok and data_file_digest(path, "md5") == expected_md5
                    print(
                        f"[data] verified {fid}: bytes={path.stat().st_size} sha256={measured_sha}",
                        flush=True,
                    )
                valid = valid and file_ok
            valid = valid and existing.get("all_required_available") is True
            if valid:
                print("[data] reusing fully re-hashed official data set", flush=True)
                return existing
        except Exception:
            valid = False
    append_command("python3 experiment.py --run  # invokes registered data download if needed")
    return run_downloads(ids=None, workers=4, full_zip_crc=True)


def get_spectral_measurements(graph: Any, config: dict[str, Any]) -> dict[str, Any]:
    path = EVIDENCE / "spectral_measurements.json"
    if path.exists():
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("source_sha256") == graph.source_sha256 and set(obj.get("measurements", {})) == {"weighted", "binary", "legacy_parallel"}:
            print("[spectral] reusing source-bound measurements", flush=True)
            return obj
    settings = config["connectome"]["spectral_radius_estimator"]
    measurements: dict[str, Any] = {}
    for name, weights in (
        ("weighted", graph.weighted),
        ("binary", graph.binary),
        ("legacy_parallel", graph.legacy_parallel_weighted),
    ):
        print(f"[spectral] measuring {name}", flush=True)
        measurements[name] = power_spectral_radius(
            graph.codes,
            weights,
            graph.n_nodes,
            max_iterations=int(settings["max_iterations"]),
            relative_tolerance=float(settings["relative_tolerance"]),
            residual_tolerance=float(settings["residual_tolerance"]),
        )
    obj = {"source_sha256": graph.source_sha256, "measurements": measurements}
    atomic_write(path, canonical_json_bytes(obj))
    return obj


def _flatten_record(prefix: str, value: Any, out: dict[str, Any]) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            _flatten_record(f"{prefix}.{k}" if prefix else str(k), v, out)
    elif isinstance(value, (list, tuple)):
        out[prefix] = json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    elif isinstance(value, np.generic):
        out[prefix] = value.item()
    else:
        out[prefix] = value


def write_csv(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    flattened: list[dict[str, Any]] = []
    for row in rows:
        x: dict[str, Any] = {}
        _flatten_record("", row, x)
        flattened.append(x)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not flattened:
        path.write_text("empty\n", encoding="utf-8")
        return
    fields = sorted({k for x in flattened for k in x})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flattened)


def compact_graph_fields(stats: dict[str, Any]) -> dict[str, Any]:
    return {
        "raw_rows": stats["raw_rows"],
        "nodes": stats["nodes"],
        "nnz": stats["nnz"],
        "duplicate_rows_merged": stats["duplicate_rows_merged"],
        "merge_rule": stats["merge_rule"],
        "weighting": stats["weighting"],
        "weight_multiset_sha256": stats["weight_multiset_sha256"],
        "in_degree_sha256": stats["in_degree_sha256"],
        "out_degree_sha256": stats["out_degree_sha256"],
        "reciprocal_edge_pairs": stats["reciprocal_edge_pairs"],
        "self_loops": stats["self_loops"],
        "spectral_radius": stats.get("spectral_radius"),
        "spectral_converged": stats.get("spectral_radius_measurement", {}).get("converged"),
    }


def run_cross_implementation_audit(
    config: dict[str, Any],
    graph: Any,
    layers: list[np.ndarray],
    selected_hop: int,
    selected_kcs: np.ndarray,
    canonical_pathway: Any,
    synthetic: dict[str, Any],
    spectral: dict[str, Any],
    base_graph_stats: dict[str, Any],
) -> dict[str, Any]:
    measured = float(spectral["measurements"]["weighted"]["spectral_radius"])
    probe = synthetic["frames"][:32]
    binary_path = build_pathway(graph, layers, selected_hop, selected_kcs, weighting="binary")
    duplicate_path = build_pathway(graph, layers, selected_hop, selected_kcs, weighting="legacy_parallel")
    legacy_fanin_path = build_pathway(
        graph,
        layers,
        selected_hop,
        selected_kcs,
        weighting="weighted",
        fan_in_definition="total_degree_including_self_twice",
    )
    legacy_endpoint_weights = graph.row_multiplicity.astype(np.float64)
    legacy_endpoint_path = build_pathway(
        graph,
        layers,
        selected_hop,
        selected_kcs,
        weighting="binary",
        fan_in_definition="total_degree_including_self_twice",
        codes_override=graph.codes,
        weights_override=legacy_endpoint_weights,
    )
    canonical_settings = {
        "adjacency": "log1p_merged_weighted_directed",
        "duplicate_merge": "sum_before_log1p",
        "normalization_lambda": measured,
        "fan_in": "weighted_in_excluding_self",
        "frame_aggregation": "soft_mean",
        "random_stream": "PCG64",
        "fixed_gain": False,
        "data_sha256_binding": graph.source_sha256,
    }
    factor_specs = [
        (
            "adjacency_convention",
            binary_path,
            {**canonical_settings, "adjacency": "binary_directed"},
            True,
        ),
        (
            "duplicate_pair_merge",
            duplicate_path,
            {**canonical_settings, "duplicate_merge": "parallel_rows_log1p_then_sum"},
            True,
        ),
        (
            "spectral_radius_protocol",
            canonical_pathway,
            {**canonical_settings, "normalization_lambda": 504.30, "lambda_source": "18273_prior_reference_not_reproduced"},
            True,
        ),
        (
            "fan_in_definition",
            legacy_fanin_path,
            {**canonical_settings, "fan_in": "total_degree_including_self_twice"},
            True,
        ),
        (
            "frame_aggregation",
            canonical_pathway,
            {**canonical_settings, "frame_aggregation": "last"},
            True,
        ),
        (
            "random_stream_gain_init",
            canonical_pathway,
            {**canonical_settings, "random_stream": "MT19937", "gain_init": "sequential_legacy_stream"},
            True,
        ),
        (
            "data_version_sha256_binding",
            canonical_pathway,
            {**canonical_settings, "data_sha256_binding": "legacy_unbound_no_alternate_bytes_available"},
            False,
        ),
    ]
    single: list[dict[str, Any]] = []
    for factor, pathway, settings, testable in factor_specs:
        print(f"[cross-audit] single factor {factor}", flush=True)
        row = audit_variant_trace(
            f"single_factor__{factor}", probe, graph, pathway, config, measured, settings
        )
        row["factor"] = factor
        row["single_factor_controlled"] = True
        row["factor_testable_with_available_bytes"] = testable
        row["graph_statistics"] = compact_graph_fields(base_graph_stats)
        if factor == "adjacency_convention":
            row["graph_statistics"]["weighting"] = "binary_directed"
            row["graph_statistics"]["weight_multiset_sha256"] = hashlib.sha256(
                np.sort(graph.binary).astype("<f8").tobytes()
            ).hexdigest()
            row["graph_statistics"]["spectral_radius"] = spectral["measurements"]["binary"]["spectral_radius"]
            row["graph_statistics"]["spectral_converged"] = spectral["measurements"]["binary"]["converged"]
        elif factor == "duplicate_pair_merge":
            row["graph_statistics"]["weighting"] = "parallel_rows_log1p_then_sum"
            row["graph_statistics"]["weight_multiset_sha256"] = hashlib.sha256(
                np.sort(graph.legacy_parallel_weighted).astype("<f8").tobytes()
            ).hexdigest()
            row["graph_statistics"]["spectral_radius"] = spectral["measurements"]["legacy_parallel"]["spectral_radius"]
            row["graph_statistics"]["spectral_converged"] = spectral["measurements"]["legacy_parallel"]["converged"]
        single.append(row)
        np.savez_compressed(
            RAW / f"cross_audit_{factor}_seed01.npz",
            **{name: value for name, value in row["tensor_fingerprints"].items() if False},
            y_true=np.asarray([], dtype=np.int8),
            y_pred=np.asarray([], dtype=np.int8),
            scores=np.asarray([], dtype=np.float32),
            features_summary=np.asarray([row["kc_feature_std"], row["hard_spike_rate"], row["nonconstant_dimensions"]]),
            fingerprint_json=np.asarray(json.dumps(row["tensor_fingerprints"], sort_keys=True)),
        )
    endpoints: list[dict[str, Any]] = []
    endpoint_specs = [
        (
            "all_18273_reconstructed",
            legacy_endpoint_path,
            {
                **canonical_settings,
                "adjacency": "binary_parallel_contributions",
                "duplicate_merge": "off_parallel_rows",
                "normalization_lambda": 504.30,
                "lambda_source": "prior_reference_only",
                "fan_in": "total_degree_including_self_twice",
                "frame_aggregation": "last",
                "random_stream": "MT19937",
                "data_sha256_binding": "legacy_unbound_no_alternate_bytes_available",
            },
        ),
        ("all_18390_canonical", canonical_pathway, canonical_settings),
    ]
    for endpoint_id, pathway, settings in endpoint_specs:
        row = audit_variant_trace(endpoint_id, probe, graph, pathway, config, measured, settings)
        row["endpoint_status"] = (
            "reconstructed_from_supplied_report_not_exact_reproduction"
            if endpoint_id.startswith("all_18273")
            else "canonical_current_implementation"
        )
        row["graph_statistics"] = compact_graph_fields(base_graph_stats)
        endpoints.append(row)
        np.savez_compressed(
            RAW / f"cross_audit_{endpoint_id}_seed01.npz",
            y_true=np.asarray([], dtype=np.int8),
            y_pred=np.asarray([], dtype=np.int8),
            scores=np.asarray([], dtype=np.float32),
            features_summary=np.asarray([row["kc_feature_std"], row["hard_spike_rate"], row["nonconstant_dimensions"]]),
            fingerprint_json=np.asarray(json.dumps(row["tensor_fingerprints"], sort_keys=True)),
        )
    current_std = next(x for x in endpoints if x["variant_id"] == "all_18390_canonical")["kc_feature_std"]
    zero_factors = [
        x["factor"]
        for x in single
        if x["factor_testable_with_available_bytes"] and x["kc_feature_std"] <= 1e-12 and current_std > 1e-12
    ]
    return {
        "contract_frozen_before_results": True,
        "single_factor_variants": single,
        "endpoints": endpoints,
        "specific_single_factor_reproducing_zero_to_nonzero_flip": zero_factors,
        "single_factor_flip_localized": bool(zero_factors),
        "if_none_interpretation": "The supplied 18273 zero-variance report is not explained by any testable registered single factor in this reconstruction; this is a failed sub-hypothesis, not deletion of the discrepancy.",
        "prior_report_references": {
            "18273_spectral_radius": 504.30,
            "18273_spectral_radius_reported_text": "504.30",
            "18390_spectral_radius": 292.41506239264993,
            "18273_kc_feature_std": 0.0,
            "18390_kc_feature_std": 0.049855,
            "504_30_status": "retained prior value; approximately mapped to the measured unmerged parallel-row log-weight convention",
        },
        "spectral_radius_weighting_reconciliation": {
            "current_frozen_merged_log1p_sum_syn_count": float(
                spectral["measurements"]["weighted"]["spectral_radius"]
            ),
            "measured_binary_directed": float(
                spectral["measurements"]["binary"]["spectral_radius"]
            ),
            "prior_18390_binary_reference": 292.41506239264993,
            "binary_absolute_difference_from_prior": abs(
                float(spectral["measurements"]["binary"]["spectral_radius"])
                - 292.41506239264993
            ),
            "measured_unmerged_parallel_row_sum_log1p": float(
                spectral["measurements"]["legacy_parallel"]["spectral_radius"]
            ),
            "prior_18273_parallel_reference": 504.30,
            "parallel_absolute_difference_from_prior": abs(
                float(spectral["measurements"]["legacy_parallel"]["spectral_radius"])
                - 504.30
            ),
            "interpretation": (
                "The two historical values map to different adjacency-weight conventions: "
                "the 18390 value matches binary directed adjacency, while the 18273 value "
                "approximately matches summing log1p per parallel row before pair merging. "
                "The current frozen contract uses log1p after syn_count summation; none of "
                "the historical discrepancies is deleted or treated as biological evidence."
            ),
        },
        "measured_current_spectral_radius": measured,
        "measured_current_kc_feature_std": current_std,
        "data_version_factor_limitation": "No hash-bound 18273 data file exists in this workspace; the factor is retained and marked untestable rather than deleted or fabricated.",
    }


def determine_migration(states: dict[str, Any]) -> tuple[str, bool]:
    usable = [d for d, x in states.items() if x["decidability_state"] == "DOMAIN_USABLE"]
    if not usable:
        return "NO_TRANSFER_CLAIM_BOTH_REAL_DOMAINS_UNAVAILABLE", False
    if len(usable) == 2:
        return "REAL_DOMAIN_EVALUATION_PERMITTED_BOTH_DOMAINS", True
    return f"REAL_DOMAIN_EVALUATION_PERMITTED_{usable[0]}_ONLY", True


def c1_guidance_summary(config: dict[str, Any], real_contrasts: dict[str, Any]) -> dict[str, Any]:
    if not real_contrasts:
        return {
            "verdict": "failure",
            "reason": "no_DOMAIN_USABLE_real_domain_no_real_domain_delta",
            "minimum_met": False,
            "expected_strong_met": False,
            "minimum_threshold": config["thresholds"]["c1_minimum_real_delta"],
            "expected_strong_threshold": config["thresholds"]["c1_expected_strong_real_delta"],
        }
    per_domain = {d: x["c1_guidance_verdict"] for d, x in real_contrasts.items()}
    strong = any(v == "expected_strong" for v in per_domain.values())
    minimum = strong or any(v == "minimum" for v in per_domain.values())
    return {
        "verdict": "expected_strong" if strong else ("minimum" if minimum else "failure"),
        "reason": "frozen_real_domain_delta_thresholds_applied",
        "minimum_met": minimum,
        "expected_strong_met": strong,
        "minimum_threshold": config["thresholds"]["c1_minimum_real_delta"],
        "expected_strong_threshold": config["thresholds"]["c1_expected_strong_real_delta"],
        "per_domain": per_domain,
    }


def manifest_bytes(project: Path, primary_bytes: dict[Path, bytes]) -> bytes:
    # Cover every self-contained source/reproduction file and every evidence
    # file, rather than silently omitting download integrity or intermediate
    # measurements.  Large public archives are represented by the verified
    # byte counts and digests in evidence/data_integrity.json, not duplicated
    # into this artifact manifest.
    expected_set = {
        *project.glob("*.py"),
        project / "entrypoint.sh",
        project / "config_preregistered.json",
        project / "config_preregistered.sha256",
        project / "config.json",
        project / "result.json",
    }
    expected_set.update(
        path for path in (project / "evidence").rglob("*") if path.is_file()
    )
    expected = sorted(expected_set, key=lambda path: path.relative_to(project).as_posix())
    manifest_path = project / "MANIFEST.txt"
    predicted_self_size = 0
    for _ in range(20):
        lines = [
            "# f-research-v1 P4 C1 attempt #5 artifact manifest",
            "# path\texists\tbytes\tsha256",
        ]
        for path in expected:
            rel = path.relative_to(project)
            if path in primary_bytes:
                data = primary_bytes[path]
                exists, size, digest = True, len(data), hashlib.sha256(data).hexdigest()
            else:
                exists = path.exists()
                size = path.stat().st_size if exists else 0
                digest = file_sha256(path) if exists else "MISSING"
            lines.append(f"{rel}\t{str(exists).lower()}\t{size}\t{digest}")
        lines.append(f"MANIFEST.txt\ttrue\t{predicted_self_size}\tSELF_SHA256_NOT_RECURSIVELY_DEFINED")
        data = ("\n".join(lines) + "\n").encode("utf-8")
        if len(data) == predicted_self_size:
            return data
        predicted_self_size = len(data)
    raise RuntimeError("MANIFEST self-size did not converge")


def finalize_artifacts(result: dict[str, Any], final_config: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    """Required final persistence boundary; do not write files afterward."""
    result_bytes = canonical_json_bytes(result)
    config_bytes = canonical_json_bytes(final_config)
    primary = {
        PROJECT / "result.json": result_bytes,
        PROJECT / "config.json": config_bytes,
        EVIDENCE / "result_snapshot.json": result_bytes,
        EVIDENCE / "config_snapshot.json": config_bytes,
    }
    # validation.json is deliberately complete before the main-file boundary.
    atomic_write(EVIDENCE / "validation.json", canonical_json_bytes(validation))
    # The required last write group: two main files, byte-identical snapshots,
    # then MANIFEST.  entrypoint.sh immediately executes ls and SHA self-check.
    for path, data in primary.items():
        atomic_write(path, data)
    manifest = manifest_bytes(PROJECT, primary)
    atomic_write(PROJECT / "MANIFEST.txt", manifest)
    return {
        "result_bytes": len(result_bytes),
        "config_bytes": len(config_bytes),
        "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "snapshots_byte_identical": True,
        "manifest_bytes": len(manifest),
    }


def run_full() -> dict[str, Any]:
    wall_start = time.perf_counter()
    start_utc = utc_now()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    config, prereg_hash = load_locked_config()
    hardware = hardware_report()
    data_integrity = ensure_complete_data(config)
    if not data_integrity.get("all_required_available"):
        raise RuntimeError("One or more required public data files are unavailable")

    graph = build_connectome_cache(config)
    layers, hop_counts = exact_hop_layers(graph, max_hop=8)
    selected_hop, selected_kcs, hop_rule = selected_kcs_for_hop(graph, layers, hop_counts)
    spectral = get_spectral_measurements(graph, config)
    current_spectral = spectral["measurements"]["weighted"]
    graph_stats = graph_statistics(graph, spectral=current_spectral)
    null_codes, null_weights, null_meta = build_exact_degree_null(
        graph, seed=int(config["randomness"]["master_seed"]) + 313, target_successful_swaps=100_000
    )
    canonical_pathway = build_pathway(graph, layers, selected_hop, selected_kcs, weighting="weighted")
    null_pathway = build_pathway(
        graph,
        layers,
        selected_hop,
        selected_kcs,
        weighting="weighted",
        codes_override=null_codes,
        weights_override=null_weights,
    )

    synthetic = generate_synthetic(config)
    synthetic_ceiling = evaluate_synthetic_ceiling(config, synthetic["frames"], synthetic["labels"], RAW)
    drive_bundle = build_drive_bundle(synthetic, graph, canonical_pathway, null_pathway)
    synthetic_conditions, main_rows = evaluate_synthetic_conditions(
        config,
        synthetic,
        drive_bundle,
        float(current_spectral["spectral_radius"]),
        RAW,
    )
    power_rows, power_meta = build_statistical_power_matrix(config, synthetic_conditions)

    prepared, real_preparation = prepare_real_domains(config, prereg_hash, use_cache=True)
    ladder_rows, full_ladder = evaluate_real_ladder(config, prepared, RAW)
    states = assign_decidability_states(config, full_ladder)
    migration_verdict, transfer_claim_allowed = determine_migration(states)
    real_contrasts: dict[str, Any] = {}
    for domain, state in states.items():
        if state["decidability_state"] == "DOMAIN_USABLE":
            c = prepared[domain]["current"]
            real_contrasts[domain] = evaluate_real_domain_models_if_usable(
                config,
                domain,
                c.frames,
                c.y,
                graph,
                canonical_pathway,
                null_pathway,
                float(current_spectral["spectral_radius"]),
                RAW,
            )

    cross_audit = run_cross_implementation_audit(
        config,
        graph,
        layers,
        selected_hop,
        selected_kcs,
        canonical_pathway,
        synthetic,
        spectral,
        graph_stats,
    )

    # Evidence tables are written before the final main-file persistence boundary.
    write_csv(EVIDENCE / "real_domain_ceiling_ladder.csv", ladder_rows)
    oracle_rows = [
        {
            "domain": domain,
            "oracle_upper_bound": full_ladder[domain]["oracle_gt"]["five_seed_ceiling"]["mean"],
            "bootstrap_95pct_ci": full_ladder[domain]["oracle_gt"]["five_seed_ceiling"]["bootstrap_95pct_ci"],
            "values": full_ladder[domain]["oracle_gt"]["five_seed_ceiling"]["values"],
            "sample_count": full_ladder[domain]["oracle_gt"]["sample_count"],
            "direct_official_gt": True,
        }
        for domain in ("DAVIS", "SINTEL")
    ]
    write_csv(EVIDENCE / "oracle_upper_bound.csv", oracle_rows)
    atomic_write(EVIDENCE / "decidability_states.json", canonical_json_bytes(states))
    audit_csv_rows = cross_audit["single_factor_variants"] + cross_audit["endpoints"]
    write_csv(EVIDENCE / "cross_implementation_audit.csv", audit_csv_rows)
    write_csv(EVIDENCE / "statistical_power_matrix.csv", power_rows)
    write_csv(EVIDENCE / "main_table.csv", main_rows)
    ablation_names = set(config["synthetic"]["one_factor_ablations"])
    negative_names = set(config["synthetic"]["negative_controls"])
    write_csv(EVIDENCE / "ablation.csv", [x for x in main_rows if x["condition"] in ablation_names])
    write_csv(EVIDENCE / "negative_controls.csv", [x for x in main_rows if x["condition"] in negative_names])

    unavailable: list[dict[str, Any]] = []
    for domain in ("DAVIS", "SINTEL"):
        for variant in VARIANTS:
            row = full_ladder[domain][variant]
            if not row["available_at_frozen_0_70_threshold"]:
                unavailable.append(
                    {
                        "condition": f"{domain}:{variant}",
                        "reason": "five_seed_ceiling_below_frozen_0_70_threshold",
                        "measured_ceiling": row["five_seed_ceiling"]["mean"],
                        "threshold": 0.70,
                        "sample_count": row["sample_count"],
                    }
                )
        if states[domain]["decidability_state"] != "DOMAIN_USABLE":
            unavailable.append(
                {
                    "condition": f"{domain}:real_domain_delta",
                    "reason": f"decidability_state={states[domain]['decidability_state']}",
                    "measured_current_ceiling": states[domain]["current_ceiling"],
                    "oracle_upper_bound": states[domain]["oracle_upper_bound"],
                }
            )
    c1 = c1_guidance_summary(config, real_contrasts)
    oracle_expected = any(x["oracle_upper_bound"] >= 0.85 for x in states.values())
    state_expected = all(x["decidability_state"] in {"INPUT_BOTTLENECK", "DOMAIN_USABLE"} for x in states.values())
    factor_expected = cross_audit["single_factor_flip_localized"]
    negative_calibrated = all(x["calibrated_nonsignificant"] for x in power_meta["negative_control_calibration"].values())
    expected_signal_components = {
        "at_least_one_oracle_upper_bound_ge_0_85": oracle_expected,
        "all_states_input_bottleneck_or_domain_usable": state_expected,
        "single_factor_localizes_kc_feature_std_flip": factor_expected,
        "negative_controls_calibrated_nonsignificant": negative_calibrated,
        "c1_minimum_real_delta_met": c1["minimum_met"],
        "c1_expected_strong_real_delta_met": c1["expected_strong_met"],
    }

    raw_count = len(list(RAW.glob("*.npz")))
    final_config = copy.deepcopy(config)
    final_config["preregistration_lock"] = {
        "path": "config_preregistered.json",
        "sha256": prereg_hash,
        "verified_before_execution": True,
        "registration_timestamp_utc": config["registration_timestamp_utc"],
    }
    final_config["runtime_environment"] = {
        "hardware": hardware,
        "package_versions": package_versions(),
        "implementation_details": {
            "hop_probe_dimension_cap": 4096,
            "hop_probe_pca_max_components": 64,
            "degree_null_successful_swaps": null_meta["successful_swaps"],
            "real_two_frame_to_eight_frame_interpolation": "fixed linear endpoints only when DOMAIN_USABLE",
            "all_absolute_paths_root": str(PROJECT),
        },
    }

    result: dict[str, Any] = {
        "schema_version": "f-research-v1.p4.c1.attempt5.result.v1",
        "experiment_id": config["experiment_id"],
        "attempt": 5,
        "start_utc": start_utc,
        "end_utc": utc_now(),
        "preregistration": {
            "path": "config_preregistered.json",
            "sha256": prereg_hash,
            "hash_lock_verified": True,
            "frozen_before_outcomes": True,
            "post_hoc_ladder_variants_added": False,
        },
        "grind_block": {
            "上一轮失败点": GRIND_PREVIOUS_FAILURE,
            "本轮假设": GRIND_HYPOTHESIS,
            "具体改动": GRIND_CHANGES,
            "预期信号_若失败下一步": GRIND_EXPECTED_FAILURE,
        },
        "hardware": hardware,
        "data_integrity": data_integrity,
        "connectome": {
            "graph_statistics": graph_stats,
            "eye_to_kc_exact_hop_counts": hop_counts,
            "selected_hop": selected_hop,
            "selected_kc_count": int(len(selected_kcs)),
            "frozen_hop_selection_rule": hop_rule,
            "degree_null": null_meta,
            "spectral_measurements_all_contract_weightings": spectral["measurements"],
        },
        "synthetic": {
            "domain_label": "SYNTHETIC",
            "ceiling": synthetic_ceiling,
            "conditions": synthetic_conditions,
            "A0_interpretation": config["synthetic"]["A0_definition"],
            "migration_claim_source": False,
        },
        "real_domain_preparation": real_preparation,
        "real_domain_ceiling_ladder": full_ladder,
        "oracle_upper_bounds": {d: full_ladder[d]["oracle_gt"] for d in ("DAVIS", "SINTEL")},
        "decidability_states": states,
        "migration_verdict": migration_verdict,
        "real_domain_evaluation_permitted": bool(transfer_claim_allowed),
        "real_domain_evaluation_executed": bool(real_contrasts),
        # Permission to evaluate is not itself a positive transfer claim.  A
        # claim requires the frozen C1 minimum effect threshold to be met.
        "transfer_claim_made": bool(
            transfer_claim_allowed and real_contrasts and c1["minimum_met"]
        ),
        "transfer_outcome_verdict": (
            "POSITIVE_TRANSFER_C1_MINIMUM_MET"
            if transfer_claim_allowed and c1["minimum_met"]
            else "NO_POSITIVE_TRANSFER_C1_MINIMUM_NOT_MET"
            if transfer_claim_allowed
            else "NO_TRANSFER_CLAIM_REAL_DOMAINS_UNAVAILABLE"
        ),
        "real_domain_contrasts": real_contrasts,
        "c1_guidance": c1,
        "cross_implementation_audit": cross_audit,
        "statistical_power_matrix": power_rows,
        "statistical_power": power_meta,
        "expected_signal_components": expected_signal_components,
        "diagnostic_expected_signal_met": bool(oracle_expected and state_expected and negative_calibrated),
        "expected_signal_met": bool(oracle_expected and state_expected and factor_expected and negative_calibrated),
        "c1_expected_signal_met": bool(c1["minimum_met"]),
        "configuration_diff_from_18390": config["configuration_diff_from_query_round007_attempt4"],
        "unavailable_conditions": unavailable,
        "invariant_checks": {
            "kc_reachable_count": {
                "passed": len(selected_kcs) >= 2000,
                "hop_1_to_8": hop_counts,
                "selected_hop": selected_hop,
                "selected_kc_count": int(len(selected_kcs)),
            },
            "synthetic_ceiling": synthetic_ceiling,
            "real_domain_ceiling": {
                "passed": all(set(full_ladder[d]) == set(VARIANTS) for d in ("DAVIS", "SINTEL")),
                "threshold": 0.70,
                "current_protocol": {d: states[d]["current_ceiling"] for d in states},
                "all_registered_variants_measured": True,
            },
            "data_integrity": {
                "passed": data_integrity["all_required_available"],
                "files": [
                    {"id": x["id"], "bytes": x["bytes"], "sha256": x.get("sha256"), "available": x["available"]}
                    for x in data_integrity["files"]
                ],
            },
        },
        "zero_information_termination": False,
        "artifact_counts": {
            "raw_npz": raw_count,
            "real_ladder_rows": len(ladder_rows),
            "statistical_power_rows": len(power_rows),
            "synthetic_condition_seed_rows": len(main_rows),
            "cross_audit_rows": len(audit_csv_rows),
        },
        "interpretation_guardrails": config["interpretation_guardrails"],
        "runtime": {
            "wall_seconds": time.perf_counter() - wall_start,
            "wall_hours": (time.perf_counter() - wall_start) / 3600.0,
            "runtime_hours_is_feasibility_estimate_not_timeout": True,
            "all_processes_completed": True,
            "peak_gpu_mib": max(
                x["peak_gpu_mib"]
                for condition in synthetic_conditions.values()
                for x in condition["seed_results"]
            ),
        },
        "design_valid": False,
        "validation_summary": None,
        "scientific_conclusion_scope": (
            "Measured protocol-level diagnostic only. No method-superiority claim; no mechanism claim from n increase; "
            "A=0 is an input-information upper bound; unavailable domains cannot support transfer claims."
        ),
        "abandon_allowed": False,
        "failure_next_steps": ["I2_end_to_end_trainable_membrane_state", "I4_hopwise_information_budget_and_residual_repair"],
    }
    validation = validate_objects(result, final_config, PROJECT)
    result["design_valid"] = validation["design_valid"]
    result["validation_summary"] = {
        "total": validation["total"],
        "passed": validation["passed"],
        "failed": validation["failed"],
        "design_valid": validation["design_valid"],
        "failed_checks": validation["failed_checks"],
    }
    if not validation["design_valid"]:
        print(json.dumps(validation["failed_checks"], ensure_ascii=False, indent=2), flush=True)
        raise RuntimeError(f"Pre-finalization validator failed {validation['failed']}/{validation['total']} checks")
    persist = finalize_artifacts(result, final_config, validation)
    print(f"[finalize] {json.dumps(persist, sort_keys=True)}", flush=True)
    return {"result": result, "persist": persist}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="execute the complete registered experiment")
    args = parser.parse_args(argv)
    if not args.run:
        parser.error("--run is required")
    try:
        run_full()
    except Exception:
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
