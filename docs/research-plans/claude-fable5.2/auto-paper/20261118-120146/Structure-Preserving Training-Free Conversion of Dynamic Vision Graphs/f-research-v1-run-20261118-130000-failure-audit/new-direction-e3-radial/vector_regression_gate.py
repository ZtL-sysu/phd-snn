import json, math
from pathlib import Path
import numpy as np
import torch

root=Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-130000-failure-audit\new-direction-e3-radial')
sdf=root/'data/qm9.sdf'

def parse_sdf(path, limit=20000):
    blocks=path.read_text(encoding='utf-8',errors='ignore').split('$$$$')
    out=[]
    for block in blocks:
        lines=block.splitlines()
        if len(lines)<5: continue
        counts_idx=next((i for i,line in enumerate(lines[:8]) if 'V2000' in line),None)
        if counts_idx is None: continue
        counts=lines[counts_idx]
        if len(counts)<6 or not counts[0:3].strip(): continue
        natoms=int(counts[0:3])
        coords=[]; symbols=[]
        for line in lines[counts_idx+1:counts_idx+1+natoms]:
            parts=line.split()
            if len(parts)<4: break
            coords.append([float(parts[0]),float(parts[1]),float(parts[2])]); symbols.append(parts[3])
        if len(coords)!=natoms or natoms<2: continue
        header=lines[0].split('\t')
        if len(header)<5:
            fields=lines[0].split()
        else: fields=header
        if len(fields)<5: continue
        try: mu=float(fields[4])
        except ValueError: continue
        out.append((np.array(coords,dtype=np.float32),mu))
        if len(out)>=limit: break
    return out

mols=parse_sdf(sdf,20000)
MAX=18

def pack(transform):
    X=[]; Y=[]
    for coords,mu in mols:
        if len(coords)>MAX: continue
        coords=coords.astype(np.float64)
        f=transform(coords)
        f=np.asarray(f,dtype=np.float32)
        if len(f)<2 or f.ndim!=2 or f.shape[1]!=3: continue
        pad=np.zeros((MAX,3),dtype=np.float32); mask=np.zeros((MAX,1),dtype=np.float32)
        pad[:len(f)]=f; mask[:len(f)]=1
        X.append(np.concatenate([pad,mask],axis=1)); Y.append(mu)
    X=torch.tensor(np.stack(X)); Y=torch.tensor(Y,dtype=torch.float32)
    good=(X[:,:,3:4].sum(dim=1).squeeze(-1)>1) & (Y==Y)
    print('packed',len(X),'good',int(good.sum()),'zero',int((~good).sum()))
    return X[good],Y[good]

def radial_event(x,levels=8):
    norms=np.linalg.norm(x,axis=1,keepdims=True); directions=x/np.maximum(norms,1e-12)
    scale=max(float(norms.max()),1e-12); step=scale/(levels-1)
    idx=np.floor(norms/step+0.5).clip(0,levels-1)
    return idx*step*directions

def component_event(x,levels=8):
    lo=x.min(axis=0,keepdims=True); hi=x.max(axis=0,keepdims=True)
    step=np.maximum((hi-lo)/(levels-1),1e-12)
    return np.floor((x-lo)/step+0.5).clip(0,levels-1)*step+lo

def split(n,seed):
    rng=np.random.RandomState(seed); idx=rng.permutation(n)
    return torch.tensor(idx[:int(.7*n)]),torch.tensor(idx[int(.7*n):int(.85*n)]),torch.tensor(idx[int(.85*n):])

class EqNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp=torch.nn.Sequential(torch.nn.Linear(4,32),torch.nn.SiLU(),torch.nn.Linear(32,32),torch.nn.SiLU(),torch.nn.Linear(32,1))
    def forward(self,x):
        coords=x[:,:,:3]; mask=x[:,:,3:4]
        count=mask.sum(1).clamp_min(1)
        center=(coords*mask).sum(1,keepdim=True)/count.unsqueeze(1)
        rel=(coords-center)*mask
        r=torch.norm(rel,dim=2,keepdim=True)
        d=torch.cdist(rel,rel)
        d=d.masked_fill(mask.squeeze(-1).unsqueeze(1)==0,1e3)
        d=d.masked_fill(mask.squeeze(-1).unsqueeze(2)==0,1e3)
        d=d+1e3*torch.eye(MAX,device=x.device).unsqueeze(0)
        dmin=d.min(dim=2,keepdim=True).values
        feat=torch.cat([r,dmin,torch.ones_like(r)],dim=-1)
        weights=self.mlp(feat).squeeze(-1)*mask.squeeze(-1)
        return (weights.unsqueeze(-1)*rel).sum(1), rel, weights

