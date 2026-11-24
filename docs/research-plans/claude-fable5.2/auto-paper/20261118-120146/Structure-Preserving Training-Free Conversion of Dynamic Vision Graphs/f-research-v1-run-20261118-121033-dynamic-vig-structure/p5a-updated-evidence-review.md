# P5A final scientific review — updated with cross-dataset and paired statistics

- Added evidence: `mnist-teacher-training-results.json`, `mnist-v2-results.json`, and `paired-bootstrap-results.json`.
- Fashion-MNIST: teacher 83.60%, v1 50.23%, v2 78.83%, 85.71% gap closure.
- MNIST: teacher 77.88%, v1 15.93%, v2 70.78%, 88.54% gap closure.
- Fashion-MNIST paired v2-v1 over 6,000 example-seed predictions: mean +28.60 points, bootstrap 95% CI [27.17, 30.08].
- Message MSE reductions: 82.19% Fashion-MNIST, 86.07% MNIST.
- Event parity holds within each dataset.
- The evidence supports a method paper with a clear mechanism, two public datasets, three seeds each, ablations, and uncertainty reporting.
- Remaining limitations are honest scope boundaries: small patch-grid Graphers, event accounting rather than hardware energy, and no claim of universal architecture transfer.
- Verdict: pass.
