# local_full 版本说明

本目录为**旧配置**（`ours_beta=star`，即带 `β*=θ/(2T)`）的 5-seed 全量，用作配对基线。

`results/local_full_v2/` 为**修正配置**（`ours_beta=zero`，去掉冗余 β*）的同规格全量。

两者同 seeds、同 splits、同 teacher 配置，仅 β 不同，构成「组合内部重认定」的配对证据。

注意：CUDA 稀疏归约非确定，两份独立运行的 ANN 精度有约 0.5 pp 差异；配对比较一律使用各自运行内的 conversion loss，不跨运行混用 ANN 数值。

novix `20049` 仍在途（长时间 `queued / NO_ALLOCATION`），其产物单独回收，不与本机结果混列。

所有能耗均为 45 nm 理论算术能耗估算，非硬件实测。
