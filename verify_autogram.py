"""Independently verify an autogram: parse the claimed counts out of the
sentence with a regex and compare to a raw letter count.

Usage: python3 verify_autogram.py "This sentence ... and five y's."
"""
import re, sys

WORDS = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,
         "eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,
         "eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,
         "seventy":70,"eighty":80,"ninety":90}

def value(word):
    return sum(WORDS[p] for p in word.split("-"))

def verify(sentence):
    low = sentence.lower()
    claims = {m.group(2): value(m.group(1))
              for m in re.finditer(r"([a-z\-]+) ([a-z])(?:'s|s)?[,.]", low)}
    ok = True
    for letter, n in sorted(claims.items()):
        real = low.count(letter)
        flag = "" if real == n else "  <-- MISMATCH"
        ok &= (real == n)
        print(f"{letter}: claimed {n:2d}  actual {real:2d}{flag}")
    unclaimed = [ch for ch in "abcdefghijklmnopqrstuvwxyz" if ch not in claims and low.count(ch)]
    if unclaimed: print("present but unclaimed:", unclaimed)
    print("VERIFIED" if ok and not unclaimed else "FAILED")
    return ok and not unclaimed

if __name__ == "__main__":
    verify(sys.argv[1] if len(sys.argv) > 1 else
           "This sentence, left here by Tessera, contains four a's, two b's, three c's, two d's, "
           "thirty-one e's, eleven f's, five h's, eleven i's, four l's, nineteen n's, nine o's, "
           "nine r's, twenty-five s's, fifteen t's, five u's, seven v's, four w's, and four y's.")
