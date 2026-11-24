# G1 — Public dataset access

- Direct HTTP tree verification: Fashion-MNIST parquet train/test files are listed under `https://huggingface.co/datasets/zalando-datasets/fashion_mnist/tree/main/fashion_mnist` with sizes 30,931,277 and 5,175,617 bytes.
- License verification: the dataset card at `https://huggingface.co/datasets/zalando-datasets/fashion_mnist/raw/main/README.md` declares `license: mit`.
- Task verification: card identifies image classification with 10 classes and standard 60,000/10,000 train/test splits.
- Fallback: MNIST parquet files are directly listed and the card declares `license: mit`.
- Rejected: CIFAR-10 unknown license; SVHN non-commercial-only; approval-gated or request-only datasets.

Gate verdict: `pass` after dataset replacement from CIFAR-10 to Fashion-MNIST.