def eval_model(model,x,y,idx):
    model.eval()
    with torch.no_grad():
        pred,_,_=model(x[idx])
        mae=float((pred-y[idx]).abs().mean())
        rmse=float(torch.sqrt(((pred-y[idx])**2).mean()))
    return mae,rmse

def rot_errors(model,x):
    model.eval()
    rng=np.random.default_rng(123)
    q=rng.normal(size=(len(x),4)); q/=np.linalg.norm(q,axis=1,keepdims=True)
    w,xx,yy,z=q[:,0],q[:,1],q[:,2],q[:,3]
    R=np.empty((len(x),3,3))
    R[:,0,0]=1-2*(yy*yy+zz*zz); R[:,0,1]=2*(xx*yy-zz*w); R[:,0,2]=2*(xx*zz+yy*w)
    R[:,1,0]=2*(xx*yy+zz*w); R[:,1,1]=1-2*(xx*xx+zz*zz); R[:,1,2]=2*(yy*zz-xx*w)
    R[:,2,0]=2*(xx*zz-yy*w); R[:,2,1]=2*(yy*zz+xx*w); R[:,2,2]=1-2*(xx*xx+yy*yy)
    R=torch.tensor(R,dtype=torch.float32)
    with torch.no_grad():
        pred,rel,_=model(x)
        xr=x.clone(); xr[:,:,:3]=torch.bmm(x[:,:,:3],R.transpose(1,2))
        predr,_,_=model(xr)
        err=torch.norm(predr-torch.bmm(pred.unsqueeze(1),R.transpose(1,2)).squeeze(1),dim=1)
    return float(err.max()),float(err.mean())

rows=[]
for seed in range(3):
    torch.manual_seed(seed)
    Xraw,Y=pack(lambda x:x)
    Xrad,_=pack(lambda x:radial_event(x,8))
    Xcomp,_=pack(lambda x:component_event(x,8))
    tr,va,te=split(len(Y),seed)
    model=EqNet()
    opt=torch.optim.AdamW(model.parameters(),lr=3e-3,weight_decay=1e-5)
    best=1e9; best_state=None
    for epoch in range(80):
        model.train(); pred,_,_=model(Xraw[tr]); loss=((pred-Y[tr])**2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        model.eval()
        with torch.no_grad(): p,_,_=model(Xraw[va]); val=float(((p-Y[va])**2).mean())
        if val<best: best=val; best_state={k:v.detach().clone() for k,v in model.state_dict().items()}
    model.load_state_dict(best_state)
    raw_mae,raw_rmse=eval_model(model,Xraw,Y,te)
    rad_mae,rad_rmse=eval_model(model,Xrad,Y,te)
    comp_mae,comp_rmse=eval_model(model,Xcomp,Y,te)
    raw_rot=rot_errors(model,Xraw[te[:500]])
    rad_rot=rot_errors(model,Xrad[te[:500]])
    comp_rot=rot_errors(model,Xcomp[te[:500]])
    rows.append({'seed':seed,'raw':{'mae':raw_mae,'rmse':raw_rmse,'rot_max':raw_rot[0],'rot_mean':raw_rot[1]},'radial8':{'mae':rad_mae,'rmse':rad_rmse,'rot_max':rad_rot[0],'rot_mean':rad_rot[1]},'component8':{'mae':comp_mae,'rmse':comp_rmse,'rot_max':comp_rot[0],'rot_mean':comp_rot[1]}})

report={'dataset':'QM9 CC0 mirror, dipole moment vector regression, first 20000 SDF records','samples':len(Y),'max_atoms':MAX,'rows':rows,'gate':'PASS if radial8 MAE <= raw MAE*1.10, radial8 rot_mean <=1e-5, and component8 rot_mean >=10x radial8; else FAIL'}
(root/'vector-regression-gate.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
