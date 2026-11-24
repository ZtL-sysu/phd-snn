from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "notion-export" / "raw"
MARKDOWN_DIR = ROOT / "notion-export" / "markdown"
ASSET_DIR = ROOT / "notion-export" / "assets"
NOTION_API = "https://www.notion.so/api/v3/getSignedFileUrls"
NOTION_PAGE_BASE = "https://app.notion.com/p/"

PAGE_FILES = {
    "41b0e334-2e6f-818f-86b9-d9a6cbc71968": "00-overview.md",
    "41b0e334-2e6f-8100-a67c-d692f7be6d08": "01-one-page.md",
    "41b0e334-2e6f-81d8-9aa3-fad02e1a9faa": "02-foundations.md",
    "41b0e334-2e6f-81d9-ad63-c20ebe0b51b5": "03-conversion-timeline.md",
    "41b0e334-2e6f-812c-aa0e-c9ae9c741522": "04-spiking-graph-timeline.md",
    "41b0e334-2e6f-81d3-b941-f53e1b53937f": "05-vision-graph-models.md",
    "41b0e334-2e6f-81dc-b2a2-c3c138cfe0f7": "06-partial-computation.md",
    "41b0e334-2e6f-81fd-8f2a-f94f380e93da": "07-energy-accounting.md",
    "41b0e334-2e6f-81c6-8e0a-c192040b01d3": "08-difficulty-map.md",
    "41b0e334-2e6f-815c-b595-c1c6c712b79c": "09-paper-ideas.md",
    "41b0e334-2e6f-81cb-a505-e4f774ccf728": "10-claude-audit.md",
    "41b0e334-2e6f-811e-8e69-f0040d257997": "11-glossary.md",
    "41b0e334-2e6f-814a-98b5-c85f2ded4083": "12-literature.md",
}


def unwrap(value: dict[str, Any]) -> dict[str, Any]:
    current = value
    while isinstance(current, dict) and "value" in current and isinstance(current["value"], dict):
        current = current["value"]
    return current


def load_sources() -> tuple[dict[str, dict[str, Any]], dict[str, Any], list[str]]:
    blocks: dict[str, dict[str, Any]] = {}
    collection: dict[str, Any] = {}
    collection_order: list[str] = []
    for path in sorted(RAW_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        record_map = data.get("recordMap", {})
        for block_id, entry in record_map.get("block", {}).items():
            blocks[block_id] = unwrap(entry)
        for collection_id, entry in record_map.get("collection", {}).items():
            collection[collection_id] = unwrap(entry)
        if path.name == "collection-query.json":
            collection_order = (
                data.get("result", {})
                .get("reducerResults", {})
                .get("collection_group_results", {})
                .get("blockIds", [])
            )
    return blocks, collection, collection_order


def plain_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, list):
        return str(value)
    parts: list[str] = []
    for segment in value:
        if isinstance(segment, str):
            parts.append(segment)
        elif isinstance(segment, list) and segment:
            parts.append(str(segment[0]))
    return "".join(parts)


def clean_file_name(value: str, fallback: str) -> str:
    name = Path(value).name or fallback
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    return name[:180] or fallback


def notion_page_url(page_id: str) -> str:
    return NOTION_PAGE_BASE + page_id.replace("-", "")


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def open_with_retry(request: urllib.request.Request, timeout: int):
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            return urllib.request.urlopen(request, timeout=timeout)
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(attempt + 1)
    raise last_error


def referenced_block_ids(blocks: dict[str, dict[str, Any]]) -> set[str]:
    referenced: set[str] = set()
    for block in blocks.values():
        referenced.update(str(block_id) for block_id in block.get("content", []))
    return referenced


