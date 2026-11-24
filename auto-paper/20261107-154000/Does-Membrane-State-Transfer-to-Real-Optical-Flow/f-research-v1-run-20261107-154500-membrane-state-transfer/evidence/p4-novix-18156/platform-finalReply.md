# novix task 18156 platform finalReply (verbatim)

status: processing
steps: 317

# P4 全量实验最终结果

## 1. 完成状态

以下内容均已实际运行并落盘，不是计划值：

- 总状态：`completed`
- Stage A：`completed`
- Stage B：`completed`
- Stage C：`completed`
- Seeds：`[1, 2, 3, 4, 5]`
- `unavailable`：`[]`
- 独立验证：`passed`
- 验证错误：`[]`
- 已复核 raw/evidence artifacts：`121`
- `entrypoint.sh` 实际退出码：`0`
- 快速 invariant tests：`4 passed`
- 当前无运行中的训练、下载或评估进程。

主检查点：

`/home/novix/workspace/project/result.json`

---

# 2. 实测：硬件与运行环境

- GPU：NVIDIA GeForce RTX 4090
- GPU 显存：
  - `47,661,645,824 bytes`
  - `45,453.69 MiB`
- NVIDIA Driver：`580.126.09`
- CUDA：`13.0`
- PyTorch：`2.11.0+cu130`
- cuDNN：`91900`
- Python：`3.11.18`
- NumPy：`2.4.6`
- SciPy：`1.17.1`
- scikit-learn：`1.9.1`
- pandas：`3.1.1`
- OpenCV：`5.0.0`

依赖直接安装在默认运行环境中，没有创建 virtualenv。

---

# 3. 实测：连接组与映射

## 3.1 Zenodo edge prefix

按照协议，仅对 edge 文件执行 HTTP Range：

- Range：`bytes=0-8388607`
- HTTP 状态：`206`
- 实际下载：`8,388,608 bytes`
- 远端完整文件大小：`178,853,187 bytes`
- prefix SHA-256：

`61345a1d739fe9bc2b6251100055779aa69cf8ebb03ade8b565ffb648d33978e`

截断 gzip 采用流式 zlib 解压，忽略预期中的不完整 gzip 尾部，并删除末尾不完整 CSV 行：

- 完整真实 edge 数据行：`791,218`
- `gzip_stream_eof=false`：这是 Range 截断的预期结果，不是完整 gzip 校验成功声明。

## 3.2 图统计

- 节点数：`130,391`
- COO 合并前完整边行：`791,218`
- 合并重复边：`8,457`
- CSR nnz：`782,761`
- 矩阵方向：`A[post, pre]`
- 权重：`log1p(syn_count)`
- 输入复眼 root IDs：`5,354`
- KC 读出节点：`2,559`
- inhibitory signed edges：`309,071`
- 原始 40-step 谱半径：`102.71229437283591`
- 缩放后谱半径：`0.9499999658640129`
- 目标谱半径：`0.95`
- 行归一化：未使用
- 原图互反边对：`10,673`

## 3.3 Voronoi 复眼映射

- 输入图像：`32×32 = 1,024` pixels
- 使用列：`x_axis`、`y_axis`
- 1,024 个 pixel 映射到：`717` 个 active eye root IDs
- 总 eye root IDs：`5,354`
- 每帧 receptor drive 按最大值归一化到 1。
- 没有使用 3D `x/y/z` 列。

## 3.4 KC 可达性诊断

从 active eye roots 到 KC 的 exact-hop 可达数：

| Hop | 可达 KC 数 |
|---:|---:|
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |
| 4 | 8 |
| 5 | 714 |
| 6 | 2,231 |
| 7 | 2,526 |
| 8 | 2,539 |

因此，指定的三步 stateless 传播在拓扑上不能到达 KC；其 KC 特征恒定不是随机训练失败，而是可复核的结构诊断。

## 3.5 保度零模型验证

每个 seed 的 degree-null 图都满足：

