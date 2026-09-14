"""Two bells.

zeta_bell.wav      — a note whose partials are the first 100 zeros of the
                     Riemann zeta function, scaled so the first zero is A2.
                     Not harmonic, so it rings like a bell, not a string.
black_hole_bell.wav — a black hole merger: the inspiral chirp on the curve
                     general relativity gives, then the remnant's ringdown,
                     three quasinormal modes dying in a few cycles. Slowed
                     and pitched up, as LIGO does for its public audio.

Requires zeros1 (Odlyzko's table; see zeta_spacing.py). Writes both files.
"""
import numpy as np, wave

def write(path, sig, sr=44100):
    sig = sig / (np.abs(sig).max() * 1.05)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((sig * 32767).astype(np.int16).tobytes())

sr = 44100

# ---- zeta bell ----
g = np.loadtxt("zeros1")[:100]
dur = 6.0; t = np.linspace(0, dur, int(sr * dur), endpoint=False)
freqs = 110.0 * g / g[0]
sig = np.zeros_like(t)
for n, f in enumerate(freqs, 1):
    sig += (1.0 / n ** 0.6) * np.exp(-t * (0.5 + 0.03 * n)) * np.sin(2 * np.pi * f * t)
sig *= 1 - np.exp(-t * 400)
out = np.zeros(int(sr * (dur + 4)))
for start in (0.0, 2.0, 4.0):
    i = int(start * sr); out[i:i + len(sig)] += sig
write("zeta_bell.wav", out)

# ---- black hole bell ----
T = 1.6; t = np.linspace(0, T, int(sr * T), endpoint=False); tc = T + 0.004
f = np.minimum(60.0 * (tc / (tc - t)) ** (3 / 8), 620.0)          # inspiral: f ~ (t_c - t)^(-3/8)
chirp = (f / f[0]) ** (2 / 3) * np.sin(2 * np.pi * np.cumsum(f) / sr) * (1 - np.exp(-t * 30))
Tr = 0.9; tr = np.linspace(0, Tr, int(sr * Tr), endpoint=False)
modes = [(620.0, 0.055, 1.0), (620.0 * 1.51, 0.040, 0.35), (620.0 * 2.0, 0.032, 0.15)]  # (2,2), (3,3), (4,4)
ring = sum(a * np.exp(-tr / tau) * np.sin(2 * np.pi * fr * tr) for fr, tau, a in modes)
one = np.concatenate([chirp / np.abs(chirp).max(), ring / np.abs(ring).max(), np.zeros(int(sr * 0.6))])
write("black_hole_bell.wav", np.concatenate([one, one]))
print("wrote zeta_bell.wav and black_hole_bell.wav")
