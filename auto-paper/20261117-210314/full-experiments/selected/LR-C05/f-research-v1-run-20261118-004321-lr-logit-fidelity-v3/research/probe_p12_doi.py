from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = RUN_ROOT / "results" / "p12-doi-probe.json"

DOIS = {
    "one-spike": "10.1109/TETC.2024.3386893",
    "asgcn": "10.1609/aaai.v39i2.32154",
    "spikenet": "10.1609/aaai.v37i1.26034",
    "dy-sign": "10.1609/aaai.v38i15.29587",
    "signnn": "10.1016/j.patcog.2024.111026",
    "sight": "10.1145/3774904.3793044",
    "sgspose": "10.1109/ACCESS.2026.3651795",
    "deepgcn": "10.1109/ICCV.2019.00936",
    "qgtc": "10.1145/3503221.3508408",
    "error-aware-conversion": "10.1007/s11263-024-02046-2",
    "degree-quant": "10.48550/arxiv.2008.05000",
    "vqgnn": "10.48550/arxiv.2110.14363",
    "optimal-annsnn": "10.48550/arxiv.2303.04347",
    "graph-1bit-spikes": "10.48550/arxiv.2305.19306",
}


def fetch_doi(doi: str) -> dict:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    request = urllib.request.Request(url, headers={"User-Agent": "phd-snn-citation-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8")).get("message", {})


def main() -> int:
    records = []
    for key, doi in DOIS.items():
        try:
            records.append({"key": key, "doi": doi, "record": fetch_doi(doi)})
        except Exception as exc:
            records.append({"key": key, "doi": doi, "error": str(exc)})
    OUTPUT.write_text(json.dumps({"schema_version": 1, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
