\\ zeros of L(s, chi_D) for fundamental discriminants, |D| in [lo, hi], up to height T
quadfam(lo, hi, T, file) = {
  my(n = 0);
  for (a = lo, hi,
    foreach([a, -a], D,
      if (isfundamental(D),
        my(z = lfunzeros(lfuncreate(D), T));
        write(file, D, " ", z);
        n++)));
  n;
}