- in-degree 精确保留：`true`
- out-degree 精确保留：`true`
- nnz 精确保留：`true`
- 原始互反边保持不变：`true`
- 权重集合及顺序保持：`true`

---

# 4. 实测：SYNTHETIC direction

每个 seed 有 400 个样本，固定 70/30 stratified split。以下顺序均为 seed 1–5。

## 4.1 Ceiling

- Accuracy：`[1.000000, 1.000000, 1.000000, 1.000000, 0.991667]`
- Mean：`0.9983333333`

说明合成方向标签本身可由输入数据可靠学习。

## 4.2 五个主条件

| 条件 | Seed 1–5 accuracy | Mean | 相对 stateless Δ | 2000次 bootstrap 95% CI | exact p | BH q | FDR拒绝 |
|---|---|---:|---:|---|---:|---:|---|
| stateless | `[0.500000, 0.500000, 0.500000, 0.500000, 0.500000]` | `0.500000` | `0` | `[0, 0]` | `1` | `1` | 否 |
| lif_homeostasis | `[0.500000, 0.500000, 0.500000, 0.500000, 0.500000]` | `0.500000` | `0` | `[0, 0]` | `1` | `1` | 否 |
| lif_combo | `[0.500000, 0.500000, 0.500000, 0.500000, 0.500000]` | `0.500000` | `0` | `[0, 0]` | `1` | `1` | 否 |
| degree_null_lif | `[0.841667, 0.716667, 0.658333, 0.650000, 0.650000]` | `0.703333` | `+0.203333` | `[0.151667, 0.268333]` | `0.0625` | `0.25` | 否 |
| A=0 | `[0.891667, 0.908333, 0.883333, 0.891667, 0.883333]` | `0.891667` | `+0.391667` | `[0.385000, 0.400000]` | `0.0625` | `0.25` | 否 |

虽然 degree-null 和 `A=0` 的 bootstrap CI 不含零，但只有 5 个 paired seeds 时，exact sign-flip test 的最小双侧非零 p 值为 `0.0625`；因此二者均未通过 BH-FDR q=0.05。

## 4.3 动力学和效率诊断

| 条件 | 全图 spike rate | KC readout spike rate | Feature std | Peak GPU MiB | 五 seeds 总耗时 s |
|---|---:|---:|---:|---:|---:|
| stateless | `0` | `0` | `0` | `1289.596` | `3.374` |
| lif_homeostasis | `0.001326909545` | `0` | `0` | `191.050` | `3.269` |
| lif_combo | `0.000274476862` | `0` | `0` | `209.061` | `2.795` |
| degree_null_lif | `0.000252535163` | `1.97098e-05` | `0.001923886311` | `209.061` | `40.291` |
| A=0 | `0` | `0` | `0.056186642156` | `0` | `2.613` |

这里的 `0 MiB` 表示该条件没有使用被 GPU allocator 统计的神经传播张量，不代表整台机器没有 GPU 占用。

---

# 5. 实测：SYNTHETIC flash control

## 5.1 Ceiling

- Accuracy：`[1, 1, 1, 1, 1]`
- Mean：`1.000000`

## 5.2 五个主条件

| 条件 | Seed 1–5 accuracy | Mean | Spike rate | KC spike rate | Feature std |
|---|---|---:|---:|---:|---:|
| stateless | `[0.500000, 0.500000, 0.500000, 0.500000, 0.500000]` | `0.500000` | `0` | `0` | `0` |
| lif_homeostasis | `[0.500000, 0.500000, 0.500000, 0.500000, 0.500000]` | `0.500000` | `0.000354980884` | `0` | `0` |
| lif_combo | `[0.500000, 0.500000, 0.500000, 0.500000, 0.500000]` | `0.500000` | `9.03786496e-05` | `0` | `0` |
| degree_null_lif | `[0.600000, 0.675000, 0.641667, 0.608333, 0.533333]` | `0.611667` | `8.18964691e-05` | `7.40035170e-06` | `0.001087193159` |
| A=0 | `[0.491667, 0.625000, 0.491667, 0.433333, 0.533333]` | `0.515000` | `0` | `0` | `0.02457630641` |

