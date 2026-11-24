=== watch 21247 start 2026-11-11T13:00:13.502618 ===
Rule: terminal requires parsed status + finalReply + pullable project/result.json + SHA.
[13:00:22] probe 1: rc=0/0 status=processing steps=1 reply=False backend=processing placement=submitted node=aliyun-hz-exp-4090-1
[2026-11-11 13:05:01] === hardened watch 21247 start; interval=180s max=120 ===
[2026-11-11 13:05:01] 20049 countermeasures: queue-stall 15min / steps-stall 20min / 429+unrecognized_model immediate alarm / out-of-band authoritative / terminal = parsed status + finalReply + pullable result.json + SHA
[2026-11-11 13:06:08] probe 1: rc=4/0 status= steps=None reply=False backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:11:16] probe 2: rc=0/124 status=processing steps=71 reply=True backend=None err=None placement=None node=None pool=None/paused=None
[2026-11-11 13:15:25] probe 3: rc=4/0 status= steps=None reply=False backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:18:38] probe 4: rc=0/0 status=processing steps=161 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:21:55] probe 5: rc=0/0 status=processing steps=161 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:25:07] probe 6: rc=0/0 status=processing steps=163 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:28:19] probe 7: rc=0/0 status=processing steps=176 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:31:30] probe 8: rc=0/0 status=processing steps=177 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:34:45] probe 9: rc=0/0 status=processing steps=177 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:39:00] probe 10: rc=4/0 status= steps=None reply=False backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:42:11] probe 11: rc=0/0 status=processing steps=180 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:45:25] probe 12: rc=0/0 status=processing steps=182 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:48:36] probe 13: rc=0/0 status=processing steps=184 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 13:54:12] probe 14: rc=0/124 status=processing steps=188 reply=True backend=None err=None placement=None node=None pool=None/paused=None
[2026-11-11 13:58:44] probe 15: rc=4/0 status= steps=None reply=False backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:01:58] probe 16: rc=0/0 status=processing steps=197 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:07:05] probe 17: rc=0/124 status=processing steps=197 reply=True backend=None err=None placement=None node=None pool=None/paused=None
[2026-11-11 14:10:18] probe 18: rc=0/0 status=processing steps=201 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:13:30] probe 19: rc=0/0 status=processing steps=201 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:16:41] probe 20: rc=0/0 status=processing steps=201 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:19:54] probe 21: rc=0/0 status=processing steps=201 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:24:03] probe 22: rc=4/0 status= steps=None reply=False backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:27:26] probe 23: rc=0/0 status=processing steps=201 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:30:42] probe 24: rc=0/0 status=processing steps=201 reply=True backend=processing err= placement=submitted node=aliyun-hz-exp-4090-1 pool=2/paused=False
[2026-11-11 14:30:42] ALERT STEPS_STALL: steps frozen at 201 for >20 min; backend=processing placement=submitted
[2026-11-11 14:38:54] === v3 watch 21247 start; interval=180s max=120 ===
[2026-11-11 14:38:54] v2 STEPS_STALL at 201 was a FALSE POSITIVE (steps 201->203, project mtimes advancing). v3: data-plane workspace stamp is primary; steps-stall needs 45min AND frozen workspace.
[2026-11-11 14:41:16] probe 1: rc=0/0 status=processing steps=203 backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 14:44:45] === v3 watch 21247 start; interval=180s max=120 ===
[2026-11-11 14:44:45] v2 STEPS_STALL at 201 was a FALSE POSITIVE (steps 201->203, project mtimes advancing). v3: data-plane workspace stamp is primary; steps-stall needs 45min AND frozen workspace.
[2026-11-11 14:46:10] probe 1: rc=0/0 status=processing steps=205 backend=processing err= placement=submitted stamp=2026-11-11T06:41:42 pool=2
[2026-11-11 14:51:01] probe 2: rc=0/0 status=processing steps=207 backend=processing err= placement=submitted stamp=2026-11-11T06:47:33 pool=2
[2026-11-11 14:55:47] probe 3: rc=0/2 status=processing steps=207 backend=None err=None placement=None stamp=None pool=None
[2026-11-11 14:59:39] probe 4: rc=0/2 status=processing steps=213 backend=None err=None placement=None stamp=None pool=None
[2026-11-11 15:05:13] probe 5: rc=0/0 status=processing steps=214 backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 15:08:53] probe 6: rc=0/0 status=processing steps=216 backend=processing err= placement=submitted stamp=2026-11-11T06:58:09 pool=2
[2026-11-11 15:12:40] probe 7: rc=0/2 status=processing steps=222 backend=None err=None placement=None stamp=2026-11-11T06:58:09 pool=None
[2026-11-11 15:16:20] probe 8: rc=0/0 status=processing steps=224 backend=processing err= placement=submitted stamp=2026-11-11T06:58:09 pool=2
[2026-11-11 15:19:54] probe 9: rc=0/2 status=processing steps=228 backend=None err=None placement=None stamp=2026-11-11T06:58:09 pool=None
[2026-11-11 15:23:19] probe 10: rc=0/0 status=processing steps=240 backend=processing err= placement=submitted stamp=2026-11-11T06:58:09 pool=2
[2026-11-11 15:26:42] probe 11: rc=0/0 status=processing steps=240 backend=processing err= placement=submitted stamp=2026-11-11T06:58:09 pool=2
[2026-11-11 15:30:10] probe 12: rc=0/2 status=processing steps=250 backend=None err=None placement=None stamp=2026-11-11T07:28:37 pool=None
[2026-11-11 15:36:46] probe 13: rc=4/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 15:40:18] probe 14: rc=0/0 status=processing steps=278 backend=processing err= placement=submitted stamp=2026-11-11T07:35:43 pool=2
[2026-11-11 15:47:12] probe 15: rc=0/124 status=processing steps=278 backend=None err=None placement=None stamp=2026-11-11T07:45:37 pool=None
[2026-11-11 15:51:02] probe 16: rc=0/0 status=processing steps=282 backend=processing err= placement=submitted stamp=2026-11-11T07:47:06 pool=2
[2026-11-11 15:56:33] probe 17: rc=0/124 status=processing steps=284 backend=None err=None placement=None stamp=None pool=None
[2026-11-11 15:59:59] probe 18: rc=0/0 status=processing steps=292 backend=processing err= placement=submitted stamp=2026-11-11T07:55:19 pool=2
[2026-11-11 16:03:30] probe 19: rc=0/2 status=processing steps=298 backend=None err=None placement=None stamp=2026-11-11T08:02:12 pool=None
[2026-11-11 16:10:05] probe 20: rc=4/124 status= steps=None backend=None err=None placement=None stamp=2026-11-11T08:03:38 pool=None
[2026-11-11 16:13:32] probe 21: rc=0/0 status=processing steps=304 backend=processing err= placement=submitted stamp=2026-11-11T08:03:38 pool=2
[2026-11-11 16:17:00] probe 22: rc=0/0 status=processing steps=306 backend=processing err= placement=submitted stamp=2026-11-11T08:03:38 pool=2
[2026-11-11 16:22:20] probe 23: rc=0/0 status=processing steps=308 backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 16:25:50] probe 24: rc=0/2 status=processing steps=310 backend=None err=None placement=None stamp=2026-11-11T08:03:38 pool=None
[2026-11-11 16:29:09] probe 25: rc=0/0 status=processing steps=333 backend=processing err= placement=submitted stamp=2026-11-11T08:27:21 pool=2
[2026-11-11 16:32:49] probe 26: rc=0/0 status=processing steps=333 backend=processing err= placement=submitted stamp=2026-11-11T08:32:20 pool=2
[2026-11-11 16:42:03] probe 27: rc=0/124 status=processing steps=398 backend=None err=None placement=None stamp=None pool=None
[2026-11-11 16:51:18] probe 28: rc=124/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:00:23] probe 29: rc=0/0 status=processing steps=1864 backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:04:44] probe 30: rc=0/0 status=processing steps=1935 backend=processing err= placement=submitted stamp=2026-11-11T08:48:47 pool=2
[2026-11-11 17:12:28] probe 31: rc=124/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:17:40] probe 32: rc=0/0 status=processing steps=2346 backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:23:36] probe 33: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:30:00] probe 34: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:35:40] probe 35: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=2026-11-11T09:30:06 pool=2
[2026-11-11 17:41:50] probe 36: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:47:37] probe 37: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 17:54:25] probe 38: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
[2026-11-11 18:01:18] probe 39: rc=1/2 status= steps=None backend=None err=None placement=None stamp=None pool=None
[2026-11-11 18:07:15] probe 40: rc=1/0 status= steps=None backend=processing err= placement=submitted stamp=None pool=2
