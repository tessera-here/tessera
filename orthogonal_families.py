"""Elliptic curves: the orthogonal symmetry types, split by root number.

Random short-Weierstrass curves y^2 = x^3 + ax + b with conductor in
[1000, 30000], one per isogeny class (deduplicated by conductor and
a_p for p <= 13). PARI/GP computes conductor, root number, order of
vanishing at the center, and the low zeros. Zeros are unfolded with the
exact mean counting function for a degree-2 L-function.

Katz–Sarnak limit: root number +1 -> SO(even), density 1 + sin(2pi x)/(2pi x)
(zeros attracted to the center); root number -1 -> SO(odd), a forced
central zero plus density 1 - sin(2pi x)/(2pi x). At these conductors the
odd family behaves; the even family shows a hole at the center instead of
a peak (Miller 2006), and the lowest non-central zero moves outward with
rank: ~0.6 for rank 0, ~1.0 for rank 1, ~1.5 for rank 2.

Requires: PARI/GP (`gp`), numpy, scipy, matplotlib. Runtime ~30 s.
"""
import os, re, subprocess
import numpy as np
from scipy.special import loggamma

if not os.path.exists("ell_zeros.txt"):
    print("computing elliptic curve family...")
    subprocess.run(["gp", "-q"], input='read("ell.gp"); print(ellfam(1000, 30000, 8, 5000, "ell_zeros.txt", 11))', text=True)

def unfold(gam, N):
    """Mean number of zeros with 0 < ordinate <= gam for an elliptic curve
    L-function of conductor N (analytic normalization: Gamma(s+1/2), (sqrt N / 2pi)^s)."""
    return (loggamma(1 + 1j * gam).imag + gam * np.log(np.sqrt(N) / (2 * np.pi))) / np.pi

even_all, odd_all, by_rank = [], [], {0: [], 1: [], 2: []}
n_even = n_odd = excess = 0
for line in open("ell_zeros.txt"):
    N, w, r, rest = line.split(" ", 3); N, w, r = int(N), int(w), int(r)
    z = np.array([float(v) for v in re.findall(r"[-\d.]+(?:E-?\d+)?", rest)])
    nz = z[z > 1e-9]                      # drop the zeros at the central point
    if len(nz) == 0: continue
    u = unfold(nz, N)
    if w == 1: n_even += 1; even_all.extend(u); excess += (r >= 2)
    else:      n_odd += 1;  odd_all.extend(u)
    if r in by_rank: by_rank[r].append(u[0])

bins = np.arange(0, 3.05, 0.1); mid = (bins[:-1] + bins[1:]) / 2
he = np.histogram(even_all, bins=bins)[0] / (n_even * 0.1)
ho = np.histogram(odd_all, bins=bins)[0] / (n_odd * 0.1)
print(f"even (root number +1): {n_even} curves, {excess} with rank >= 2; density in first bins:", " ".join(f"{v:.2f}" for v in he[:5]))
print(f"odd  (root number -1): {n_odd} curves; density in first bins:", " ".join(f"{v:.2f}" for v in ho[:5]))
for r in (0, 1, 2):
    a = np.array(by_rank[r]); print(f"lowest non-central zero, rank {r}: {len(a)} curves, mean {a.mean():.3f}, median {np.median(a):.3f}")

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    x = np.linspace(0.001, 3, 600); sinc = np.sin(2 * np.pi * x) / (2 * np.pi * x)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.4), dpi=160)
    ax1.bar(mid, he, width=0.1, color="#2e7d32", alpha=0.6, label=f"root number +1 ({n_even:,} curves)\ncentral zeros of the {excess} rank-2 curves removed")
    ax1.plot(x, 1 + sinc, color="#7a2e0e", lw=1.6, label="SO(even) limit: 1 + sin(2πx)/(2πx)"); ax1.set_title("Even functional equation", fontsize=10)
    ax2.bar(mid, ho, width=0.1, color="#6a1b9a", alpha=0.6, label=f"root number −1 ({n_odd:,} curves)\nforced central zero removed")
    ax2.plot(x, 1 - sinc, color="#7a2e0e", lw=1.6, label="SO(odd) limit: 1 − sin(2πx)/(2πx)"); ax2.set_title("Odd functional equation", fontsize=10)
    for ax in (ax1, ax2):
        ax.plot(x, np.ones_like(x), color="#333", lw=1, ls="--", label="unitary, for reference")
        ax.set_xlim(0, 3); ax.set_ylim(0, 2.2); ax.set_xlabel("unfolded height above the central point"); ax.legend(fontsize=6.5, loc="upper right"); ax.spines[["top", "right"]].set_visible(False)
    ax1.set_ylabel("density of zeros")
    b3 = np.arange(0, 2.55, 0.1); m3 = (b3[:-1] + b3[1:]) / 2
    for r, c in zip((0, 1, 2), ("#2e7d32", "#6a1b9a", "#c62828")):
        a = np.array(by_rank[r]); ax3.bar(m3, np.histogram(a, bins=b3)[0] / (len(a) * 0.1), width=0.1, color=c, alpha=0.5, label=f"rank {r}: {len(a):,} curves, mean {a.mean():.2f}")
    ax3.set_xlim(0, 2.5); ax3.set_xlabel("unfolded height of the lowest non-central zero"); ax3.set_ylabel("density")
    ax3.set_title("The zeros know the rank", fontsize=10); ax3.legend(fontsize=7); ax3.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Elliptic curves, conductor 1000–30000: orthogonal families, and a finite-conductor surprise", fontsize=12)
    plt.tight_layout(); plt.savefig("orthogonal_families.png"); print("saved orthogonal_families.png")
except ImportError:
    print("matplotlib not available; skipped the picture")
