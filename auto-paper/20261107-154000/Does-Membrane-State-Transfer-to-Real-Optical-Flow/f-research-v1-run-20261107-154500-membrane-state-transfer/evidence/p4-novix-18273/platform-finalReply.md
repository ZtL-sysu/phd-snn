# novix 18273 finalReply (verbatim)

## 完成状态

- 终态：`COMPLETED_VALID_DESIGN_EXPECTED_SIGNAL_NOT_MET`
- `design_valid=true`
- `expected_signal_met=false`
- 含义：**实验、机制诊断和验证均已完整完成，但预注册的强恢复信号没有达到固定标准**。这不能表述为方法成功、方法优越或机制已被否证。
- 全部后台进程均已结束。
- 最终证据提交：`5e0f768 Record full five-seed experiment evidence`

## 实测结果

### 1. 完整连接组

- 数据文件：178,853,187 bytes
- SHA256：`402fa0e61198e6f26b2ef4fd18e0123cc2edff0bb1edca9dd31b29b8171580bc`
- `prefix=false`
- 节点数：138,639
- 去重有向边数：15,091,983
- biological graph 谱半径：504.30373775432537
- degree-null 谱半径：461.8065675505941
- degree-null：
  - accepted pairs：5,357,831
  - rewired edges：10,715,662
  - rewired fraction：0.7100234608003467
  - 每节点 in/out degree、nnz、权重 multiset、reciprocity 均精确保留

eye→KC exact shortest-hop：

| Hop | annotated KC 数 |
|---:|---:|
| 1 | 0 |
| 2 | 15 |
| 3 | 2,544 |
| 4 | 0 |
| 5 | 0 |
| 6 | 0 |
| 7 | 0 |
| 8 | 0 |

按冻结回退规则解析为 `K=3`，最终读出使用全部 2,544 个 exact-hop-3 annotated KCs，没有使用随机神经元替代。

### 2. Ceiling 与真实域

- SYNTHETIC：
  - 五个 seed 均为 1.0
  - mean：1.0
  - 2000次 paired-seed bootstrap 95% CI：`[1.0, 1.0]`
  - invariant #3 通过
- DAVIS full-frame v1：
  - mean：0.4769161133187838
  - 95% CI：`[0.44776788191288874, 0.5060643447246788]`
  - 低于冻结的 0.70 门槛，因此标记为 `unavailable`
- Sintel：
  - 受控下载未完成，partial 已删除
  - 标记为 `unavailable`
- 未注册或使用 post-hoc DAVIS v2，未用 toy 数据冒充真实域。
- 因两个真实域均不可用，**不做 SYNTHETIC→REAL 泛化主张**。

### 3. 主条件

| 条件 | Accuracy mean | 读出跨样本 std |
|---|---:|---:|
| `stateless` | 0.875000 | `1.4355410334152546e-08` |
| `lif_homeostasis` | 0.500000 | 0 |
| `lif_combo` | 0.500000 | 0 |
| `lif_drive_every_frame` | 0.500000 | 0 |
| `degree_null_lif` | 0.473333 | `9.073245051152311e-07` |
| `A=0` | 1.000000 | `0.20875875535562027` |
| `stateless_skip` | 0.988333 | 非零 |
| `lif_homeostasis_skip` | 1.000000 | `0.14461838414490796`（composite） |
| `lif_combo_skip` | 1.000000 | 非零 |
| `lif_drive_every_frame_skip` | 1.000000 | 非零 |
| `degree_null_skip` | 0.976667 | 非零 |

补充统计：

- `stateless` 95% CI：`[0.8483333333333334, 0.9033333333333333]`
- `lif_homeostasis - stateless = -0.375`
- exact paired sign-flip `p=0.0625`
- BH-FDR `q≈0.06818`

`A=0` 的 1.0 只解释为**原始输入信息上界**，不能解释为生物接线优势。

### 4. 预注册强对比

`lif_homeostasis_skip - stateless_skip`：

- 五个 paired-seed 差值：
  - `[0.0, 0.01666666666666672, 0.0, 0.01666666666666672, 0.025000000000000022]`
- mean：`+0.011666666666666691`
- 2000次 bootstrap 95% CI：
  - `[0.0033333333333333435, 0.02000000000000004]`
- exact paired sign-flip：`p=0.25`
- BH-FDR：`q=0.25`
- 固定强信号门槛：`+0.15`

虽然 CI 下界为正，但效应量远低于 `+0.15`，因此：

- `expected_strong_met=false`
- 不能声称 skip 恢复了预期的 LIF 机制增益。

统计边界：五个 paired seeds 下，全部非零差值同向时，双侧 exact sign-flip 的最小非零 p 值为：

