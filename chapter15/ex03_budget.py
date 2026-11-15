"""Example 15.5 - equal budgets on the two 9-bit QUBOs.
Every method sees only f(x); one call of f = one evaluation."""
import json
import numpy as np
import shop9, tsp4
from qubo import energy
from sa import sa_qubo
from bin_algs import random_bin, GA_bin, QEA_bin, KA_bin
from common import evals99
RUNS, BUDGETS = 2000, [25, 50, 100, 200, 400]
algs = {
    'random': lambda f, Q, c, B, s: random_bin(f, 9, B, s)[0],
    'SA':     lambda f, Q, c, B, s: sa_qubo(Q, c, B, s, T0=10,
                                            T_end=1.0)[0],
    'GA':     lambda f, Q, c, B, s: GA_bin(f, 9, B, s)[0],
    'QEA':    lambda f, Q, c, B, s: QEA_bin(f, 9, B, s)[0],
    'KA':     lambda f, Q, c, B, s: KA_bin(f, 9, B, s)[0]}
table = {}
for prob, mod in [('shop', shop9), ('tsp', tsp4)]:
    Q, c, H, E = mod.setup(lam=20)
    best = E.min()
    f = lambda x: energy(Q, x, c)
    print(f'{prob}: optimum value {best}')
    print('  method   ' + ''.join(f'B={B:<6d}' for B in BUDGETS)
          + ' best evals99')
    for name, run in algs.items():
        P = [np.mean([run(f, Q, c, B, s) == best
                      for s in range(RUNS)]) for B in BUDGETS]
        e99 = [evals99(p, B) for p, B in zip(P, BUDGETS)]
        k = int(np.argmin(e99))
        table[f'{prob}/{name}'] = {'P': P, 'e99': e99}
        print(f'  {name:7s}  ' + ''.join(f'{p:<8.3f}' for p in P)
              + f' {e99[k]} (B={BUDGETS[k]})')
json.dump(table, open('budget_table.json', 'w'), indent=1)
