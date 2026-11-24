import json, math, re, hashlib, random
from pathlib import Path
import numpy as np
import torch

root=Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-130000-failure-audit\new-direction-e3-radial')
sdf=root/'data/qm9.sdf'
# Parse first N SDF records: atom coordinates, atomic numbers, bonds.
def parse_sdf(path, limit=20000):
    text=path.read_text(encoding='utf-8',errors='ignore')
    blocks=text.split('$$$$')
    out=[]
    for block in blocks:
        lines=block.splitlines()
        if len(lines)<5: continue
        counts_idx=next((i for i,line in enumerate(lines[:8]) if 'V2000' in line),None)
        counts_line=lines[counts_idx] if counts_idx is not None else None
        if counts_line is None: continue
        counts=counts_line
        if len(counts)<6 or not counts[0:3].strip() or not counts[3:6].strip(): continue
        natoms=int(counts[0:3]); nbonds=int(counts[3:6])
        coords=[]; symbols=[]
        for line in lines[counts_idx+1:counts_idx+1+natoms]:
            parts=line.split()
            if len(parts)<4: break
            coords.append([float(parts[0]),float(parts[1]),float(parts[2])])
            symbols.append(parts[3])
        edges=[]
        start=counts_idx+1+natoms
        for line in lines[start:start+nbonds]:
            parts=line.split()
            if len(parts)>=2:
                edges.append((int(parts[0])-1,int(parts[1])-1))
        if coords and len(coords)==natoms:
            out.append((np.array(coords,dtype=np.float32),symbols,edges))
        if len(out)>=limit: break
    return out

mols=parse_sdf(sdf,20000)
# Elements in first N; keep those with >=300 samples for a classification probe.
from collections import Counter
counts=Counter(m[1][0] for m in mols if m[1])
keep=[e for e,c in counts.items() if c>=300]
print('molecules',len(mols),'root element counts',counts.most_common(10),'keep',keep)
if not keep: raise SystemExit('no class with >=300')

def radial_event(x, levels=8, scale_mode='max'):
    norms=np.linalg.norm(x,axis=1,keepdims=True)
    directions=x/np.maximum(norms,1e-12)
    scale=norms.max() if scale_mode=='max' else np.quantile(norms,0.995)
    step=scale/(levels-1)
    indices=np.floor(norms/step+0.5).clip(0,levels-1)
    qn=indices*step
    return qn*directions

def component_event(x, levels=8):
    lo=x.min(axis=0,keepdims=True); hi=x.max(axis=0,keepdims=True)
    step=np.maximum((hi-lo)/(levels-1),1e-12)
    return np.floor((x-lo)/step+0.5).clip(0,levels-1)*step+lo

def random_rot(n,seed):
    rng=np.random.default_rng(seed)
    q=rng.normal(size=(n,4)); q/=np.linalg.norm(q,axis=1,keepdims=True)
    w,x,y,z=q[:,0],q[:,1],q[:,2],q[:,3]
    R=np.empty((n,3,3))
    R[:,0,0]=1-2*(y*y+z*z); R[:,0,1]=2*(x*y-z*w); R[:,0,2]=2*(x*z+y*w)
    R[:,1,0]=2*(x*y+z*w); R[:,1,1]=1-2*(x*x+z*z); R[:,1,2]=2*(y*z-x*w)
    R[:,2,0]=2*(x*z-y*w); R[:,2,1]=2*(y*z+x*w); R[:,2,2]=1-2*(x*x+y*y)
    return R

def pad_features(mols, transform):
    feats=[]; labels=[]
    for coords,symbols,edges in mols:
        if symbols[0] not in keep: continue
        f=transform(coords)
        d=f.shape[1]
        if d>30: continue
        pad=np.zeros((30,d),dtype=np.float32); pad[:len(f)]=f
        feats.append(pad); labels.append(keep.index(symbols[0]))
    return np.stack(feats).reshape(len(feats),-1),np.array(labels,dtype=np.int64)

def split_labels(labels, seed):
    rng=np.random.RandomState(seed); idx=rng.permutation(len(labels))
    n=len(labels); tr=idx[:int(.7*n)]; va=idx[int(.7*n):int(.85*n)]; te=idx[int(.85*n):]
    return tr,va,te

def linear_probe(X,y,seed):
    torch.manual_seed(seed)
    Xt=torch.tensor(X,dtype=torch.float32,device='cuda' if torch.cuda.is_available() else 'cpu')
    yt=torch.tensor(y,dtype=torch.long,device=Xt.device)
    tr,va,te=split_labels(y,seed)
    idx={n:torch.tensor(v,device=Xt.device) for n,v in [('tr',tr),('va',va),('te',te)]}
    model=torch.nn.Sequential(torch.nn.LayerNorm(Xt.shape[1]).to(Xt.device),torch.nn.Linear(Xt.shape[1],64).to(Xt.device),torch.nn.ReLU(),torch.nn.Linear(64,len(set(y.tolist()))).to(Xt.device))
    opt=torch.optim.AdamW(model.parameters(),lr=1e-2,weight_decay=1e-4)
    best=-1; best_state=None
    for epoch in range(150):
        model.train(); logits=model(Xt[idx['tr']]); loss=torch.nn.functional.cross_entropy(logits,yt[idx['tr']])
        opt.zero_grad(); loss.backward(); opt.step()
        model.eval()
        with torch.no_grad(): acc=float((model(Xt[idx['va']]).argmax(1)==yt[idx['va']]).float().mean())
        if acc>best: best=acc; best_state={k:v.detach().clone() for k,v in model.state_dict().items()}
    model.load_state_dict(best_state)
    with torch.no_grad(): test=float((model(Xt[idx['te']]).argmax(1)==yt[idx['te']]).float().mean())
    return {'val':best,'test':test}

rows=[]
for seed in range(5):
    raw,labels=pad_features(mols,lambda x:x)
    comp,_=pad_features(mols,lambda x:component_event(x,8))
    rad,_=pad_features(mols,lambda x:radial_event(x,8))
    rows.append({'seed':seed,'raw':linear_probe(raw,labels,seed),'component8':linear_probe(comp,labels,seed),'radial8':linear_probe(rad,labels,seed)})
# O(3) equivariance max error under random rotations for all molecules with <=12 atoms.
R=random_rot(len(mols),0)
raw_err=rad_err=0.0
for i,(coords,_,_) in enumerate(mols):
    if coords.shape[0]>30: continue
    rot=coords @ R[i].T
    raw_err=max(raw_err,float(np.max(np.abs(rot-coords @ R[i].T))))
    a=radial_event(coords,8); b=radial_event(rot,8)
    rad_err=max(rad_err,float(np.max(np.abs(b-a @ R[i].T))))
report={'dataset':'QM9 CC0 mirror, first 20000 SDF records','classes':keep,'n_per_class':{e:counts[e] for e in keep},'rows':rows,'equivariance_raw_max_error':raw_err,'equivariance_radial_max_error':rad_err,'gate':'GO if radial8 beats component8 on >=4/5 seeds, mean gain >=2pp, and equivariance error <=1e-6; else NO-GO'}
(root/'new-direction-gate.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
