## 执行终态

本轮已完成代码实现、真实数据获取、图构建、训练前检查、fail-fast、独立验证与交付。最终科学状态为：

- `status = design_invalid`
- `phase = design_invalid_final`
- 不是运行崩溃。
- 触发原因：多个 biological-graph LIF 条件的 KC 特征跨样本方差严格为零。
- 已按协议立即停止，未继续拟合 Ridge，未生成或补造方法准确率、bootstrap CI、sign-flip p 值或 BH-FDR 结果。

## 实测结果

### 图与可达性

- 完整连接组：`178,853,187 B`
- SHA-256：`402fa0e61198e6f26b2ef4fd18e0123cc2edff0bb1edca9dd31b29b8171580bc`
- `prefix=false`
- 节点数：`138,639`
- 去重非零边：`15,091,983`
- 32×32 Voronoi 映射：717 个唯一 receptor roots，其中 704 个在图中
- exact-length eye→KC，hop 1..8：
  - `0, 15, 2559, 2559, 2559, 2559, 2559, 2559`
- 最终选择：`K=5`
- KC readout：`2559`

### Ceiling

- SYNTHETIC 五种子：`[1.0, 1.0, 1.0, 1.0, 1.0]`
- SYNTHETIC mean：`1.0`

DAVIS 过程已完整披露：

- 初版 full-frame mean：`0.685`，低于 0.70，标 unavailable
- Sintel：120 秒时仅下载 `423,001,855 B`，curl rc=28，标 unavailable
- 随后注册了明确标为 **post-hoc** 的 DAVIS v2：
  - 八帧 GT foreground union 固定 ROI
  - 10% margin
  - 保留 ROI 内未遮罩灰度像素
  - mask 不乘入或替换输入像素
- DAVIS v2 五种子：
  - `[0.6416667, 0.7583333, 0.7666667, 0.7166667, 0.7166667]`
- DAVIS v2 mean：`0.72`

### KC feature invariant

| 条件 | feature std | 结果 |
|---|---:|---|
| stateless | `3.233602379551713e-08` | pass |
| lif_homeostasis | `0.0` | fail |
| lif_combo | `0.0` | fail |
| degree_null_lif | `1.0940825987779166e-06` | pass |
| A0 | `0.10334160100319024` | KC invariant 不适用 |
| lif_combo_no_adaptive | `0.0` | fail |
| lif_combo_no_refractory | `0.0` | fail |
| lif_combo_no_ei | `0.0` | fail |

失败的 biological LIF 条件还实测到：

- KC soft feature 全部等于 `0.04742586985230446`
- 非常数 KC 维度数：`0`
- KC hard-spike rate：`0.0`

Degree-null 图的 exact in/out degree、nnz、weight multiset、duplicate 和 reciprocal constraints 全部验证通过。

## 严格解释

**实测：** 注册的 biological-graph LIF 动力学未在 KC readout 产生任何跨样本变化。

**推断：** 当前动力学、阈值和传播参数组合不适合检验膜状态增益；这不能解释为 stateless 优于 LIF，也不能解释为膜状态机制被普遍否定。由于 readout 未运行，本轮没有方法优越性、迁移或显著性主张。

五 paired seeds 的最小双侧 exact sign-flip p 为 `0.0625`；本轮在统计检验前已 fail-fast，因此仅披露该功效限制，没有伪造检验结果。

## 验证与交付

- 单元/协议测试：`10/10` 通过
- 独立结果验证：`72/72` 通过
- Raw ceiling NPZ：10 个
- Pre-readout feature NPZ：8 个
- Bootstrap NPZ：0 个，原因是未进入方法 readout
- `main_table.csv` 明确标为 ceiling-only partial evidence
- `entrypoint.sh` 已验证可复现该合法 `design_invalid` 终态，返回码为 2
- Git 工作区干净
- 最终提交：`e073451`

最终 `result.json`：

- 字节数：`63,003`
- SHA-256：`feecf369ae3ce9c2ddbdf62207e59736ecffe879b3f61eb6cab36b5fb45173ca`
- SHA-256 前 16 位：`feecf369ae3ce9c2`

主要文件及 10 个 raw NPZ 已交付，包括 `result.json`、`validation.json`、`main_table.csv`、traceability、配置、入口脚本、测试和命令历史。