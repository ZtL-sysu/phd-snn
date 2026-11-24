from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


RUN_ROOT = Path(__file__).resolve().parents[1]
ARC_ROOT = Path(r"C:\code\AutoResearchClaw")
REQUEST_PATH = RUN_ROOT / "writing" / "request-p6.json"
OUTPUT_ROOT = RUN_ROOT / "writing" / "arc-outline-v3"
ARC_CONFIG_PATH = RUN_ROOT / "config.arc.yaml"
ARC_SECRET_CONFIG_PATH = ARC_ROOT / "config.yaml"

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


class IsolatedARCChat:
    """Run ARC stage control flow while sending only the clean packet messages."""

    def __init__(self, clean_client: Any, clean_messages: list[dict[str, str]]) -> None:
        self.clean_client = clean_client
        self.clean_messages = clean_messages
        self.internal_call_count = 0
        self.external_call_count = 0
        self.response: CapturedResponse | None = None
        self.clean_messages_sha256 = hash_json(clean_messages)

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
        if self.response is not None:
            return self.response

        self.external_call_count += 1
        external_response = self.clean_client.chat(
            self.clean_messages,
            max_tokens=16384,
            strip_thinking=True,
        )
        self.response = CapturedResponse(
            content=external_response.content,
            model=external_response.model,
            prompt_tokens=external_response.prompt_tokens,
            completion_tokens=external_response.completion_tokens,
            total_tokens=external_response.total_tokens,
            finish_reason=external_response.finish_reason,
            truncated=external_response.truncated,
            raw=external_response.raw,
        )
        return self.response