Flash control 的 stateless、homeostasis 和 combo 同样没有形成可变 KC 特征。

---

# 6. 实测：DAVIS-2017 获取与动态标签

## 6.1 下载和解压

- ZIP 大小：`832,766,765 bytes`
- ZIP magic：`PK`
- SHA-256：

`e3d0b5b77c3d031b000a19e0e25e3e2cac65d183755601bc2cf066df1a2aa492`

- 下载耗时：`78.194 s`
- 解压耗时：`459.172 s`
- 下载加解压总耗时：约 `537.37 s`
- 解压成员数：`12,610`

## 6.2 Clip 构造

- DAVIS sequences：`90`
- 保留连续 8 帧 clips：`728`
- Clip shape：`[728, 8, 32, 32]`
- Left：`378`
- Right：`350`
- DAVIS annotation union 前景质心标签：`727`
- Frame-difference motion-energy fallback：`1`
- 因低运动或歧义跳过：`15`

处理顺序：

1. JPEG 解码；
2. 转灰度；
3. INTER_AREA 缩放到 32×32；
4. 反相为 `1 - pixel/255`；
5. 使用动态前景质心的时间斜率生成左右标签。

没有用静态外观直接生成标签。

---

# 7. 实测：DAVIS ceiling failure gate

5 seeds ceiling accuracy：

`[0.5388127854, 0.5068493151, 0.5114155251, 0.5388127854, 0.5114155251]`

Mean：

`0.5214611872`

协议阈值：

`0.70`

因此：

`0.5214611872 < 0.70`

failure gate 已被激活。后续真实域方法数值仍完整执行并保存，用于审计，但按预先规定的规则，不允许据此作真实域方法优势或迁移主张。

---

# 8. 实测：DAVIS 五个主条件

| 条件 | Seed 1–5 accuracy | Mean | 相对 stateless Δ | 2000次 bootstrap 95% CI | exact p | BH q | FDR拒绝 |
|---|---|---:|---:|---|---:|---:|---|
| stateless | `[0.520548, 0.520548, 0.520548, 0.520548, 0.520548]` | `0.520548` | `0` | `[0, 0]` | `1` | `1` | 否 |
| lif_homeostasis | `[0.520548, 0.520548, 0.520548, 0.520548, 0.520548]` | `0.520548` | `0` | `[0, 0]` | `1` | `1` | 否 |
| lif_combo | `[0.520548, 0.520548, 0.520548, 0.520548, 0.520548]` | `0.520548` | `0` | `[0, 0]` | `1` | `1` | 否 |
| degree_null_lif | `[0.506849, 0.529680, 0.511416, 0.534247, 0.525114]` | `0.521461` | `+0.000913` | `[-0.009132, 0.010046]` | `1` | `1` | 否 |
| A=0 | `[0.589041, 0.497717, 0.534247, 0.538813, 0.525114]` | `0.536986` | `+0.016438` | `[-0.006393, 0.045662]` | `0.4375` | `1` | 否 |

动力学诊断：

| 条件 | 全图 spike rate | KC readout spike rate | Feature std | Peak GPU MiB |
|---|---:|---:|---:|---:|
| stateless | `0` | `0` | `0` | `1289.596` |
| lif_homeostasis | `0.01470643852` | `0` | `0` | `191.050` |
| lif_combo | `0.002359935009` | `0` | `0` | `209.061` |
| degree_null_lif | `0.002177856377` | `0.000164215181` | `0.006812522193` | `209.061` |
| A=0 | `0` | `0` | `0.2152185486` | `0` |

---

# 9. 实测：DAVIS 四个单因素消融

比较基准为完整 `lif_combo`，其 mean accuracy 为 `0.5205479452`。

