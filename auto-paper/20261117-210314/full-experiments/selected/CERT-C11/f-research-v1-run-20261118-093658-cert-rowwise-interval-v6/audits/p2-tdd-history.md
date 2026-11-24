# P2 TDD history

The rowwise functions were developed test-first in the preserved v5 run:

- RED: `rowwise_quantize` and `certificate_bounds_matrix` imports failed because the functions did not exist.
- GREEN: implementations were added and the two rowwise tests passed.
- The final v6 run imports the exact tested files and passes the complete 9-test suite.

No production code was changed during v6 setup except the run-local protocol/config labels.
