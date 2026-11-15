import numpy as np
from qubo import brute_force
from supplier import supplier_qubo
Q, const = supplier_qubo(lam=100)
print(Q); print('constant:', const)
for lam in [0, 20, 40, 45, 46, 60, 100]:
    Q, const = supplier_qubo(lam)
    X, E = brute_force(Q, const); i = int(np.argmin(E))
    s = ''.join(map(str, X[i])); ok = 'feasible' if X[i].sum() == 2 else 'INFEASIBLE'
    print(f'lam {lam:3d}: best {s}  value {E[i]:5.0f}  {ok}')
