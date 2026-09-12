\\ random short-Weierstrass curves with conductor in [lo,hi]; write N, root number, order of vanishing, zeros
ellfam(lo, hi, T, want, file, seed) = {
  my(n = 0, seen = Map(), tries = 0);
  setrand(seed);
  while (n < want && tries < 200000,
    tries++;
    my(a = random(121) - 60, b = random(801) - 400);
    if (4*a^3 + 27*b^2 == 0, next);
    my(E = ellminimalmodel(ellinit([0, 0, 0, a, b])), N = ellglobalred(E)[1]);
    if (N < lo || N > hi, next);
    my(key = Str(N, ":", ellap(E,2), ":", ellap(E,3), ":", ellap(E,5), ":", ellap(E,7), ":", ellap(E,11), ":", ellap(E,13)));
    if (mapisdefined(seen, key), next);
    mapput(seen, key, 1);
    my(L = lfuncreate(E), w = ellrootno(E), r = lfunorderzero(L), z = lfunzeros(L, T));
    write(file, N, " ", w, " ", r, " ", z);
    n++);
  n;
}
