# Correction: CUDA peak-memory accounting

- Trigger: traceability audit found elapsed time but no peak-memory metric required by LR-D.
- Repair: reset/read CUDA peak allocator around each reconstruction/evaluation and add `peak_memory_mb` to every row. No target or method changes.
- Action: rerun baseline and method batches; prior outputs without memory are superseded.
