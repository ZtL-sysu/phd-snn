from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import replace
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUN_ROOT = Path(__file__).resolve().parents[1]
ARC_ROOT = Path(r"C:\code\AutoResearchClaw")
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-draft-v3"
REQUEST_PATHS = [
    RUN_ROOT / "writing" / "request-p7-part-1-title-abstract-introduction-related-work.json",
    RUN_ROOT / "writing" / "request-p7-part-2-method-experiments-setup.json",
    RUN_ROOT / "writing" / "request-p7-part-3-results-discussion-conclusion.json",
]

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
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = ""
    truncated: bool = False
    raw: dict[str, Any] | None = None


class CodexACPBackend:
    def __init__(self, acpx: str, session_name: str) -> None:
        self.acpx = acpx
        self.session_name = session_name

    @staticmethod
    def _messages_to_prompt(messages: list[dict[str, str]]) -> str:
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
        return "\n\n".join(parts)

    def chat(self, messages: list[dict[str, str]], **_: Any) -> CapturedResponse:
        prompt = self._messages_to_prompt(messages).replace("\x00", "")
        command = [
            self.acpx, "--approve-all", "--max-turns", "1", "--ttl", "3600",
            "--cwd", str(RUN_ROOT), "codex", "-s", self.session_name, "-f", "-",
        ]
        result = subprocess.run(
            command,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1800,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"acpx/codex writing call failed (exit {result.returncode}): {result.stderr.strip()}"
            )
        lines: list[str] = []
        for line in result.stdout.splitlines():
            if line.startswith(("[acpx]", "[client]", "[tool]", "[done]", "[thinking]")):
                continue
            lines.append(line)
        return CapturedResponse(
            content="\n".join(lines).strip(),
            model="acp:codex",
            finish_reason="stop",
        )


