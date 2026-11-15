import numpy as np
from qubo import brute_force
from crossdock_qubo import crossdock_qubo
for lam in [24, 25, 26]:
    X, E = brute_force(*crossdock_qubo(lam)); o = np.argsort(E, kind='stable')
    print(f'lam {lam}:', [(''.join(map(str, X[k])), int(E[k])) for k in o[:2]])
