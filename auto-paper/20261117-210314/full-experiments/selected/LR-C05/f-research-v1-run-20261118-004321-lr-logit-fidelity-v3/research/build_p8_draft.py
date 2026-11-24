from __future__ import annotations

from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[1]
SOURCE = RUN_ROOT / "writing" / "arc-draft-v3" / "stage-17" / "paper_draft.md"
OUTPUT = RUN_ROOT / "writing" / "p8" / "paper-data-figures.md"


def insert_after(text: str, anchor: str, addition: str) -> str:
    if anchor not in text:
        raise RuntimeError(f"missing insertion anchor: {anchor[:80]}")
    return text.replace(anchor, anchor + "\n\n" + addition, 1)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    text = SOURCE.read_text(encoding="utf-8")
    text = insert_after(
        text,
        "The measurement scope excludes hardware energy and does not establish temporal-event equivalence or broad GNN generality.",
        "![Exact-cost output-Jacobian residual transport](../../../figures/figure1-architecture.png)\n\n**Figure 1.** Exact-cost output-Jacobian residual transport for frozen GNN-to-SNN conversion. A rank-128 basis and selected sparse exact residual records are serialized under a matched total padded serialized-bit budget before rate-coded conversion.",
    )
    text = insert_after(
        text,
        "The result is held-out confirmation after validation exposure because the focal setting and logit-fidelity reframing were fixed after validation exposure and before the test run.",
        "![Matched-budget logit MSE for the proposed selector and controls](../../../figures/data/figure2-main-logit-mse.png)\n\n**Figure 2.** Matched-budget logit fidelity on Cora, Chameleon, and Squirrel at rank 128 and a 2% residual budget. Bars show three-seed means and sample SD; lower is better.",
    )
    text = insert_after(
        text,
        "This validation-grid sensitivity result shows that the direction of the logit-MSE difference was consistent across the evaluated cells, while the focal 2% setting later received held-out confirmation after validation exposure.",
        "![Logit-MSE reduction across residual budgets](../../../figures/data/figure3-budget-sensitivity.png)\n\n**Figure 3.** Logit-MSE reduction over the evaluated residual-budget grid. The focal 2% setting later received held-out confirmation after validation exposure.",
    )
    text = insert_after(
        text,
        "This is a wall-clock pipeline measurement and does not measure hardware energy.",
        "![Task trade-off and warmed runtime overhead](../../../figures/data/figure4-tradeoff-and-runtime.png)\n\n**Figure 4.** Bounded task trade-off and warmed runtime overhead. Panel a reports official-test fidelity gains versus worst three-seed-mean task loss; panel b reports paired p95 runtime ratios at rank128/1%.",
    )
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
