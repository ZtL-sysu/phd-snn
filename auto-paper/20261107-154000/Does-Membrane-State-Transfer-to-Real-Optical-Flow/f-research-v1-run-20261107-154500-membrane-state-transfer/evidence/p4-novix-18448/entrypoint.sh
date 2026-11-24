#!/usr/bin/env bash
set -euo pipefail

PROJECT=/home/novix/workspace/project
export PYTHONHASHSEED=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export OPENBLAS_NUM_THREADS=8

cd "$PROJECT"
mkdir -p "$PROJECT/logs" "$PROJECT/evidence/raw" "$PROJECT/data"
printf '%s\n' "python3 $PROJECT/experiment.py --run" >> "$PROJECT/evidence/command_history.log"

# The experiment owns all data preparation, registered computation, and the
# final atomic artifact write.  Keep stdout/stderr on the invoking process so
# no project file remains open or changes after the final MANIFEST write.
python3 "$PROJECT/experiment.py" --run

# Required immediate, measured post-persistence self-check.  Do not place any
# file-writing command after this boundary.
ls -l "$PROJECT/result.json" "$PROJECT/config.json"
python3 -c "import hashlib,json,os; paths=['$PROJECT/result.json','$PROJECT/config.json']; [print(f'{p}: exists={os.path.exists(p)} bytes={os.path.getsize(p)} sha256={hashlib.sha256(open(p,\"rb\").read()).hexdigest()} sha256_16={hashlib.sha256(open(p,\"rb\").read()).hexdigest()[:16]}') for p in paths]; r=json.load(open(paths[0])); print('MEASURED_SUMMARY',json.dumps({'design_valid':r['design_valid'],'migration_verdict':r['migration_verdict'],'transfer_claim_made':r['transfer_claim_made'],'transfer_outcome_verdict':r['transfer_outcome_verdict'],'states':{k:v['decidability_state'] for k,v in r['decidability_states'].items()},'current_ceilings':{k:v['current_ceiling'] for k,v in r['decidability_states'].items()},'oracle_upper_bounds':{k:v['oracle_upper_bound'] for k,v in r['decidability_states'].items()},'synthetic_ceiling':r['synthetic']['ceiling']['mean'],'selected_hop':r['connectome']['selected_hop'],'selected_kc_count':r['connectome']['selected_kc_count'],'spectral_radius':r['connectome']['graph_statistics']['spectral_radius'],'c1_guidance':r['c1_guidance']['verdict'],'expected_signal_met':r['expected_signal_met'],'raw_npz':r['artifact_counts']['raw_npz'],'wall_seconds':r['runtime']['wall_seconds']},ensure_ascii=False,sort_keys=True))"
python3 -B "$PROJECT/validate_results.py" --project "$PROJECT" --summary
