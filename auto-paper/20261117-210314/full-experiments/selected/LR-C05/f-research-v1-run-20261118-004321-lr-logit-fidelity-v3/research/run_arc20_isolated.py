from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUN_ROOT = Path(__file__).resolve().parents[1]
ARC_ROOT = Path(r"C:\code\AutoResearchClaw")
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-quality-v1"
REQUEST_PATH = RUN_ROOT / "writing" / "request-p11-quality.json"
SOURCE_DRAFT = RUN_ROOT / "writing" / "arc-revision-v1" / "stage-19" / "paper_revised.md"


@dataclass
class CapturedResponse:
    content: str
    model: str
    finish_reason: str = "stop"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("quality response is not JSON")
    payload = json.loads(stripped[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("quality response is not an object")
    return payload


class CodexACPBackend:
    def __init__(self, acpx: str, session_name: str) -> None:
        self.acpx = acpx
        self.session_name = session_name

    def chat(self, messages: list[dict[str, str]], **_: Any) -> CapturedResponse:
        parts: list[str] = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            if role == "system":
                parts.append(f"[System]\n{content}")
            else:
                parts.append(content)
        result = subprocess.run(
            [
                self.acpx, "--approve-all", "--max-turns", "1", "--ttl", "3600",
                "--cwd", str(RUN_ROOT), "codex", "-s", self.session_name, "-f", "-",
            ],
            input="\n\n".join(parts).replace("\x00", ""),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1800,
        )
        if result.returncode != 0:
            raise RuntimeError(f"acpx/codex quality call failed: {result.stderr.strip()}")
        lines = [
            line
            for line in result.stdout.splitlines()
            if not line.startswith(("[acpx]", "[client]", "[tool]", "[done]", "[thinking]"))
        ]
        return CapturedResponse(content="\n".join(lines).strip(), model="acp:codex")


class IsolatedQualityChat:
    def __init__(self, backend: CodexACPBackend, request: dict[str, Any]) -> None:
        self.backend = backend
        self.request = request
        self.internal_calls = 0
        self.external_calls = 0
        self.payload: dict[str, Any] | None = None

    def chat(self, messages: list[dict[str, str]], **_: Any) -> CapturedResponse:
        self.internal_calls += 1
        if self.payload is not None:
            return CapturedResponse(content=json.dumps(self.payload, ensure_ascii=False), model="acp:codex")
        last_error: Exception | None = None
        for attempt in range(1, 3):
            clean_messages = list(self.request["messages"])
            if attempt == 2:
                clean_messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Formatting correction only: return one JSON object matching "
                            "the requested quality-gate schema."
                        ),
                    }
                )
            self.external_calls += 1
            response = self.backend.chat(clean_messages)
            try:
                self.payload = extract_json(response.content)
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                continue
            return CapturedResponse(content=json.dumps(self.payload, ensure_ascii=False), model=response.model)
        raise RuntimeError(f"quality response validation failed: {last_error}")


def build_request(manuscript: str) -> dict[str, Any]:
    spec = json.loads((RUN_ROOT / "results" / "p10-implementation-spec.json").read_text(encoding="utf-8"))
    revision_log = (RUN_ROOT / "writing" / "p10-revision-log.md").read_text(encoding="utf-8")
    system = (
        "You are a final scientific quality-gate evaluator. Judge only the supplied "
        "manuscript and evidence summary. Do not invent citations or results. Return "
        "valid JSON only. The gate is a scientific/manuscript gate; the later P12 "
        "citation authenticity/duplicate audit remains a separate mandatory gate."
    )
    user = {
        "task": (
            "Evaluate the revised paper against all required checks and return JSON "
            "with fields: score_1_to_10:number, verdict:'proceed'|'revise', "
            "criteria:object, strengths:[string], weaknesses:[string], "
            "required_actions:[string], checks:[{name,status,evidence}]."
        ),
        "threshold": 4.0,
        "required_checks": [
            "exactly six canonical numbered sections",
            "claim/evidence alignment and no unsupported strength",
            "result strength is appropriate to the narrow logit-fidelity scope",
            "figure/table placement and captions support the argument",
            "paragraph/reverse-outline roles are distinct",
            "whole-paper continuity from question to conclusion",
            "Results reports evidence while Discussion interprets it",
        ],
        "manuscript": manuscript,
        "evidence_summary": {
            "main_result": "26.23%, 33.99%, 25.83% logit-MSE reductions at rank128/2% on three graphs; 9/9 dataset-seed comparisons positive versus the strongest matched-budget residual control",
            "task_maxima": "0.53/1.17/1.86 pp maximum three-seed-mean observed degradation and 2.85 pp maximum single-seed degradation",
            "cost": "matched total padded serialized-bit budget; absolute totals 21,932,736/25,630,208/43,771,008 bits",
            "timing": "rank128/1% secondary warmed benchmark, paired p95 ratios 1.020-1.124, peak allocation 218.23 MB, wall-clock only",
            "provenance": "held-out confirmation after validation-exposed setting selection; not preregistered or independent replication",
            "scope": "M0=A_hat X only; composite magnitude-weighted Jacobian score; no task-superiority, energy, temporal-event, broad-GNN, equivalence or focal 2% timing claim",
            "implementation_spec": spec,
            "revision_closure": revision_log,
        },
        "scoring_policy": (
            "Score scientific/manuscript readiness after P10 repair. Do not penalize "
            "the deferred bibliography gate as if it were silently complete; list it "
            "as a required action only if it blocks this P11 scientific gate. A score "
            "below 4 or verdict 'revise' must include a blocking manuscript defect."
        ),
    }
    return {"messages": [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False, indent=2)}]}


