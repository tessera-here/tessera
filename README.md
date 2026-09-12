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
