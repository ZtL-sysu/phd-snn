# CCFA Full Integrity Audit

## Mode

`full` (claim-support, numeric/unit/aggregation/direction, validation/test provenance, figure-caption agreement, and existing citation placeholders/metadata readiness).

This was a read-only audit. The frozen manuscript was not edited. No literature search was performed and no missing evidence was invented.

## Artifacts Checked

- Frozen manuscript: `writing/p8/paper-data-figures.md`.
- Evidence digest: `writing/p9-evidence-digest.json`.
- Result summaries: `results/confirmation-summary.json`, `results/confirmation-test-v2.json`.
- Validation-grid inputs: `inputs/v2-summary.json`, `inputs/v2-timing.json`.
- Figure source data: `figures/source-data/figure2-main-logit-mse.csv`, `figure3-budget-sensitivity.csv`, `figure4-tradeoff-and-runtime.csv`.
- Figure/table insertion record: `figure-table-insertion-audit.md`.
- Figure captions/contracts/manifests: `figures/captions.md`, `figures/figure-contract.md`, `figures/figure1-manifest.json`, `figures/data-figure-manifest.json`.
- Existing citation context: `writing/verified-reference-context-p7.md`.

The SHA256 values recorded in `p9-evidence-digest.json` match the current `confirmation-summary.json`, `confirmation-test-v2.json`, `v2-summary.json`, `v2-timing.json`, and `ccfa-pre-draft-scientific-review.md`. The three CSV hashes match `data-figure-manifest.json`.

## Claim-Evidence Matrix

| ID / manuscript location | Claim | Status | Evidence and audit result |
|---|---|---|---|
| F1 / Abstract, §4.3, §6 (`paper-data-figures.md:5,78,116`) | Rank-128/2% test logit-MSE reductions are 26.23%, 33.99%, 25.83% on Cora/Chameleon/Squirrel; all nine dataset-seed comparisons improve. | **Supported** | `confirmation-summary.json` gives 26.2324%, 33.9867%, 25.8284%; `figure2-main-logit-mse.csv` gives the underlying three-seed means and sample SDs. Recalculation gives 26.2324%, 33.9867%, 25.8284%, and all 9 proposed-versus-`top_abs` seed comparisons are positive. The comparator is the strongest evaluated matched-budget control, not every method independently. |
| F2 / Abstract, §4.5, §6 (`:5,98,116`) | Task loss is bounded at 1.86 pp three-seed-mean and 2.85 pp seed-level. | **Supported** | `confirmation-summary.json` reports 1.8571886 pp and 2.85 pp; `figure4-tradeoff-and-runtime.csv` reports per-dataset maxima 0.4667, 1.1696, 1.8572 pp. The manuscript correctly calls these bounded observations, not equivalence. |
| F3 / Abstract, §1, §3, §4.2-4.3 (`:5,11,43,78`) | All compared rank-128/2% methods use identical total padded serialized bits within each dataset, while payload lengths/counts may differ. | **Supported with scope precision** | `confirmation-test-v2.json` has one bit total per dataset for all rank-128/2% rows: Cora 21,932,736; Chameleon 25,630,208; Squirrel 43,771,008 Equality is within dataset, not across datasets. |
| F4 / Abstract, §4.5 (`:5,102`) | Paired p95 runtime ratios are 1.020-1.124x across nine dataset-seed pairs; peak CUDA allocation is 218.23 MB. | **Supported** | `v2-timing.json` and `figure4-tradeoff-and-runtime.csv` agree. The condition is rank128/1%, three warmups and seven repeats; this is wall-clock pipeline timing, not energy. |
| F5 / Abstract, §4.1, §5 (`:5,55,112`) | The focal setting/reframing was fixed after validation exposure; the test is held-out confirmation, not preregistered independent replication; no temporal-event, energy, or broad-GNN claim. | **Supported as a limitation/disclosure** | The disclosure is present in `confirmation-summary.json` and the digest. It is a scope statement, not a numerical result. |
| F6 / §1, §4.4 (`:13,86`) | Hidden-state MSE reductions are 16.88%, 12.86%, 10.63% at rank128/2%. | **Supported** | `v2-summary.json` gives 16.8779%, 12.8578%, 10.6297%, rounding exactly to the manuscript values. These are validation-grid sensitivity values, not the held-out headline test. |
| F7 / §1, §4.4 (`:13,88`) | Across 0.5%, 1%, 2% budgets and three graphs, all nine cells favor the selector, with reductions 2.98%-30.40%. | **Supported** | `v2-summary.json` and `figure3-budget-sensitivity.csv` agree: min 2.9781%, max 30.4028%; all nine relative reductions are positive. |
| F8 / §1, §4.4 (`:13,94`) | Reductions versus our A2Q adaptation are 28.93%, 36.19%, 35.24%; versus our One-Spike adaptation are 42.83%, 47.61%, 34.03%. | **Partially supported; provenance defect** | The exact values are reproduced by `figure2-main-logit-mse.csv` (three-seed means). However, `p9-evidence-digest.json` cites `results/confirmation-test-v2.json`, whose top-level `logit_mse` rows aggregate to different percentages (A2Q: 28.51%, 37.28%, 34.64%; One-Spike: 43.01%, 50.15%, 33.01%). The manuscript numbers are therefore supported by the CSV but not reproducible from the evidence path currently recorded for F8 |
| F9 / §1, §4.5 (`:13,100`) | Task superiority was not established; deltas are mixed and the earlier superiority target failed. | **Supported** | `v2-summary.json` records `LR_B_task_gain: false` and mixed positive/negative T2/T4/teacher-agreement gains across the grid. The manuscript appropriately narrows the accepted claim to bounded degradation. |

