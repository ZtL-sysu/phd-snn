# P8 fallback completion report

## Completed

- The data-figure contract, source data, captions, and Python/matplotlib production script are complete.
- Figures 2-4 exist in editable SVG plus PDF, PNG, and TIFF.
- Source CSVs and a hash manifest are present.
- Figures 2-4 passed visual QA after targeted layout fixes.
- Figures 2-4 are inserted in an independent P8 manuscript copy near their explanatory text.
- Three evidence tables are selected with purposes and placement.

## User-authorized fallback

Three built-in GPT attempts across consecutive goal turns failed with the same `502/ECONNRESET` condition. The user then explicitly directed: if the image-generation model is unavailable, draw the framework figure locally first and keep all other standards unchanged.

The accepted fallback is a deterministic, editable FigureSpec-style SVG generated locally from a structured specification, then exported to PDF and PNG. It was structurally validated and visually inspected. The pipeline may proceed because the user explicitly changed the Figure 1 production route while preserving the scientific and quality requirements.
