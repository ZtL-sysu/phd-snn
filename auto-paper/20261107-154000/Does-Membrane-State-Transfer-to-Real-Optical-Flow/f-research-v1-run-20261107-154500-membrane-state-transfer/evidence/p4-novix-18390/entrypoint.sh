#!/usr/bin/env bash
# Reproduce the complete f-research-v1 P4 C1 attempt #4 batch.
# There is intentionally no quick/demo/synthetic fallback.
set -euo pipefail

ROOT=/home/novix/workspace/project
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONHASHSEED=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export CUDA_DEVICE_ORDER=PCI_BUS_ID

mkdir -p "$ROOT/evidence/raw" "$ROOT/logs" "$ROOT/data"
printf '[entrypoint] root=%s\n' "$ROOT"
printf '[entrypoint] python=%s\n' "$(python3 --version 2>&1)"

if ! python3 - <<'PY'
import numpy, scipy, pandas, sklearn, PIL, requests, torch
print({
    "numpy": numpy.__version__, "scipy": scipy.__version__,
    "pandas": pandas.__version__, "sklearn": sklearn.__version__,
    "Pillow": PIL.__version__, "requests": requests.__version__,
    "torch": torch.__version__, "cuda_available": torch.cuda.is_available(),
})
if not torch.cuda.is_available():
    raise SystemExit("CUDA is required for the complete registered batch")
PY
then
  python3 -m pip install -r "$ROOT/requirements.txt"
  python3 - <<'PY'
import torch
if not torch.cuda.is_available():
    raise SystemExit("CUDA remains unavailable after dependency setup")
PY
fi

sha256sum -c "$ROOT/config_preregistered.sha256"

# A failed reproduction must not leave stale final deliverables that appear new.
rm -f "$ROOT/result.json" "$ROOT/config.json" "$ROOT/MANIFEST.txt" \
      "$ROOT/evidence/result_snapshot.json" "$ROOT/evidence/config_snapshot.json" \
      "$ROOT/evidence/result_working.json" "$ROOT/evidence/config_working.json" \
      "$ROOT/evidence/validation.json" "$ROOT/evidence/test_pipeline.log"
rm -f "$ROOT/evidence/raw/"*.npz
for table in main_table.csv gate_operating_point.csv yoked_firing_rate_2x2.csv \
             variance_vs_information.csv readout_state_variables.csv probe_vs_hop.csv \
             variance_trajectory.csv experiment-traceability.csv; do
  rm -f "$ROOT/$table" "$ROOT/evidence/$table"
done

printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 src/download_official_data.py connectome annotations retina davis sintel --workers 4" \
  >> "$ROOT/evidence/command_history.log"
python3 "$ROOT/src/download_official_data.py" connectome annotations retina davis sintel --workers 4

python3 -m py_compile "$ROOT/experiment.py" "$ROOT/validate_results.py" \
  "$ROOT/test_pipeline.py" "$ROOT/src/"*.py

# Build or verify the full graph before isolated forward-pass tests.
printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 -c build_graph_bundle(config, force=False)" \
  >> "$ROOT/evidence/command_history.log"
python3 - <<'PY'
import json
from pathlib import Path
from src.graph_pipeline import build_graph_bundle
root = Path("/home/novix/workspace/project")
config = json.loads((root / "config_preregistered.json").read_text())
graph = build_graph_bundle(config, force=False)
print({
    "edge_count": graph["dense_graph"]["edge_count"],
    "actual_K": graph["actual_K"],
    "resolved_kc_count": graph["resolved_kc_count"],
    "degree_null_exact": graph["degree_null_audit"]["all_required_properties_preserved"],
})
PY

printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 test_pipeline.py (preflight)" >> "$ROOT/evidence/command_history.log"
python3 "$ROOT/test_pipeline.py" 2>&1 | tee "$ROOT/evidence/test_pipeline_preflight.log"

printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 experiment.py --run" >> "$ROOT/evidence/command_history.log"
python3 "$ROOT/experiment.py" --run

printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 test_pipeline.py (post-run)" >> "$ROOT/evidence/command_history.log"
python3 "$ROOT/test_pipeline.py" 2>&1 | tee "$ROOT/evidence/test_pipeline.log"

printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 validate_results.py" >> "$ROOT/evidence/command_history.log"
python3 "$ROOT/validate_results.py"

# Log this command before crossing the final persistence boundary. The finalizer
# writes mains -> snapshots -> MANIFEST, then performs only read-only checks.
printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "python3 src/finalize_outputs.py" >> "$ROOT/evidence/command_history.log"
python3 "$ROOT/src/finalize_outputs.py"
