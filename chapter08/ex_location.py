import numpy as np
from qubo import brute_force
from location_qubo import location_qubo, decode
for lam in [5, 10, 14.5, 14.7, 20]:
    X, E = brute_force(*location_qubo(lam)); k = int(np.argmin(E)); opened, serve, ok = decode(X[k])
    print(f'lam {lam:4}: value {E[k]:5.1f}  open {opened}  customer->warehouse {serve}', 'feasible' if ok else 'INFEASIBLE')
