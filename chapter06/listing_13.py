# Chapter 6, code listing 13 (in order of appearance)
import numpy as np
from qea import observe, rotate
from keys import decode_keys
# a 20-job workshop (random but fixed data)
r = np.random.default_rng(2026)
n = 20
p = r.integers(2, 10, n); w = r.integers(1, 5, n)
d = (r.uniform(0.2, 0.8, n) * p.sum()).astype(int)
def twt(seq):
    t = tot = 0
    for j in seq:
        t += p[j]; tot += w[j] * max(0, t - d[j])
    return int(tot)
wspt = sorted(range(n), key=lambda j: p[j] / w[j])
k, budget = 5, 3000
def qea(seed, pop=20, gens=150, dtheta=np.radians(3)):
    rng = np.random.default_rng(seed)
    Q = [np.full(n * k, np.pi/4) for _ in range(pop)]
    bb, bv = None, 10**9
    for g in range(gens):
        for i in range(pop):
            x = observe(Q[i], rng); v = twt(decode_keys(x, n, k)[1])
            if v < bv: bb, bv = x, v
            Q[i] = rotate(Q[i], x, bb, dtheta)
    return bv
def random_search(seed):
    rng = np.random.default_rng(seed)
    return min(twt(rng.permutation(n)) for _ in range(budget))
q = [qea(s) for s in range(10)]
rs = [random_search(s) for s in range(10)]
print('WSPT rule            :', twt(wspt))
print('random search (3000) : best', min(rs), ' mean', np.mean(rs))
print('QEA (3000 evaluations): best', min(q), ' mean', np.mean(q))