#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/home/novix/workspace/project"
cd "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/evidence/raw" "$PROJECT_DIR/evidence/features" "$PROJECT_DIR/evidence/bootstrap"
exec > >(tee -a "$PROJECT_DIR/logs/entrypoint.log") 2>&1

printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "bash /home/novix/workspace/project/entrypoint.sh $*" >> "$PROJECT_DIR/command_history.log"

printf '\n=== [1/6] Hardware report ===\n'
nvidia-smi
python3 "$PROJECT_DIR/experiment.py" --hardware-only

printf '\n=== [2/6] Install exact Python dependencies in default environment ===\n'
python3 -m pip install -r "$PROJECT_DIR/requirements.txt"

printf '\n=== [3/6] Compile source ===\n'
python3 -m py_compile "$PROJECT_DIR/experiment.py" \
  "$PROJECT_DIR/validate_results.py" "$PROJECT_DIR/test_pipeline.py" \
  "$PROJECT_DIR"/src/fresearch/*.py

printf '\n=== [4/6] Run protocol unit/integration tests ===\n'
python3 "$PROJECT_DIR/test_pipeline.py"

printf '\n=== [5/6] Run complete experiment ===\n'
# Optional caller flags such as --reuse-features are forwarded.  With no flags,
# feature encodings are recomputed; source downloads/caches are still validated.
# Exit 2 is the intentional fail-fast code for a measured design-invalid state;
# validation must still run so that this terminal state is independently audited.
set +e
python3 "$PROJECT_DIR/experiment.py" --run-full "$@"
experiment_rc=$?
set -e

printf '\n=== [6/6] Independently validate artifacts and numerical consistency ===\n'
set +e
python3 "$PROJECT_DIR/validate_results.py" --project-dir "$PROJECT_DIR"
validation_rc=$?
set -e

if (( validation_rc != 0 )); then
  printf '\nArtifact validation failed (experiment_rc=%d, validation_rc=%d).\n' \
    "$experiment_rc" "$validation_rc"
  exit 1
fi
if (( experiment_rc == 2 )); then
  printf '\nPipeline reproduced a validated design_invalid terminal state; no method superiority claim is allowed.\n'
  exit 2
fi
if (( experiment_rc != 0 )); then
  printf '\nExperiment failed with runtime exit code %d despite artifact validation.\n' "$experiment_rc"
  exit "$experiment_rc"
fi
printf '\nAll pipeline commands completed and validated. See project/result.json and project/validation.json.\n'
