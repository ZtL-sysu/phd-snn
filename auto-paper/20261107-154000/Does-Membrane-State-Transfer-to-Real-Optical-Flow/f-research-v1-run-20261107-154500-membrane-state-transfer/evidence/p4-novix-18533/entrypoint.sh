#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/novix/workspace/project"
LOG_DIR="$PROJECT/logs"
mkdir -p "$LOG_DIR" "$PROJECT/evidence/raw" "$PROJECT/data" "$PROJECT/checkpoints"

run_logged() {
  local label="$1"
  shift
  local timestamp
  timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s command=%q' "$timestamp" "$1" >> "$PROJECT/evidence/command_history.log"
  for arg in "${@:2}"; do printf ' %q' "$arg" >> "$PROJECT/evidence/command_history.log"; done
  printf '\n' >> "$PROJECT/evidence/command_history.log"
  echo "[$timestamp] START $label"
  "$@"
  local code=$?
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] END $label exit=$code"
  return "$code"
}

cd "$PROJECT"

run_logged "hardware report" nvidia-smi
run_logged "torch CUDA report" python3 -c 'import json,torch; print(json.dumps({"torch":torch.__version__,"torch_cuda":torch.version.cuda,"cuda_available":torch.cuda.is_available(),"gpu":torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,"memory_bytes":torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None},indent=2))'

if ! python3 -c 'import numpy, scipy, sklearn, pandas, requests, PIL, torch; print("required imports available")'; then
  run_logged "install required packages" python3 -m pip install scipy scikit-learn pandas requests Pillow
fi
run_logged "dependency versions" python3 -c 'import importlib.metadata as m; names=["numpy","scipy","scikit-learn","pandas","requests","Pillow","torch"]; print("\n".join(f"{x}=={m.version(x)}" for x in names))'

# A delivered project may contain final JSON but omit multi-gigabyte generated data.
# In that case start a genuinely fresh, self-contained reproduction ledger rather
# than incorrectly skipping stages because the delivered result says complete.
needs_fresh_reset="$(python3 - <<'PY'
import json
from pathlib import Path
p = Path('/home/novix/workspace/project')
result = p / 'result.json'
status = None
if result.exists():
    try:
        status = json.loads(result.read_text(encoding='utf-8')).get('status')
    except Exception:
        status = 'INVALID'
required = [
    p / 'data' / 'connections_biological.csv.gz',
    p / 'data' / 'DAVIS-2017-trainval-480p.zip',
    p / 'data' / 'MPI-Sintel-complete.zip',
    p / 'data' / 'cache' / 'connectome_round012.npz',
    p / 'data' / 'cache' / 'current_DAVIS_baseline.npz',
    p / 'data' / 'cache' / 'current_SINTEL_baseline.npz',
]
print('yes' if status == 'COMPLETE' and not all(x.is_file() and x.stat().st_size > 0 for x in required) else 'no')
PY
)"
if [[ "$needs_fresh_reset" == "yes" ]]; then
  echo "Delivered final ledger found without generated data; resetting restartable artifacts."
  rm -f "$PROJECT"/evidence/checkpoint_*.json "$PROJECT"/evidence/raw/*.npz "$PROJECT"/checkpoints/*.json
  run_logged "fresh reproduction phase zero" python3 "$PROJECT/experiment.py" --phase0
elif [[ ! -s "$PROJECT/result.json" ]]; then
  run_logged "phase zero persistence" python3 "$PROJECT/experiment.py" --phase0
fi
if [[ ! -s "$PROJECT/config_preregistered.json" || ! -s "$PROJECT/config_preregistered.sha256" ]]; then
  run_logged "freeze preregistration" python3 "$PROJECT/preregister.py"
fi
run_logged "verify preregistration lock" python3 -c 'from pathlib import Path; import hashlib; p=Path("/home/novix/workspace/project/config_preregistered.json"); e=Path("/home/novix/workspace/project/config_preregistered.sha256").read_text().split()[0]; a=hashlib.sha256(p.read_bytes()).hexdigest(); print({"actual":a,"expected":e,"match":a==e}); assert a==e'

run_logged "download and byte-verify public data" python3 "$PROJECT/download_data.py" --workers 3
run_logged "pipeline unit tests" python3 "$PROJECT/test_pipeline.py"
run_logged "full restartable experiment" python3 "$PROJECT/experiment.py" --run-all
# Do not append command_history after final atomic persistence: validation is
# read-only so MANIFEST hashes and the "manifest written last" contract remain true.
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] START final result validation (read-only)"
python3 "$PROJECT/validate_results.py"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] END final result validation exit=0"

echo "Reproduction complete. Main outputs:"
ls -l "$PROJECT/result.json" "$PROJECT/config.json"
python3 -c 'import hashlib,os; from pathlib import Path; [print(f"{p}: bytes={os.path.getsize(p)} sha256={hashlib.sha256(Path(p).read_bytes()).hexdigest()}") for p in ["/home/novix/workspace/project/result.json","/home/novix/workspace/project/config.json"]]'