```text
2 / 2^5 = 0.0625
```

因此本设计不可能产生小于 0.05 的双侧 exact p 值。

### 5. 方差与 collapse 定位

实测：

- resolved KC readout 的 stateless 方差在 hop 3 首次变为正：
  - hop 3 mean per-frame KC std 约 `2.59147e-08`
  - temporal-mean final std：`1.4355410334152546e-08`
- biological LIF baseline：
  - hop 0–3 KC std 均为 0
  - hop 3 membrane cross-sample std 为 0
  - hop 3 KC hard-spike rate 为 0
- `drive_every_frame=true`：
  - hop 3 KC std 仍为 0
  - hop 3 membrane cross-sample std 仍为 0
- residual skip：
  - composite readout std 恢复到 `0.14461838414490796`
  - 但 graph-KC branch 仍为零方差

因此 invariant #2 通过的原因是**预注册 residual input branch 保留了跨样本方差**，而不是 biological graph 上的 KC/LIF 分支恢复了方差。

### 6. Probe、消融与 phase map

Probe accuracy：

- `A=0`：hop 0–3 均为 1.0
- biological stateless：
  - h0=1.0
  - h1=0.5
  - h2=0.5
  - h3=0.875
- biological LIF baseline/combo/drive-every-frame：
  - h0=1.0
  - h1=0.5
  - h2=0.5
  - h3=0.5
- skip LIF：hop 0–3 均为 1.0

去 adaptive、去 refractory、去 E/I、frozen gain、drive once/every、shuffled frame 和 flash control 均得到：

- accuracy=0.5
- KC std=0
- 一因子直接差值=0
- exact `p=1`
- BH-FDR `q=1`

λ×K phase map：

- 20/20 cells 完成
- λ：`{0.3, 0.6, 0.95, 1.1}`
- K：`{1,2,3,5,8}`
- biological baseline LIF 与 drive-every-frame LIF 的所有 cell 均为 KC std=0
- drive reinjection interaction fraction=0
- `directional_structure_supported=false`

### 7. Structure × dynamics 2×2

| Structure | Dynamics | Accuracy | Std |
|---|---|---:|---:|
| biological | stateless | 0.875000 | `1.43554e-08` |
| biological | LIF | 0.500000 | 0 |
| degree-null | stateless | 0.898333 | `2.21507e-06` |
| degree-null | LIF | 0.473333 | `9.07325e-07` |
| identity | stateless | 0.886667 | `0.0688906264` |
| identity | LIF | 0.506667 | `0.2075246933` |
| A=0 | stateless | 1.000000 | `0.2087587554` |
| A=0 | LIF | 0.506667 | `0.00155661859` |

## 有限推断

结果支持的有限表述是：

1. 严格零方差 collapse 最迟发生在 biological graph + hard-spike 到 resolved KC readout 的路径上。
2. 每帧重注入输入没有恢复 biological KC 或 membrane 的跨样本方差。
3. residual skip 保留的是绕过图传播的输入信息；它没有修复 graph-KC 分支。
4. identity/A=0 LIF 条件能保留非零方差，但准确率仍接近 chance，因此“严格零方差”和“标签信息丢失”不是同一现象。
5. 当前测量不能证明所有隐藏节点收敛到唯一数学固定点，也不能简单归因于“只有图结构”或“只有膜动力学”。
6. 预注册的高 λ×高 K 等高线及 drive-reinjection interaction 预测不受支持。

## 测试与复现

- `project/entrypoint.sh`：端到端成功
- 单元/集成测试：18/18 通过
- 严格 validator：440/440 通过
- failed checks：0
- raw NPZ：685 个
- `result.json` 与 `evidence/result_snapshot.json` byte-identical
- 主要结果、配置、表格、验证文件和复现入口均已交付。

## 最终文件实测审计

实际执行：

```text
$ ls -l project/result.json project/config.json
-rw------- 1 novix novix   16314 Nov  8 02:23 project/config.json
-rw------- 1 novix novix 1322902 Nov  8 02:25 project/result.json
```

| 文件 | Bytes | SHA256 | 前16位 |
|---|---:|---|---|
| `project/result.json` | 1,322,902 | `2c15f8466687d7ef4c572b12748d1bef0b1d7263e9b8437b06be3de1ff691aed` | `2c15f8466687d7ef` |
| `project/config.json` | 16,314 | `5fab75f3a4122d61b9e49de5b764ec8672e8777a051e67f92a3ee5921364cbc3` | `5fab75f3a4122d61` |

```text
$ git check-ignore -v project/result.json
```

stdout 为空，exit code 为 `1`，即 `project/result.json` **未被 Git ignore**。
