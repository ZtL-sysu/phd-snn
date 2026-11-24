from __future__ import annotations

import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = RUN_ROOT / "results" / "p12-official-page-probe.json"

URLS = {
    "one-spike": "https://doi.org/10.1109/TETC.2024.3386893",
    "asgcn": "https://ojs.aaai.org/index.php/AAAI/article/view/32154",
    "spikinggcn": "https://www.ijcai.org/proceedings/2022/338",
    "spikenet": "https://ojs.aaai.org/index.php/AAAI/article/view/26034",
    "dy-sign": "https://doi.org/10.1609/aaai.v38i15.29587",
    "delay-dsgn": "https://proceedings.mlr.press/v267/wang25dm.html",
    "signnn": "https://doi.org/10.1016/j.patcog.2024.111026",
    "msg": "https://proceedings.neurips.cc/paper_files/paper/2024/hash/3ba7560b4c3e66d760fbdd472cf4a5a9-Abstract-Conference.html",
    "negative-spike": "https://www.ijcai.org/proceedings/2025/719",
    "adaqp": "https://proceedings.mlsys.org/paper_files/paper/2023/hash/420bcf98bb3615a21468f1efb426e96d-Abstract-mlsys2023.html",
    "seenn": "https://papers.neurips.cc/paper_files/paper/2023/hash/c801e68207da477bbc44182b9fac1129-Abstract-Conference.html",
    "spikezip": "https://proceedings.mlr.press/v235/you24b.html",
    "ttfsformer": "https://proceedings.mlr.press/v267/zhao25n.html",
    "sight": "https://doi.org/10.1145/3774904.3793044",
    "sgspose": "https://doi.org/10.1109/ACCESS.2026.3651795",
}


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, list[str]] = {}
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        if tag.lower() == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            content = values.get("content", "")
            if key and content:
                self.meta.setdefault(key, []).append(content)
        elif tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def fetch(key: str, url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 phd-snn-citation-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8", errors="replace")
        final_url = response.geturl()
    parser = MetaParser()
    parser.feed(raw)
    meta = parser.meta
    title_values = meta.get("citation_title") or meta.get("dc.title") or meta.get("og:title") or [parser.title]
    author_values = meta.get("citation_author") or meta.get("dc.creator") or meta.get("author") or []
    date_values = meta.get("citation_publication_date") or meta.get("citation_date") or meta.get("dc.date") or []
    doi_values = meta.get("citation_doi") or meta.get("dc.identifier") or []
    venue_values = meta.get("citation_journal_title") or meta.get("citation_conference_title") or meta.get("citation_publisher") or []
    return {
        "key": key,
        "requested_url": url,
        "final_url": final_url,
        "title": html.unescape(" ".join(title_values).strip()),
        "authors": [html.unescape(value.strip()) for value in author_values],
        "dates": [value.strip() for value in date_values],
        "identifiers": [value.strip() for value in doi_values],
        "venues": [html.unescape(value.strip()) for value in venue_values],
        "meta_keys": sorted(meta),
    }


def main() -> int:
    records = []
    for key, url in URLS.items():
        try:
            records.append(fetch(key, url))
        except Exception as exc:
            records.append({"key": key, "requested_url": url, "error": str(exc)})
    OUTPUT.write_text(json.dumps({"schema_version": 1, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
