import json, math, time
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid

audit = Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-130000-failure-audit')
torch.manual_seed(0)
np.random.seed(0)
data = Planetoid(root=str(audit/'data/PyG'), name='Cora')[0]
N = data.num_nodes
edges = data.edge_index.t().cpu().numpy()
rng = np.random.default_rng(0)
perm = rng.permutation(len(edges))
initial_n = int(0.9*len(edges))
initial = edges[perm[:initial_n]]
events = [(int(u), int(v)) for u,v in edges[perm[initial_n:initial_n+2000]] if u!=v]

deg = np.bincount(initial.ravel(), minlength=N).astype(np.float32)
norm = np.power(np.maximum(deg,1.0), -0.5)
src,dst = initial[:,0], initial[:,1]
adj = torch.sparse_coo_tensor(np.vstack([dst,src]), norm[src]*norm[dst], (N,N)).coalesce()

in_dim = data.num_node_features; hidden=64
W1 = torch.randn(in_dim,hidden)*0.1
W2 = torch.randn(hidden,int(data.y.max())+1)*0.1
X = data.x.cpu()

def gcn_forward(adj):
    h=F.relu(torch.sparse.mm(adj, X @ W1))
    return torch.sparse.mm(adj,h) @ W2, h

out0,h0 = gcn_forward(adj)

def add_edge(adj,u,v):
    d_u,d_v=deg[u],deg[v]
    if d_u<=0 or d_v<=0: return adj
    new_deg_u=d_u+1.0; new_deg_v=d_v+1.0
    coords=torch.tensor([[v,u]],dtype=torch.long)
    vals=torch.tensor([1/np.sqrt(new_deg_u*new_deg_v)],dtype=torch.float32)
    existing = adj.coalesce()
    mask=(existing.indices()[0]==v)&(existing.indices()[1]==u)
    if mask.any():
        new_vals=existing.values().clone(); new_vals[mask]=vals[0]
        return torch.sparse_coo_tensor(existing.indices(),new_vals,adj.shape).coalesce()
    idx=torch.cat([existing.indices(),coords],dim=1)
    val=torch.cat([existing.values(),vals])
    return torch.sparse_coo_tensor(idx,val,adj.shape).coalesce()

def full_recompute():
    out,_=gcn_forward(adj); return out

def exact_ripple_like(prob_batch=0.0):
    cur_adj=adj; cur_deg=deg.copy(); cur_h=h0.clone(); cur_out=out0.clone(); propagated=0; repaired=0
    for u,v in events:
        if u==v: continue
        du,dv=cur_deg[u],cur_deg[v]
        new_du=du+1; new_dv=dv+1
        delta = norm[u]*norm[v]*(X[v]@W1)
        if prob_batch==0.0 or np.random.random()<prob_batch:
            cur_h[u] = F.relu(cur_h[u] + delta)
            propagated += 1
            out_delta=torch.sparse.mm(cur_adj,delta.unsqueeze(0).t())@W2
            cur_out += out_delta
        cur_adj=add_edge(cur_adj,u,v); cur_deg[u]=new_du; cur_deg[v]=new_dv
    return cur_out, propagated

def residual_debt(tau, lazy_k=0):
    cur_adj=adj; cur_deg=deg.copy(); cur_h=h0.clone(); cur_out=out0.clone(); debt=torch.zeros_like(cur_h); propagated=0
    for step,(u,v) in enumerate(events):
        if u==v: continue
        du,dv=cur_deg[u],cur_deg[v]
        debt[u] += norm[u]*norm[v]*(X[v]@W1)
        repair = debt[u].norm().item()>tau or (lazy_k>0 and step%lazy_k==0)
        if repair:
            delta=debt[u].clone(); debt[u].zero_()
            cur_h[u]=F.relu(cur_h[u]+delta)
            propagated += 1
        cur_adj=add_edge(cur_adj,u,v); cur_deg[u]=du+1; cur_deg[v]=dv+1
    for node in np.nonzero(debt.norm(dim=1).numpy()>0)[0]:
        cur_h[node]=F.relu(cur_h[node]+debt[node]); propagated+=1
    out=torch.sparse.mm(cur_adj,cur_h)@W2
    return out, propagated

rows=[]; scale=np.linalg.norm(h0,dim=1).mean().item()
full_start=time.time(); full=full_recompute(); full_time=time.time()-full_start
for tau_rel in [1e-4,3e-4,1e-3,3e-3]:
    tau=tau_rel*scale
    for method in ['exact','nodb','debt','lazy']:
        start=time.time()
        if method=='exact': out,prop=exact_ripple_like(1.0)
        elif method=='nodb': out,prop=exact_ripple_like(tau/scale)
        elif method=='debt': out,prop=residual_debt(tau)
        else: out,prop=residual_debt(1e9,lazy_k=50)
        elapsed=time.time()-start
        drift=float((out-full).norm()/full.norm())
        rows.append({'method':method,'tau_rel':tau_rel,'time_sec':elapsed,'drift':drift,'propagated':prop,'speedup_vs_full':full_time/elapsed})
report={'dataset':'Cora PyG static graph with 2000 edge-addition events','nodes':N,'initial_edges':len(initial),'events':len(events),'hidden':hidden,'full_time_sec':full_time,'scale':scale,'rows':rows,'gate':'GO only if >=2x speedup, <=1% drift, and >=50% drift reduction over no-debt/lazy at matched activity; otherwise NO-GO','status':'pilot'}
(audit/'ripple-residual-debt-pilot.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
