# Rejected or inconclusive candidates

These failures are preserved to prevent goalpost movement.

| Candidate | Evidence | Outcome |
|---|---|---|
| C09-v1 prefix uncertainty upgrades | `rejections/C09-v1.md`, `smoke/results/C09-v1.json` | reject: MNIST accuracy −0.39 pp; selected all T4; mean T=4 |
| C10-v1 operator scalar calibration | `rejections/C10-v1.md`, `smoke/results/C10-v1.json` | reject: +0.53/+0.23 pp, below +1 pp minimum; unstable spikes |
| LAW-C07 topology scalar law | `smoke/results/LAW-C07-v1.json` | reject: no statistic met same-sign |ρ|≥0.6 at T2/T4 |
| CONF-C09 conformal selection | `smoke/results/CONF-C09-v1.json` | reject: CIFAR coverage 9.18% <30% |
| ZERO-C10 zero-message pruning | `smoke/results/ZERO-C10-v1.json` | reject: zero-node fraction 0%/0.058% |
| EDGEPRUNE-C12 top-edge pruning | `smoke/results/more-mechanisms.json` | reject: Chameleon message error 23.26% >15% |
| TRANS-C15 uniform centroid events | `smoke/results/TRANS-C15-v1.json` | reject: relative error 16.04% >10% |
| NM-C16 strict non-monotonic law | `smoke/results/NM-C16-v1.json` | reject: 0/3 seeds met mixed-sign gate |
| HOM-C17 grouped homophily gain | partial command output; seed6 checkpoint absent | inconclusive: 2 available seeds passed, frozen 3-seed gate incomplete |

No rejected scalar threshold, loss, codebook, or all-upgrade variant was recycled as a new accepted idea.