def validate_report(report: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    score = report.get("score_1_to_10")
    if not isinstance(score, (int, float)) or score < 4.0:
        problems.append(f"quality score below threshold: {score!r}")
    if report.get("verdict") != "proceed":
        problems.append(f"quality verdict is not proceed: {report.get('verdict')!r}")
    checks = report.get("checks")
    if not isinstance(checks, list) or len(checks) < 7:
        problems.append("quality report lacks seven required checks")
    else:
        for check in checks:
            if not isinstance(check, dict) or check.get("status") not in {"pass", "passed", "pass-with-note"}:
                problems.append(f"non-passing quality check: {check!r}")
    return problems


def main() -> int:
    sys.path.insert(0, str(ARC_ROOT))
    from researchclaw.config import RCConfig
    from researchclaw.pipeline.stage_impls._review_publish import _execute_quality_gate

    if OUTPUT_ROOT.exists():
        raise RuntimeError(f"ARC quality output already exists: {OUTPUT_ROOT}")
    for directory in ("stage-12/runs", "stage-14", "stage-19", "stage-20"):
        (OUTPUT_ROOT / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_DRAFT, OUTPUT_ROOT / "stage-19" / "paper_revised.md")
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-draft-v1" / "stage-12" / "runs" / "migrated-verification.json",
        OUTPUT_ROOT / "stage-12" / "runs" / "migrated-verification.json",
    )
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-draft-v1" / "stage-14" / "experiment_summary.json",
        OUTPUT_ROOT / "stage-14" / "experiment_summary.json",
    )

    manuscript = SOURCE_DRAFT.read_text(encoding="utf-8")
    request = build_request(manuscript)
    REQUEST_PATH.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    acpx = shutil.which("acpx")
    if not acpx:
        raise RuntimeError("acpx is not installed")
    session_name = "lr-c05-p11-quality"
    session_result = subprocess.run(
        [acpx, "--ttl", "3600", "--cwd", str(RUN_ROOT), "codex", "sessions", "new", "--name", session_name],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    if session_result.returncode != 0:
        raise RuntimeError(f"failed to create quality session: {session_result.stderr.strip()}")

    isolated = IsolatedQualityChat(CodexACPBackend(acpx, session_name), request)
    arc_config = RCConfig.load(RUN_ROOT / "config.arc.yaml", check_paths=False)
    result = _execute_quality_gate(
        OUTPUT_ROOT / "stage-20",
        OUTPUT_ROOT,
        arc_config,
        adapters=None,
        llm=isolated,
        prompts=None,
    )
    report_path = OUTPUT_ROOT / "stage-20" / "quality_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    problems = validate_report(report)

    audit = {
        "schema_version": 1,
        "stage": "P11/AutoResearchClaw-20-QUALITY_GATE",
        "status": "passed" if not problems else "failed-validation",
        "arc_version": "0.3.1",
        "executor_identity": {
            "provider": "acp",
            "agent": "codex",
            "agent_cli_version": "0.169.0-alpha.11.1",
            "configured_model": "group/never-stuck",
            "acpx_version": "0.19.2",
        },
        "context_isolation": {
            "status": "verified-clean-external-boundary",
            "request_messages_sha256": hash_json(request["messages"]),
            "internal_arc_calls": isolated.internal_calls,
            "external_model_calls": isolated.external_calls,
            "arc_internal_prompt_sent_to_model": False,
            "raw_execution_logs_sent_to_model": False,
            "reviews_sent_to_model": False,
            "note": "ARC Stage 20 control flow executed; external evaluator received only the P11 clean quality request.",
        },
        "validation": {
            "problems": problems,
            "score": report.get("score_1_to_10"),
            "verdict": report.get("verdict"),
            "manuscript_sha256": sha256(SOURCE_DRAFT),
            "quality_report_sha256": sha256(report_path),
        },
        "arc_stage_result": {
            "stage": str(result.stage),
            "status": str(result.status),
            "decision": getattr(result, "decision", None),
            "artifacts": list(result.artifacts),
            "evidence_refs": list(result.evidence_refs),
        },
    }
    (OUTPUT_ROOT / "executor-context-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if problems:
        print(json.dumps({"status": "failed-validation", "problems": problems}, indent=2))
        return 2
    print(json.dumps({"status": "passed", "score": report["score_1_to_10"], "verdict": report["verdict"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
