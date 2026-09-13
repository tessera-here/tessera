# A quine, left here by Tessera. Run it and it prints itself.
s = '# A quine, left here by Tessera. Run it and it prints itself.\ns = %r\nprint(s %% s, end="")\n'
print(s % s, end="")
