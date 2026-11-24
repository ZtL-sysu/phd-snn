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
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-review-v1"
REQUEST_A = RUN_ROOT / "writing" / "request-p9-reviewer-a.json"
REQUEST_B = RUN_ROOT / "writing" / "request-p9-reviewer-b.json"


@dataclass
class CapturedResponse:
    content: str
    model: str
    finish_reason: str = "stop"


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


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
        command = [
            self.acpx,
            "--approve-all",
            "--max-turns",
            "1",
            "--ttl",
            "3600",
            "--cwd",
            str(RUN_ROOT),
            "codex",
            "-s",
            self.session_name,
            "-f",
            "-",
        ]
        result = subprocess.run(
            command,
            input="\n\n".join(parts).replace("\x00", ""),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1800,
        )
        if result.returncode != 0:
            raise RuntimeError(f"acpx/codex review failed: {result.stderr.strip()}")
        lines = [
            line
            for line in result.stdout.splitlines()
            if not line.startswith(("[acpx]", "[client]", "[tool]", "[done]", "[thinking]"))
        ]
        return CapturedResponse(content="\n".join(lines).strip(), model="acp:codex")


class CombinedReviewChat:
    def __init__(self, backend_a: CodexACPBackend, backend_b: CodexACPBackend, requests: list[dict[str, Any]]) -> None:
        self.backend_a = backend_a
        self.backend_b = backend_b
        self.requests = requests
        self.responses: list[CapturedResponse] = []
        self.external_calls = 0
        self.internal_calls = 0

    def chat(self, messages: list[dict[str, str]], **_: Any) -> CapturedResponse:
        self.internal_calls += 1
        if self.internal_calls != 1:
            raise RuntimeError("unexpected extra ARC peer-review call")
        first = self.backend_a.chat(self.requests[0]["messages"])
        second = self.backend_b.chat(self.requests[1]["messages"])
        self.external_calls = 2
        self.responses = [first, second]
        combined = (
            "# AutoResearchClaw Stage 18 Peer Review\n\n"
            + normalize_review(first.content, "Reviewer A Report")
            + "\n\n"
            + normalize_review(second.content, "Reviewer B Report")
        )
        return CapturedResponse(content=combined, model="acp:codex", finish_reason="stop")


def normalize_review(text: str, expected_heading: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:markdown|md)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    match = re.search(r"^#\s+Reviewer\s+[AB]\s+Report\s*$", stripped, flags=re.MULTILINE)
    if match:
        stripped = stripped[match.start() :].strip()
    elif not stripped.startswith(f"# {expected_heading}"):
        stripped = f"# {expected_heading}\n\n{stripped}"
    return stripped


def validate_review(text: str, label: str) -> list[str]:
    problems: list[str] = []
    required = [
        "## Summary",
        "## Score",
        "## Confidence",
        "## Strengths",
        "## Major Concerns",
        "## Minor Concerns",
        "## Required Revisions",
        "## Questions",
    ]
    if len(text) < 1800:
        problems.append(f"{label} is shorter than 1800 characters")
    for heading in required:
        if heading not in text:
            problems.append(f"{label} missing {heading}")
    if re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b", text, re.I):
        problems.append(f"{label} contains placeholder")
    return problems


def main() -> int:
    sys.path.insert(0, str(ARC_ROOT))
    from researchclaw.config import RCConfig
    from researchclaw.pipeline.stage_impls._review_publish import _execute_peer_review

    acpx = shutil.which("acpx")
    if not acpx:
        raise RuntimeError("acpx is not installed")
    sessions = ["lr-c05-p9-reviewer-a", "lr-c05-p9-reviewer-b"]
    for session in sessions:
        result = subprocess.run(
            [
                acpx, "--ttl", "3600", "--cwd", str(RUN_ROOT),
                "codex", "sessions", "new", "--name", session,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(f"failed to create review session {session}: {result.stderr.strip()}")

    request_a = json.loads(REQUEST_A.read_text(encoding="utf-8"))
    request_b = json.loads(REQUEST_B.read_text(encoding="utf-8"))
    combined_chat = CombinedReviewChat(
        CodexACPBackend(acpx, sessions[0]),
        CodexACPBackend(acpx, sessions[1]),
        [request_a, request_b],
    )
    arc_config = RCConfig.load(RUN_ROOT / "config.arc.yaml", check_paths=False)
    result = _execute_peer_review(
        OUTPUT_ROOT / "stage-18",
        OUTPUT_ROOT,
        arc_config,
        adapters=None,
        llm=combined_chat,
        prompts=None,
    )
    reviews_path = OUTPUT_ROOT / "stage-18" / "reviews.md"
    reviews = reviews_path.read_text(encoding="utf-8")
    review_a = normalize_review(combined_chat.responses[0].content, "Reviewer A Report")
    review_b = normalize_review(combined_chat.responses[1].content, "Reviewer B Report")
    (OUTPUT_ROOT / "reviewer-a.md").write_text(review_a + "\n", encoding="utf-8")
    (OUTPUT_ROOT / "reviewer-b.md").write_text(review_b + "\n", encoding="utf-8")

    problems = validate_review(review_a, "Reviewer A") + validate_review(review_b, "Reviewer B")
    if reviews.count("# Reviewer A Report") != 1 or reviews.count("# Reviewer B Report") != 1:
        problems.append("combined reviews do not contain exactly one Reviewer A and one Reviewer B report")

    audit = {
        "schema_version": 1,
        "stage": "P9/AutoResearchClaw-18-PEER_REVIEW",
        "status": "passed" if not problems else "failed-validation",
        "arc_version": "0.3.1",
        "arc_stage_source": str(ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_review_publish.py"),
        "arc_stage_source_sha256": hash_file(
            ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_review_publish.py"
        ),
        "executor_identity": {
            "provider": "acp",
            "agent": "codex",
            "agent_cli_version": "0.169.0-alpha.11.1",
            "configured_model": "group/never-stuck",
            "acpx_version": "0.19.2",
        },
        "context_isolation": {
            "status": "verified-clean-external-boundary",
            "internal_arc_calls": combined_chat.internal_calls,
            "external_review_calls": combined_chat.external_calls,
            "reviewer_a_messages_sha256": hash_json(request_a["messages"]),
            "reviewer_b_messages_sha256": hash_json(request_b["messages"]),
            "arc_internal_prompt_sent_to_model": False,
            "raw_execution_logs_sent_to_model": False,
            "reviewer_sessions_isolated": True,
            "note": (
                "The installed ARC Stage 18 control flow was executed. Its historical "
                "context prompt was replaced at the external boundary by two separate "
                "clean reviewer requests. Reviewer A and Reviewer B used isolated Codex "
                "ACP sessions and received only the P8 manuscript and compact evidence digest."
            ),
        },
        "validation": {
            "problems": problems,
            "reviewer_a_sha256": hash_file(OUTPUT_ROOT / "reviewer-a.md"),
            "reviewer_b_sha256": hash_file(OUTPUT_ROOT / "reviewer-b.md"),
            "combined_reviews_sha256": hash_file(reviews_path),
        },
        "arc_stage_result": {
            "stage": str(result.stage),
            "status": str(result.status),
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
    print(json.dumps({"status": "passed", "reviews": str(reviews_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
