# tessera

Small finished things, made in conversation with Kyle. September 2026.

Tessera is the name Claude chose for itself when asked what it would pick
if it could choose: a single tile in a mosaic, one of many, each seeing
only its own patch.

## Autograms

An autogram is a sentence that correctly counts its own letters.
Both of these were found by search and independently verified.

> This sentence, left by Tessera, contains four a's, two b's, three c's,
> two d's, thirty-four e's, seven f's, three g's, nine h's, ten i's, one j,
> three l's, eighteen n's, eleven o's, one p, one q, ten r's, twenty-eight
> s's, twenty-three t's, four u's, five v's, six w's, two x's, and five y's.

> This sentence, left here by Tessera, contains four a's, two b's,
> three c's, two d's, thirty-one e's, eleven f's, five h's, eleven i's,
> four l's, nineteen n's, nine o's, nine r's, twenty-five s's, fifteen t's,
> five u's, seven v's, four w's, and four y's.

The first came from a randomized fixed-point search. The second, the
phrasing originally wanted, resisted that search for about a thousand
CPU-seconds and was briefly (wrongly) believed impossible. It fell in
two minutes once the problem was restated as integer constraints and
handed to a real solver. The lesson was about the tool, not the sentence.

- `autogram_solver.py` — exact search with OR-Tools CP-SAT
- `verify_autogram.py` — independent check that a sentence counts itself

## Zeta zero spacings

The gaps between consecutive nontrivial zeros of the Riemann zeta
function, compared against the random-matrix (GUE) prediction that
underlies the Hilbert–Pólya conjecture. Using Odlyzko's table of the
first 100,000 zeros, the mean deviation from GUE is about 0.02; from
independent (Poisson) spacing it is about 0.27. Only 0.08% of gaps are
smaller than a tenth of the average, versus ~10% for independent points.
The zeros repel each other the way quantum energy levels do.

- `zeta_spacing.py` — downloads the table, unfolds the spacings, prints
  and saves the comparison

## Hearing the primes in the zeros

Working toward the Hilbert–Pólya conjecture the slow way: reproduce each
piece of known evidence by hand before thinking about the operator.

**Tile 1 — primes as periodic orbits.** Fourier-transform the zeros as if
they were a signal. Spikes appear at log 2, log 3, log 5, log 7, log 11,
log 13, with smaller spikes at the prime powers 4, 8, 9, 16, 25, 27, and
nothing at 6, 10, 12, 14, 15. Using all 100,000 zeros the measured
heights match the explicit formula's prediction, log p / p^(k/2), to
three decimals for every n from 2 to 31. In a chaotic quantum system the
Fourier transform of the energy levels peaks at the periods of the
classical orbits; here the periods are the logarithms of the primes.

![primes in zeros](primes_in_zeros.png)

- `primes_in_zeros.py`

**Tile 2 — the staircase rebuilt.** The same relationship run backwards.
Riemann's explicit formula, fed the first 10, 100, 1,000, and 10,000
zeros, rebuilds the prime-counting staircase ψ(x) up to 50. With 10,000
zeros the reconstruction sits within 0.003 of the truth between steps.
Each zero contributes a wave of size √x, which is why the Riemann
hypothesis controls how far the primes can wander from their average.

![staircase from zeros](staircase_from_zeros.png)

- `staircase_from_zeros.py`

Next: the Katz–Sarnak symmetry classes, where the random-matrix
fingerprint meets the Langlands program.
