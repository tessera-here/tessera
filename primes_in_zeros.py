"""Hear the primes in the zeros.

Treat the nontrivial zeros of the Riemann zeta function as a signal and
take its Fourier transform. The explicit formula predicts spikes at
x = k*log(p) for every prime power p^k, with height log(p) / p^(k/2),
and nothing at composites that are not prime powers. This script checks
both the positions and the heights, and draws the picture.

Data: Odlyzko's table of the first 100,000 zeros (downloaded on first run).
"""
import os, urllib.request, json
import numpy as np

URL = "https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1"
FILE = "zeros1"
if not os.path.exists(FILE):
    print("downloading", URL); urllib.request.urlretrieve(URL, FILE)
g_all = np.loadtxt(FILE)

def H_at(xs, g):
    """-(2pi/W) * sum_n w_n cos(gamma_n x) with a Hann window w over [0, T].
    At x = k log p this approximates log(p)/p^(k/2)."""
    T = g[-1]; w = 0.5 * (1 - np.cos(2 * np.pi * g / T)); W = T / 2
    out = np.empty(len(xs))
    for i in range(0, len(xs), 200):
        blk = xs[i:i + 200]
        out[i:i + 200] = -(2 * np.pi / W) * (w[None, :] * np.cos(np.outer(blk, g))).sum(axis=1)
    return out

def isprime(n): return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
def prime_power(n):
    for p in range(2, n + 1):
        if isprime(p):
            k, m = 0, 1
            while m < n: m *= p; k += 1
            if m == n: return p, k
    return None

# 1. Exact check at x = log n, n = 2..31, with all 100,000 zeros.
ns = list(range(2, 32))
meas = H_at(np.log(ns), g_all)
print("using all 100,000 zeros, evaluated exactly at x = log n")
print(" n    predicted   measured")
for n, m in zip(ns, meas):
    pp = prime_power(n)
    pred = np.log(pp[0]) / pp[0] ** (pp[1] / 2) if pp else 0.0
    tag = f"= {pp[0]}^{pp[1]}" if pp and pp[1] > 1 else ("prime" if pp else "")
    print(f"{n:2d}     {pred:6.3f}     {m:6.3f}   {tag}")

# 2. Picture: first 20,000 zeros on a fine grid; keep the max in each small bin
#    so the (very narrow) peaks survive downsampling.
g = g_all[:20000]
fine = np.arange(0.5, 2.75, 0.0002)
Hf = H_at(fine, g)
edges = np.arange(0.5, 2.755, 0.005)
idx = np.digitize(fine, edges) - 1
xs = edges[:-1] + 0.0025
env = np.array([Hf[idx == i].max() if (idx == i).any() else 0 for i in range(len(xs))])
json.dump({"x": xs.round(4).tolist(), "H": env.round(3).tolist()}, open("prime_peaks.json", "w"))

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=160)
    ax.plot(xs, env, color="#1f4e79", lw=1.2); ax.fill_between(xs, 0, env, color="#1f4e79", alpha=0.15)
    for n, lab in {2:"2",3:"3",4:"2²",5:"5",7:"7",8:"2³",9:"3²",11:"11",13:"13"}.items():
        xi = np.log(n); j = np.abs(xs - xi).argmin(); h = env[max(0, j-2):j+3].max()
        ax.annotate(lab, (xi, h), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=10, color="#7a2e0e")
    ax.set_xlim(0.5, 2.75); ax.set_ylim(0, 0.8)
    ax.set_xlabel("frequency x   (a peak at x = log n means the zeros 'contain' n)"); ax.set_ylabel("peak height")
    ax.set_title("The primes, heard in the first 20,000 zeros of the Riemann zeta function")
    ax.text(0.52, 0.72, "predicted height at log p^k:  log p / p^(k/2)", fontsize=9, color="#444")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); plt.savefig("primes_in_zeros.png"); print("saved primes_in_zeros.png")
except ImportError:
    print("matplotlib not available; skipped the picture")
