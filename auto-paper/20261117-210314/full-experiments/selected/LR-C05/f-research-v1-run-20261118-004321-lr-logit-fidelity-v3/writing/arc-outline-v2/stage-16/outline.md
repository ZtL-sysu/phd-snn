```json
{
  "artifact_type": "canonical_six_section_outline_and_claim_evidence_map",
  "manuscript_plan": {
    "numbered_sections": [
      {
        "number": 1,
        "heading": "Introduction",
        "purpose": "Open from output-sensitive information loss in compressed graph messages; state the bounded logit-fidelity question and contribution.",
        "paragraph_plan": [
          {
            "id": "P1",
            "point": "Low-rank graph-message transport can preserve the wrong output-sensitive directions under a fixed serialization budget.",
            "fact_ids": ["F1", "F3"],
            "adds": "problem statement and bounded contribution"
          }
        ],
        "qualification_placement": "State the contribution with the reported-test-split and matched-padded-bit qualifications from F1 and F3. Do not imply energy, temporal-event, task-superiority, or broad GNN-generality claims here."
      },
      {
        "number": 2,
        "heading": "Related Work and Background",
        "purpose": "Situate prior work on low-rank graph-message compression, SVD transport, ANN-to-SNN conversion, and sensitivity-based residual sparsity. Contrast assumptions, trade-offs, and evaluation settings. Claim prior-work limitations only with verified supporting citations.",
        "paragraph_plan": [
          {
            "id": "P_RW",
            "point": "Existing low-rank transport and ANN-to-SNN conversion methods trade cost against fidelity under different selection assumptions; prior-art adaptations require verified citations before any comparative claim.",
            "fact_ids": [],
            "adds": "context only; no packet-supported empirical claim"
          }
        ],
        "qualification_placement": "No packet-verified facts are assigned to this section. Drafting prose is blocked until verified citation facts are supplied; do not insert unverified references."
      },
      {
        "number": 3,
        "heading": "Method",
        "purpose": "Define SVD transport, exact padded-bit ledger, output-Jacobian squared sensitivity score, sparse coefficient encoding, rate-coded conversion, and evaluation scope. Place the F5 scope limitation at its home.",
        "paragraph_plan": [
          {
            "id": "P2a",
            "point": "Output-Jacobian squared sensitivity selects sparse residual coefficients after SVD transport under an exact padded-bit budget.",
            "fact_ids": ["F1", "F3"],
            "adds": "selection mechanism and cost model"
          },
          {
            "id": "P2b",
            "point": "The test run is held-out confirmation after validation-exposed reframing; sparse residual coefficients are not temporal SNN events; no energy or broad GNN-generality claim is supported.",
            "fact_ids": ["F5"],
            "adds": "experimental scope and limitation home"
          }
        ],
        "qualification_placement": "F5 is stated fully here. F3 is stated here as transport-only cost equality and repeated wherever resource claims are made."
      },
      {
        "number": 4,
        "heading": "Experiments and Results",
        "purpose": "Report matched-budget logit MSE, bounded task degradation, prior-art adaptations, and warmed cost. Organize around questions and observed patterns, not table cells or run IDs.",
        "paragraph_plan": [
          {
            "id": "P3",
            "point": "The held-out test run confirms logit-MSE reductions on all three graphs at matched padded bits.",
            "fact_ids": ["F1", "F3"],
            "adds": "main fidelity comparison"
          },
          {
            "id": "P4a",
            "point": "Task degradation remains bounded in the same rank-128/2% matched-budget comparison.",
            "fact_ids": ["F2"],
            "adds": "task trade-off bound"
          },
          {
            "id": "P4b",
            "point": "Warmed runtime and memory overhead are modest in the measured rank-128/1% setting.",
            "fact_ids": ["F4"],
            "adds": "cost trade-off evidence with explicit budget qualifier"
          }
        ],
        "qualification_placement": "F1 uncertainty is stated beside the main result: no formal CI is claimed. F2 is stated here as a bounded observation, not equivalence proof. F4 is stated with the rank-128/1% budget distinction and wall-clock-only scope."
      },
      {
        "number": 5,
        "heading": "Discussion",
        "purpose": "Interpret fidelity gains and task trade-offs; distinguish observed results from mechanism hypotheses; state limitations.",
        "paragraph_plan": [
          {
            "id": "P5",
            "point": "The result is a local fidelity/resource contribution, not task superiority, temporal-event conversion, or energy evidence.",
            "fact_ids": ["F5"],
            "adds": "scope and limitations interpretation"
          }
        ],
        "qualification_placement": "Repeat F5 if any statement of generality, novelty, energy, or event semantics is made. Do not repeat the full Results inventory."
      },
      {
        "number": 6,
        "heading": "Conclusion",
        "purpose": "Answer the Introduction's question with supported evidence and meaning; add no new result, mechanism, or application promise.",
        "paragraph_plan": [
          {
            "id": "P6",
            "point": "Output-Jacobian residual allocation is a promising exact-budget fidelity mechanism within the tested frozen-GCN scope.",
            "fact_ids": ["F1", "F2"],
            "adds": "bounded conclusion"
          }
        ],
        "qualification_placement": "Conclude only the reported logit-MSE improvement and bounded task degradation for the tested frozen GCN setting."
      }
    ],
    "claim_evidence_map": [
      {
        "fact_id": "F1",
        "kind": "result",
        "status": "observed_verified",
        "exact_qualified_statement": "At rank 128 and a 2% sparse residual budget on the reported test split, output-Jacobian selection reduced the ratio of three-seed mean split-specific logit MSE versus the strongest evaluated matched-budget control by 26.23% on Cora, 33.99% on Chameleon, and 25.83% on Squirrel; all nine dataset-seed paired comparisons were positive. No formal confidence interval is claimed.",
        "model": "frozen two-layer hidden-16 GCN checkpoint seeds 0/1/2",
        "condition": "SVD rank 128 plus 2% output-Jacobian-selected sparse residual coefficients",
        "metric": "split-specific logit MSE reduction",
        "value": [26.23, 33.99, 25.83],
        "unit": "percent reduction",
        "aggregation": "ratio of three-seed mean per dataset",
        "uncertainty": "all nine dataset-seed paired comparisons positive; no formal CI claimed",
        "measurement_scope": "reported test split; validation-exposed reframing preceded the run",
        "home_section": "4 Experiments and Results, main fidelity comparison",
        "repeat_when": "Introduction and Conclusion state the bounded main result"
      },
      {
        "fact_id": "F2",
        "kind": "result",
        "status": "observed_verified",
        "exact_qualified_statement": "In the same rank-128/2% matched-budget comparison, the maximum three-seed-mean degradation across T=2/4 accuracy and teacher agreement was 1.86 percentage points; the largest seed-level degradation was 2.85 percentage points. This is a bounded observation, not an equivalence proof.",
        "model": "frozen two-layer hidden-16 GCN checkpoint seeds 0/1/2",
        "condition": "same rank-128/2% matched-budget comparison",
        "metric": "task degradation relative to the strongest evaluated control",
        "value": [1.86, 2.85],
        "unit": "percentage points",
        "aggregation": "maximum three-seed-mean and maximum seed-level",
        "uncertainty": "bounded observation, not equivalence proof",
        "measurement_scope": "reported test split",
        "home_section": "4 Experiments and Results, task trade-off",
        "repeat_when": "Introduction and Conclusion state the bounded task-degradation result"
      },
      {
        "fact_id": "F3",
        "kind": "result",
        "status": "observed_verified",
        "exact_qualified_statement": "All compared rank-128/2% methods used identical total padded serialized bits within each dataset, although payload lengths and coefficient counts could differ. This equality is for serialized transport only and excludes energy.",
        "model": "exact serialized-cost ledger",
        "condition": "rank 128 and 2% residual budget",
        "metric": "total padded serialized bits",
        "value": "matched within each dataset",
        "unit": "bits",
        "aggregation": "row-level equality",
        "uncertainty": "not applicable",
        "measurement_scope": "serialized transport, excluding energy",
        "home_section": "3 Method, exact cost ledger",
        "repeat_when": "any resource-cost or matched-budget claim is made"
      },
      {
        "fact_id": "F4",
        "kind": "result",
        "status": "observed_verified",
        "exact_qualified_statement": "Across nine dataset-seed pairs at rank 128/1% on an RTX3060 warmed benchmark with three warmups and seven measured repeats, paired p95 full-pipeline runtime ratios versus SVD-only ranged from 1.020 to 1.124, and peak CUDA allocation was 218.23 MB. Timing variance was retained in raw repeats; this measurement is wall-clock pipeline cost, not hardware energy. Note: this is the 1% residual-budget setting, not the 2% main fidelity setting.",
        "model": "RTX3060 warmed benchmark with three warmups and seven measured repeats",
        "condition": "rank 128/1% full encode/selection/decode/conversion timing",
        "metric": "runtime ratio and peak memory",
        "value": [1.020, 1.124, 218.23],
        "unit": "ratio and MB",
        "aggregation": "p95 range across dataset-seed pairs; maximum memory",
        "uncertainty": "timing variance retained in raw repeats",
        "measurement_scope": "wall-clock pipeline; not hardware energy",
        "home_section": "4 Experiments and Results, runtime/memory trade-off",
        "repeat_when": "runtime or memory overhead is generalized beyond the 1% measured setting"
      },
      {
        "fact_id": "F5",
        "kind": "limitation",
        "status": "observed_verified",
        "exact_qualified_statement": "The focal setting and logit-fidelity reframing were fixed after validation exposure and before the test run; the test run is held-out confirmation, not preregistered or independent replication. Sparse residual coefficients are not temporal SNN events, and no energy or broad GNN-generality claim is supported.",
        "model": "not applicable",
        "condition": "not applicable",
        "metric": "scope limitation",
        "value": "not applicable",
        "unit": "not applicable",
        "aggregation": "not applicable",
        "uncertainty": "run contract and independent pre-draft review",
        "measurement_scope": "whole-paper scope boundary",
        "home_section": "3 Method, experimental scope",
        "repeat_when": "Discussion or any statement of generality, novelty, energy, event semantics, or broad GNN applicability occurs"
      }
    ],
    "blocked_or_missing_evidence": [
      "Related Work and Background prose and citations: no verified citation facts are present in the current packet; drafting is blocked until verified prior-art facts are supplied.",
      "Prior-art adaptations: listed as a supporting priority in the brief but absent from the fact set; do not invent baseline descriptions or results.",
      "Hidden MSE, rank/budget sensitivity, and negative task-superiority diagnostics: listed in diagnostic priorities but not supported by current fact IDs; do not draft from memory.",
      "Runtime/memory at the main rank-128/2% budget: F4 was measured at rank 128/1%; do not generalize it to 2% without an additional verified measurement."
    ]
  },
  "notes": "This is a P6 outline and claim/evidence map, not a prose manuscript. The six numbered body sections are Introduction, Related Work and Background, Method, Experiments and Results, Discussion, and Conclusion. Limitations are embedded in Discussion and scope is placed at home in Method; no separate numbered Limitations section is used. The original P2 was split into P2a and P2b so F5 sits at its Method home, and P4 was split into P4a and P4b because F4 is measured at rank 128/1% and requires a distinct budget qualifier. No references, title, or abstract are finalized here. Final bibliography acceptance is blocked until verified citations are supplied. All values, units, model conditions, uncertainty types, and measurement scopes above are preserved from the packet; no author-reported result was upgraded to independent verification and no plan was converted into an observation."
}
```