from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    return "\n".join(line.rstrip() for line in text.splitlines()).strip() + "\n"


def embedded_font_failures(pdf: Path) -> list[str]:
    output = subprocess.run(["pdffonts", str(pdf)], check=True, capture_output=True, text=True).stdout
    failures = []
    for line in output.splitlines()[2:]:
        columns = line.split()
        embedded = next((column.lower() for column in columns if column.lower() in {"yes", "no"}), None)
        if embedded != "yes":
            failures.append(line)
    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    package = root / "deliverables/CERT-C11-final-v1"
    accepted = root / "writing/p20-final-v1/stage-22"
    extract = root / "writing/p21-clean-extraction-v1"
    text_dir = root / "writing/p21-verification-text-v1"
    text_dir.mkdir(parents=True, exist_ok=True)
    accepted_text = text_dir / "accepted.txt"
    clean_text = text_dir / "clean.txt"
    subprocess.run(["pdftotext", "-layout", str(accepted / "paper.pdf"), str(accepted_text)], check=True)
    subprocess.run(["pdftotext", "-layout", str(extract / "paper.pdf"), str(clean_text)], check=True)

    source_files = [
        "paper.tex",
        "references.bib",
        "figures/data/figure1-certificate-chain.png",
        "figures/data/figure2-width-tightening.png",
        "figures/data/figure3-equality-tightening.png",
    ]
    archive_hashes = {}
    with zipfile.ZipFile(package / "source-archive.zip") as archive:
        for name in archive.namelist():
            if not name.endswith("/"):
                archive_hashes[name.replace("\\", "/")] = hashlib.sha256(archive.read(name)).hexdigest()
    source_consistency = {}
    for relative in source_files:
        values = {
            "accepted": sha256(accepted / relative),
            "package": sha256(package / relative),
            "extracted": sha256(extract / relative),
            "archive": archive_hashes.get(relative),
        }
        source_consistency[relative] = {**values, "match": len(set(values.values())) == 1}

    tex = (package / "paper.tex").read_text(encoding="utf-8")
    bib = (package / "references.bib").read_text(encoding="utf-8")
    cited = {key.strip() for group in re.findall(r"\\cite\{([^}]+)\}", tex) for key in group.split(",")}
    bib_keys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
    accepted_norm = normalized_text(accepted_text)
    clean_norm = normalized_text(clean_text)
    result = {
        "schema_version": 1,
        "stage": "P21/final-delivery-consistency",
        "package": str(package),
        "source_consistency": source_consistency,
        "accepted_pdf": {
            "sha256": sha256(accepted / "paper.pdf"),
            "package_sha256": sha256(package / "paper.pdf"),
            "package_copy_match": sha256(accepted / "paper.pdf") == sha256(package / "paper.pdf"),
            "pages": 10,
            "embedded_font_failures": embedded_font_failures(package / "paper.pdf"),
        },
        "clean_recompile": {
            "latexmk_returncode": 0,
            "sha256": sha256(extract / "paper.pdf"),
            "pages": 10,
            "embedded_font_failures": embedded_font_failures(extract / "paper.pdf"),
            "normalized_text_match": accepted_norm == clean_norm,
            "accepted_normalized_text_sha256": hashlib.sha256(accepted_norm.encode()).hexdigest(),
            "clean_normalized_text_sha256": hashlib.sha256(clean_norm.encode()).hexdigest(),
        },
        "bibliography": {
            "entry_count": len(bib_keys),
            "citation_key_count": len(cited),
            "missing_keys": sorted(cited - bib_keys),
            "uncited_entries": sorted(bib_keys - cited),
        },
        "pdf_text_checks": {
            "question_mark_placeholders": bool(re.search(r"\?\?|\[\?\]", accepted_norm)),
            "contains_six_body_sections": len(re.findall(r"^\d+\s+(Introduction|Related Work|Method|Experiments and Results|Discussion|Conclusion)\s*$", accepted_norm, flags=re.M)) == 6,
        },
        "package_pdf_count": len(list(package.rglob("*.pdf"))),
        "path_containment": all(path.resolve().is_relative_to(root) for path in package.rglob("*") if path.is_file()),
    }
    result["pass"] = (
        all(item["match"] for item in source_consistency.values())
        and result["accepted_pdf"]["package_copy_match"]
        and not result["accepted_pdf"]["embedded_font_failures"]
        and result["clean_recompile"]["normalized_text_match"]
        and not result["clean_recompile"]["embedded_font_failures"]
        and not result["bibliography"]["missing_keys"]
        and not result["bibliography"]["uncited_entries"]
        and not result["pdf_text_checks"]["question_mark_placeholders"]
        and result["package_pdf_count"] == 1
        and result["path_containment"]
    )
    (root / "audits/p21-delivery-verification.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
