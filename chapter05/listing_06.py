# Chapter 5, code listing 6 (in order of appearance)
from alg import *
from shop import code, twt
marked = lambda s: s in code and twt(code[s]) <= 5   # only the optimum
for k in range(5):
    psi = grover(marked, n=3, k=k)
    print('iterations', k, ' P(101) =', round(abs(psi[0b101])**2, 3))