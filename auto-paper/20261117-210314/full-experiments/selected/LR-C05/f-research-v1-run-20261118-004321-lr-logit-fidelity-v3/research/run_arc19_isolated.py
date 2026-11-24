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
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-revision-v1"
REQUEST_PATH = RUN_ROOT / "writing" / "request-p10-revision.json"
SOURCE_DRAFT = RUN_ROOT / "writing" / "p8" / "paper-data-figures.md"

EXPECTED_SECTIONS = [
    "1 Introduction",
    "2 Related Work",
    "3 Method",
    "4 Experiments and Results",
    "5 Discussion",
    "6 Conclusion",
]


@dataclass
class CapturedResponse:
    content: str
    model: str
    finish_reason: str = "stop"
    raw: dict[str, Any] | None = None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_writer_json(text: str) -> dict[str, str]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("revision response is not JSON")
    payload = json.loads(stripped[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("revision response is not an object")
    manuscript = payload.get("manuscript")
    notes = payload.get("notes")
    if not isinstance(manuscript, str) or not manuscript.strip():
        raise ValueError("revision response has no manuscript")
    if not isinstance(notes, str) or not notes.strip():
        raise ValueError("revision response has no notes")
    return {"manuscript": manuscript.strip(), "notes": notes.strip()}


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
            elif role == "assistant":
                parts.append(f"[Previous Response]\n{content}")
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
            raise RuntimeError(f"acpx/codex revision failed: {result.stderr.strip()}")
        lines = [
            line
            for line in result.stdout.splitlines()
            if not line.startswith(("[acpx]", "[client]", "[tool]", "[done]", "[thinking]"))
        ]
        return CapturedResponse(content="\n".join(lines).strip(), model="acp:codex")


class IsolatedRevisionChat:
    def __init__(self, backend: CodexACPBackend, request: dict[str, Any]) -> None:
        self.backend = backend
        self.request = request
        self.internal_calls = 0
        self.external_calls = 0
        self.payload: dict[str, str] | None = None
        self.response: CapturedResponse | None = None

    def chat(self, messages: list[dict[str, str]], **_: Any) -> CapturedResponse:
        self.internal_calls += 1
        if self.payload is not None:
            return CapturedResponse(
                content=self.payload["manuscript"],
                model=self.response.model if self.response else "acp:codex",
            )
        last_error: Exception | None = None
        for attempt in range(1, 3):
            clean_messages = list(self.request["messages"])
            if attempt == 2:
                clean_messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Formatting correction only: return one JSON object with "
                            "nonempty string fields manuscript and notes. Do not change "
                            "the requested scientific revision."
                        ),
                    }
                )
            self.external_calls += 1
            response = self.backend.chat(clean_messages)
            try:
                self.payload = parse_writer_json(response.content)
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                continue
            self.response = response
            (OUTPUT_ROOT / "model-response.json").write_text(
                json.dumps(self.payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            return CapturedResponse(content=self.payload["manuscript"], model=response.model)
        raise RuntimeError(f"revision response validation failed: {last_error}")


def top_level_sections(text: str) -> list[str]:
    sections = []
    for line in text.splitlines():
        match = re.match(r"^##\s+([1-6])\s+(.+?)\s*$", line.strip())
        if match:
            sections.append(f"{match.group(1)} {match.group(2).strip()}")
    return sections


def validate_revision(text: str, source: str) -> list[str]:
    problems: list[str] = []
    sections = top_level_sections(text)
    if sections != EXPECTED_SECTIONS:
        problems.append(f"top-level sections are {sections!r}")
    if len(text.split()) < int(len(source.split()) * 0.9):
        problems.append("revision lost more than 10% of the manuscript")
    required = [
        "M_0",
        "r_i^2",
        "J_i",
        "21,932,736",
        "25,630,208",
        "43,771,008",
        "top-absolute",
        "random",
        "dense uniform",
        "A2Q-style",
        "One-Spike-style",
        "maximum observed degradation",
        "0.53",
        "1.17",
        "1.86",
        "2.85",
        "post hoc",
        "16, 32, 64, and 128",
        "0.5%, 1%, and 2%",
        "three warmups",
        "seven",
    ]
    for phrase in required:
        if phrase not in text:
            problems.append(f"missing required repair phrase: {phrase}")
    if not ("A_hat X" in text or r"\hat{A}X" in text):
        problems.append("missing normalized input-message notation A_hat X or \\hat{A}X")
    forbidden = [
        "bounded task loss",
        "task superiority was established",
        "establishes energy savings",
        "supports broad GNN generality",
    ]
    for phrase in forbidden:
        if phrase in text:
            problems.append(f"forbidden overclaim remains: {phrase}")
    if text.count("![") != 4:
        problems.append(f"expected four figure references, found {text.count('![')}")
    if not ("3 pp reference" in text or "3 pp task-loss reference" in text):
        problems.append("Figure 4 caption does not explain the 3 pp reference")
    return problems


def main() -> int:
    sys.path.insert(0, str(ARC_ROOT))
    from researchclaw.config import RCConfig
    from researchclaw.pipeline.stage_impls._review_publish import _execute_paper_revision

    acpx = shutil.which("acpx")
    if not acpx:
        raise RuntimeError("acpx is not installed")
    session_name = "lr-c05-p10-revision"
    session_result = subprocess.run(
        [
            acpx, "--ttl", "3600", "--cwd", str(RUN_ROOT),
            "codex", "sessions", "new", "--name", session_name,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    if session_result.returncode != 0:
        raise RuntimeError(f"failed to create revision session: {session_result.stderr.strip()}")

    request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    isolated = IsolatedRevisionChat(CodexACPBackend(acpx, session_name), request)
    arc_config = RCConfig.load(RUN_ROOT / "config.arc.yaml", check_paths=False)
    result = _execute_paper_revision(
        OUTPUT_ROOT / "stage-19",
        OUTPUT_ROOT,
        arc_config,
        adapters=None,
        llm=isolated,
        prompts=None,
    )
    revised_path = OUTPUT_ROOT / "stage-19" / "paper_revised.md"
    revised = revised_path.read_text(encoding="utf-8")
    source = SOURCE_DRAFT.read_text(encoding="utf-8")
    problems = validate_revision(revised, source)
    if isolated.payload:
        (OUTPUT_ROOT / "revision-notes.md").write_text(isolated.payload["notes"] + "\n", encoding="utf-8")

    audit = {
        "schema_version": 1,
        "stage": "P10/AutoResearchClaw-19-PAPER_REVISION",
        "status": "passed" if not problems else "failed-validation",
        "arc_version": "0.3.1",
        "arc_stage_source": str(ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_review_publish.py"),
        "arc_stage_source_sha256": sha256(ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_review_publish.py"),
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
            "note": (
                "The installed ARC Stage 19 control flow was executed. Its historical "
                "draft/review/raw-metrics context was replaced at the external model "
                "boundary by the clean writing_adapter P10 request containing the current "
                "manuscript, scientific facts, and explicit edit decisions only."
            ),
        },
        "validation": {
            "problems": problems,
            "source_sha256": sha256(SOURCE_DRAFT),
            "revised_sha256": sha256(revised_path),
            "source_words": len(source.split()),
            "revised_words": len(revised.split()),
            "expected_sections": EXPECTED_SECTIONS,
            "actual_sections": top_level_sections(revised),
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
    print(json.dumps({"status": "passed", "revised": str(revised_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
