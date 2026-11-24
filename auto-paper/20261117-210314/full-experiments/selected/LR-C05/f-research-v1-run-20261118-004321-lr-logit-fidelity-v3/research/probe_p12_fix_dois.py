from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = RUN_ROOT / "results" / "p12-fix-dois.json"

DOIS = [
    "10.1109/TPAMI.2023.3275769",
    "10.1109/ICASSP48485.2024.10448202",
    "10.1145/3664647.3680620",
    "10.1016/j.ins.2026.123828",
    "10.1109/ICMLT65785.2025.11193154",
    "10.1109/TNNLS.2023.3263008",
    "10.1109/ACCESS.2022.3179968",
]


def fetch(doi: str) -> dict:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    request = urllib.request.Request(url, headers={"User-Agent": "phd-snn-citation-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8")).get("message", {})


def main() -> int:
    records = []
    for doi in DOIS:
        try:
            records.append({"doi": doi, "record": fetch(doi)})
        except Exception as exc:
            records.append({"doi": doi, "error": str(exc)})
    OUTPUT.write_text(json.dumps({"schema_version": 1, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