| 消融条件 | Seed 1–5 accuracy | Mean | 相对完整 combo Δ |
|---|---|---:|---:|
| minus adaptive threshold | `[0.520548, 0.520548, 0.520548, 0.520548, 0.520548]` | `0.520548` | `0` |
| minus refractory | `[0.520548, 0.520548, 0.520548, 0.520548, 0.520548]` | `0.520548` | `0` |
| minus E/I | `[0.520548, 0.520548, 0.520548, 0.520548, 0.520548]` | `0.520548` | `0` |
| minus homeostasis | `[0.547945, 0.534247, 0.534247, 0.543379, 0.552511]` | `0.542466` | `+0.021918` |

`minus homeostasis` 的配对统计：

- Mean delta：`+0.0219178082`
- 95% bootstrap CI：`[0.0155251142, 0.0283105023]`
- exact paired sign-flip p：`0.0625`
- BH q：`0.25`
- q=0.05 rejection：`false`

由于真实域 ceiling failure，该结果不能作为方法发现；同时它也未通过 BH-FDR。

---

# 10. 实测：保度零模型差值

差值严格定义为：

`degree_null_lif - biological lif_combo`

## SYNTHETIC

- Per seed：
  `[+0.341667, +0.216667, +0.158333, +0.150000, +0.150000]`
- Mean：`+0.2033333333`
- 95% bootstrap CI：`[0.1516666667, 0.2783333333]`
- Exact p：`0.0625`

## REAL DAVIS

- Per seed：
  `[-0.013699, +0.009132, -0.009132, +0.013699, +0.004566]`
- Mean：`+0.0009132420`
- 95% bootstrap CI：`[-0.0082191781, 0.0100456621]`
- Exact p：`1`

符号为正表示零模型高于 biological combo。该结果不能反向描述成“生物接线优势”。

---

# 11. 实测：域间 gap

定义：

`gap = delta_real - delta_synthetic`

| 条件 | Gap mean | 95% bootstrap CI | Exact p |
|---|---:|---|---:|
| stateless | `0` | `[0, 0]` | `1` |
| lif_homeostasis | `0` | `[0, 0]` | `1` |
| lif_combo | `0` | `[0, 0]` | `1` |
| degree_null_lif | `-0.2024200913` | `[-0.2819863014, -0.1461872146]` | `0.0625` |
| A=0 | `-0.3752283105` | `[-0.4073059361, -0.3443378995]` | `0.0625` |

负值表示相对 stateless 的数值增益在 DAVIS 上小于 SYNTHETIC。由于只有 5 个 paired seeds，degree-null 和 `A=0` 的 exact p 均仍为 `0.0625`。

---

# 12. 推断与正式裁决

持久化裁决为：

`failure_real_ceiling_below_0.70_no_method_claim`

严格解释如下：

1. `lif_homeostasis` 和 `lif_combo` 在 SYNTHETIC direction 上相对 stateless 的增益均为精确的 `0`。
2. 因而本批次没有检测到可供迁移检验的 “synthetic membrane-state gain”。
3. DAVIS ceiling mean 只有 `0.521461`，低于预注册阈值 `0.70`。
4. 因此不能支持“膜状态增益可迁移”。
5. 也不能把结果解释为“膜状态增益只属于合成规则运动”，因为真实域评估协议没有通过 ceiling gate。
6. 最终结论是 **协议失败下的不可判定**，而不是“迁移失败”的阳性发现。
7. Degree-null 在 SYNTHETIC 上的较高数值是零模型条件的结果，不是生物接线优势，也不是膜状态可迁移证据。
8. 所有主比较的 BH-FDR rejection 均为 `false`。

---

# 13. 已记录的限制

