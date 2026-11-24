#!/usr/bin/env python3
"""f-research-v1 P4 C1 correction-loop-v3 attempt #7 (round-012).

Phase-0 crash-safe skeleton.  The complete implementation is filled in before the
first scientific run.  Every phase writes project/result.json atomically so a
platform interruption cannot leave the workspace with zero evidence.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

PROJECT = Path("/home/novix/workspace/project")
RESULT_PATH = PROJECT / "result.json"

GRIND_BLOCK = {
    "上一轮失败点": """（1）平台层：`18489`（attempt #6）= `FAILED` / 平台沙箱故障、`steps=0`、零产物、远程 agent 从未执行实验代码 → 梯度路径 2×2 与三项必修诊断一项都没跑，attempt #6 的假设仍未被检验（不是被否证）。\n（2）科学层：`18448`（attempt #5）= `REJECT_FAILURE`，SINTEL `delta(lif_homeostasis − stateless)=0.000000`（5/11 seeds、CI `[0,0]`、三检验族 p=1、11 个 paired differences 全 0）→ `minimum` / `expected_strong` 未达、`transfer_claim_made=false`；DAVIS `INPUT_BOTTLENECK`；阴性对照校准失败 `−0.115909` p=0.0009765625；跨实现 `single_factor_flip_localized=false`。""",
    "本轮假设": """历轮 6 次远程实验反复出现「两条件 accuracy 完全相同 / paired differences 全 0 / delta 恒 0」与「阴性对照却显著非 0」这一组合。可能存在两个叠加的、此前从未同时被检验的前置条件：\n① 测量装置不可辨识：决策规则退化为常数/多数类预测器（0.466667 与类别边际、混淆矩阵、logit margin 的结构从未被报告），且历轮从未在真实域特征流水线上注入一个已知强度的信号并检验读出能否单调恢复它（只有阴性对照，没有灵敏度传递函数）。若装置测不出已知 +0.25 的信号，则一切 `delta≈0` 都不可解释，既不是负结果也不是正结果；\n② 梯度路径从未被检验：连续 5 次有效实验全部只用「冻结图传播特征 + train-only linear ridge 探针」，膜状态递推从未接收梯度、脉冲动力学从未被训练；而本机 `+0.2817`（CI `[0.2033,0.3617]`）恰来自训练过的 LIF。\n可证伪推论（全部训练前冻结、可落盘判定）：\n(i) 装置可辨识：混淆矩阵非常数、`predicted_class_marginal` 非退化、logit margin 分布有非零方差，且已知信号注入阶梯的 `sensitivity_slope > 0` 且 bootstrap CI 下界 > 0、`recover_known_plus_0_25 = true`；\n(ii) 主门通过后，端到端 `delta(LIF − stateless) >= +0.15` 且 CI 下界 > 0，且 `stateless_trained_identically` 不追平 LIF；\n(iii) 若主门失败（决策规则退化 / 注入 +0.25 仍测不出）：则 18448/18390/18489 的 `delta≈0` 必须改标 `UNINFORMATIVE_MEASUREMENT`，不得作为「膜状态无增益」也不得作为「有增益」的科学结论。该重分类不把任何失败改写成成功：`c1_guidance` 仍 failure、`transfer_claim_made` 仍 false、文章仍不合格、仍死磕同一 C1；\n(iv) 若主门通过而 e2e delta 仍 ≈0：则 attempt #6 假设被否证，如实收窄为「连接组约束协议下无可训练膜状态增益」的诊断型负结果。""",
    "具体改动": """1.【合并新增·训练前第一硬门】`measurement_identifiability_gate` 升为所有主 contrast 之前的训练前第一硬门：对每个真实域 / 每个条件落盘混淆矩阵、`predicted_class_marginal`、类别边际、logit margin 的 min/max/mean/std/非常数维、常数预测器指示、`majority_baseline_acc`，并给 `decision_rule_identifiable: true|false` 与判定依据。attempt #6 完全没有这一层（其训练前 6 项自检是 KC 可达 / SYNTHETIC ceiling / real ceiling / 梯度分支可区分 / 阴性对照校准 / 数据完整性）。\n2.【合并新增·决定性阳性对照】`known_signal_injection_ladder`：在同一条真实域特征流水线（同一图 / 复眼 / K / 归一化 / PCA / ridge / split / seeds）上，训练前一次性冻结并哈希锁定一组已知强度的方向信号注入（效应量/SNR 阶梯 {0, 0.05, 0.10, 0.15, 0.25, 0.40}，注入位置与作用维度写死、注入后不触碰标签与 split），逐档落盘 `recovered_delta` + bootstrap 95% CI + 单调性检验 + 拟合斜率与 CI 下界。预注册读出 = `sensitivity_slope` 与 `recover_known_plus_0_25` 布尔值。历轮 6 次实验从未做过任何阳性对照，这是全新的证据轴；与 attempt #6 必修①的「零效应注入蒙特卡洛」（阴性对照）方向相反、互补。\n3.【合并新增·历史证据重分析，不需新 GPU 主张】用 (1)(2) 的同一套判据重分析已哈希核验归档的 `evidence/p4-novix-18448/result.json` 与 18390/18448 的 raw NPZ，输出 `historical_delta_interpretability` 表：逐任务标注 `INFORMATIVE_NEGATIVE / UNINFORMATIVE_MEASUREMENT / INSUFFICIENT_RAW`。这是对已落盘证据的重新审计，不是新实验结论、不编造数值、不删改原始档位；若 raw NPZ 不足以判定则如实标 `INSUFFICIENT_RAW`。\n4.【合并新增·条件身份 / 标签边际阶梯】`label_marginal ∈ {平衡, 0.6/0.4, 0.75/0.25}` × `condition_dispatch ∈ {独立拟合, 共享 scaler, 共享 PCA}` 的受控小阶梯，逐格落盘 (1) 的退化指纹；目的不是调类别权重凑显著，而是定位 18448 阴性对照显著非 0 与主对比恒 0 并存的来源。与 attempt #6 必修①的置换构造审计不同：本项改的是边际与统计共享域，不是置换规则。\n5.【合并新增·主读出重分类契约】`result.json` 的 `c1_guidance` 增加第四态 `UNINFORMATIVE_MEASUREMENT`（与既有 `failure` / 达标 并列）；该态下 `transfer_claim_made` 强制 false；`migration_verdict` 增加 `NO_CLAIM_MEASUREMENT_NOT_IDENTIFIABLE`。明确：该态不是达标、不是机制否证、不是把负结果改写为正结果。\n6.【保留·必须真跑完，优先级上调】attempt #6 的梯度路径 2×2 `{frozen_features+ridge, surrogate_gradient_e2e} × {stateless, LIF}` + `stateless_trained_identically` + 三变体（learnable_decay / learnable_gain_only / straight_through_rate）、等参数量、等 SynOps、train-only、训练前冻结，与三项必修诊断全部保留为可执行条件矩阵（不删失败证据、不静默下调门槛），但只在主门通过后其数值才允许被解释；主门未过则全部 contrast 标 `uninterpretable_measurement`，数值仍原样落盘。因 18489 平台故障使 attempt #6 从未被检验，本轮不得只做诊断而丢掉主命题检验。\n7.【保留·三项必修诊断全部真跑】①阴性对照校准失效诊断（置换构造审计 + 三检验族在零效应蒙特卡洛 ≥200 次下的经验 I 类错误率 + 张量指纹重合度；未通过则全部 contrast 标 `uncalibrated`，不得事后换检验族或重定义对照）；②DAVIS 输入编码一因子修复阶梯（复眼采样密度 1×/2×/4×、逐帧时间差分、对比度归一化、光流向量直方图、多尺度池化，各 on/off；全档落盘全档报告；禁止看到 v1 后再注册 v2 / 改 0.70 门槛 / 用 CI 上界判定 / 挑 seed / post-hoc 换协议）；③SINTEL delta 恒 0 三态判定 `REAL_ZERO_EFFECT / IMPLEMENTATION_IDENTICAL_BRANCH / INSUFFICIENT_PROBE`（逐环节逐跳逐帧张量指纹差异计数与哈希、单位级反事实注入、强制分支判别探针）。若判 `IMPLEMENTATION_IDENTICAL_BRANCH`，delta=0 不得作科学结论。\n8.【平台故障加固·本轮新增，直接针对 18489 失败模式】18489 的失败是「沙箱在完成回调前变 unhealthy、final synchronization not proven、零产物」，因此本轮强制：第 0 步先落盘 `experiment.py` 骨架与阶段性 `result.json`；每个小步完成后增量 flush 到 `project/result.json`（不是只在最后写一次）；任何提前终止前先写 `experiment.py` 与阶段性 `result.json`；全程不输出超长回复（避免生成流断开）；断点可续跑；所有主文件必须写在可 pull 的 workspace 内 `project/` 目录。\n9.【保留·主读出升级】训练后动力学下的 SINTEL real-domain `delta(LIF − stateless)` 为主读出（5 / 11 seeds、bootstrap 95% CI、三检验族 p、BH q），按 C1 guidance §Expected Results 判 `minimum` / `expected_strong` / `failure`。三态 `decidability_state` 降为次级门保留（只有 `DOMAIN_USABLE` 允许 real delta 与迁移裁决）；跨实现一致性契约（7 单因子 + 2 端点）降为固定协变量审计保留。不再把 18448 已完成的 ceiling 全网格 / oracle 全网格 / ≥11-seed 效力矩阵 / 跨实现全表当主实验重跑；只保留 5-seed 可比锚点。\n10.【保留·效度修复】测试集暴露台账：前 5 次远程都用同一批 DAVIS/Sintel held-out 结果触发 redesign，属自适应评估。本轮把这些测试显式标 `exposed`，冻结一组新的不相交 holdout（DAVIS 按序列 ID 哈希、Sintel 按 scene，哈希锁定写进 `config_preregistered.json`），最终选择只在未暴露 holdout 上评估一次；exposed / unexposed 两套数值分别全部报告。冻结探针臂预注册等效性 / 非劣效界（≥11 paired seeds 下 CI 是否排除 +0.15）。\n11.【沿用·禁止退化】完整边表 178,853,187 B（`prefix=false`、HTTP Range 分块拼接 + gzip 校验）、eye→KC exact-hop 自检 K=3 / 2,544 KC、训练前 invariant checks、2000 次 paired bootstrap 95% CI、BH-FDR q=0.05、PCA/scaler/ridge/MI 分位数一律 train-only；`A=0` 明确为输入信息上界（不得写成生物接线优势）、精确保度零模型（in/out 度、权重多重集、nnz、互反边对、自环精确相等）、identity 图、自适应阈值 / 不应期 / E-I 各一因子移除消融、打乱帧序 / flash / 冻结 gain / 标签置换阴性对照、每条件每 seed 一个 raw NPZ；「保度零模型从未输给真实接线」继续成立。\n12.【沿用·已验证有效】产物持久化沿用 18390/18448 实测有效的做法：全部计算结束后最后一步用 Python 直接写 `project/result.json` 与 `project/config.json` 两个主文件 + byte-identical 双 snapshot + `project/MANIFEST.txt`，立即 `os.path.exists` / `getsize` / `sha256` 自检并把实测输出贴进最终回复，并给出 `ls -l project/result.json project/config.json` 真实输出。不许退化回前三次缺陷。\n13.【不变】`minimum` / `expected_strong` 一律沿用 C1 `guidance.md` §Expected Results（real-domain `delta >= +0.15` / `>= +0.25` + 迁移裁决 + 一因子消融），不静默下调；真实域 ceiling 冻结门槛 0.70 不下调；两域都 unavailable 时不得作迁移主张；`runtime_hours` 只是可行性估算，不是超时参数。""",
    "预期信号_若失败下一步": """· 预期：`decision_rule_identifiable=true`（混淆矩阵非常数、logit margin 非零方差）；`known_signal_injection_ladder` 的 `sensitivity_slope > 0` 且 CI 下界 > 0、`recover_known_plus_0_25=true`；历史重分析表给出每个既往 delta 的可解释性标签；三项必修诊断真跑完且阴性对照校准通过、DAVIS gap 至少一档收窄、SINTEL 三态落 `REAL_ZERO_EFFECT` 或 `IMPLEMENTATION_IDENTICAL_BRANCH` 且证据完整；主门通过后 e2e `delta(LIF − stateless) >= +0.15` 且 CI 下界 > 0，`stateless_trained_identically` 不追平，unexposed holdout 与 exposed 同号，一因子消融指认承载机制。\n· 若主门失败（决策规则退化 / 注入 +0.25 仍测不出）：如实把相关历史 `delta≈0` 重分类为 `UNINFORMATIVE_MEASUREMENT`，明确指出此前 6 次「诊断型负结果」中哪些其实不可解释；不是达标、不是机制否证、不是方法优越、不是把负结果写成正结果；保留全部失败证据，继续死磕同一 C1，下一步按 `research-recovery.md` 修装置（换可辨识读出 / 修条件分派 / 修标签边际），重跑同一主表后再判定，门槛与 `expected_strong` 仍不下调。\n· 若主门通过而 e2e delta 仍 ≈0：回到 attempt #6 假设被否证分支，如实收窄为「连接组约束协议下无可训练膜状态增益」的诊断型负结果，转 I4 逐跳信息预算 / 残差修复并结合测试集暴露台账。\n· 若阴性对照校准仍失败：本 run 全部 contrast 标 `uncalibrated`、不作机制主张，如实报告并作为下一次 correction loop 的必修项。\n· 任何情况：不把「实验跑完 / design_valid / 方差恢复 / 首次 DOMAIN_USABLE / 主门通过」写成「结果达标」；不删失败证据；不把负结果改写成正结果；不把 `A=0` 高于图条件写成生物接线优势；不编造任何数值。""",
}

