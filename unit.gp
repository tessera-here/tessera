unitfam(q, T, file) = {
  my(G = znstar(q, 1), n = 0);
  for (k = 1, q - 2,
    if (k != (q - 1) / 2,           \\ skip the one real (quadratic) character
      my(L = lfuncreate([G, [k]]), a = if (zncharisodd(G, [k]), 1, 0));
      write(file, q, " ", k, " ", a, " ", lfunzeros(L, T));
      n++));
  n;
}
