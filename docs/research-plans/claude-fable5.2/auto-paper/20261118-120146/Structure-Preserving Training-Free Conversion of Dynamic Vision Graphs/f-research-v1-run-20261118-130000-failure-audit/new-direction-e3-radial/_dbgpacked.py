import sys
from pathlib import Path
sys.path.insert(0,r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-130000-failure-audit\new-direction-e3-radial')
import importlib.util
spec=importlib.util.spec_from_file_location('vrg',r'C:\code\phd-snn\docs\research-plans\claude-fable5.2\auto-paper\20261118-120146\Structure-Preserving Training-Free Conversion of Dynamic Vision Graphs\f-research-v1-run-20261118-130000-failure-audit\new-direction-e3-radial\vector_regression_gate.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print('n mols',len(m.mols))
print('bad',sum(1 for c,y in m.mols if len(c)<2))
X,Y=m.pack(lambda x:x)
print('X',X.shape,'Y',Y.shape,'zero rows',int((X[:,:,3:4].sum(1)==0).sum()))