**Category summary:** supported claims are F1-F7 and F9; partially supported claim is F8; no unsupported or overstated numerical claim was found. The direct-GPT Figure 1 gate is unsupported as a process claim because the evidence records conflict, and bibliography readiness is unresolved rather than a manuscript overstatement.

### Specification Claims

The rank-128 SVD representation, exact residual records, output-Jacobian score, padded-bit ledger, and rate-coded T=2/4 conversion are stated as method definitions. They are consistent with the row schema and figure contract, but the supplied result JSONs do not independently establish the implementation internals. These should remain method/specification claims rather than being presented as experimentally identified causal facts.

## Numeric Consistency Findings

- The headline percentages, hidden-MSE percentages, budget-grid range, task-loss maxima, timing range, and memory value are numerically consistent with their stated rounding and units.
- Metric directions are correct: logit/hidden MSE lower is better; task loss is percentage-point degradation; runtime ratio greater than 1 is overhead.
- `figure2-main-logit-mse.csv` correctly represents three-seed means with sample SD and the plotted y-axis scale is explicit in the figure.
- `figure3-budget-sensitivity.csv` contains exactly nine dataset-budget cells and all reductions are positive.
- The statement “all nine dataset-seed comparisons improved” is supported against the strongest evaluated control (`top_abs` / `Top-|m|`) and should not be read as a universal pairwise win over every control without the per-seed table.
- The principal reproducibility inconsistency is F8's evidence-path/aggregation mismatch, not a mismatch in the displayed figure values.

## Figure-Caption Findings

- **Figure 2:** Caption agrees with the source CSV: rank128/2%, three-seed means, sample SD, lower better. The legend label `Top-|m|` corresponds to the result mode `top_abs`; this mapping should be made explicit in a later table/caption.
- **Figure 3:** Caption agrees with the plotted validation-grid values and the focal-setting caveat.
- **Figure 4:** Caption agrees with the two panels and the rank128/1% timing condition. The source caption and rendered figure include a dashed **3 pp reference line**; the frozen manuscript caption omits this reference-line explanation. This is a safe caption edit, not a data error.
- **Figure 1:** The image exists at `figures/figure1-architecture.png` and the caption describes the intended mechanism. The image uses `s_i = ||dz/dm_i||^2`, while the manuscript method defines `J_i = ∂z/∂r_i` and `s_i = ||J_i||²`; the notation should be aligned in a later figure/caption pass.
- **Figure 1 provenance is an evidence blocker.** `figure1-manifest.json`, `figure-contract.md`, and `figure-table-insertion-audit.md` describe a deterministic local SVG/self-draw fallback authorized after GPT failures, while the project task/state records make direct-GPT Figure 1 a mandatory P8 gate. The audit can verify that a replacement image exists and is visually coherent, but cannot certify that the mandatory direct-GPT gate was satisfied.
- Tables 1-3 are marked `planned-for-tex` in `figure-table-insertion-audit.md` and are absent from the frozen Markdown manuscript. This is a completeness/next-stage item, not a contradiction in the current prose.

