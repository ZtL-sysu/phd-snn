# Novix 4090 在途任务

> 提交时间 2026-11-10 18:0x GMT+8｜用户指令：「后续的全量实验，你放 novix 跑，更快」。

## 任务标识

| 项 | 值 |
|---|---|
| Task id | **`20049`** |
| chatSessionId | `d68291be714a870c42e052299baea75d` |
| 提交命令 | `novix --json task create "<query>" --provider novixlet --resource-pool exp-4090 --gpu --gpu-count 1` |
| 返回码 | 0（`{"id": "20049", ...}`） |
| 预算参数 | **未带** `--max-turns` / `--timeout` / `--agent auto`（遵循此前无预算约定；默认 ML Agent 更快） |
| 资源池 | `exp-4090`（**关键**：不加资源池参数会落到 L4 通用沙箱） |
| GPU | `--gpu --gpu-count 1` |
| 登录态 | 提交前 `ensure_login.py` 确认 `wxf@novix.science`, user_id 637, kind platform, CLI 0.1.7 |

## 提交物

- `novix/query-header.md` — 任务规格（输出契约、数据、矩阵、P1B 三项闭合条件、纪律）
- `novix/query-full.txt` — 提交的完整 query（21,208 B，含 base64 载荷）
- `novix/payload.b64` — gzip+base64 打包的三个脚本（12,588 B）
- `protocols/build_novix_query.py` — 可复现的 query 生成器

载荷内文件：`protocols/vision_pipeline.py`、`protocols/run_experiments.py`、`protocols/run_full.py`（原样、与本机 smoke 实现一致）。使用 base64 是因为直接传 33.7KB 脚本文本触发 `Argument list too long`。

## 远端执行矩阵

| 项 | 值 |
|---|---|
| 数据集 | 官方 SuperPixel `MNIST`、`CIFAR10`（`data.pyg.org/datasets/benchmarking-gnns/{MNIST,CIFAR10}_v2.zip`） |
| seeds | 0,1,2,3,4（冻结） |
| split | n_train=5000 / n_val=1000 / n_test=2000，官方 split 内抽样 |
| teacher | hidden=128, lr=0.01, epochs=1000, CUDA, sum pooling, gauge |
| 方法 | naive / qcfs / ftbc / tpp / parallel / ours × T∈{1,2,4,8,16} |
| 消融 | 4 项（去 β*、计数解码、随机第二相、朴素 IF） |
| 统计 | 5-seed 均值±std 与 95% CI、配对差值、BH 在后续汇总 |

## 远端必须闭合的三项 P1B 条件

1. **H1 能耗口径**：同时报 `primary`（脉冲触发 AC）与 `conservative`（A 传播按 MAC 计）两套 `energy_ratio_ann_over_snn`，禁止只挑有利口径；标注「45nm 理论算术能耗估算，非硬件实测」。
2. **H2 ρ_n 算子类**：除对称归一化（实测 ρ_mean≈0.9987）外，各跑 `sym_norm=False` 原始带权邻接臂，报告 ρ 分布与 conversion loss；不得把 ρ≈1 包装成 ρ≠1 证据。
3. **H3 恒等式与 teacher**：`B`/`B̂` 与膜电位累加统一 float64，报告残差（目标 <1e-10）；teacher test acc <70% 时提升 epochs/数据并记录。

另要求复核本机 smoke 的负结果：`ours_no_beta` 与 `ours_naive_if` 在 T=8 达 66.2% 高于完整 ours 60.2%（β* 与两阶段可能冗余），以及膜电位解码的巨大贡献（计数读出仅 14.8%）。**不得删除负结果**。

## 输出契约（历史踩坑后的硬约束）

远端必须在**工作区根 `project/`** 下交付：`config.json`、`result.json`、`experiment.py`、`README.md`、`protocols/*.py`、`logs/run.log`。每个 seed 完成即追加写 `result.json`，提前终止前也必须先落盘脚本与阶段性结果。历史教训：`17682` finish 零产物、`18885` 控制面 `processing` 与 `failed` 同时存在、多处 `result.json` 落在不可 pull 的路径。

## 回收流程（后续会话/轮次）

1. 只用「解析到 JSON `status` + `finalReply` + 可 pull 的 `project/result.json` + SHA-256 校验一致」判终态，**不把平台 `status` 单独当权威**。
2. `novix --json task result 20049`；遇 rc=4/HTTP 503 用带外 `novix --json debug task 20049 --logs` 或前缀探针，不重复提交。
3. `novix debug pull task:20049 <run_root>/novix/pulled/` 或定向 `--sub project`，把 `project/` 全部同步进本 run root，登记哈希。
4. 用 `results/` 下的本地脚本重算 summary 与统计，与远端 `result.json` 对账；不一致以原始 runs 为准。
5. 回填 `experiment-traceability.md`，再按 `f-research-v1` 推进 P3A → P4 → P5 → P5A。**P5 未达 `expected_strong` 不得进 P6 写作**。

