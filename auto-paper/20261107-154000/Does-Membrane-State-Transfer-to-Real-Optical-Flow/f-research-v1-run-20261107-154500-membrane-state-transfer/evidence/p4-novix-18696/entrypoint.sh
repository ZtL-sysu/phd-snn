#!/usr/bin/env bash
# End-to-end deterministic reproduction entrypoint for P4/C1 attempt #8.
set -euo pipefail
export PYTHONHASHSEED=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-4}"

PROJECT_ROOT="/home/novix/workspace/project"
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"
cd "$PROJECT_ROOT"

exec > >(tee -a "$LOG_DIR/entrypoint.log") 2>&1
printf '[entrypoint] started_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '[entrypoint] project_root=%s\n' "$PROJECT_ROOT"

printf '[entrypoint] phase=official_data_integrity\n'
python3 "$PROJECT_ROOT/download_data.py" --workers 8 --verify-crc

printf '[entrypoint] phase=unit_tests\n'
python3 "$PROJECT_ROOT/test_pipeline.py"

printf '[entrypoint] phase=full_experiment\n'
python3 "$PROJECT_ROOT/experiment.py" --run-all --force-rerun

printf '[entrypoint] phase=prefinal_validation\n'
python3 "$PROJECT_ROOT/validate_results.py" --mode prefinal

printf '[entrypoint] phase=finalization\n'
python3 "$PROJECT_ROOT/finalize_artifacts.py"

printf '[entrypoint] phase=final_validation\n'
python3 "$PROJECT_ROOT/validate_results.py" --mode final

printf '[entrypoint] completed_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
