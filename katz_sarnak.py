"""Katz–Sarnak: read a family's symmetry type off its lowest zeros.

Two families of Dirichlet L-functions, processed identically:
  symplectic — quadratic characters (D/n), fundamental D, 1000 <= |D| <= 10000
  unitary    — all non-real characters mod the primes 1009, 2003, 3001
Zeros are computed with PARI/GP (lfunzeros), unfolded with the exact mean
counting function of each L-function, and pooled. The symplectic family
should show a hole at the central point (density -> 0); the unitary
family should be flat (density = 1) all the way down.

Requires: PARI/GP on the path (`gp`), numpy, scipy, matplotlib.
Runtime: ~2.5 minutes on one core.
"""
import os, re, glob, subprocess
import numpy as np
from scipy.special import loggamma

def gp(script, call):
    return subprocess.run(["gp", "-q"], input=f'read("{script}"); print({call})',
                          text=True, capture_output=True).stdout

if not os.path.exists("quad_zeros.txt"):
    print("computing quadratic family..."); gp("quad.gp", 'quadfam(1000, 10000, 3, "quad_zeros.txt")')
for q in (1009, 2003, 3001):
    if not os.path.exists(f"unit_zeros_{q}.txt"):
        print(f"computing characters mod {q}..."); gp("unit.gp", f'unitfam({q}, 3, "unit_zeros_{q}.txt")')

def unfold(gam, q, a):
    """Mean number of zeros of L(s,chi) with 0 < ordinate <= gam;
    conductor q, parity a (chi(-1) = (-1)^a)."""
    z = 0.25 + a / 2 + 0.5j * gam
    return (loggamma(z).imag + 0.5 * gam * np.log(q / np.pi)) / np.pi

def parse(s): return np.array([float(v) for v in re.findall(r"[-\d.]+(?:E-?\d+)?", s)])

quad_all, quad_low = [], []
for line in open("quad_zeros.txt"):
    D, rest = line.split(" ", 1); D = int(D); z = parse(rest)
    if len(z): u = unfold(z, abs(D), 0 if D > 0 else 1); quad_all.extend(u); quad_low.append(u[0])
unit_all, unit_low = [], []
for f in glob.glob("unit_zeros_*.txt"):
    for line in open(f):
        q, k, a, rest = line.split(" ", 3); z = parse(rest); z = z[z > 0]
        if len(z): u = unfold(z, int(q), int(a)); unit_all.extend(u); unit_low.append(u[0])
nq, nu = len(quad_low), len(unit_low)
quad_low, unit_low = np.array(quad_low), np.array(unit_low)

bins = np.arange(0, 3.05, 0.1); mid = (bins[:-1] + bins[1:]) / 2
hq = np.histogram(quad_all, bins=bins)[0] / (nq * 0.1)
hu = np.histogram(unit_all, bins=bins)[0] / (nu * 0.1)
print(f"symplectic family: {nq} L-functions; density in first bins:", " ".join(f"{v:.2f}" for v in hq[:5]))
print(f"unitary family:    {nu} L-functions; density in first bins:", " ".join(f"{v:.2f}" for v in hu[:5]))
print(f"lowest zero below 0.2: symplectic {np.mean(quad_low < 0.2):.3f}   unitary {np.mean(unit_low < 0.2):.3f}")

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    x = np.linspace(0.001, 3, 600); Wsp = 1 - np.sin(2 * np.pi * x) / (2 * np.pi * x)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4), dpi=160)
    ax1.bar(mid, hu, width=0.1, color="#999", alpha=0.55, label=f"unitary family: complex characters mod 1009, 2003, 3001  ({nu:,} L-functions)")
    ax1.bar(mid, hq, width=0.1, color="#1f4e79", alpha=0.65, label=f"symplectic family: quadratic characters, 1000 ≤ |D| ≤ 10000  ({nq:,} L-functions)")
    ax1.plot(x, np.ones_like(x), color="#333", lw=1.4, ls="--", label="unitary prediction  W(x) = 1")
    ax1.plot(x, Wsp, color="#7a2e0e", lw=1.6, label="symplectic prediction  W(x) = 1 − sin(2πx)/(2πx)")
    ax1.set_xlim(0, 3); ax1.set_ylim(0, 1.75); ax1.set_xlabel("unfolded height of zero above the central point"); ax1.set_ylabel("density of zeros")
    ax1.set_title("One-level density of low-lying zeros", fontsize=10); ax1.legend(fontsize=6.5, loc="upper right"); ax1.spines[["top", "right"]].set_visible(False)
    b2 = np.arange(0, 2.05, 0.1); m2 = (b2[:-1] + b2[1:]) / 2
    ax2.bar(m2, np.histogram(unit_low, bins=b2)[0] / (nu * 0.1), width=0.1, color="#999", alpha=0.55, label=f"unitary: {100*np.mean(unit_low<0.2):.0f}% have lowest zero below 0.2")
    ax2.bar(m2, np.histogram(quad_low, bins=b2)[0] / (nq * 0.1), width=0.1, color="#1f4e79", alpha=0.65, label=f"symplectic: {100*np.mean(quad_low<0.2):.0f}% have lowest zero below 0.2")
    ax2.set_xlim(0, 2); ax2.set_xlabel("unfolded height of the lowest zero"); ax2.set_ylabel("density")
    ax2.set_title("Where the lowest zero sits", fontsize=10); ax2.legend(fontsize=7); ax2.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Katz–Sarnak: the symmetry type of a family shows in its lowest zeros", fontsize=12)
    plt.tight_layout(); plt.savefig("katz_sarnak.png"); print("saved katz_sarnak.png")
except ImportError:
    print("matplotlib not available; skipped the picture")
