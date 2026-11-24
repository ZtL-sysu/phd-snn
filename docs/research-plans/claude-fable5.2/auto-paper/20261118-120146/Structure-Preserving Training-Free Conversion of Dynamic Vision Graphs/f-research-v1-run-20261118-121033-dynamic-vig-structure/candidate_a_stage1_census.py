import json,torch,numpy as np,pandas as pd,re
from pathlib import Path
run=Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-121033-dynamic-vig-structure')
df=pd.read_csv(run/'data/ntu60_points.csv')
num=r'-?\d+(?:\.\d+)?'
pair=re.compile(r'\[\s*('+num+r')\s+('+num+r')\s*\]')
seqs=[]
for _,row in df.iterrows():
 s=str(row['keypoint'])
 pairs=[(float(a),float(b)) for a,b in pair.findall(s)]
 tf=int(row['total_frames']); v=int(len(pairs)/tf)
 if v<=0 or len(pairs)%tf: continue
 arr=np.array(pairs,dtype=np.float32).reshape(tf,v,2)
 seqs.append((str(row['frame_dir']),tf,str(row['label']),arr))
 if len(seqs)>=64: break
results=[]
for eps in (0.5,1.0,2.0,5.0,10.0):
 total=active=changed=0
 for name,tf,label,a in seqs:
  x=torch.from_numpy(a); d=torch.zeros((x.size(0),x.size(1)),dtype=torch.float32); d[1:]=torch.norm(x[1:]-x[:-1],dim=2); d[0]=d[1] if x.size(0)>1 else 0
  total+=d.numel(); active+=int((d>eps).sum()); changed+=int((d>eps).any(dim=1).sum())
 results.append({'eps_pixels':eps,'delta_density':active/total,'inactive_fraction':1-active/total,'mean_changed_frames_per_sequence':changed/len(seqs)})
out={'dataset':'NTU RGB+D 60 skeleton point CSV (MIT HF mirror)','sequences_sampled':len(seqs),'frames_sampled':sum(s[1] for s in seqs),'sample_shape':list(seqs[0][3].shape) if seqs else None,'result':results,'gate':'pass if inactive_fraction>=0.80 at an operating point with task loss<=0.5pp; task loss not yet measured','status':'stage-1-census-only','parser_note':'The CSV stores NumPy-style arrays truncated by ellipsis; this census parses all explicit [x y] pairs and reshapes by total_frames. It is descriptive only and not suitable for model training.'}
(run/'candidate-a-stage1-census.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
