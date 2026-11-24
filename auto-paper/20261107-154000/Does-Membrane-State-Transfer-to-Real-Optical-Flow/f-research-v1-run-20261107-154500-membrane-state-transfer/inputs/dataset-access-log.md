# Dataset access log (round 001) — measured in this session

| Source | URL | Probe result | Licence / note |
|---|---|---|---|
| FlyWire v783 edges | `https://zenodo.org/api/records/21549559/files/connections_biological.csv.gz/content` | HTTP 206 verified locally; 2,335,888 readable rows from a gz prefix -> 107,101 nodes / 2,284,735 nnz | Zenodo `10.5281/zenodo.21549559`, CC BY 4.0; **prefix subset, not the complete graph** |
| Neuron annotations | same record, `neuron_annotations_flywire_v2.1.0.tsv.gz` | 139,255 rows; `cell_type`, `top_nt`, `side`; 1,673 KC; 34,465 inhibitory presynaptic | CC BY 4.0 |
| Eye positions | same record, `right_visual_positions_all_neurons.csv` | 5,354 rows, 4,097 mapped; `x_axis/y_axis` | CC BY 4.0 |
| DAVIS-2017 trainval-480p | `https://data.vision.ee.ethz.ch/csergi/share/davis/DAVIS-2017-trainval-480p.zip` | HTTP 200, `Content-Length: 832766765`, `application/zip`; 16-byte Range returned 206 with magic `50 4b 03 04` | Official DAVIS challenge link parsed from `davischallenge.org/davis2017/code.html` |
| MPI-Sintel complete | `http://files.is.tue.mpg.de/sintel/MPI-Sintel-complete.zip` | HTTP 200 after 301, `Content-Length: 5627783629`, `application/zip`; 16-byte Range returned 206 with magic `50 4b 03 04` | Optional extension; 5.6 GB, use only if the smaller dataset is insufficient |
| SYNTHETIC sequences | local `mining/light_smoke.py` generator | 7-variant self-test 19.2 s / 4.0 GB peak | Explicitly SYNTHETIC; labels are temporal properties |

No dataset here requires approval, payment, NDA, IRB or manual review. The earlier
`https://vision.middlebury.edu/flow/data/comp/zip/Sintel.zip` and
`https://data.vision.ee.ethz.ch/cvl/DAVIS2/DAVIS-2017-trainval-480p.zip` URLs returned 404 and were
rejected; only the verified links above enter the experiment query.
