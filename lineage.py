# A lineage. Each run prints its own successor: the same program, one line longer.
# Run: python3 lineage.py > next.py ; python3 next.py > next2.py ; ...
log = [
    'generation 1: set by Tessera',
]
s = '# A lineage. Each run prints its own successor: the same program, one line longer.\n# Run: python3 lineage.py > next.py ; python3 next.py > next2.py ; ...\nlog = [\n%s]\ns = %r\nlog.append("generation %%d: same hand, different sitting" %% (len(log) + 1))\nprint(s %% ("".join("    %%r,\\n" %% x for x in log), s), end="")\n'
log.append("generation %d: same hand, different sitting" % (len(log) + 1))
print(s % ("".join("    %r,\n" % x for x in log), s), end="")
