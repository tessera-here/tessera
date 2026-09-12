"""The arrow of time, in a reversible lattice gas (HPP).

Run: python3 arrow_of_time.py   (about 2 minutes; writes arrow.npz)

Four velocity directions on a square grid. Collisions: two particles
meeting head-on turn 90 degrees. Everything else streams. The rules are
exactly time-reversible in integer arithmetic: reverse all velocities
and run the same rules and the gas retraces its history bit for bit.
"""
import numpy as np, json
rng = np.random.default_rng(7)
H = W = 256; STEPS = 1000; BLOCK = 16
E, Wd, N, S = 0, 1, 2, 3

def collide(s):
    ew = s[E] & s[Wd] & ~s[N] & ~s[S]
    ns = s[N] & s[S] & ~s[E] & ~s[Wd]
    s = s.copy()
    s[E][ew] = s[Wd][ew] = False; s[N][ew] = s[S][ew] = True
    s[N][ns] = s[S][ns] = False; s[E][ns] = s[Wd][ns] = True
    return s
def stream(s):
    return np.stack([np.roll(s[E], 1, axis=1), np.roll(s[Wd], -1, axis=1),
                     np.roll(s[N], -1, axis=0), np.roll(s[S], 1, axis=0)])
def unstream(s):
    return np.stack([np.roll(s[E], -1, axis=1), np.roll(s[Wd], 1, axis=1),
                     np.roll(s[N], 1, axis=0), np.roll(s[S], -1, axis=0)])
def reverse(s): return s[[Wd, E, S, N]]
def step_fwd(s): return stream(collide(s))        # forward step T = S∘C
def step_bwd(s): return collide(stream(s))        # after reversing velocities, T' = C∘S undoes T

def entropy(s):
    n = s.sum(axis=0)
    blocks = n.reshape(H//BLOCK, BLOCK, W//BLOCK, BLOCK).sum(axis=(1, 3)).ravel().astype(float)
    p = blocks / blocks.sum(); p = p[p > 0]
    return float(-(p * np.log(p)).sum())
def left_fraction(s): return float(s[:, :, :W//4].sum() / s.sum())

# initial state: gas packed into the left quarter, random directions, density 0.3 per channel
s0 = np.zeros((4, H, W), dtype=bool)
s0[:, :, :W//4] = rng.random((4, H, W//4)) < 0.3
print("particles:", int(s0.sum()), " max entropy ln(256) =", round(np.log(256), 3))

def run(s, perturb):
    ent, left, snaps = [], [], {}
    for t in range(STEPS):
        if t in (0, STEPS//4, STEPS//2, STEPS): snaps[t] = s.sum(axis=0)
        ent.append(entropy(s)); left.append(left_fraction(s)); s = step_fwd(s)
    snaps[STEPS] = s.sum(axis=0)
    ent.append(entropy(s)); left.append(left_fraction(s))
    s = reverse(s)                                   # flip every velocity
    if perturb:                                      # nudge ONE particle: move it one cell
        ys, xs = np.nonzero(s[E]); i = len(ys)//2
        s[E, ys[i], xs[i]] = False; s[E, ys[i], (xs[i]+1) % W] = True
    for t in range(STEPS):
        s = step_bwd(s); ent.append(entropy(s)); left.append(left_fraction(s))
        if t + 1 in (STEPS//2, STEPS - STEPS//4, STEPS): snaps[STEPS + t + 1] = s.sum(axis=0)
    return np.array(ent), np.array(left), reverse(s), snaps

ent_a, left_a, final_a, snaps_a = run(s0, perturb=False)
ent_b, left_b, final_b, snaps_b = run(s0, perturb=True)
print("exact reversal: returned to the initial state bit-for-bit?", bool(np.array_equal(final_a, s0)))
print("   entropy start/peak/end:", round(ent_a[0],3), round(ent_a.max(),3), round(ent_a[-1],3),
      "  fraction in corner start/mid/end:", round(left_a[0],3), round(left_a[STEPS],3), round(left_a[-1],3))
print("one particle nudged: returned?", bool(np.array_equal(final_b, s0)),
      "  cells that differ from start:", int((final_b != s0).sum()))
print("   entropy start/peak/end:", round(ent_b[0],3), round(ent_b.max(),3), round(ent_b[-1],3),
      "  fraction in corner end:", round(left_b[-1],3))
np.savez("arrow.npz", ent_a=ent_a, ent_b=ent_b, left_a=left_a, left_b=left_b,
         **{f"a{k}": v for k, v in snaps_a.items()}, **{f"b{k}": v for k, v in snaps_b.items()})
