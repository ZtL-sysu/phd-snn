# P3A · Baseline Evidence Review

`review_execution: same-agent-role-pass` (independent historical reviews preserved in `../ccfa-startup-packet/` and `audits/ccfa-pre-experiment-review.md`).

- Strongest recent baselines were adapted to the SAME superpixel-graph backbone, teacher, T/theta/split: naive rate, QCFS, FTBC, TPP, Parallel Conversion; directly-trained spiking GCN as technique-family control; DCGS/AdaFire/PASCAL/CS-QCFS/One-Spike SNN as literature context.
- Four independent holdouts (20 distinct seeds) show both energy conventions >=5x without exception.
- Fatal risks: none. Known limitation: teacher absolute accuracy is modest (34.02% MNIST, 27.27% CIFAR10 in E17) and the paper must not present it as accuracy SOTA.
- The v3 precision statement (measured conversion loss plus explicit accuracy-energy Pareto frontier) is evidence-grounded and user-authorized.
- P3A pass; P4 authorized.
