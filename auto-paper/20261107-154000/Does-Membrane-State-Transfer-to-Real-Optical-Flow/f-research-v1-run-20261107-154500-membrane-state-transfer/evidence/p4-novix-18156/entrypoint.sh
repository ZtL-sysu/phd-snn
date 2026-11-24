#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/novix/workspace/project"
export PYTHONPATH="${PROJECT}/src:${PYTHONPATH:-}"
export PYTHONHASHSEED=0
mkdir -p "${PROJECT}/logs" "${PROJECT}/evidence"

printf '%s\n' '=== P4 reproducible full-batch entrypoint ==='
printf 'Project: %s\n' "${PROJECT}"
printf '%s\n' '=== Hardware ==='
nvidia-smi
python3 - <<'PY'
import torch
print({
    "torch": torch.__version__,
    "cuda_available": torch.cuda.is_available(),
    "torch_cuda": torch.version.cuda,
    "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
})
if not torch.cuda.is_available():
    raise SystemExit("CUDA is required for this full P4 batch")
PY

printf '%s\n' '=== Dependencies (default environment; no virtualenv) ==='
if python3 - <<'PY'
import cv2, numpy, pandas, requests, scipy, sklearn
actual = {
    "numpy": numpy.__version__,
    "scipy": scipy.__version__,
    "scikit-learn": sklearn.__version__,
    "pandas": pandas.__version__,
    "opencv": cv2.__version__,
    "requests": requests.__version__,
}
print(actual)
required = {"numpy": "2.4.6", "scipy": "1.17.1", "scikit-learn": "1.9.1", "pandas": "3.1.1", "opencv": "5.0.0"}
raise SystemExit(0 if all(actual[key] == value for key, value in required.items()) else 1)
PY
then
  printf '%s\n' 'Pinned scientific dependencies already available; installation skipped.'
else
  python3 -m pip install -r "${PROJECT}/requirements.txt"
fi

for STAGE in A B C; do
  printf '=== Running/resuming stage %s ===\n' "${STAGE}"
  python3 "${PROJECT}/experiment.py" --stage "${STAGE}" 2>&1 | tee -a "${PROJECT}/logs/entrypoint_stage_${STAGE}.log"
done

printf '%s\n' '=== Independent raw-artifact validation ==='
python3 "${PROJECT}/validate_results.py" 2>&1 | tee -a "${PROJECT}/logs/validation.log"
printf '%s\n' '=== P4 batch complete ==='
