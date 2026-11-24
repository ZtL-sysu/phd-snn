from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = RUN_ROOT / "results" / "p12-semantic-probe.json"

QUERIES = [
    "Semi-Supervised Classification with Graph Convolutional Networks",
    "Inductive Representation Learning on Large Graphs",
    "Graph Attention Networks Velickovic",
    "Graph Isomorphism Network",
    "Simple and Deep Graph Convolutional Networks GCNII",
    "DeepGCNs Can GCNs Go as Deep as CNNs",
    "MixHop Higher-Order Graph Convolutional Architectures",
    "Degree-Quant Quantization-Aware Training for Graph Neural Networks",
    "VQ-GNN Vector Quantized Graph Neural Network",
    "Quartz Randomized Quantization Communication-Efficient Graph Neural Networks",
    "QGTC Accelerating Quantized Graph Neural Networks via GPU Tensor Core",
    "SpikingJelly End-to-End Spiking Deep Learning Framework",
    "A Survey on Spiking Neural Networks algorithms and hardware",
    "Deep Spiking Neural Networks A Survey",
    "Spiking Graph Neural Networks survey",
    "ANN to SNN conversion survey",
    "Optimal ANN-SNN Conversion High Accuracy Ultra Low Latency",
    "Taming Spikes Training and Inference for Spiking Neural Networks",
    "Low-Rank Graph Neural Networks",
    "Graph Neural Network compression low rank approximation",
    "Sensitivity Driven Regularization Quantization Aware Training Graph Neural Networks",
    "Post Training Quantization Graph Neural Networks",
    "Spiking Graph Convolutional Network Semi-Supervised Node Classification",
    "SpikeNet Graph Spiking Neural Network Multi-View Semi-Supervised Learning",
]


def search(query: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "limit": 5,
            "fields": "title,authors,year,venue,externalIds,url,abstract,publicationTypes",
        }
    )
    request = urllib.request.Request(
        "https://api.semanticscholar.org/graph/v1/paper/search?" + params,
        headers={"User-Agent": "phd-snn-citation-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    records = []
    for query in QUERIES:
        try:
            data = search(query)
            records.append({"query": query, "items": data.get("data", [])})
        except Exception as exc:
            records.append({"query": query, "error": str(exc), "items": []})
        time.sleep(1.1)
    OUTPUT.write_text(json.dumps({"schema_version": 1, "queries": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"queries": len(records), "output": str(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
