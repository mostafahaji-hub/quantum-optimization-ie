# Chapter 7, code listing 10 (in order of appearance)
import numpy as np, time
from algs import KA, GA, QEA, QIGA, QTS, QPSO, QKA
from prob20 import twt, n, p, w
wspt = twt(sorted(range(n), key=lambda j: p[j] / w[j]))
res = {}
for name, A in [('KA', KA), ('GA', GA), ('QEA', QEA), ('QIGA', QIGA), ('QTS', QTS), ('QPSO', QPSO), ('QKA', QKA)]:
    t0 = time.time(); vals = [A(s) for s in range(10)]; res[name] = vals
    print(f'{name:5s} best {min(vals):4d}  mean {np.mean(vals):6.1f}  worst {max(vals):4d}  ({time.time()-t0:.1f} s)')
best_known = min(min(v) for v in res.values())
print('WSPT', wspt, ' best known', best_known)
for name, vals in res.items():
    print(f'{name:5s} mean RPD = {100*(np.mean(vals)-best_known)/best_known:5.1f}%')