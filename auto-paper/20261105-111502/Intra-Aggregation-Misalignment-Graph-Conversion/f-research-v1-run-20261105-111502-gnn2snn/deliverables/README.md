# Delivery package — local preparation

## Manuscript
- `paper.pdf` — compiled English manuscript (10 pages incl. references and appendix; 0 errors,
  0 undefined citations/references).
- `paper.tex`, `refs.bib` — source and verified bibliography (55 entries, 46 from 2023-2026).
- Source tree: `../tex/` (sections, scripted tables, generated figures, `numbers.tex`).

## Terminal skill review
`../ccfa-review-reports/ccfa-skill-review-terminal-full.md` — `ccf-paper-reviewer` full mode:
**9 (strong accept) under the Evaluations & Datasets rubric; 8 (accept) under a main ML track.**
Both scores are recorded; the difference is venue fit under the official E&D reviewer guidelines,
not a change in evidence. No self-assigned score is used.

## Headline evidence (all from this run)
- G0 reproduction: Cora/PubMed T=8 within 0.003 pp.
- S1 mechanism separation: TPP transplant 4.24 pp behind at T=4; inter-layer permutation
  +0.54 pp; intra-aggregation phase perturbation -11.88 pp; branch A.
- Theorem G1 (a)-(d) with appendix proof, symbol table and failure depth.
- Exact bound inversion **falsified** (linear predictor -88.9% saving); two versioned repairs
  fitted on calibration graphs only; replacement feasibility band screens 3/3 held-out graphs,
  saves 50.0% timesteps on evaluable graphs, shuffled-kappa control 1.00 -> 0.50.
  The strict pre-registered strong criterion is not met and is reported as a result.
- 8 Table-1 method rows x 5 timesteps x 3 graphs x 7 seeds; three plug-in aggregation hosts.

## Reproducibility
`../registry/results.csv` is the single source for all tables and figures; `../runs/` and
`../results/` hold logs, metrics, per-run content-addressed hashes and all negative results;
`../protocols/protocol.md` is frozen; `../contracts/` holds the execution contract, the
pre-registration (v1/v3/v4/v6) and the correction loop. `../paper/claims.md` is the claim ledger.

## Status
`workflow_complete = true` (26 research stages + 12 guidance stages accepted in order).
`submission_ready = false` by construction: seven author/portal facts are pending in
`../contracts/delivery-readiness.snapshot.json`, and the 2027 venue CFP is unpublished.
No submission, upload, publication, commit or push was performed.
