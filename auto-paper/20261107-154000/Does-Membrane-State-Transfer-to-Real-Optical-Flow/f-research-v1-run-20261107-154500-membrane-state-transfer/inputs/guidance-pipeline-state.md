# Guidance pipeline state (readable view; pipeline-state.json is structural authority)

Round 001, primary idea C1, 2026-11-07, target CVPR 2027, remote compute opted in (novix exp-4090).

| Stage | Status | Evidence / reason |
|---|---|---|
| CCFA-startup | passed | `ccfa-startup-packet/` 7 files plus `feasibility-contract.json`; `startup-decision.md = proceed` |
| G0 recent literature and baselines | passed | `literature-baseline-matrix.md`; 21 first-hand entries in project `literature/closest-work.md` |
| G1 public dataset access | passed | `dataset-access-log.md`; Zenodo, DAVIS-2017 and MPI-Sintel direct links probed with HEAD plus 16-byte Range, ZIP magic verified |
| G2 task and evaluation validity | passed | fixed 70/30 split, accuracy, ceiling, 5 seeds, bootstrap CI, BH, preregistered direction |
| G3 theoretical fit | passed | `theoretical-feasibility-audit.md`; membrane state integrates across frames, stateless cannot |
| G4 novelty and non-duplication | passed | `novelty-feasibility-report.md`; transferability verdict axis, distinct from topology-advantage and null-model claims |
| G5 hardware and runtime | passed | `hardware-profile.md`; local RTX 3060 plus remotely measured RTX 4090 46,068 MiB |
| G6 strong baseline and ablation | passed | stateless, A=0, ceiling, degree-preserving null, sign-shuffled control, one-factor ablations |
| G7 strong-result plausibility | passed | `strong-result-feasibility-contract.md`, calibrated on local +0.2817 with CI [0.2033,0.3617] |
| G8 story strength | passed | `story-strength-audit.md`; transferability verdict has community value under either sign, with documented novelty/framing risk and explicit rescue path |
| validation | passed | `validate_guidance.py --strict --packet` produced `Guidance structure is valid.`; `pipeline_state.py --before CCFA-startup` PASS |
| handoff | passed | f-research-v1 P0 run root created inside this guidance directory |

G8 is passed with a documented risk, not silently: the independent review recorded a borderline
strict-idea-review guardrail hit (novelty is external validation rather than a new mechanism). That risk
is mitigated by the go-conditions written into the guidance (fixed derivation protocol, ceiling check
first, same-protocol domain comparison, and a venue-valued transferability verdict). It is tracked in
`story-strength-audit.md` and remains a P5A/P9 review concern rather than being hidden.
