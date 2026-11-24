# Dataset access log

Access date: 2026-11-18.

## Directly public and license-clear candidate

| Dataset | Direct URL | License/terms | Size | Labels/targets | Access friction | Decision |
|---|---|---|---|---|---|---|
| Fashion-MNIST (`zalando-datasets/fashion_mnist`) | `https://huggingface.co/datasets/zalando-datasets/fashion_mnist/tree/main/fashion_mnist` | Dataset card field `license: mit` | Train parquet 30,931,277 bytes; test parquet 5,175,617 bytes | 10 apparel classes; 60,000 train and 10,000 test examples | Direct unauthenticated download | `pass` |
| MNIST (`ylecun/mnist`) | `https://huggingface.co/datasets/ylecun/mnist/tree/main/mnist` | Dataset card field `license: mit` | Train parquet 15,561,616 bytes; test parquet 2,595,890 bytes | 10 digit classes; 60,000 train and 10,000 test examples | Direct unauthenticated download | `pass` as fallback |

## Rejected datasets

| Dataset | Reason |
|---|---|
| CIFAR-10 (`uoft-cs/cifar10`) | Direct file path exists, but card says `license: unknown` and Licensing Information is `[More Information Needed]`; original source requires citation but no explicit research-use license was found. Rejected under the strict builder rule. |
| SVHN (`ufldl-stanford/svhn`) | Card says `license: other` and explicitly `Non-commerical use only`; not selected for a binding top-tier contract without clearer terms. |
| ImageNet-1k | Larger local compute burden and terms/access not verified for this gate; not required for the primary mechanism test. |
| NTU RGB+D 60 | Commonly registration/approval gated; not used. |
| ModelNet40 | Public status/terms not verified in this gate; not used. |

## Dataset replacement decision

The active mechanism test is moved from CIFAR-10 to Fashion-MNIST, with MNIST as a license-clear fallback. This is a scenario repair, not a downgrade of the target tier: the claim concerns discrete topology/winner preservation in a training-free dynamic-graph conversion, which can be tested on any directly public image classification benchmark with a locally reproducible teacher. The replacement requires a versioned update of the packet's dataset URLs and split protocol before G2.
