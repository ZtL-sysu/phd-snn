from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

import cairosvg


RUN_ROOT = Path(__file__).resolve().parents[1]
FIGURES = RUN_ROOT / "figures"
SPEC_PATH = FIGURES / "specs" / "figure1-architecture-spec.json"
SVG_PATH = FIGURES / "figure1-architecture.svg"
PDF_PATH = FIGURES / "figure1-architecture.pdf"
PNG_PATH = FIGURES / "figure1-architecture.png"


SPEC = {
    "schema_version": 1,
    "kind": "architecture",
    "canvas": {"width": 1600, "height": 900},
    "style": {
        "font_family": "Arial, DejaVu Sans, sans-serif",
        "background": "#FFFFFF",
        "arrow": "#222222",
    },
    "groups": [
        {"id": "g1", "label": "INPUT + FROZEN GCN", "x": 30, "y": 105, "width": 260, "height": 525, "fill": "#F7F7F7", "stroke": "#B8B8B8"},
        {"id": "g2", "label": "LOW-RANK TRANSPORT", "x": 330, "y": 105, "width": 270, "height": 525, "fill": "#F3F7FC", "stroke": "#AFC4DF"},
        {"id": "g3", "label": "OUTPUT-SENSITIVE RESIDUALS", "x": 640, "y": 105, "width": 280, "height": 525, "fill": "#F7F2FA", "stroke": "#C8B4D6"},
        {"id": "g4", "label": "EXACT-COST CONVERSION", "x": 960, "y": 105, "width": 300, "height": 525, "fill": "#FCF5EC", "stroke": "#DCC1A3"},
        {"id": "g5", "label": "EVALUATION", "x": 1300, "y": 105, "width": 270, "height": 525, "fill": "#F0F8F6", "stroke": "#A8CECA"},
    ],
    "nodes": [
        {"id": "graph", "label": ["Graph G = (V, E)", "Node features X"], "x": 65, "y": 155, "width": 190, "height": 78, "fill": "#ECEFF1", "stroke": "#6B7280", "font_size": 19},
        {"id": "message", "label": ["Normalized message", "M = A_hat X"], "x": 65, "y": 295, "width": 190, "height": 82, "fill": "#ECEFF1", "stroke": "#6B7280", "font_size": 18},
        {"id": "frozen", "label": ["Frozen two-layer GCN", "hidden width 16", "seeds 0 / 1 / 2"], "x": 65, "y": 455, "width": 190, "height": 105, "fill": "#E8EEF5", "stroke": "#5B7897", "font_size": 17},
        {"id": "svd", "label": ["SVD rank-128 transport", "M ≈ M_128"], "x": 365, "y": 155, "width": 200, "height": 92, "fill": "#DCEAF7", "stroke": "#6F96BF", "font_size": 18},
        {"id": "basis", "label": ["Operator-aligned basis", "M_128"], "x": 365, "y": 325, "width": 200, "height": 72, "fill": "#E8F1FB", "stroke": "#7899BD", "font_size": 18},
        {"id": "residual", "label": ["Residual", "R = M - M_128"], "x": 365, "y": 475, "width": 200, "height": 82, "fill": "#EFE8F5", "stroke": "#9A7DB2", "font_size": 18},
        {"id": "jacobian", "label": ["Magnitude-weighted score", "s_i = r_i² ||dz / dr_i||²", "score residual candidates"], "x": 675, "y": 155, "width": 210, "height": 118, "fill": "#EDE3F4", "stroke": "#9A78B5", "font_size": 17},
        {"id": "topb", "label": ["Select top-B coefficients", "explicit indices + values", "2% residual budget"], "x": 675, "y": 405, "width": 210, "height": 118, "fill": "#F1E8F6", "stroke": "#A486BC", "font_size": 17},
        {"id": "merge", "label": ["Serialized transport", "basis + sparse residual", "records"], "x": 995, "y": 155, "width": 230, "height": 112, "fill": "#F8E9D7", "stroke": "#C79565", "font_size": 18},
        {"id": "ledger", "label": ["Exact padded serialized-bit ledger", "matched total padded", "serialized-bit budget"], "x": 995, "y": 335, "width": 230, "height": 112, "fill": "#FCEEDF", "stroke": "#C99B70", "font_size": 17},
        {"id": "rate", "label": ["Rate-coded frozen conversion", "T = 2 and T = 4"], "x": 995, "y": 515, "width": 230, "height": 82, "fill": "#DFF1EE", "stroke": "#6FAAA4", "font_size": 18},
        {"id": "logits", "label": ["Converted logits z_s"], "x": 1335, "y": 155, "width": 200, "height": 70, "fill": "#F6D9BF", "stroke": "#C77B3A", "font_size": 19},
        {"id": "logit_mse", "label": ["Split-specific", "logit MSE"], "x": 1335, "y": 285, "width": 200, "height": 72, "fill": "#F9E6D7", "stroke": "#C98C5E", "font_size": 18},
        {"id": "hidden_mse", "label": ["Hidden-state MSE"], "x": 1335, "y": 405, "width": 200, "height": 64, "fill": "#F9E6D7", "stroke": "#C98C5E", "font_size": 18},
        {"id": "task", "label": ["T = 2 / 4 accuracy", "teacher agreement"], "x": 1335, "y": 515, "width": 200, "height": 82, "fill": "#F9E6D7", "stroke": "#C98C5E", "font_size": 18},
    ],
    "edges": [
        {"id": "e1", "from": "graph", "to": "message", "points": [[160, 233], [160, 295]]},
        {"id": "e2", "from": "message", "to": "frozen", "points": [[160, 377], [160, 455]]},
        {"id": "e3", "from": "frozen", "to": "svd", "points": [[255, 505], [315, 505], [315, 201], [365, 201]]},
        {"id": "e4", "from": "svd", "to": "basis", "points": [[465, 247], [465, 325]]},
        {"id": "e5", "from": "svd", "to": "residual", "points": [[520, 247], [600, 247], [600, 516], [565, 516]]},
        {"id": "e6", "from": "residual", "to": "jacobian", "points": [[565, 516], [620, 516], [620, 214], [675, 214]], "label": "R"},
        {"id": "e7", "from": "frozen", "to": "jacobian", "points": [[160, 560], [160, 610], [650, 610], [650, 273], [675, 273]], "label": "frozen logits z", "style": "dashed"},
        {"id": "e8", "from": "jacobian", "to": "topb", "points": [[780, 273], [780, 405]]},
        {"id": "e9", "from": "basis", "to": "merge", "points": [[565, 361], [925, 361], [925, 211], [995, 211]]},
        {"id": "e10", "from": "topb", "to": "merge", "points": [[885, 464], [950, 464], [950, 270], [995, 270]]},
        {"id": "e11", "from": "merge", "to": "ledger", "points": [[1110, 267], [1110, 335]]},
        {"id": "e12", "from": "ledger", "to": "rate", "points": [[1110, 447], [1110, 515]]},
        {"id": "e13", "from": "rate", "to": "logits", "points": [[1225, 556], [1280, 556], [1280, 190], [1335, 190]]},
        {"id": "e14", "from": "logits", "to": "logit_mse", "points": [[1435, 225], [1435, 285]]},
        {"id": "e15", "from": "logits", "to": "hidden_mse", "points": [[1480, 225], [1510, 225], [1510, 437], [1535, 437]]},
        {"id": "e16", "from": "logits", "to": "task", "points": [[1505, 225], [1570, 225], [1570, 556], [1535, 556]]},
    ],
    "annotations": [
        {
            "id": "diagnostic",
            "label": ["Evidence scope: validation-grid sensitivity and held-out confirmation after validation exposure"],
            "x": 55,
            "y": 680,
            "width": 1490,
            "height": 68,
            "fill": "#FDECEC",
            "stroke": "#B64342",
            "style": "dashed",
            "font_size": 18,
        }
    ],
    "legend": [
        {"label": "Inputs / frozen model", "color": "#ECEFF1"},
        {"label": "Low-rank transport", "color": "#DCEAF7"},
        {"label": "Output-sensitive selection", "color": "#EDE3F4"},
        {"label": "Exact-cost serialization", "color": "#FCEEDF"},
        {"label": "Rate-coded conversion", "color": "#DFF1EE"},
        {"label": "Evaluation", "color": "#F6D9BF"},
    ],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def text_block(lines: list[str], cx: float, cy: float, font_size: int, color: str = "#222222") -> str:
    line_height = font_size + 5
    start_y = cy - ((len(lines) - 1) * line_height) / 2 + font_size * 0.34
    spans = []
    for index, line in enumerate(lines):
        spans.append(
            f'<tspan x="{cx:.1f}" y="{start_y + index * line_height:.1f}">{esc(line)}</tspan>'
        )
    return (
        f'<text text-anchor="middle" dominant-baseline="middle" font-family="Arial, DejaVu Sans, sans-serif" '
        f'font-size="{font_size}" fill="{color}">{"".join(spans)}</text>'
    )


def node_center(node: dict) -> tuple[float, float]:
    return node["x"] + node["width"] / 2, node["y"] + node["height"] / 2


def render_svg(spec: dict) -> str:
    canvas = spec["canvas"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas["width"]}" height="{canvas["height"]}" viewBox="0 0 {canvas["width"]} {canvas["height"]}">',
        '<defs>',
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8.5" refY="3.5" orient="auto" markerUnits="strokeWidth">',
        '<path d="M0,0 L0,7 L9,3.5 z" fill="#222222"/>',
        '</marker>',
        '</defs>',
        f'<rect x="0" y="0" width="{canvas["width"]}" height="{canvas["height"]}" fill="#FFFFFF"/>',
    ]

    for group in spec["groups"]:
        parts.append(
            f'<rect x="{group["x"]}" y="{group["y"]}" width="{group["width"]}" height="{group["height"]}" rx="18" '
            f'fill="{group["fill"]}" stroke="{group["stroke"]}" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{group["x"] + group["width"] / 2:.1f}" y="{group["y"] + 34:.1f}" text-anchor="middle" '
            f'font-family="Arial, DejaVu Sans, sans-serif" font-size="17" font-weight="700" fill="#30343B">'
            f'{esc(group["label"])}</text>'
        )

    for edge in spec["edges"]:
        points = " ".join(f"{x:.1f},{y:.1f}" for x, y in edge["points"])
        dash = ' stroke-dasharray="8 6"' if edge.get("style") == "dashed" else ""
        parts.append(
            f'<polyline points="{points}" fill="none" stroke="{spec["style"]["arrow"]}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"{dash}/>'
        )
        if edge.get("label"):
            lx, ly = edge["points"][len(edge["points"]) // 2]
            parts.append(
                f'<rect x="{lx - 45}" y="{ly - 13}" width="90" height="24" rx="7" fill="#FFFFFF" opacity="0.92"/>'
                f'<text x="{lx}" y="{ly + 4}" text-anchor="middle" font-family="Arial, DejaVu Sans, sans-serif" '
                f'font-size="13" fill="#444444">{esc(edge["label"])}</text>'
            )

    for node in spec["nodes"]:
        cx, cy = node_center(node)
        parts.append(
            f'<rect x="{node["x"]}" y="{node["y"]}" width="{node["width"]}" height="{node["height"]}" rx="14" '
            f'fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="1.7"/>'
        )
        parts.append(text_block(node["label"], cx, cy, node["font_size"]))

    for annotation in spec["annotations"]:
        dash = ' stroke-dasharray="10 7"' if annotation.get("style") == "dashed" else ""
        parts.append(
            f'<rect x="{annotation["x"]}" y="{annotation["y"]}" width="{annotation["width"]}" height="{annotation["height"]}" rx="14" '
            f'fill="{annotation["fill"]}" stroke="{annotation["stroke"]}" stroke-width="1.8"{dash}/>'
        )
        parts.append(
            text_block(
                annotation["label"],
                annotation["x"] + annotation["width"] / 2,
                annotation["y"] + annotation["height"] / 2,
                annotation["font_size"],
                "#7A2E2E",
            )
        )

    legend_y = 810
    legend_x = 115
    for item in spec["legend"]:
        parts.append(
            f'<rect x="{legend_x}" y="{legend_y - 13}" width="26" height="22" rx="5" fill="{item["color"]}" stroke="#666666" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{legend_x + 35}" y="{legend_y + 4}" font-family="Arial, DejaVu Sans, sans-serif" '
            f'font-size="15" fill="#333333">{esc(item["label"])}</text>'
        )
        legend_x += 245

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def validate_spec(spec: dict) -> None:
    canvas = spec["canvas"]
    node_ids = [node["id"] for node in spec["nodes"]]
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("duplicate node id")
    known = set(node_ids)
    for edge in spec["edges"]:
        if edge["from"] not in known or edge["to"] not in known:
            raise ValueError(f'unknown edge endpoint: {edge["id"]}')
    for node in spec["nodes"]:
        if node["x"] < 0 or node["y"] < 0:
            raise ValueError(f'negative node position: {node["id"]}')
        if node["x"] + node["width"] > canvas["width"] or node["y"] + node["height"] > canvas["height"]:
            raise ValueError(f'node outside canvas: {node["id"]}')
    for index, first in enumerate(spec["nodes"]):
        for second in spec["nodes"][index + 1 :]:
            overlap = not (
                first["x"] + first["width"] <= second["x"]
                or second["x"] + second["width"] <= first["x"]
                or first["y"] + first["height"] <= second["y"]
                or second["y"] + second["height"] <= first["y"]
            )
            if overlap:
                raise ValueError(f'node overlap: {first["id"]}, {second["id"]}')


def main() -> int:
    validate_spec(SPEC)
    SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(json.dumps(SPEC, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SVG_PATH.write_text(render_svg(SPEC), encoding="utf-8")
    cairosvg.svg2pdf(url=str(SVG_PATH), write_to=str(PDF_PATH), output_width=1600, output_height=900)
    cairosvg.svg2png(url=str(SVG_PATH), write_to=str(PNG_PATH), output_width=3200, output_height=1800)

    artifacts = []
    for path in (SPEC_PATH, SVG_PATH, PDF_PATH, PNG_PATH):
        artifacts.append({"path": str(path.relative_to(RUN_ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size})
    manifest = {
        "schema_version": 1,
        "generator": "research/make_figure1_svg.py",
        "method": "deterministic FigureSpec-style SVG rendered locally after user-authorized self-draw fallback",
        "artifacts": artifacts,
    }
    (FIGURES / "figure1-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "passed", "artifacts": artifacts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
