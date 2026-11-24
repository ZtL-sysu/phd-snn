from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = RUN_ROOT / "results" / "p12-openalex-probe.json"

QUERIES = [
    "Semi-Supervised Classification with Graph Convolutional Networks",
    "Inductive Representation Learning on Large Graphs",
    "Graph Attention Networks Velickovic",
    "Graph Isomorphism Network Xu",
    "Simple and Deep Graph Convolutional Networks",
    "DeepGCNs Can GCNs Go as Deep as CNNs",
    "MixHop Higher-Order Graph Convolutional Architectures",
    "Degree-Quant Quantization-Aware Training for Graph Neural Networks",
    "VQ-GNN Vector Quantized Graph Neural Network",
    "Quartz Randomized Quantization for Communication-Efficient Graph Neural Networks",
    "QGTC Accelerating Quantized Graph Neural Networks via GPU Tensor Core",
    "SpikingJelly End-to-End Spiking Deep Learning Framework",
    "A Survey on Spiking Neural Networks",
    "Deep Spiking Neural Networks A Survey",
    "Spiking Graph Neural Networks survey",
    "ANN to SNN conversion survey",
    "Optimal ANN-SNN Conversion High Accuracy Ultra Low Latency",
    "Taming Spikes Training and Inference for Spiking Neural Networks",
    "Low-Rank Graph Neural Networks",
    "Graph compression low rank approximation graph neural networks",
    "Sensitivity-Driven Regularization for Quantization-Aware Training of Graph Neural Networks",
    "Post-Training Quantization for Graph Neural Networks",
    "Spiking Graph Convolutional Network for Semi-Supervised Node Classification",
    "SpikeNet Graph Spiking Neural Network Multi-View Semi-Supervised Learning",
    "VQ-GNN: A Vector Quantized Graph Neural Network",
    "Quartz: Randomized Quantization for Communication-Efficient Graph Neural Networks",
]


def search(query: str) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search": query,
            "per-page": 5,
            "select": "id,doi,title,display_name,publication_year,publication_date,authorships,primary_location,ids,type",
        }
    )
    request = urllib.request.Request(
        "https://api.openalex.org/works?" + params,
        headers={"User-Agent": "phd-snn-citation-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8")).get("results", [])


def main() -> int:
    records = []
    for query in QUERIES:
        try:
            records.append({"query": query, "items": search(query)})
        except Exception as exc:
            records.append({"query": query, "error": str(exc), "items": []})
        time.sleep(0.2)
    OUTPUT.write_text(json.dumps({"schema_version": 1, "queries": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"queries": len(records), "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
