"""Check distinct actually-cited works, bib coverage and recency arithmetic (P12/P14)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "tex"
raw = (TEX / "main.tex").read_text(encoding="utf-8") + "\n" + (
    TEX / "appendix.tex").read_text(encoding="utf-8")
# TeX comments: an unescaped '%' discards the rest of the line, including the newline.
lines = []
for line in raw.splitlines():
    m = re.search(r"(?<!\\)%", line)
    lines.append(line[:m.start()] if m else line)
text = "\n".join(lines)
bib_text = (TEX / "refs.bib").read_text(encoding="utf-8")

keys = set()
for group in re.findall(r"\\cite\{([^}]*)\}", text):
    for k in group.replace("\n", " ").split(","):
        if k.strip():
            keys.add(k.strip())
keys_bib = {k.strip() for _, k in re.findall(r"@(\w+)\{([^,]+),", bib_text)}

years = {}
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)(?=\n@|\Z)", bib_text, re.S):
    y = re.search(r"\byear\s*=\s*\{?\s*(\d{4})", m.group(3))
    if y:
        years[m.group(2).strip()] = int(y.group(1))

recent = [k for k in keys if years.get(k, 0) >= 2023]
missing = sorted(keys - keys_bib)
print("distinct actually cited :", len(keys))
print("bib entries             :", len(keys_bib))
print("cited but missing in bib:", missing)
print("uncited bib entries     :", len(keys_bib - keys), sorted(keys_bib - keys))
print("bib year coverage       :", len(years), "/", len(keys_bib))
print("cited 2023-2026         :", len(recent))
print("strict recent majority  :", 2 * len(recent) > len(keys))
print("min_unique>=36          :", len(keys) >= 36)
ok = (len(keys) >= 36 and 2 * len(recent) > len(keys) and not missing
      and len(years) >= len(keys_bib) - 2)
print("RESULT:", "PASS" if ok else "FAIL")