def fetch_missing_blocks(blocks: dict[str, dict[str, Any]]) -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    sync_number = 1
    fetched = 0
    while True:
        missing = sorted(referenced_block_ids(blocks) - blocks.keys())
        if not missing:
            return fetched
        for offset in range(0, len(missing), 100):
            batch = missing[offset : offset + 100]
            payload = json.dumps(
                {
                    "requests": [
                        {"table": "block", "id": block_id, "version": -1}
                        for block_id in batch
                    ]
                }
            ).encode("utf-8")
            request = urllib.request.Request(
                "https://www.notion.so/api/v3/syncRecordValues",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5",
                    "notion-client-version": "web-23.13.20261117.2333",
                },
                method="POST",
            )
            with open_with_retry(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
            sync_path = RAW_DIR / f"block-sync-{sync_number:02d}.json"
            sync_path.write_text(raw, encoding="utf-8")
            sync_number += 1
            data = json.loads(raw)
            for block_id, entry in data.get("recordMap", {}).get("block", {}).items():
                blocks[block_id] = unwrap(entry)
            fetched += len(batch)


class NotionExporter:
    def __init__(
        self,
        blocks: dict[str, dict[str, Any]],
        collections: dict[str, Any],
        collection_order: list[str],
    ) -> None:
        self.blocks = blocks
        self.collections = collections
        self.collection_order = collection_order
        self.asset_paths: dict[str, str] = {}
        self.asset_manifest: list[dict[str, Any]] = []

    def page_link(self, page_id: str, label: str) -> str:
        if page_id in PAGE_FILES:
            return f"[{label}]({PAGE_FILES[page_id]})"
        if page_id in self.blocks:
            return f"[{label}]({notion_page_url(page_id)})"
        return f"{label}（Notion page `{page_id}`）"

    def rich(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            return value
        if not isinstance(value, list):
            return str(value)
        output: list[str] = []
        for segment in value:
            if isinstance(segment, str):
                output.append(segment)
                continue
            if not isinstance(segment, list) or not segment:
                continue
            text = str(segment[0])
            formats = segment[1] if len(segment) > 1 and isinstance(segment[1], list) else []
            rendered = text
            link_url = ""
            for item in formats:
                if not isinstance(item, list) or not item:
                    continue
                kind = str(item[0])
                if kind == "a" and len(item) > 1:
                    link_url = str(item[1])
                elif kind == "p" and len(item) > 1:
                    page_id = str(item[1])
                    page = self.blocks.get(page_id, {})
                    label = plain_text(page.get("properties", {}).get("title")) or text.strip("‣ ")
                    rendered = self.page_link(page_id, label)
                elif kind == "e" and len(item) > 1:
                    rendered = f"${str(item[1])}$"
                elif kind == "b":
                    rendered = f"**{rendered}**"
                elif kind == "i":
                    rendered = f"*{rendered}*"
                elif kind == "s":
                    rendered = f"~~{rendered}~~"
                elif kind == "c":
                    rendered = f"`{rendered}`"
                elif kind == "u":
                    rendered = f"<u>{rendered}</u>"
            if link_url:
                rendered = f"[{rendered}]({link_url})"
            output.append(rendered)
        return "".join(output)

    def download_assets(self) -> None:
        ASSET_DIR.mkdir(parents=True, exist_ok=True)
        seen: set[tuple[str, str]] = set()
        for block_id, block in self.blocks.items():
            block_type = block.get("type")
            if block_type not in {"image", "embed", "video", "file", "pdf"}:
                continue
            properties = block.get("properties", {})
            source = plain_text(properties.get("source"))
            title = plain_text(properties.get("title"))
            if not source:
                continue
            key = (block_id, source)
            if key in seen:
                continue
            seen.add(key)
            fallback = f"{block_id}.{block_type}"
            if source.startswith("attachment:"):
                file_name = clean_file_name(source.split(":", 2)[-1], fallback)
                file_name = f"{block_id[:8]}-{file_name}"
                target = ASSET_DIR / file_name
                record: dict[str, Any] = {
                    "block_id": block_id,
                    "type": block_type,
                    "title": title,
                    "source": source,
                    "local_path": str(target.relative_to(ROOT)).replace("\\", "/"),
                }
                if target.exists() and target.stat().st_size > 0:
                    content = target.read_bytes()
                    record["bytes"] = len(content)
                    record["sha256"] = hashlib.sha256(content).hexdigest()
                    record["reused_existing"] = True
                    self.asset_paths[block_id] = file_name
                    self.asset_manifest.append(record)
                    continue
                try:
                    payload = json.dumps(
                        {
                            "urls": [
                                {
                                    "url": source,
                                    "permissionRecord": {
                                        "table": "block",
                                        "id": block_id,
                                    },
                                }
                            ]
                        }
                    ).encode("utf-8")
                    request = urllib.request.Request(
                        NOTION_API,
                        data=payload,
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": "Mozilla/5",
                            "notion-client-version": "web-23.13.20261117.2333",
                        },
                        method="POST",
                    )
                    with open_with_retry(request, timeout=30) as response:
                        signed = json.loads(response.read().decode("utf-8"))
                    signed_url = signed["signedUrls"][0]
                    download_request = urllib.request.Request(
                        signed_url,
                        headers={"User-Agent": "Mozilla/5"},
                    )
                    with open_with_retry(download_request, timeout=60) as response:
                        content = response.read()
                    target.write_bytes(content)
                    record["bytes"] = len(content)
                    record["sha256"] = hashlib.sha256(content).hexdigest()
                    self.asset_paths[block_id] = file_name
                except Exception as error:
                    record["error"] = str(error)
                self.asset_manifest.append(record)
            else:
                self.asset_manifest.append(
                    {
                        "block_id": block_id,
                        "type": block_type,
                        "title": title,
                        "source": source,
                    }
                )

    def asset_markdown(self, block: dict[str, Any]) -> str:
        block_id = str(block.get("id"))
        properties = block.get("properties", {})
        title = plain_text(properties.get("title"))
        caption = plain_text(properties.get("caption"))
        file_name = self.asset_paths.get(block_id)
        source = plain_text(properties.get("source"))
        if file_name:
            target = f"../assets/{file_name}"
            if block.get("type") == "image":
                line = f"![{markdown_escape(caption or title)}]({target})"
            else:
                line = f"[打开本地附件：{title or file_name}]({target})"
        elif source:
            line = f"[{title or source}]({source})"
        else:
            line = title
        if caption:
            line += f"\n\n*{caption}*"
        return line

    def table_markdown(self, block: dict[str, Any]) -> list[str]:
        row_ids = block.get("content", [])
        rows = [self.blocks[row_id] for row_id in row_ids if row_id in self.blocks]
        if not rows:
            return []
        column_order = block.get("format", {}).get("table_block_column_order")
        if not column_order:
            column_order = list(rows[0].get("properties", {}).keys())
        lines = []
        for index, row in enumerate(rows):
            values = [
                markdown_escape(self.rich(row.get("properties", {}).get(column, "")))
                for column in column_order
            ]
            lines.append("| " + " | ".join(values) + " |")
            if index == 0 and block.get("format", {}).get("table_block_column_header", True):
                lines.append("| " + " | ".join(["---"] * len(column_order)) + " |")
        return lines

    def collection_markdown(self, block: dict[str, Any]) -> list[str]:
        collection_id = str(block.get("collection_id") or block.get("format", {}).get("collection_pointer", {}).get("id"))
        collection = self.collections.get(collection_id, {})
        schema = collection.get("schema", {})
        title = self.rich(block.get("properties", {}).get("title")) or self.rich(collection.get("name"))
        lines = [f"## {title}", ""]
        description = self.rich(collection.get("description"))
        if description:
            lines.extend([description, ""])
        row_ids = [row_id for row_id in self.collection_order if row_id in self.blocks]
        lines.append(f"共 {len(row_ids)} 条记录。")
        lines.append("")
        for row_id in row_ids:
            row = self.blocks[row_id]
            row_title = self.rich(row.get("properties", {}).get("title")) or row_id
            lines.append(f'### <a id="{row_id}"></a>{row_title}')
            lines.append("")
            for field_id, field in schema.items():
                if field_id == "title":
                    continue
                field_name = plain_text(field.get("name"))
                field_value = self.rich(row.get("properties", {}).get(field_id))
                if field_value:
                    lines.append(f"- **{field_name}：** {field_value}")
            if row.get("content"):
                lines.append("")
                lines.extend(self.render_children(row.get("content", []), heading_level=4))
            lines.append("")
        return lines

    def render_block(self, block_id: str, heading_level: int = 2) -> list[str]:
        block = self.blocks.get(block_id)
        if not block:
            return [f"（缺失块 `{block_id}`）"]
        block_type = str(block.get("type"))
        properties = block.get("properties", {})
        title = self.rich(properties.get("title"))
        content_ids = block.get("content", [])

        if block_type == "page":
            label = title or block_id
            return [self.page_link(str(block.get("id")), label), ""]
        if block_type == "collection_view_page":
            return self.collection_markdown(block)
        if block_type == "table":
            return self.table_markdown(block) + [""]
        if block_type == "table_row":
            return []
        if block_type in {"image", "embed", "video", "file", "pdf"}:
            return [self.asset_markdown(block), ""]
        if block_type == "divider":
            return ["---", ""]
        if block_type == "code":
            language = plain_text(properties.get("language")).lower()
            return [f"```{language}", title, "```", ""]
        if block_type == "quote":
            lines = [f"> {title}"] if title else [">"]
            for child_id in content_ids:
                lines.extend(f"> {line}" if line else ">" for line in self.render_block(child_id, heading_level))
            return lines + [""]
        if block_type == "callout":
            icon = plain_text(block.get("format", {}).get("page_icon")) or ">"
            lines = [f"> {icon} {title}".rstrip()]
            for child_id in content_ids:
                child_lines = self.render_block(child_id, heading_level)
                lines.extend(f"> {line}" if line else ">" for line in child_lines if line != "")
            return lines + [""]
        if block_type == "header":
            prefix = "#" * max(1, min(6, heading_level))
            return [f"{prefix} {title}", ""]
        if block_type == "sub_header":
            prefix = "#" * max(1, min(6, heading_level + 1))
            return [f"{prefix} {title}", ""]
        if block_type == "sub_sub_header":
            prefix = "#" * max(1, min(6, heading_level + 2))
            return [f"{prefix} {title}", ""]
        if block_type == "bulleted_list":
            lines = [f"- {title}"]
            for child_id in content_ids:
                lines.extend(f"  {line}" for line in self.render_block(child_id, heading_level))
            return lines
        if block_type == "numbered_list":
            lines = [f"1. {title}"]
            for child_id in content_ids:
                lines.extend(f"   {line}" for line in self.render_block(child_id, heading_level))
            return lines
        if block_type == "to_do":
            checked = bool(properties.get("checked"))
            mark = "x" if checked else " "
            return [f"- [{mark}] {title}"]
        if block_type == "toggle":
            lines = [f"<details><summary>{title}</summary>", ""]
            lines.extend(self.render_children(content_ids, heading_level + 1))
            lines.extend(["", "</details>"])
            return lines
        if block_type in {"column_list", "column"}:
            return self.render_children(content_ids, heading_level)
        if block_type == "equation":
            return [f"$$\n{title}\n$$", ""]
        if block_type in {"bookmark", "link_preview"}:
            source = plain_text(properties.get("source") or properties.get("link"))
            return [f"[{title or source}]({source})", ""] if source else [title, ""]
        if block_type == "text" or title:
            lines = [title] if title else []
            lines.extend(self.render_children(content_ids, heading_level))
            return lines + [""]
        return self.render_children(content_ids, heading_level)

    def render_children(self, block_ids: list[str], heading_level: int = 2) -> list[str]:
        output: list[str] = []
        for block_id in block_ids:
            output.extend(self.render_block(block_id, heading_level))
        while output and output[-1] == "":
            output.pop()
        return output

    def render_page(self, page_id: str) -> str:
        page = self.blocks[page_id]
        title = self.rich(page.get("properties", {}).get("title")) or page_id
        lines = [
            f"# {title}",
            "",
            f"> 本地化来源：[Notion 原页面]({notion_page_url(page_id)})；由 `export_notion.py` 从只读块数据导出。",
            "",
        ]
        lines.extend(self.render_children(page.get("content", []), heading_level=2))
        return "\n".join(lines).rstrip() + "\n"

    def export(self) -> None:
        self.download_assets()
        MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
        for page_id, file_name in PAGE_FILES.items():
            if page_id not in self.blocks:
                continue
            (MARKDOWN_DIR / file_name).write_text(self.render_page(page_id), encoding="utf-8")
        (ROOT / "notion-export" / "assets-manifest.json").write_text(
            json.dumps(self.asset_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        index_lines = [
            "# Notion 本地导出",
            "",
            "原始页面：[视觉图网络免训练转脉冲网络：通俗讲解](https://app.notion.com/p/41b0e3342e6f818f86b9d9a6cbc71968)",
            "",
            "## 页面",
            "",
        ]
        for page_id, file_name in PAGE_FILES.items():
            page = self.blocks.get(page_id, {})
            title = self.rich(page.get("properties", {}).get("title")) or file_name
            index_lines.append(f"- [{title}]({file_name})")
        index_lines.extend(
            [
                "",
                "## 目录说明",
                "",
                "- `markdown/`：完整可读 Markdown 导出，包含 12 个子页面与 115 条文献数据库记录。",
                "- `raw/`：Notion 只读 API 原始 JSON，保留块、数据库和视图结构。",
                "- `assets/`：页面内 SVG 与交互动画 HTML 附件。",
                "- `assets-manifest.json`：附件来源、本地路径、字节数与 SHA256。",
            ]
        )
        (MARKDOWN_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def main() -> None:
    blocks, collections, collection_order = load_sources()
    fetch_missing_blocks(blocks)
    exporter = NotionExporter(blocks, collections, collection_order)
    exporter.export()
    print(f"Exported {len(PAGE_FILES)} pages, {len(collection_order)} collection rows, and {len(exporter.asset_manifest)} assets.")


if __name__ == "__main__":
    main()
