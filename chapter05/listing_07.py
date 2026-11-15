# Chapter 5, code listing 7 (in order of appearance)
from alg import *
from shop import code, twt
f = lambda s: twt(code[s]) if s in code else None   # None = invalid code
marked = lambda s: f(s) is not None and f(s) <= 8
psi = grover(marked, n=3, k=1)
for s, p in probs(psi).items():
    print(s, p, code.get(s, 'invalid'), f(s))