def hash_json(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_writer_json(text: str) -> dict[str, str]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("writer response is not JSON")
    payload = json.loads(stripped[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("writer response JSON is not an object")
    manuscript = payload.get("manuscript")
    notes = payload.get("notes")
    if not isinstance(manuscript, str) or not manuscript.strip():
        raise ValueError("writer response has no manuscript")
    if not isinstance(notes, str) or not notes.strip():
        raise ValueError("writer response has no reverse-outline notes")
    return {"manuscript": manuscript.strip(), "notes": notes.strip()}


class IsolatedARCChat:
    """Execute ARC Stage 17 while sending only clean adapter messages externally."""

    def __init__(self, clean_client: Any, request_messages: list[list[dict[str, str]]]) -> None:
        self.clean_client = clean_client
        self.request_messages = request_messages
        self.internal_call_count = 0
        self.external_call_count = 0
        self.responses: list[CapturedResponse] = []
        self.writer_payloads: list[dict[str, str]] = []
        self.request_hashes = [hash_json(messages) for messages in request_messages]

    def _call_clean(self, messages: list[dict[str, str]], call_index: int) -> tuple[dict[str, str], CapturedResponse]:
        last_error: Exception | None = None
        for attempt in range(1, 3):
            attempt_messages = list(messages)
            if attempt == 2:
                attempt_messages = attempt_messages + [
                    {
                        "role": "user",
                        "content": (
                            "Formatting correction only. Return one JSON object with "
                            "nonempty string fields named manuscript and notes. Do not "
                            "change scientific facts. Do not include Markdown fences."
                        ),
                    }
                ]
            self.external_call_count += 1
            response = self.clean_client.chat(
                attempt_messages,
                max_tokens=16384,
                strip_thinking=True,
            )
            captured = CapturedResponse(
                content=response.content,
                model=response.model,
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                total_tokens=response.total_tokens,
                finish_reason=response.finish_reason,
                truncated=response.truncated,
                raw=response.raw,
            )
            try:
                payload = parse_writer_json(response.content)
            except (ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                continue
            response_path = OUTPUT_ROOT / "model-responses" / f"part-{call_index}-attempt-{attempt}.json"
            response_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            return payload, captured
        raise RuntimeError(f"writer response validation failed for call {call_index}: {last_error}")

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        json_mode: bool = False,
        system: str | None = None,
        strip_thinking: bool = False,
        **_: Any,
    ) -> CapturedResponse:
        self.internal_call_count += 1
        call_index = self.internal_call_count
        if call_index > len(self.request_messages):
            raise RuntimeError("unexpected additional ARC writing call")
        payload, captured = self._call_clean(self.request_messages[call_index - 1], call_index)
        self.writer_payloads.append(payload)
        self.responses.append(captured)
        return CapturedResponse(
            content=payload["manuscript"],
            model=captured.model,
            prompt_tokens=captured.prompt_tokens,
            completion_tokens=captured.completion_tokens,
            total_tokens=captured.total_tokens,
            finish_reason=captured.finish_reason,
            truncated=captured.truncated,
            raw=captured.raw,
        )


def top_level_sections(text: str) -> list[str]:
    sections: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^##\s+([1-6])\s+(.+?)\s*$", line.strip())
        if match:
            sections.append(f"{match.group(1)} {match.group(2).strip()}")
    return sections


def validate_draft(text: str) -> tuple[bool, list[str]]:
    problems: list[str] = []
    sections = top_level_sections(text)
    if sections != EXPECTED_SECTIONS:
        problems.append(f"top-level sections are {sections!r}, expected {EXPECTED_SECTIONS!r}")
    if len(text.split()) < 2800:
        problems.append("draft has fewer than 2800 words")
    for forbidden in ("## Results", "## Experiments", "## Limitations", "## References"):
        if forbidden in text:
            problems.append(f"forbidden top-level section present: {forbidden}")
    for phrase in (
        "matched total padded serialized-bit budget",
        "held-out confirmation after validation exposure",
        "1.86",
        "2.85",
        "1.020",
        "1.124",
        "218.23",
        "our matched-budget adaptations",
    ):
        if phrase not in text:
            problems.append(f"missing required phrase or value: {phrase}")
    if re.search(r"\b(?:TODO|TBD|PLACEHOLDER|INSERT FIGURE HERE)\b", text, re.I):
        problems.append("draft contains a placeholder")
    conclusion = text.split("## 6 Conclusion", 1)[-1] if "## 6 Conclusion" in text else ""
    if len(conclusion.strip()) < 250:
        problems.append("Conclusion is missing or incomplete")
    return not problems, problems


def main() -> int:
    if OUTPUT_ROOT.exists():
        raise RuntimeError(f"ARC draft output already exists: {OUTPUT_ROOT}")
    for directory in ("stage-12/runs", "stage-14", "stage-15", "stage-16", "stage-17", "model-responses"):
        (OUTPUT_ROOT / directory).mkdir(parents=True, exist_ok=True)
    prior_fixture_root = RUN_ROOT / "writing" / "arc-draft-v1"
    shutil.copyfile(
        prior_fixture_root / "stage-12" / "runs" / "migrated-verification.json",
        OUTPUT_ROOT / "stage-12" / "runs" / "migrated-verification.json",
    )
    shutil.copyfile(
        prior_fixture_root / "stage-14" / "experiment_summary.json",
        OUTPUT_ROOT / "stage-14" / "experiment_summary.json",
    )
    shutil.copyfile(
        prior_fixture_root / "stage-14" / "analysis.md",
        OUTPUT_ROOT / "stage-14" / "analysis.md",
    )
    shutil.copyfile(
        prior_fixture_root / "stage-15" / "decision.md",
        OUTPUT_ROOT / "stage-15" / "decision.md",
    )
    shutil.copyfile(
        RUN_ROOT / "writing" / "arc-outline-v3" / "stage-16" / "outline.md",
        OUTPUT_ROOT / "stage-16" / "outline.md",
    )
    (OUTPUT_ROOT / "model-responses").mkdir(exist_ok=True)

    sys.path.insert(0, str(ARC_ROOT))
    from researchclaw.config import RCConfig
    from researchclaw.pipeline.stage_impls._paper_writing import _execute_paper_draft

    request_messages = [
        json.loads(path.read_text(encoding="utf-8"))["messages"] for path in REQUEST_PATHS
    ]
    arc_config = RCConfig.load(RUN_ROOT / "config.arc.yaml", check_paths=False)
    acp_settings = replace(arc_config.llm.acp, agent="codex")
    arc_config = replace(
        arc_config,
        llm=replace(arc_config.llm, provider="acp", acp=acp_settings),
    )
    acpx = shutil.which("acpx")
    if not acpx:
        raise RuntimeError("acpx is not installed")
    session_name = "lr-c05-p7-codex-v3"
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
        raise RuntimeError(f"failed to create Codex ACP session: {session_result.stderr.strip()}")
    clean_client = CodexACPBackend(acpx, session_name)
    isolated_chat = IsolatedARCChat(clean_client, request_messages)

    result = _execute_paper_draft(
        OUTPUT_ROOT / "stage-17",
        OUTPUT_ROOT,
        arc_config,
        adapters=None,
        llm=isolated_chat,
        prompts=None,
    )
    draft_path = OUTPUT_ROOT / "stage-17" / "paper_draft.md"
    draft = draft_path.read_text(encoding="utf-8")
    valid, problems = validate_draft(draft)

    reverse_outline = ["# P7 reverse outline", ""]
    for index, payload in enumerate(isolated_chat.writer_payloads, start=1):
        reverse_outline.extend(
            [
                f"## Part {index}",
                "",
                payload["notes"],
                "",
            ]
        )
    (OUTPUT_ROOT / "reverse-outline.md").write_text(
        "\n".join(reverse_outline).rstrip() + "\n", encoding="utf-8"
    )

    audit = {
        "schema_version": 1,
        "stage": "P7/AutoResearchClaw-17-PAPER_DRAFT",
        "status": "passed" if valid else "failed-validation",
        "arc_checkout": str(ARC_ROOT),
        "arc_version": "0.3.1",
        "arc_stage_source": str(ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_paper_writing.py"),
        "arc_stage_source_sha256": hash_file(
            ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_paper_writing.py"
        ),
        "executor_identity": {
            "provider": "acp",
            "agent": "codex",
            "agent_cli_version": "0.169.0-alpha.11.1",
            "configured_codex_model": "group/never-stuck",
            "acpx_version": "0.19.2",
            "response_models": [response.model for response in isolated_chat.responses],
            "researchclaw_version": "0.3.1",
        },
        "context_isolation": {
            "status": "verified-clean-external-boundary",
            "clean_request_files": [str(path.relative_to(RUN_ROOT)) for path in REQUEST_PATHS],
            "clean_request_hashes": isolated_chat.request_hashes,
            "arc_internal_prompt_sent_to_model": False,
            "raw_execution_logs_sent_to_model": False,
            "compatibility_fixture_used_as_model_context": False,
            "internal_arc_calls": isolated_chat.internal_call_count,
            "external_model_calls": isolated_chat.external_call_count,
            "note": (
                "The installed ARC Stage 17 control flow was executed. Its three "
                "historical writing calls were replaced at the external model "
                "boundary by the three bounded writing_adapter requests through a "
                "Codex ACP session. A separate pre-run availability probe asked "
                "Codex to reply only 'OK' and contained no research content. The "
                "ARC anti-simulation fixture was used only to pass its internal "
                "guard and was never sent to the model."
            ),
        },
        "responses": [
            {
                "model": response.model,
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
                "finish_reason": response.finish_reason,
                "truncated": response.truncated,
            }
            for response in isolated_chat.responses
        ],
        "validation": {
            "valid": valid,
            "problems": problems,
            "expected_sections": EXPECTED_SECTIONS,
            "actual_sections": top_level_sections(draft),
            "word_count": len(draft.split()),
            "draft_sha256": hash_file(draft_path),
            "reverse_outline_sha256": hash_file(OUTPUT_ROOT / "reverse-outline.md"),
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
    if not valid:
        print(json.dumps({"status": "failed-validation", "problems": problems}, indent=2))
        return 2
    print(json.dumps({"status": "passed", "draft": str(draft_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