# The protocol requires these four sections byte-for-byte as supplied.  Keep the
# verbatim payload in a small, auditable UTF-8 JSON file rather than normalizing
# Markdown, whitespace, punctuation, or line wrapping in Python source.
_GRIND_BLOCK_VERBATIM_PATH = PROJECT / "grind_block_verbatim.json"
if _GRIND_BLOCK_VERBATIM_PATH.exists():
    GRIND_BLOCK = json.loads(_GRIND_BLOCK_VERBATIM_PATH.read_text(encoding="utf-8"))


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def atomic_json(path: Path, payload: Any) -> None:
    """Crash-safe UTF-8 JSON write with fsync + atomic rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    raw = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with tmp.open("wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def hardware_probe() -> dict[str, Any]:
    out: dict[str, Any] = {
        "python": sys.version,
        "platform": platform.platform(),
    }
    try:
        import torch
        out.update({
            "torch": torch.__version__,
            "torch_cuda": torch.version.cuda,
            "cuda_available": bool(torch.cuda.is_available()),
            "cuda_device_count": int(torch.cuda.device_count()),
        })
        if torch.cuda.is_available():
            prop = torch.cuda.get_device_properties(0)
            out.update({
                "gpu_model": torch.cuda.get_device_name(0),
                "gpu_total_memory_bytes": int(prop.total_memory),
            })
    except Exception as exc:  # phase-0 must still persist diagnostics
        out["torch_probe_error"] = repr(exc)
    return out


def phase0() -> None:
    payload = {
        "schema_version": "round012.attempt7.phase0.v1",
        "experiment_id": "f-research-v1-P4-C1-round012-attempt7",
        "status": "PHASE0_SKELETON_WRITTEN",
        "started_at_utc": utcnow(),
        "last_incremental_flush_utc": utcnow(),
        "resume_supported": True,
        "scientific_results_available": False,
        "grind_block": GRIND_BLOCK,
        "hardware": hardware_probe(),
        "phase_ledger": [{
            "phase": 0,
            "name": "crash_safe_skeleton",
            "status": "complete",
            "note": "experiment.py skeleton and incremental result.json persisted before data access or training",
        }],
        "warnings": [
            "No scientific result exists at phase 0.",
            "18489 remains platform FAILED with steps=0 and zero artifacts; its hypothesis was not tested.",
            "18448 remains REJECT_FAILURE; its measured failures are preserved verbatim in grind_block.",
        ],
        "transfer_claim_made": False,
        "c1_guidance": {"verdict": "not_evaluated_phase0"},
    }
    atomic_json(RESULT_PATH, payload)
    print(f"phase0 persisted: {RESULT_PATH} ({RESULT_PATH.stat().st_size} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase0", action="store_true", help="persist crash-safe phase-0 skeleton")
    parser.add_argument("--run-all", action="store_true", help="run/resume the complete preregistered experiment")
    parser.add_argument("--stage", help="run one named restartable stage")
    parser.add_argument("--force", action="store_true", help="rerun the selected stage")
    args = parser.parse_args()
    if args.phase0:
        phase0()
        return
    if args.run_all or args.stage:
        from run_experiment import run_all, run_named
        if args.run_all:
            run_all(force_stage=args.stage if args.force else None)
        else:
            run_named(args.stage, force=args.force)
        return
    parser.error("choose --phase0, --run-all, or --stage")


if __name__ == "__main__":
    main()
