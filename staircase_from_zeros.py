"""Rebuild the prime staircase from the zeros.

Riemann's explicit formula for the Chebyshev function
    psi(x) = sum of log p over prime powers p^k <= x
is
    psi(x) = x - sum_rho x^rho / rho - log(2 pi) - (1/2) log(1 - x^-2)
where rho runs over the nontrivial zeros. Feeding it the first N zeros
and watching the steps sharpen as N grows is the primes-from-zeros
direction of the same relationship that primes_in_zeros.py shows the
other way round.

Data: Odlyzko's table of the first 100,000 zeros (downloaded on first run).
"""
import os, urllib.request
import numpy as np

URL = "https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1"
FILE = "zeros1"
if not os.path.exists(FILE):
    print("downloading", URL); urllib.request.urlretrieve(URL, FILE)
g = np.loadtxt(FILE)

def isprime(n): return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))

XMAX = 50
X = np.arange(1.5, XMAX + 0.001, 0.01)
jumps = {}
for p in range(2, XMAX + 1):
    if isprime(p):
        m = p
        while m <= XMAX: jumps[m] = np.log(p); m *= p
psi_true = np.array([sum(v for n, v in jumps.items() if n <= x) for x in X])

def psi_from_zeros(N):
    gam = g[:N]; L = np.log(X); s = np.zeros_like(X)
    for i in range(0, N, 2000):
        gg = gam[i:i + 2000]
        s += ((0.5 * np.cos(np.outer(L, gg)) + gg * np.sin(np.outer(L, gg))) / (0.25 + gg ** 2)).sum(axis=1)
    return X - 2 * np.sqrt(X) * s - np.log(2 * np.pi) - 0.5 * np.log(1 - X ** -2)

away = np.array([min(abs(x - j) for j in jumps) > 0.2 for x in X])
results = {}
for N in [10, 100, 1000, 10000]:
    est = psi_from_zeros(N); err = np.abs(est - psi_true)[away].mean(); results[N] = (est, err)
    print(f"{N:6d} zeros  mean error away from jumps: {err:.4f}")

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), dpi=160, sharex=True, sharey=True)
    for ax, (N, (est, err)) in zip(axes.flat, results.items()):
        ax.step(X, psi_true, where="post", color="#999", lw=1.2, label="true ψ(x): sum of log p over prime powers ≤ x")
        ax.plot(X, est, color="#1f4e79", lw=1.0, label=f"rebuilt from the first {N:,} zeros")
        ax.set_title(f"{N:,} zeros    (mean error between steps: {err:.3f})", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        if N == 10: ax.legend(fontsize=8, loc="upper left")
    for ax in axes[1]: ax.set_xlabel("x")
    for ax in axes[:, 0]: ax.set_ylabel("ψ(x)")
    fig.suptitle("Riemann's explicit formula: the prime staircase rebuilt from zeta zeros", fontsize=12)
    plt.tight_layout(); plt.savefig("staircase_from_zeros.png"); print("saved staircase_from_zeros.png")
except ImportError:
    print("matplotlib not available; skipped the picture")
