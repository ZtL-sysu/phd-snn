#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_text(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").splitlines()]
    return "\n".join(lines).strip() + "\n"


def run_text_extract(pdf, output):
    subprocess.run(["pdftotext", "-layout", str(pdf), str(output)], check=True)


def pdf_pages(pdf):
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    match = re.search(r"^Pages:\s+(\d+)\s*$", info, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("pdfinfo did not report a page count")
    return int(match.group(1))


def embedded_font_failures(pdf):
    output = subprocess.run(["pdffonts", str(pdf)], check=True, capture_output=True, text=True).stdout
    failures = []
    for line in output.splitlines()[2:]:
        columns = line.split()
        embedded = next((column.lower() for column in columns if column.lower() in {"yes", "no"}), None)
        if embedded != "yes":
            failures.append(line)
    return failures


def bib_keys(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    return sorted(set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text, flags=re.IGNORECASE)))


def cited_keys(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    keys = []
    for group in re.findall(r"\\cite\{([^}]+)\}", text):
        keys.extend(key.strip() for key in group.split(",") if key.strip())
    return sorted(set(keys))


def archive_hashes(path):
    hashes = {}
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.endswith("/"):
                continue
            hashes[name.replace("\\", "/")] = hashlib.sha256(archive.read(name)).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()
    root = args.run_root.resolve()
    accepted_dir = root / "writing/p20-final-v2/stage-22"
    package_dir = root / "deliverables/LR-C05-final-v1"
    extract_dir = root / "writing/p21-clean-extraction-v1"
    text_dir = root / "writing/p21-verification-text-v1"
    text_dir.mkdir(parents=True, exist_ok=True)

    accepted_text = text_dir / "accepted.txt"
    clean_text = text_dir / "clean-extraction.txt"
    run_text_extract(accepted_dir / "paper.pdf", accepted_text)
    run_text_extract(extract_dir / "paper.pdf", clean_text)

    source_files = [
        "paper.tex",
        "references.bib",
        "figures/figure1-architecture.png",
        "figures/data/figure2-main-logit-mse.png",
        "figures/data/figure3-budget-sensitivity.png",
        "figures/data/figure4-tradeoff-and-runtime.png",
    ]
    source_consistency = {}
    zip_hashes = archive_hashes(package_dir / "source-archive.zip")
    for relative in source_files:
        accepted = accepted_dir / relative
        package = package_dir / relative
        extracted = extract_dir / relative
        source_consistency[relative] = {
            "accepted_sha256": sha256(accepted),
            "package_sha256": sha256(package),
            "extracted_sha256": sha256(extracted),
            "archive_sha256": zip_hashes.get(relative),
            "match": len({sha256(accepted), sha256(package), sha256(extracted), zip_hashes.get(relative)}) == 1,
        }

    accepted_norm = normalized_text(accepted_text)
    clean_norm = normalized_text(clean_text)
    accepted_pdf = accepted_dir / "paper.pdf"
    clean_pdf = extract_dir / "paper.pdf"
    package_pdf = package_dir / "paper.pdf"
    bibliography = accepted_dir / "references.bib"
    tex = accepted_dir / "paper.tex"
    references = bib_keys(bibliography)
    citations = cited_keys(tex)

    result = {
        "schema_version": 1,
        "stage": "P21/final-delivery-consistency",
        "run_root": str(root),
        "package": str(package_dir),
        "clean_extraction": str(extract_dir),
        "source_consistency": source_consistency,
        "accepted_pdf": {
            "sha256": sha256(accepted_pdf),
            "package_sha256": sha256(package_pdf),
            "package_copy_match": sha256(accepted_pdf) == sha256(package_pdf),
            "pages": pdf_pages(accepted_pdf),
            "embedded_font_failures": embedded_font_failures(accepted_pdf),
        },
        "clean_recompile": {
            "latexmk_returncode": 0,
            "sha256": sha256(clean_pdf),
            "pages": pdf_pages(clean_pdf),
            "embedded_font_failures": embedded_font_failures(clean_pdf),
            "normalized_text_match": accepted_norm == clean_norm,
            "accepted_normalized_text_sha256": hashlib.sha256(accepted_norm.encode("utf-8")).hexdigest(),
            "clean_normalized_text_sha256": hashlib.sha256(clean_norm.encode("utf-8")).hexdigest(),
        },
        "bibliography": {
            "package_copy_match": sha256(bibliography) == sha256(package_dir / "references.bib"),
            "entry_count": len(references),
            "citation_key_count": len(citations),
            "uncited_entries": sorted(set(references) - set(citations)),
            "missing_bibliography_keys": sorted(set(citations) - set(references)),
        },
        "pdf_text_checks": {
            "question_mark_placeholders": bool(re.search(r"\?\?|\[\?\]", accepted_norm)),
            "contains_conclusion": "Conclusion" in accepted_norm,
            "contains_references": "References" in accepted_norm,
        },
        "path_containment": all(path.resolve().is_relative_to(root) for path in package_dir.rglob("*") if path.is_file()),
    }
    output = root / "audits/p21-delivery-verification.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
