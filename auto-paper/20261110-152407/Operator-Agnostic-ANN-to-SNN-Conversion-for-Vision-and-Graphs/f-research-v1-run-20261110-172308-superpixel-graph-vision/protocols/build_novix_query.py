#!/usr/bin/env python3
"""Build the self-contained novix query: header + gzip/base64 script payload."""
from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[1]
header = (R / "novix" / "query-header.md").read_text(encoding="utf-8")
vp = (R / "protocols" / "vision_pipeline.py").read_text(encoding="utf-8")
rx = (R / "protocols" / "run_experiments.py").read_text(encoding="utf-8")

run_full = '''import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_experiments as RE

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "project"
PROJ.mkdir(parents=True, exist_ok=True)
CFG = {"datasets": ["MNIST", "CIFAR10"], "seeds": [0, 1, 2, 3, 4],
       "n_train": 5000, "n_val": 1000, "n_test": 2000, "epochs": 1000,
       "hidden": 128, "lr": 0.01, "device": "cuda", "pool": "sum"}
(PROJ / "config.json").write_text(json.dumps(CFG, indent=2), encoding="utf-8")
result = {"meta": {"note": "all numbers produced by real runs"}, "runs": []}
for ds in CFG["datasets"]:
    for seed in CFG["seeds"]:
        t = time.time()
        rec = RE.run_one(ds, seed, CFG["n_train"], CFG["n_val"], CFG["n_test"],
                         CFG["epochs"], device=CFG["device"], hidden=CFG["hidden"],
                         lr=CFG["lr"], pool=CFG["pool"])
        rec["dataset"], rec["seed"], rec["wall_sec"] = ds, seed, round(time.time() - t, 2)
        result["runs"].append(rec)
        (PROJ / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
        print(ds, seed, "ANN", round(rec["ann"]["test_acc"] * 100, 2), flush=True)
import numpy as np
sm = {}
for ds in CFG["datasets"]:
    rs = [r for r in result["runs"] if r["dataset"] == ds]
    sm[ds] = {"ann_test_mean": float(np.mean([r["ann"]["test_acc"] for r in rs])),
              "methods": {k: float(np.mean([r["methods"][k]["acc"] for r in rs]))
                          for k in rs[0]["methods"]},
              "energy_T1_primary": float(np.mean(
                  [r["energy"]["ours_T1"]["energy_ratio_ann_over_snn"] for r in rs])),
              "energy_T8_primary": float(np.mean(
                  [r["energy"]["ours_T8"]["energy_ratio_ann_over_snn"] for r in rs]))}
result["summary"] = sm
(PROJ / "result.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
print("DONE", json.dumps(sm)[:600], flush=True)
'''

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr("protocols/vision_pipeline.py", vp)
    z.writestr("protocols/run_experiments.py", rx)
    z.writestr("protocols/run_full.py", run_full)
payload = base64.b64encode(buf.getvalue()).decode("ascii")

decode_note = """
## 8. 脚本还原（必须先做，再执行）

上面的两个实现脚本与 `run_full.py` 已打包为一个 gzip 压缩 zip 的 base64 载荷，**避免命令行长度限制**。请在工作区根目录执行以下还原命令，得到 `protocols/vision_pipeline.py`、`protocols/run_experiments.py`、`protocols/run_full.py`：

```
python -c "import base64,io,zipfile,pathlib; pathlib.Path('payload.b64').write_text('PAYLOAD_PLACEHOLDER'); zipfile.ZipFile(io.BytesIO(base64.b64decode(pathlib.Path('payload.b64').read_text()))).extractall('.')"
python -c "import shutil,pathlib; p=pathlib.Path('project/protocols'); p.mkdir(parents=True,exist_ok=True); [shutil.copy(f,p/f.name) for f in pathlib.Path('protocols').glob('*.py')]"
```

还原后先做语法检查 `python -m py_compile protocols/*.py`，再按第 4 节跑 `python protocols/run_full.py 2>&1 | tee project/logs/run.log`（先建 `project/logs/`）。把 `payload.b64` 也复制一份到 `project/` 作为可复现附件。

**载荷已内嵌在上一条还原命令中，无需另行替换**。

"""
query = header + decode_note.replace("PAYLOAD_PLACEHOLDER", payload) + \
    "\n按第 0 节的输出契约交付，最终回复给出实际数值摘要。\n"
(R / "novix" / "query-full.txt").write_text(query, encoding="utf-8")
(R / "novix" / "payload.b64").write_text(payload, encoding="ascii")
print("query_bytes", len(query.encode("utf-8")), "payload_b64_len", len(payload),
      "scripts_bytes", len(vp) + len(rx) + len(run_full))