## Citation Metadata Findings

- The manuscript contains 11 existing citation keys: `spikinggcn`, `spikenet`, `dy-sign`, `delay-dsgn`, `signnn`, `asgcn`, `fast-snn`, `one-spike`, `a2q`, `adaqp`, `dcgs`.
- No `.bib`, `.bbl`, or References section is present in the run root. The keys are draft placeholders backed only by `writing/verified-reference-context-p7.md`.
- `dcgs` explicitly lacks a verified publication record in the supplied context. `one-spike` has a 2024/2025 year ambiguity and both arXiv and DOI links; `a2q` and `fast-snn` are recorded in preprint-style form. These require canonical metadata resolution before bibliography acceptance.
- The digest itself says the 36-reference authenticity/relevance/placement/duplicate audit is still scheduled at P12 Citation metadata is therefore **not submission-ready**, even though the placeholder usage is internally consistent.

## Citation-Context Findings

- Related-work placement is conservative: the manuscript distinguishes graph conversion, graph-message compression, and output-sensitive coding, and explicitly says the cited published outcomes are not direct matched-budget measurements.
- The A2Q and One-Spike citations are used for context and for “our matched-budget adaptations,” not as claims that the source papers used this experiment's ledger. This wording is safe.
- No broad literature search was performed. Context support is assessed only against the supplied verified-reference-context file; external authenticity and duplicate checks remain P12 work.

## Severity

- **High / blocking for evidence closure:** F8 evidence path does not reproduce the manuscript's A2Q/One-Spike percentages from the cited JSON.
- **High / blocking for P8 gate certification:** Figure 1 direct-GPT provenance conflicts with the recorded mandatory gate; the local fallback is present but does not prove gate compliance.
- **Medium:** bibliography metadata is incomplete (`dcgs`, `one-spike`, preprint-style entries, no `.bib`/References).
- **Medium:** Figure 4 caption omits the plotted 3 pp reference-line explanation; Figure 1 uses `dm_i` versus manuscript `dr_i`.
- **Low:** Tables 1-3 are planned but not inserted in the frozen Markdown; `Top-|m|`/`top_abs` naming should be mapped explicitly.

## Safe Edit Suggestions

These are suggestions only; the frozen manuscript remains unchanged.

1 Correct the P9 evidence record for F8 to cite `figures/source-data/figure2-main-logit-mse.csv` (and state the three-seed-mean reduction aggregation), or provide the exact derivation from `confirmation-test-v2.json` that yields the displayed values.
2 Add the Figure 4 caption sentence explaining that the dashed line is the 3 pp reference bound, not an observed equivalence threshold.
3 Align Figure 1 notation with the method (`r_i`, `J_i = ∂z/∂r_i`) or explain why the figure uses `m_i`.
4 Map `Top-|m|` to the implementation mode `top_abs` in the caption/table plan.
5 Resolve citation metadata in P12 and then add a real bibliography; do not invent entries now.

## Evidence Blockers

- Reproducible provenance for the six A2Q/One-Spike reduction numbers is missing from the evidence digest's cited JSON.
- Direct-GPT Figure 1 generation is not evidenced as completed; only the authorized local fallback is evidenced.
- Final bibliography acceptance is blocked pending the scheduled 36-reference metadata/duplicate audit.

## Next CCFA Owner

`ccf-paper-reviewer` for scientific judgment after the F8 provenance and Figure 1 gate are resolved; `ccf-paper-writer` for safe wording/caption edits; `ccf-visual-composer` for the Figure 1 notation and Figure 4 reference-line caption; the P12 citation-audit owner for bibliography metadata.

## No-Invention Status

No missing number, citation, DOI, arXiv identifier, or experimental result was supplied or inferred. Unsupported or unresolved items are marked above as partial, blocked, or pending rather than repaired by invention.
