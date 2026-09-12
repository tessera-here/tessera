"""Nearest-neighbor spacing of Riemann zeta zeros vs. random-matrix theory.

Downloads Odlyzko's table of the first 100,000 nontrivial zeros, unfolds
the gaps by the local density log(t/2pi)/(2pi), and compares the spacing
histogram to the GUE Wigner surmise and to Poisson (independent) spacing.
"""
import os, urllib.request, json
import numpy as np

URL = "https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1"
FILE = "zeros1"

if not os.path.exists(FILE):
    print("downloading", URL); urllib.request.urlretrieve(URL, FILE)

z = np.loadtxt(FILE)
gaps = np.diff(z)
density = np.log(z[:-1] / (2 * np.pi)) / (2 * np.pi)
s = gaps * density                                   # normalized spacings, mean ~1

bins = np.arange(0, 3.05, 0.1)
hist, edges = np.histogram(s, bins=bins, density=True)
mid = (edges[:-1] + edges[1:]) / 2
gue = (32 / np.pi**2) * mid**2 * np.exp(-4 * mid**2 / np.pi)   # Wigner surmise (GUE)
poisson = np.exp(-mid)

print(f"zeros: {len(z)}   mean normalized spacing: {s.mean():.4f}")
print(f"fraction of gaps < 0.1: {(s < 0.1).mean():.5f}   (Poisson would give ~{1-np.exp(-0.1):.3f})")
print(f"mean |data - GUE|:     {np.abs(hist - gue).mean():.4f}")
print(f"mean |data - Poisson|: {np.abs(hist - poisson).mean():.4f}")
print("\n  s     data    GUE   Poisson")
for m, h, g, p in zip(mid, hist, gue, poisson):
    print(f"{m:4.2f}  {h:6.3f}  {g:6.3f}  {p:6.3f}")

json.dump({"s": mid.round(2).tolist(), "data": hist.round(4).tolist(),
           "gue": gue.round(4).tolist(), "poisson": poisson.round(4).tolist()},
          open("spacing.json", "w"), indent=1)
