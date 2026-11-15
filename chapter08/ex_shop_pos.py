import numpy as np
from qubo import brute_force
from shop_pos_qubo import shop_pos_qubo
X, E = brute_force(*shop_pos_qubo(lam=20))
for k in np.argsort(E, kind='stable')[:7]:
    M = X[k].reshape(3, 3)                                   # rows: jobs, columns: positions
    ok = (M.sum(0) == 1).all() and (M.sum(1) == 1).all()
    order = ' '.join('J%d' % (np.argmax(M[:, c]) + 1) for c in range(3)) if ok else 'infeasible'
    print(''.join(map(str, X[k])), f'{E[k]:3.0f}', order)
