from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = RUN_ROOT / "results" / "p12-reference-probe.json"

TITLES = [
    "Semi-Supervised Classification with Graph Convolutional Networks",
    "Inductive Representation Learning on Large Graphs",
    "Graph Attention Networks",
    "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning",
    "DeepGCNs: Can GCNs Go as Deep as CNNs?",
    "MixHop: Higher-Order Graph Convolutional Architectures via Sparsified Neighborhood Mixing",
    "Simple and Deep Graph Convolutional Networks",
    "A Comprehensive Survey on Graph Neural Networks",
    "Degree-Quant: Quantization-Aware Training for Graph Neural Networks",
    "VQ-GNN: A universal framework to scale up graph neural networks using vector quantization",
    "Spiking Graph Convolutional Network for Semi-Supervised Node Classification",
    "SpikeNet: A Graph Spiking Neural Network for Multi-View Semi-Supervised Learning",
    "A2Q: Aggregation-Aware Quantization for Graph Neural Networks",
    "AdaQP: Adaptive Quantization with Guaranteed Performance for Graph Neural Networks",
    "QGTC: Accelerating Quantized Graph Neural Networks via GPU Tensor Core",
    "Fast SNN: Fast Spiking Neural Network with High Performance",
    "SEENN: Self-Distilled Early Exit Neural Networks",
    "SpikeZIP-TF: Conversion is All You Need for Transformer-based Models",
    "TTFSFormer: Temporal Transformer",
    "Optimal ANN-SNN Conversion with Group Neurons",
    "LaSNN: Layer-wise ANN-to-SNN Distillation for Effective and Efficient Training in Deep Spiking Neural Networks",
    "Bridging the Gap between ANNs and SNNs by Calibrating Offset Spikes",
    "When Bio-Inspired Computing meets Deep Learning: Low-Latency, Accurate, & Energy-Efficient Spiking Neural Networks from Artificial Neural Networks",
    "SpikingJelly: An End-to-End Spiking Deep Learning Framework",
    "A Survey on Spiking Neural Networks",
    "Spiking Neural Networks: A Survey on Hardware Implementation",
    "Deep Spiking Neural Networks: A Survey",
    "Advancing Spiking Neural Networks: From Algorithms to Hardware",
    "Inference-Scale Complexity in ANN-SNN Conversion for High-Performance and Low-Power Applications",
    "Optimal ANN-SNN Conversion for High-Accuracy and Ultra-Low-Latency",
    "Taming Spikes: Training and Inference for Spiking Neural Networks",
    "Spiking Graph Neural Networks: A Survey",
    "Efficient Graph Neural Networks with Spiking Neural Networks",
    "Graph Neural Networks with Spiking Neurons",
    "Sensitivity-Driven Regularization for Quantization-Aware Training of Graph Neural Networks",
    "Post-Training Quantization for Graph Neural Networks",
    "A Comprehensive Survey of Quantization in Graph Neural Networks",
    "Low-Rank Graph Neural Networks",
    "Compressing Graph Neural Networks via Low-Rank Approximation",
    "Graph Compression via Low-Rank Matrix Approximation",
]

ARXIV_IDS = [
    "1609.02907",
    "1706.02216",
    "1710.10903",
    "1810.00826",
    "1904.01332",
    "1905.00067",
    "2007.02133",
    "2008.05000",
    "2110.14363",
    "2208.10364",
    "2303.04347",
    "2305.19306",
    "2403.08786",
    "2302.00193",
    "2305.19868",
    "2403.15480",
    "2509.21342",
    "2502.21193",
    "2304.9101",
    "2302.10685",
    "2402.19061",
]


def get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "phd-snn-citation-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_xml(url: str) -> ET.Element:
    request = urllib.request.Request(url, headers={"User-Agent": "phd-snn-citation-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return ET.fromstring(response.read())


def crossref_probe(title: str) -> dict:
    query = urllib.parse.urlencode({"query.title": title, "rows": 3, "select": "DOI,title,author,published,container-title,type,URL"})
    data = get_json("https://api.crossref.org/works?" + query)
    return {"query": title, "items": data.get("message", {}).get("items", [])}


def arxiv_probe(ids: list[str]) -> list[dict]:
    url = "https://export.arxiv.org/api/query?id_list=" + ",".join(ids) + "&max_results=" + str(len(ids))
    root = get_xml(url)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    records = []
    for entry in root.findall("a:entry", ns):
        records.append(
            {
                "id": (entry.findtext("a:id", "", ns) or "").strip(),
                "title": " ".join((entry.findtext("a:title", "", ns) or "").split()),
                "authors": [author.findtext("a:name", "", ns) for author in entry.findall("a:author", ns)],
                "published": (entry.findtext("a:published", "", ns) or "").strip(),
                "updated": (entry.findtext("a:updated", "", ns) or "").strip(),
                "summary": " ".join((entry.findtext("a:summary", "", ns) or "").split())[:800],
            }
        )
    return records


def main() -> int:
    crossref = []
    for index, title in enumerate(TITLES, start=1):
        try:
            crossref.append(crossref_probe(title))
        except Exception as exc:
            crossref.append({"query": title, "error": str(exc), "items": []})
        time.sleep(0.2)
    try:
        arxiv = arxiv_probe(ARXIV_IDS)
    except Exception as exc:
        arxiv = [{"error": str(exc)}]
    payload = {
        "schema_version": 1,
        "crossref_queries": crossref,
        "arxiv_records": arxiv,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"crossref_queries": len(crossref), "arxiv_records": len(arxiv), "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
