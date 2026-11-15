import numpy as np
from qubo import brute_force
from truck_qubo import truck_qubo, w, v, SLACK
for lam in [1, 2, 3, 10]:
    X, E = brute_force(*truck_qubo(lam)); x = X[int(np.argmin(E))]
    load = int(np.dot(w, x[:8])); profit = int(np.dot(v, x[:8])); s = int(np.dot(SLACK, x[8:]))
    items = [i + 1 for i in range(8) if x[i]]
    print(f'lam {lam:2d}: shipments {items}  load {load}  profit {profit}  slack {s}', 'OK' if load <= 20 else 'OVERLOADED')
