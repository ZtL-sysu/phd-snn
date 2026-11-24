# Guidance — Cross-subject EEG Low-latency Probabilistic SNN（SpikeMLDA + 吴老师）

> 生成：2026-10-28｜层级目标：**B 会（EMBC/ICASSP/IJCNN）→ A 会潜力**｜复用 xhf 既有 SpikeMLDA

## 中央科学问题
能否用吴老师的**概率脉冲神经元（TPP）/时序校准**，把跨被试 EEG 解码做成**超低延迟、低能耗**的 SNN，并把"目标数据预算"作为校准/适配的显式变量，适配可穿戴边缘（呼应吴 FDCT 的可穿戴/忆阻器方向）？

## 目标领域 / 层级
- 领域：脑信号解码 + 类脑边缘计算
- 会议：EMBC、ICASSP、IJCNN（B）→ NeurIPS/ICLR（A，若强）
- **贡献声明（planned_claim）**：首个把 ANN→SNN 转换 + 概率脉冲神经元用于跨被试低延迟 EEG 解码，在少样本/低预算下以 ≤8 时间步逼近全精度模型，推理能耗远低于稠密 ANN。

## 故事（Problem→Gap→Insight→Evidence）
- **Problem**：可穿戴 EEG 需实时低功耗；现有 EEG SNN（Li2024 CBM、Loihi STDP）多为直训/STDP，跨被试漂移下低延迟难。
- **Gap**：转换法（FTBC/TPP）在 EEG 上未被系统用；概率神经元解决超低 T 信息密度恰好对症跨被试少数据。
- **Insight**：把"目标数据预算"作为校准的显式变量——预算越少，概率神经元的超低 T 鲁棒性收益越大。
- **Evidence**：SEED/SEED-IV/SEED-VIG（公开）+ xhf 已用 SADT/MPD-DF；对比全精度 ANN、直训脉冲 SNN、Li2024 风格 STDP SNN、转换基线。

## 实验（概要）
- 数据：SEED 系列（公开/轻注册）、BCI Competition；xhf 自有 SADT/MPD-DF/SEED-VIG。
- 基线：全精度 ANN（must-rerun）、直训脉冲 SNN（adaptation-attempt）、Li2024 风格 STDP（literature-context/adaptation）、FTBC/TPP 适配（adaptation-attempt）、朴素转换（internal-matched）。
- 变体：有/无概率神经元；T∈{1,2,4,8}；数据预算∈{10%,25%,50%,100%} 跨被试。
- 指标：解码准确率（主）、时间步、理论能耗（spike 数）、跨被试泛化（leave-subject-out）。
- 统计：多被试均值±std。
- 硬件：RTX 3060 12GB，EEG 小模型，分钟级。

## 预期
- minimum：T≤8 精度 ≥ ANN −3%，优于朴素转换。
- expected_strong：T≤4 精度 ≥ ANN −1.5%，低预算下优于直训脉冲 SNN。
- failure：低 T 精度塌且概率神经元无救 → 退回"直训脉冲 SNN + 跨被试适配"定位。

## 引用范围（预备）
- 必引：TPP/时序错位(Wu)、FTBC(ECCV24)、Li2024(CBM 109225)、Loihi EEG、SEED 数据集、SpikeMLDA（xhf 既有）。
- 锁定时扩到 ≥36 条近 3–5 年多数。

## 与 D1 关系
D3 是 D1 在"序列/生物信号"模态的姊妹篇；两者共同构成 D4（统一 non-vision 转换基准）的实证基础。
