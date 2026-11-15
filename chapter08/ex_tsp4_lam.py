import numpy as np
from qubo import brute_force
from tsp_qubo import tsp_qubo, decode_tour
D = [[0, 5, 12, 4], [5, 0, 7, 4], [12, 7, 0, 10], [4, 4, 10, 0]]
for lam in [5, 8, 9, 10, 12]:
    X, E = brute_force(*tsp_qubo(D, lam)); k = int(np.argmin(E)); t = decode_tour(X[k], 4)
    print(f'lam {lam:2d}: best value {E[k]:4.0f}', '-'.join('ABCD'[c] for c in t) + '-A' if t else ''.join(map(str, X[k])) + ' infeasible')