def hash_json(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_transient_api_key() -> str:
    secret_config = read_yaml(ARC_SECRET_CONFIG_PATH)
    api_key = ((secret_config.get("llm") or {}).get("api_key") or "").strip()
    if not api_key:
        raise RuntimeError("AutoResearchClaw config does not contain a transient API key")
    return api_key


def section_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+([1-6])\s+(.+?)\s*$", line.strip())
        if match:
            headings.append(f"{match.group(1)} {match.group(2).strip()}")
    return headings


def validate_outline(text: str) -> tuple[bool, list[str]]:
    problems: list[str] = []
    headings = section_headings(text)
    if headings != EXPECTED_SECTIONS:
        problems.append(f"section headings are {headings!r}, expected {EXPECTED_SECTIONS!r}")
    if len(text.strip()) < 1800:
        problems.append("outline is shorter than 1800 characters")
    if re.search(r"\b(?:truncated|to be continued|continues? below)\b", text, re.I):
        problems.append("outline contains a truncation marker")
    conclusion = text.split("6 Conclusion", 1)[-1] if "6 Conclusion" in text else ""
    if len(conclusion.strip()) < 220:
        problems.append("Conclusion section is missing or incomplete")
    required_fragments = [
        "26.23",
        "33.99",
        "25.83",
        "1.86",
        "2.85",
        "1.020",
        "1.124",
        "218.23",
        "matched total padded serialized-bit budget",
        "held-out confirmation",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            problems.append(f"missing required evidence fragment: {fragment}")
    return not problems, problems


def prepare_output_root() -> Path:
    if OUTPUT_ROOT.exists():
        raise RuntimeError(f"output directory already exists: {OUTPUT_ROOT}")
    (OUTPUT_ROOT / "stage-14").mkdir(parents=True)
    (OUTPUT_ROOT / "stage-15").mkdir(parents=True)
    (OUTPUT_ROOT / "stage-16").mkdir(parents=True)

    source_analysis = RUN_ROOT / "writing" / "arc" / "stage-14" / "analysis.md"
    source_decision = RUN_ROOT / "writing" / "arc" / "stage-15" / "decision.md"
    shutil.copyfile(source_analysis, OUTPUT_ROOT / "stage-14" / "analysis.md")
    shutil.copyfile(source_decision, OUTPUT_ROOT / "stage-15" / "decision.md")
    return OUTPUT_ROOT


def main() -> int:
    sys.path.insert(0, str(ARC_ROOT))
    from researchclaw.config import RCConfig
    from researchclaw.llm import create_llm_client
    from researchclaw.pipeline.stage_impls._paper_writing import _execute_paper_outline

    request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    clean_messages = request["messages"]
    if not isinstance(clean_messages, list) or not clean_messages:
        raise RuntimeError("request-p6.json has no clean messages")
    base_messages_sha256 = hash_json(clean_messages)
    clean_messages = clean_messages + [
        {
            "role": "user",
            "content": (
                "P6 format correction only; do not change any scientific fact. "
                "Return a Markdown outline, not JSON. Use exactly these six "
                "numbered body headings in this order and no other numbered "
                "headings: 1 Introduction; 2 Related Work; 3 Method; "
                "4 Experiments and Results; 5 Discussion; 6 Conclusion. Use "
                "the exact phrase 'matched total padded serialized-bit budget' "
                "for F3. Keep the outline complete but concise, omit title "
                "candidate tables, and end with a complete Conclusion section."
            ),
        }
    ]

    os.environ["DEEPSEEK_API_KEY"] = load_transient_api_key()
    arc_config = RCConfig.load(ARC_CONFIG_PATH, check_paths=False)
    clean_client = create_llm_client(arc_config)
    isolated_chat = IsolatedARCChat(clean_client, clean_messages)
    output_root = prepare_output_root()

    result = _execute_paper_outline(
        output_root / "stage-16",
        output_root,
        arc_config,
        adapters=None,
        llm=isolated_chat,
        prompts=None,
    )
    outline_path = output_root / "stage-16" / "outline.md"
    outline = outline_path.read_text(encoding="utf-8")
    valid, problems = validate_outline(outline)

    audit = {
        "schema_version": 1,
        "stage": "P6/AutoResearchClaw-16-PAPER_OUTLINE",
        "status": "passed" if valid else "failed-validation",
        "arc_checkout": str(ARC_ROOT),
        "arc_version": "0.3.1",
        "arc_stage_source": str(
            ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_paper_writing.py"
        ),
        "arc_stage_source_sha256": hash_file(
            ARC_ROOT / "researchclaw" / "pipeline" / "stage_impls" / "_paper_writing.py"
        ),
        "executor_identity": {
            "provider": arc_config.llm.provider,
            "base_url": arc_config.llm.base_url,
            "wire_api": arc_config.llm.wire_api,
            "configured_model": arc_config.llm.primary_model,
            "response_model": isolated_chat.response.model if isolated_chat.response else "",
            "researchclaw_version": "0.3.1",
        },
        "context_isolation": {
            "status": "verified-clean-external-boundary",
            "external_message_count": len(clean_messages),
            "base_request_messages_sha256": base_messages_sha256,
            "external_messages_sha256": isolated_chat.clean_messages_sha256,
            "arc_internal_prompt_sent_to_model": False,
            "raw_execution_logs_collected": False,
            "internal_arc_calls": isolated_chat.internal_call_count,
            "external_model_calls": isolated_chat.external_call_count,
            "note": (
                "The installed ARC Stage 16 implementation was executed, but an "
                "adapter replaced its historical context prompt at the external "
                "model boundary with the writing_adapter messages from "
                "request-p6.json plus one format-only correction. ARC "
                "analysis/decision files were not sent."
            ),
        },
        "response": {
            "prompt_tokens": isolated_chat.response.prompt_tokens if isolated_chat.response else 0,
            "completion_tokens": isolated_chat.response.completion_tokens if isolated_chat.response else 0,
            "total_tokens": isolated_chat.response.total_tokens if isolated_chat.response else 0,
            "finish_reason": isolated_chat.response.finish_reason if isolated_chat.response else "",
            "truncated": isolated_chat.response.truncated if isolated_chat.response else True,
        },
        "validation": {
            "valid": valid,
            "problems": problems,
            "expected_sections": EXPECTED_SECTIONS,
            "actual_sections": section_headings(outline),
            "outline_sha256": hash_file(outline_path),
        },
        "inputs": {
            "request_p6_sha256": hash_file(REQUEST_PATH),
            "analysis_sha256": hash_file(output_root / "stage-14" / "analysis.md"),
            "decision_sha256": hash_file(output_root / "stage-15" / "decision.md"),
        },
        "arc_stage_result": {
            "stage": str(result.stage),
            "status": str(result.status),
            "artifacts": list(result.artifacts),
            "evidence_refs": list(result.evidence_refs),
        },
    }
    (OUTPUT_ROOT / "executor-context-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if not valid:
        print(json.dumps({"status": "failed-validation", "problems": problems}, indent=2))
        return 2
    print(json.dumps({"status": "passed", "outline": str(outline_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
