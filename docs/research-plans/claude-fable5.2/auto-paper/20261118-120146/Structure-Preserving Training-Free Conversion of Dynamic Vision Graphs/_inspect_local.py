import pathlib, torch
data=pathlib.Path(r'C:\code\phd-snn\auto-paper\20261110-152407\Operator-Agnostic-ANN-to-SNN-Conversion-for-Vision-and-Graphs\f-research-v1-run-20261110-172308-superpixel-graph-vision\data\pyg_bench')
for name in ['MNIST/processed/train_data.pt','MNIST/processed/test_data.pt','CIFAR10/processed/train_data.pt']:
    obj=torch.load(data/name,map_location='cpu',weights_only=False)
    sample=obj[0] if isinstance(obj,(list,tuple)) else next(iter(obj.values()))
    print('\n',name,'outer',type(obj).__name__,'len',len(obj),'sample',type(sample).__name__)
    if isinstance(sample,dict):
        print('sample keys',sorted(sample.keys()))
        for k,v in sample.items(): print(' ',k,type(v).__name__,tuple(v.shape) if hasattr(v,'shape') else '')
    elif hasattr(sample,'keys'):
        print('sample keys',sorted(sample.keys()))
        for k in sample.keys: print(' ',k,tuple(getattr(sample,k).shape))
