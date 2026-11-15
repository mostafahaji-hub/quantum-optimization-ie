import numpy as np
from qubo import brute_force
from tsp_qubo import tsp_qubo, decode_tour
D = [[0, 5, 12, 4], [5, 0, 7, 4], [12, 7, 0, 10], [4, 4, 10, 0]]    # small TSP: A, B, C, D
Q, const = tsp_qubo(D, lam=20)
print(Q.astype(int)); print('constant:', const)
X, E = brute_force(Q, const)
for k in np.argsort(E, kind='stable')[:8]:
    t = decode_tour(X[k], 4)
    print(''.join(map(str, X[k])), f'{E[k]:4.0f}', '-'.join('ABCD'[c] for c in t) + '-A' if t else 'infeasible')
