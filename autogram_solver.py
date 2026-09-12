"""Exact autogram search using OR-Tools CP-SAT.

An autogram is a sentence that counts its own letters, e.g.
"This sentence contains four a's, ... and five y's."

Usage: python3 autogram_solver.py "This sentence, left by Tessera, contains " [timeout_s] [workers]

Letters with count zero are omitted from the sentence. Counts are bounded
by MAXN; raise it if a solution seems to need larger numbers.
"""
import sys, time
from collections import Counter
from ortools.sat.python import cp_model

ONES = ["zero","one","two","three","four","five","six","seven","eight","nine","ten",
        "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
TENS = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
LETTERS = "abcdefghijklmnopqrstuvwxyz"
MAXN = 60

def num(n):
    if n < 20: return ONES[n]
    t, o = divmod(n, 10)
    return TENS[t] + ("-" + ONES[o] if o else "")

def build(prefix, counts, plural="'s", joiner="and"):
    parts = [f"{num(counts[x])} {x}" + (plural if counts[x] > 1 else "")
             for x in LETTERS if counts[x] > 0]
    return prefix + ", ".join(parts[:-1]) + f", {joiner} " + parts[-1] + "."

def actual(sentence):
    c = Counter(ch for ch in sentence.lower() if ch in LETTERS)
    return {x: c[x] for x in LETTERS}

def solve(prefix, plural="'s", joiner="and", timeout=120, workers=8):
    fixed = Counter(ch for ch in (prefix + joiner).lower() if ch in LETTERS)
    m = cp_model.CpModel()
    c = {y: m.NewIntVar(0, MAXN, f"c{y}") for y in LETTERS}
    for x in LETTERS:
        terms = []
        for y in LETTERS:
            # contribution of letter x from the clause for letter y, as a function of count[y]
            table = []
            for n in range(MAXN + 1):
                k = 0
                if n > 0:
                    k += num(n).count(x) + (1 if x == y else 0)
                    if n > 1: k += plural.count(x)
                table.append(k)
            if any(table):
                e = m.NewIntVar(0, max(table), f"e{x}{y}")
                m.AddElement(c[y], table, e)
                terms.append(e)
        m.Add(c[x] == fixed[x] + sum(terms))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = timeout
    s.parameters.num_workers = workers
    t0 = time.time(); status = s.Solve(m)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        counts = {y: s.Value(c[y]) for y in LETTERS}
        sent = build(prefix, counts, plural, joiner)
        return s.StatusName(status), round(time.time() - t0, 1), sent, actual(sent) == counts
    return s.StatusName(status), round(time.time() - t0, 1), None, None

if __name__ == "__main__":
    prefix = sys.argv[1] if len(sys.argv) > 1 else "This sentence, left by Tessera, contains "
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    status, secs, sent, ok = solve(prefix, timeout=timeout, workers=workers)
    print(f"[{status} in {secs}s]")
    print(sent if sent else "no solution found in time (UNKNOWN) or none exists (INFEASIBLE)")
    if sent: print("self-consistent:", ok)
