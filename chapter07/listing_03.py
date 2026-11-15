# Chapter 7, code listing 3 (in order of appearance)
import numpy as np
from ka_perm import keshtel_perm
from shop8 import twt
res = []
for s in range(10):
    val, order = keshtel_perm(twt, 8, budget=3000, n_pop=20, pn1=0.2, pn2=0.4, n_swirl=5, seed=s)
    res.append(val)
    if s == 0:
        print('run 0:', ['J%d' % (j + 1) for j in order], 'TWT', val)
print('10 runs:', res)
print('optimum 58 found in', res.count(58), 'of 10 runs (3000 evaluations each, as QEA in Chapter 6)')