## 当前状态（18:42 复核）

`SUBMITTED / QUEUED`，**尚未开跑**。

| 通道 | 观测 |
|---|---|
| 主 API `task result 20049` | `status=processing`, `steps=0` |
| 带外 `debug task 20049` | `backend.status=processing`, `error_code=""`, `placement.state=queued`, `pool=exp-4090`, `gpu=1`, `cpu=4`, `memory_mb=49152`, `pool_status={dispatch_paused:false, eligible_nodes:2}`, `diagnosis=NO_ALLOCATION` |
| `debug ls task:20049` | `no session matches ... under /mnt/novix-k8s-workspace-root` → 工作区尚未创建 |
| 带外建议 | 「尚未分配 sandbox；检查队列和父任务交接状态，**不要重复提交**」 |

判读：池内有 2 个可用节点且未暂停，属于**排队等 sandbox 分配**，不是任务失败、不是零产物、不是结果不达标。`task list` 在本机只返回本地 create 日志（无服务端 status），不能用于队列诊断。

**处置**：不重提、不换题、不并行提交同 idea 任务。按历史教训（`18885` 控制面与数据面不同步、`17682` finish 零产物），只有「解析到 JSON 终态 + finalReply + 可 pull 的 `project/result.json` + SHA-256 一致」才判完成。

## 持续盯梢

`protocols/watch_20049.py` 已以后台任务启动（每 180 s 探测一次，最多 40 次 ≈ 2 h），同时查主通道与带外通道，日志追加到 `novix/watch-log.md`；一旦满足终态条件即自动 `novix debug pull task:20049 <run_root>/novix/pulled/`，校验 `result.json` 并写 `results/novix-20049-summary.json`。**不**在 queued/processing 阶段重复提交。

## 21:0x 状态复核：3 小时零分配，判定为调度侧卡住

后台盯梢 `YPbmmr` 跑满 **40 次探测 / 2h14m** 后按脚本设计退出（exit 2 = `WATCH_TIMEOUT`，非崩溃）。40 次探测全部为 `status=processing, steps=0, placement=queued, diagnosis=NO_ALLOCATION, error=''`，其中主通道偶发 rc=4、带外偶发 rc=124/2，但带外可读时结论一致。21:01 直查仍是同一状态。

`debug task 20049 --logs` 补充：`node=null`、`nomad_alloc_id=null`、`dispatch_phase=null`、`artifact_sync=null`、`runtime_logs.source=unavailable`、`log_warnings=["Runtime diagnostics not archived: legacy task or upload pending"]`。即 **claim 已创建但从未转成 allocation**，池子仍报 `eligible_nodes=2 / dispatch_paused=false`。`track list` 显示若干历史 active track（9 月起、`runtime_status=running`），但无权威证据表明它们占用本池；不据此臆断。

**判定**：这是平台调度侧卡住，不是任务失败、不是零产物、不是结果不达标。与历史 `18885`（卡 >27h、控制面状态矛盾）同型。继续单纯盯梢不产生科学进展。

### 采取的并行措施（不取消、不重提、不改故事）

| 措施 | 说明 |
|---|---|
| 保留 `20049` | 不 cancel、不重提、不换题；一旦终态仍按输出契约 pull 并回收 |
| 低频盯梢重启 | `watch_20049.py` 改为 600 s / 36 次（≈6 h），后台 `y7PR2S`；终态自动 pull + SHA 校验 |
| **本机 3060 并行全量** | `protocols/run_full_local.py`，后台 `2fx4x1`；规格与 `20049` **完全一致**（MNIST+CIFAR10 × 5 seeds × 5000/1000/2000 × epochs 1000 × hidden 128 × 六方法 × 5 T + 消融 + 能耗），产物 `results/local_full/` |
| 性质 | **并行保险，不是替代**。本机 3060 单 seed 全套实测 66.87 s，全量预计 10–40 min；结果明确标注来源，与远端结果分开记，不混列、不互相冒充 |

用户更高优先级目标是「冲强结果、故事不能再退」，因此不等一个卡住的调度器；`contracts/strong-result-no-retreat.md` 的五条定位与四项 `expected_strong` 全部不变。

## 目标策略（用户 18:42 指令）

「目标肯定是冲强结果的，我们目前的故事不能再退」→ 见 `contracts/strong-result-no-retreat.md`：故事五条定位冻结、`expected_strong` 四项目标冻结、明确作废 v2 里预留的「回退为纯 benchmark / 诊断型论文」路线；P5 未达标时只允许按修正回路**改进方法并重跑**（实现对齐、teacher 质量、β* 与两阶段冗余、低 T 精度、稀疏化换能耗、加强基线、规模算力），不允许改定位或降阈值。
