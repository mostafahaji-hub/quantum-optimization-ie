import numpy as np
from qubo import brute_force
from shop_qubo import shop_qubo, decode_schedule, VARS
print('variables:', len(VARS), ' bit strings:', 2 ** len(VARS))
for lam in [5, 6, 20]:
    X, E = brute_force(*shop_qubo(lam)); x = X[int(np.argmin(E))]; r = decode_schedule(x)
    if r: print(f'lam {lam:2d}: value {E.min():.0f}  order', ['J%d' % (j + 1) for j in r[0]], ' start times', {'J%d' % (j + 1): t for j, t in r[1].items()})
    else: print(f'lam {lam:2d}: value {E.min():.0f}  infeasible:', [('J%d' % (j + 1), t) for b, (j, t) in zip(x, VARS) if b])
