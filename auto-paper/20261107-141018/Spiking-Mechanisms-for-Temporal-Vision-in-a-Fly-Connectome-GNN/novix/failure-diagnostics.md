# novix task 17682 — 回收诊断（实测记录）

时间：2026-11-07 14:55 GMT+8。任务 `status=finish`，但**实验未执行**。
本文件只记录可核对的事实；推断均显式标注，不作为结论。

## 平台命令与原始输出

```
novix --json task result 17682
  -> {"event":"result","id":"17682","status":"finish",
      "chatSessionId":"2a8823db9cc05765727c871f2740d1cd","steps":40}

novix debug ls task:17682 -L 2
  -> workspace 存在：.claude/、.runtime_data/、progress.md、project/、
     search_results/、user_data/、writing_space/、plugins/

novix debug pull task:17682 ./pulled
  -> exit 4，后端 GET /track-ops/debug/sessions 读超时；
     已落盘部分到 pulled/.novix-pull.4b4o70x3/workspace/
  -> pulled 内：workspace/project/ 文件数 = 0，result.json = 0，experiment.py = 0

novix debug traj task:17682
  -> "40 events, 20 tool calls, 0 error-looking messages"
  -> 末几步：装 scipy / scikit-learn（远程原本缺失）、
     git commit progress.md、TodoWrite 把 Data 标为 in_progress、
     用 urllib 探测 Zenodo 注释表与坐标表的表头列名。
```

## 远程 progress.md 原文要点

```
## Status
- [x] Setup and hardware report
- [ ] Bounded real-data acquisition and graph construction
- [ ] Model/dynamics/evaluation implementation
- [ ] Five-seed GPU experiment
- [ ] Reproducibility/QA and final handoff
## Results log
- Pending experiment run. Do not infer or fill numerical results before execution.
```

## 远程硬件（实测，可用于 G5 档案）

RTX 4090 46,068 MiB，驱动 580.126.09，CUDA 13.0，torch 2.11.0+cu130，
`torch.cuda.is_available()=True`，单卡。远程 Python 初始缺 scipy / scikit-learn，
agent 自行 `pip install` 后可用。`progress.md` 已 pull 到本地，可作证据。

## 推断（未证实，不写进任何结论）

任务在 40 events / 20 tool calls 处终止，可能与 v1 口径的
`--max-turns 12 --timeout 3600` 或平台侧默认限制有关；现有日志不足以证明因果。
**但用户 14:34 指令已明确取消这类预算**，后续提交一律不带这两个参数，
且结果由后续轮次跨轮回收，本机不阻塞等待。

## 对下一次 query 的加固要求（交给下一轮 f-guidance）

1. 把「公开数据可达性 + 列名校验」放最前，失败立刻标 unavailable 并落盘。
2. 依赖清单显式写出（scipy / scikit-learn / pandas / torch），远程干净环境需自行安装。
3. 要求**在任何提前终止之前**先写出可运行的 `experiment.py` 和阶段性的 `result.json`，
   即使实验未跑完也要落盘结构与状态字段，避免「finish 但零产物」。
4. 明确要求最终回复里给出 result.json 中每个字段的实际数值，禁止只汇报进度。
5. 不重复提交同一实验配置；换设计或加固后再提。
