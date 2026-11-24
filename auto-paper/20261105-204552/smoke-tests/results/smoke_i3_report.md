# I3 冒烟实验记录（复眼几何前端）→ 淘汰

环境：`dyg-cold`，Windows 11，RTX 3060 12 GB，CUDA 12.8。
数据：`data/zenodo/right_visual_positions_all_neurons.csv`（官方 Zenodo 存档，629 KB，
5,354 行，含 `x_axis/y_axis` 投影坐标与 R7/R8 类型）。
刺激：`cogstim ans --ratios easy --img-size 128 --seed 42`（面积受控的数量辨别，336 张 PNG，
脚本内按固定 seed 打乱后 75/25 切分）。
下游：共享的可导软脉冲两层读出，T=8，等输入脉冲预算（目标 0.20）。
**单 seed、60 步、非论文实验**，只用于 Go/No-Go。

## 运行历史（三次）

| 轮次 | 数据 | 说明 | Voronoi test acc | Grid test acc | delta | 判定 |
|---|---|---|---:|---:|---:|---|
| R0 dry-run | 合成小图 + shapes | 输入白底饱和、切分 bug | 0.0 | 0.0 | 0.0 | 无效（发现编码缺陷） |
| R1 真实 | Zenodo 复眼坐标 + ans | **坐标列解析 bug**：选中 3D `x/y` 而非投影 `x_axis/y_axis` | 0.2941 | 0.4118 | −0.1177 | 无效（实验有 bug） |
| R2 真实 | 同上，修复坐标列 | 使用 `x_axis/y_axis`；输入反相成稀疏墨迹；等脉冲预算 | 0.3725 | 0.4118 | **−0.0393** | **DROP_OR_REVISE** |

R2 详细：mean input intensity voronoi 0.0601 / grid 0.0447；rate_scale 3.3262 / 4.4718；
实测输入脉冲率 0.1147 / 0.1071（近似等预算）；train loss 0.739→0.141 / 0.745→0.210；
peak GPU 19 MB；单条件 0.47s / 0.33s。

## 判定

按预注册失败信号：
- `no_geometry_gain = True`（delta = −0.0393 < 0.02，且方向为负）；
- `no_learnable_signal = True`（两者 test acc 均 <= 0.55）；
- `too_slow = False`。

→ **I3 淘汰，按用户规则换到 I1。**

## 诚实解读（不能过度解读）

1. 两条件 test acc 都低于 0.5，而 train loss 明显下降（0.14 / 0.21），
   主要是**小样本过拟合**（仅 240 张用于训练、60 步、400 维输入），
   不能据此断言"ANS 任务不可学"——官方论文在 5,000+ 图上生物图达到 63.69%。
2. 因此本轮能支持的结论只是：**在当前受控小样本设置下，实测复眼 Voronoi 几何
   没有表现出优于规则网格的可分辨信号**，且该结论在修复坐标 bug 后方向未变。
   这与 CCF 评审给 I3 的致命风险（"拆模块 + 换基准"、novelty 2/5）一致。
3. 若日后要复活 I3，前提是先解决过拟合（更大训练集、早停、正则、跨 backbone），
   并在 ≥2 个下游与 ≥2 个数据集上复现；本轮 11 天窗口内不具备条件。
4. R1 的 −0.1177 因坐标 bug 作废，不作为证据；只保留 R2。

## 产物

- `smoke_i3.py`（可复现脚本）
- `smoke_i3.json`（R2 机器可读结果）
- 本报告
