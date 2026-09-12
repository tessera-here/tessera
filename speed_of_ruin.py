"""How fast the ruin spreads.

After the reversal, run the exact and the nudged gas side by side and,
every step, count the cells where they disagree and how far the
disagreement has travelled from the nudge. Run after arrow_of_time.py.
"""
import numpy as np
exec(open("arrow_of_time.py").read().split("# initial state")[0])   # reuse the gas rules
STEPS = 1000
rng = np.random.default_rng(7)
s0 = np.zeros((4, H, W), dtype=bool); s0[:, :, :W//4] = rng.random((4, H, W//4)) < 0.3
s = s0
for t in range(STEPS): s = step_fwd(s)
s = reverse(s)
a = s.copy(); b = s.copy()
ys, xs = np.nonzero(b[E]); i = len(ys)//2; y0, x0 = ys[i], xs[i]
b[E, y0, x0] = False; b[E, y0, (x0+1) % W] = True
yy, xx = np.mgrid[:H, :W]
dy = np.minimum(abs(yy - y0), H - abs(yy - y0)); dx = np.minimum(abs(xx - x0), W - abs(xx - x0))
dist = np.maximum(dy, dx)                       # Chebyshev distance (cells step one lattice unit per tick)
count, r90, rmax = [], [], []
for t in range(1, STEPS + 1):
    a = step_bwd(a); b = step_bwd(b)
    dmg = (a != b).any(axis=0)
    n = int(dmg.sum()); count.append(n)
    if n:
        dd = dist[dmg]; r90.append(float(np.percentile(dd, 90))); rmax.append(int(dd.max()))
    else:
        r90.append(0.0); rmax.append(0)
count, r90, rmax = map(np.array, (count, r90, rmax))
np.savez("spread.npz", count=count, r90=r90, rmax=rmax)
for t in [1, 5, 10, 25, 50, 100, 200, 400, 700, 1000]:
    print(f"t={t:5d}  damaged cells={count[t-1]:6d}  r90={r90[t-1]:6.1f}  rmax={rmax[t-1]:4d}")
# fit the speed on the stretch before the damage wraps around the box
m = (np.arange(1, STEPS+1) >= 50) & (r90 < 100)
v = np.polyfit(np.arange(1, STEPS+1)[m], r90[m], 1)[0]
print("damage speed (r90 slope, cells per step):", round(v, 3), "  lattice light speed = 1.0")
