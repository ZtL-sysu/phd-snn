[2026-11-11 12:36:19] teacher_probe start config_hash=4238b0dc8d31 exps=['T0', 'T2'] datasets=['MNIST', 'CIFAR10'] seeds=[0, 1, 2, 3, 4]
[2026-11-11 12:37:23] A T0 MNIST seed0 teacher_full=68.20 point=33.45 wall=64.2s
[2026-11-11 12:38:25] A T0 MNIST seed1 teacher_full=62.95 point=32.55 wall=61.5s
[2026-11-11 12:39:23] A T0 MNIST seed2 teacher_full=65.75 point=40.25 wall=58.7s

## 本机修正（14:5x，响应 novix 端只读审计）
- `pick_strong()` 改用 `teacher_val`（validation 精度）选 T4/T5，不再用 test 上的 `teacher_at_working_point`；`run_all.py` 新增该列。旧 CSV 已归档为 `teacher_probe_pre_valfix.csv`（schema 变化），A 重跑。
- 能量：新增 `cons_prompt()`，按提示词口径 `R_cons = MAC·4.6/(0.9·S·H + 4.6·S·d̄·C)` 重算 B/C/D 的保守倍率；`convert_f64` 的 `0.9·S·H + 4.6·T·E·C` 口径保留给论文，不改写既有结果。两套口径差异在此备案。
- 其余审计发现（config_hash 绑定、snapshot 不可变、test-once、float64 输入源自 float32）记录但不阻塞执行，由 novix 端 `AUDIT_NOTES.md` 承载。
[2026-11-11 14:44:45] teacher_probe start config_hash=4238b0dc8d31 exps=['T0', 'T2'] datasets=['MNIST', 'CIFAR10'] seeds=[0, 1, 2, 3, 4]
[2026-11-11 14:45:39] A T0 MNIST seed0 teacher_full=67.50 point=32.60 wall=53.3s
[2026-11-11 14:46:28] A T0 MNIST seed1 teacher_full=64.10 point=31.70 wall=49.1s
[2026-11-11 14:47:17] A T0 MNIST seed2 teacher_full=66.45 point=36.30 wall=49.2s
[2026-11-11 14:48:06] A T0 MNIST seed3 teacher_full=66.35 point=34.15 wall=49.3s
[2026-11-11 14:48:55] A T0 MNIST seed4 teacher_full=65.30 point=34.30 wall=49.3s
[2026-11-11 14:50:18] A T0 CIFAR10 seed0 teacher_full=33.45 point=26.65 wall=82.8s
[2026-11-11 14:51:41] A T0 CIFAR10 seed1 teacher_full=33.65 point=25.85 wall=82.5s
[2026-11-11 14:53:03] A T0 CIFAR10 seed2 teacher_full=35.05 point=28.00 wall=81.9s
[2026-11-11 14:54:24] A T0 CIFAR10 seed3 teacher_full=35.40 point=26.60 wall=81.6s
[2026-11-11 14:55:46] A T0 CIFAR10 seed4 teacher_full=37.35 point=27.90 wall=81.7s
[2026-11-11 14:56:12] A T2 MNIST seed0 teacher_full=66.80 point=66.80 wall=25.5s
[2026-11-11 14:56:37] A T2 MNIST seed1 teacher_full=63.20 point=63.20 wall=25.3s
[2026-11-11 14:57:02] A T2 MNIST seed2 teacher_full=66.30 point=66.30 wall=25.5s
[2026-11-11 14:57:28] A T2 MNIST seed3 teacher_full=66.25 point=66.25 wall=25.4s
[2026-11-11 14:57:53] A T2 MNIST seed4 teacher_full=66.35 point=66.35 wall=25.3s
[2026-11-11 14:58:35] A T2 CIFAR10 seed0 teacher_full=33.10 point=33.10 wall=42.4s
[2026-11-11 14:59:18] A T2 CIFAR10 seed1 teacher_full=34.80 point=34.80 wall=42.4s
[2026-11-11 15:00:00] A T2 CIFAR10 seed2 teacher_full=34.65 point=34.65 wall=41.9s
[2026-11-11 15:00:42] A T2 CIFAR10 seed3 teacher_full=35.70 point=35.70 wall=42.0s
[2026-11-11 15:01:24] A T2 CIFAR10 seed4 teacher_full=36.15 point=36.15 wall=42.1s
[2026-11-11 15:01:24] experiment A done
[2026-11-11 18:22:43] teacher_probe start config_hash=4238b0dc8d31 exps=['T1', 'T3', 'T4', 'T5'] datasets=['MNIST', 'CIFAR10'] seeds=[0, 1, 2, 3, 4]
[2026-11-11 22:06:37] A T1 MNIST seed0 teacher_full=70.15 point=32.45 wall=13433.3s
[2026-11-12 01:44:39] A T1 MNIST seed1 teacher_full=64.95 point=32.50 wall=13082.6s
