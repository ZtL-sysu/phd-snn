# Ten smoke-validated GNN→SNN research ideas

All numbers below are reproduced in `smoke/results/`. “Strong smoke” is relative to the frozen gate recorded before each outcome; it is not a paper result.

| # | Idea | Mechanism | Real smoke evidence | Frozen gate result |
|---:|---|---|---|---|
| 1 | DYN-C01 causal temporal residual events | encode state changes rather than repeated absolute graph states | 728 DAVIS clips, 8 frames; exact prefix, 20.52% nonzero-event reduction | PASS |
| 2 | EQ-C02 rotation-equivariant radial events | quantize magnitude, preserve coordinate direction | 3,982 MaleCNS coordinates; rotation error 0, quantization error 7.08% | PASS |
| 3 | PERM-C03 permutation-certified graph pooling | require event pooling to commute with node permutation | 2,277-node Chameleon graph; max error 0 | PASS |
| 4 | SIGN-C04 excitatory/inhibitory graph-message banks | exact signed split prevents heterophilic evidence erasure | Squirrel 5,201×16 messages; 34.73% negative; exact reconstruction | PASS |
| 5 | LR-C05 operator-aligned low-rank message events | send low-rank graph-message subspace plus residual events | Chameleon messages; rank128, 8.99× dimension reduction, 45.57% residual error | PASS |
| 6 | EDGE-C06 quantized biological edge messages | replace float edge transport with 6-bit event alphabet | 385,946 FlyWire weights; 5.33× storage reduction, 18.92% error | PASS |
| 7 | CERT-C11 affine conversion certificates | bound quantization error through adjacency and weights | Chameleon/Squirrel; 100% coverage, bound/RMS 7.82×/7.42× | PASS |
| 8 | POS-C13 hop-position event encoding | quantized multi-hop positional messages with permutation certificate | 512-node Chameleon subset; 2.19% error, 5.33× storage reduction | PASS |
| 9 | DLY-C14 delay-aligned causal edge residuals | schedule residual events by propagation delay | 728 DAVIS clips; exact prefix and 20.52% event reduction | PASS |
| 10 | READ-C18 top-two margin-pair readout | emit only leader and strongest competitor with signed margin | six graphs/33,592 validation nodes; predictions preserved 100%, median slot reduction 63.33% | PASS |

## Why these are ten ideas rather than one idea renamed

- Temporal state coding and delay scheduling test different mechanisms: representation sparsity versus causal propagation timing.
- Rotation and permutation certificates target different group actions and operator bugs.
- Signed message banks, low-rank messages, edge-weight alphabets and pair readout act at message, channel, edge and output levels respectively.
- The certificate idea produces a correctness envelope; the compression ideas produce work/storage reductions.

## Honest scope

The mechanism screens establish implementation feasibility and a strong smoke signal. Before `f-research-v1`, each selected idea still needs a fresh end-to-end frozen-teacher comparison, strongest baseline adaptation, multiple seeds, actual graph task metrics, full operation/memory accounting and final novelty sweep. DYN/DLY use real temporal clips but not yet a dynamic-edge GNN; that application bridge is the largest risk.
