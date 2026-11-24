import json, torch
from pathlib import Path
run=Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-121033-dynamic-vig-structure')
out={'candidate':'A_layerwise_thresholded_delta_inference','stage':'stage-1-sparsity-census','status':'blocked','reason':'No directly public NTU RGB+D 60 skeleton sequence dataset was found inside the run root or imported material set. Stage-1 gate requires frame-wise sequences; static Fashion-MNIST/MNIST cannot proxy temporal sparsity.','gate':'At least 80 percent layer activations inactive at a threshold that changes accuracy by at most 0.5 pp.','next':'Search only directly public/license-clear or locally available streaming graph datasets; otherwise screen other material-backed directions.','preserved_negative':True}
(run/'candidate-a-stage1-blocked.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
