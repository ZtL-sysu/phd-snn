# Idea red-team review

- Review execution: same-agent-role-pass. An independent agent review is still required at f-research-v1 P1B; this startup review is not a substitute.
- Readiness score: 4/10 at startup. The mechanism is specific, but direct public teacher weights, licensing, and a baseline-calibrated strong target are unresolved.
- Development potential: 8/10 if the dynamic-neighbor/max failure is observable on a reproducible teacher; 3/10 if teacher structure is robust under low-step encoding.
- Confidence: 3/5 that a strong method paper can be built from the current evidence; 5/5 that a decisive diagnostic can be run first.
- Fatal risks: (1) no official CIFAR-10 ViG teacher weights; (2) DCGS and Efficient-AI-Backbones show no detected license; (3) baseline-only conversion may already make structure flips rare; (4) local RTX 3060 may not train an ImageNet-scale ViG teacher; (5) signed max is unsupported by current DCGS code.
- Score-change conditions: readiness rises to at least 6/10 when a public licensed teacher or a locally reproducible teacher exists, a runnable matched baseline is implemented, and a pilot measures material neighbor/max disagreement. It falls below 3/10 if the pilot shows <1% structure disagreement and <1 pp accuracy gap at T=4.
- Recommended decision: `pivot-with-rescue-route`. Begin with a small, licensed, locally reproducible dynamic-graph teacher on a directly public dataset; freeze the failure-census diagnostic as the rescue route. Do not start a full ImageNet conversion campaign.
- Preserved concern-to-action ledger: public data -> verify CIFAR-10 card and license; code license -> reimplement operators rather than copy; teacher availability -> local trainable small ViG-style model on CIFAR-10; baseline strength -> implement rate coding, signed multi-threshold coding, and teacher-structure oracle; strong target -> derive from pilot baseline gaps, never from a desired headline number.
