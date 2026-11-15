# Chapter 6, code listing 8 (in order of appearance)
import numpy as np
from qea import observe, rotate
from repair import repair
from truck import value
def run_qea(seed, pop=10, gens=40, dtheta=np.radians(4)):
    rng = np.random.default_rng(seed)
    Q = [np.full(8, np.pi/4) for _ in range(pop)]
    best, best_val = None, -1
    for g in range(gens):
        for k in range(pop):
            x = repair(observe(Q[k], rng), add=False)
            if value(x) > best_val:
                best, best_val = x, value(x)
            Q[k] = rotate(Q[k], x, best, dtheta)
    return best_val
for dt in (2, 4, 10):
    res = [run_qea(s, dtheta=np.radians(dt)) for s in range(20)]
    print(f'dtheta = {dt:2d} deg: optimum 34 found in {res.count(34)} of 20 runs,',
          'average', np.mean(res), ' worst', min(res))