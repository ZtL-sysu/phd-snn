import json,time,sys
from pathlib import Path
import torch
import torch.nn.functional as F

run = Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-121033-dynamic-vig-structure')
sys.path.insert(0,str(run/'src')); sys.path.insert(0,str(run))
from structure_conversion import load_images
from train_teacher import SmallViGTeacher
from v2_message_calibration import teacher_state, graph_message, forward_with_codes

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
scales=[5.0,9.0,15.0]; offsets=[0.0,0.05,0.1]

def encode_pc(values, scale, offset):
    centered=(values+offset).clamp(-1,1)
    q=torch.round(((centered+1)/2)*scale)/scale
    return 2*q-1-offset

def objective(kind, model, feat, codes):
    if kind=='feature':
        return float(((feat-codes)**2).mean())
    if kind=='message':
        return float(((graph_message(model,feat)-graph_message(model,codes))**2).mean())
    if kind=='logit':
        lt,_=forward_with_codes(model,feat,feat)
        lc,_=forward_with_codes(model,feat,codes)
        return float(((lt-lc)**2).mean())
    raise ValueError(kind)

def calibrate(model, cal_feat, kind, sweeps=2):
    hidden=cal_feat.size(-1)
    scale=torch.full((hidden,),9.0,device=device)
    offset=torch.zeros(hidden,device=device)
    history=[]
    for sweep in range(sweeps):
        for ch in range(hidden):
            best=None
            for sc in scales:
                for off in offsets:
                    ts=scale.clone(); to=offset.clone(); ts[ch]=sc; to[ch]=off
                    codes=encode_pc(cal_feat,ts,to)
                    val=objective(kind,model,cal_feat,codes)
                    if best is None or val<best[0]: best=(val,sc,off)
            scale[ch]=best[1]; offset[ch]=best[2]
        history.append(objective(kind,model,cal_feat,encode_pc(cal_feat,scale,offset)))
    return scale,offset,history

def evaluate_seed(seed, train_images, test_images, test_labels):
    state=torch.load(run/f'teacher_seed{seed}.pt',map_location=device,weights_only=False)
    model=SmallViGTeacher().to(device); model.load_state_dict(state['state_dict']); model.eval()
    cal_feat=teacher_state(model,train_images[:512].to(device))
    out={}
    imgs=test_images[:2000].to(device); targets=test_labels[:2000].to(device)
    tf=teacher_state(model,imgs)
    tlog,_=forward_with_codes(model,imgs,tf)
    teacher_acc=float((tlog.argmax(1)==targets).float().mean())
    for kind in ('feature','message','logit'):
        st=time.time(); scale,offset,hist=calibrate(model,cal_feat,kind)
        codes=encode_pc(tf,scale,offset)
        logits,msg=forward_with_codes(model,imgs,codes)
        out[kind]={
            'accuracy':float((logits.argmax(1)==targets).float().mean()),
            'message_mse':float(((graph_message(model,tf)-msg)**2).mean()),
            'feature_mse':float(((tf-codes)**2).mean()),
            'logit_mse':float(((tlog-logits)**2).mean()),
            'events':int((codes!=0).sum()),
            'sweep_objectives':hist,
            'cal_seconds':time.time()-st,
            'scale_head':scale[:8].tolist(),'offset_head':offset[:8].tolist(),
        }
    out['seed']=seed; out['teacher_accuracy']=teacher_acc
    return out

def main():
    started=time.time()
    train_images,_=load_images(run/'data/fashion_mnist_train.parquet')
    test_images,test_labels=load_images(run/'data/fashion_mnist_test.parquet')
    rows=[evaluate_seed(seed,train_images,test_images,test_labels) for seed in (41,)]
    report={'dataset':'Fashion-MNIST','purpose':'per-channel calibration objective competition','cal_samples':512,'test_limit':2000,'grid':{'scales':scales,'offsets':offsets,'sweeps':2},'wall_seconds':time.time()-started,'rows':rows}
    p=Path(r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-130000-failure-audit\perchannel-calibration-seed41.json')
    p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
