# f-research-v1 P4 / C1 correction loop v3 进度

更新时间：2026-11-08T00:25:00Z

## 阶段状态

- Setup：完成
- Implementation：完成
- Testing / pre-training invariants：完成，合法 fail-fast 终态
- Evaluation / method readout：按协议未执行（KC feature-std invariant 失败）
- Artifact validation：完成，72/72 checks passed

## 硬件实测

- GPU：NVIDIA GeForce RTX 4090
- 显存：46068 MiB（`nvidia-smi`）
- 驱动：580.126.09
- NVIDIA-SMI CUDA：13.0
- Python：3.11.18
- PyTorch：2.11.0+cu130
- `torch.version.cuda`：13.0
- `torch.cuda.is_available()`：true
- cuDNN：91900

## 数据状态

- 连接组：完整 178,853,187 B。单请求在 120 秒时仅到 112,121,920 B；随后按 HTTP Range 分成 64 MiB + 64 MiB + 44,635,459 B，字节级拼接并通过 gzip 完整性校验。sha256=`402fa0e61198e6f26b2ef4fd18e0123cc2edff0bb1edca9dd31b29b8171580bc`，`prefix=false`。
- 注释表：7,740,866 B，gzip 校验通过。
- 复眼坐标：629,193 B；确认字段含 `x_axis`,`y_axis`。
- DAVIS-2017：832,766,765 B，120 秒内完成；ZIP 魔数 `PK`，12,610 个成员，`testzip=OK`。
- 完整图实测：16,847,997 原始行、138,639 节点、15,091,983 个去重非零边。
- 32×32 `x_axis/y_axis` Voronoi 映射：717 个唯一 receptor root，其中 704 个出现在图中。
- exact-length eye→KC：hop1=0, hop2=15, hop3=2559, hop4..8=2559；correction K=5。
- 真实域 v1 full-frame ceiling 实测均值 0.685，按阈值标 unavailable；Sintel 在 120 秒时仅 423,001,855 B，curl rc=28，标 unavailable。
- 透明注册的 DAVIS v2 修订：8 帧 GT foreground union 固定 ROI + 10% margin；输入保留 ROI 内未遮罩 grayscale pixels，mask 不乘入像素。五种子 ceiling 均值 0.72，通过 0.70 门槛。该修订是 post-hoc，已在 config/result 明示。

## 重要运行进程

- 无运行中进程。
- `bqy5hd9xe`：`experiment.py --run-full --skip-download` 已正常按 invariant fail-fast 结束，CLI exit code 2；这不是 runtime crash。

## 关键实测结果

- SYNTHETIC flattened ceiling：`[1, 1, 1, 1, 1]`，mean=1.0。
- DAVIS v2 flattened ceiling：`[0.6416667, 0.7583333, 0.7666667, 0.7166667, 0.7166667]`，mean=0.72。
- degree-null：15,091,983 edges；所有 exact degree/nnz/weight/reciprocal constraints 验证通过。
- SYNTHETIC-direction pre-readout feature std：
  - stateless `3.233602379551713e-08`（pass）
  - lif_homeostasis `0.0`（fail）
  - lif_combo `0.0`（fail）
  - degree_null_lif `1.0940825987779166e-06`（pass）
  - A0 `0.10334160100319024`（不适用 KC invariant）
  - lif_combo_no_adaptive `0.0`（fail）
  - lif_combo_no_refractory `0.0`（fail）
  - lif_combo_no_ei `0.0`（fail）
- 终态：`status=design_invalid`，原因是 biological-graph LIF KC features 跨样本零方差。按用户规则立即停止，没有拟合任何方法 Ridge readout，也没有生成或宣称未运行的 accuracy/statistics。
- 独立 validator：72/72 checks passed。