1. 只使用 edge 文件前 8 MiB，共 `791,218` 条完整真实数据行，不是完整 connectome。
2. 32×32 Voronoi 映射只直接驱动 `717/5,354` 个 eye roots。
3. `8×32×32` 的真实数学维数是 `8192`，不是任务文本中的 `4096`；实现保留 8192 维，并只在训练集拟合 PCA(32)。
4. 神经动力学参数固定且未训练；seed 变化主要来自刺激、split 和 null topology。
5. CUDA `index_add_` 的浮点原子运算可能存在末位数值非确定性。
6. 三跳 stateless 传播在拓扑上无法到达 KC。
7. 指定 LIF 条件虽产生全图 spikes，但 biological graph 的 KC readout spike rate 为 0，特征方差为 0。
8. DAVIS ceiling `<0.70`，禁止真实方法和迁移主张。

---

# 14. 产物路径

## 主入口与配置

- `/home/novix/workspace/project/experiment.py`
- `/home/novix/workspace/project/entrypoint.sh`
- `/home/novix/workspace/project/config.json`
- `/home/novix/workspace/project/requirements.txt`
- `/home/novix/workspace/project/validate_results.py`
- `/home/novix/workspace/project/test_pipeline.py`
- `/home/novix/workspace/project/result.json`
- `/home/novix/workspace/progress.md`

## 主要证据

- `/home/novix/workspace/project/evidence/main_table.csv`
- `/home/novix/workspace/project/evidence/stats.json`
- `/home/novix/workspace/project/evidence/real_ceiling.json`
- `/home/novix/workspace/project/evidence/synthetic_ceiling.json`
- `/home/novix/workspace/project/evidence/ablation.json`
- `/home/novix/workspace/project/evidence/null.json`
- `/home/novix/workspace/project/evidence/diagnostics.json`
- `/home/novix/workspace/project/evidence/robustness.json`
- `/home/novix/workspace/project/evidence/efficiency.json`
- `/home/novix/workspace/project/evidence/run_manifest.json`
- `/home/novix/workspace/project/evidence/experiment-traceability.csv`
- `/home/novix/workspace/project/evidence/stage_A_raw.json`
- `/home/novix/workspace/project/evidence/stage_B_raw.json`
- `/home/novix/workspace/project/evidence/validation.json`
- `/home/novix/workspace/project/evidence/command_history.log`

`experiment-traceability.csv` 的每一行均包含对应且存在的产物路径。

## 原始预测

目录：

`/home/novix/workspace/project/evidence/raw/`

其中每个 task × condition × seed 的 `.npz` 均保存：

- `train_idx`
- `test_idx`
- `y_true`
- `y_pred`
- `decision`

Stage C 和独立 validator 均从这些 `y_true/y_pred` 重算 accuracy，而不是仅信任 JSON 状态位。

## 处理后的数据元信息

- `/home/novix/workspace/project/data/processed/graph_metadata.json`
- `/home/novix/workspace/project/data/processed/davis2017_motion_clips.json`
- `/home/novix/workspace/project/data/processed/pixel32_to_compound_eye_voronoi.json`
- `/home/novix/workspace/project/data/null_graphs/degree_null_seed1.json`
- `/home/novix/workspace/project/data/null_graphs/degree_null_seed2.json`
- `/home/novix/workspace/project/data/null_graphs/degree_null_seed3.json`
- `/home/novix/workspace/project/data/null_graphs/degree_null_seed4.json`
- `/home/novix/workspace/project/data/null_graphs/degree_null_seed5.json`
- `/home/novix/workspace/project/data/splits/`

---

# 15. 复现方式

完整入口：

```bash
bash /home/novix/workspace/project/entrypoint.sh
```

该入口会：

1. 实测并打印 GPU/CUDA/PyTorch；
2. 检查固定版本依赖，缺失时直接安装到默认环境；
3. 依次运行或续跑 Stage A、B、C；
4. 执行独立 raw-artifact 验证；
5. 生成日志和全部 evidence。

该命令已实际完整运行并返回 `0`。

Git 分支：

`p4-full-experiment`

阶段提交：

- `577c10d` — Implement Stage A connectome and synthetic experiments
- `d5723c7` — Complete DAVIS real-domain batch and acquisition pipeline
- `26f2921` — Add paired statistics and validated P4 evidence
- `e34c9da` — Finalize validated full-batch experiment artifacts