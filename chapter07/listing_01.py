# Chapter 7, code listing 1 (in order of appearance)
import numpy as np
# the 20-job workshop of Chapter 6 (seed 2026)
r = np.random.default_rng(2026)
n = 20
p = r.integers(2, 10, n); w = r.integers(1, 5, n)
d = (r.uniform(0.2, 0.8, n) * p.sum()).astype(int)
def twt(seq):
    t = tot = 0
    for j in seq:
        t += p[j]; tot += w[j] * max(0, t - d[j])
    return int(tot)
def order_from_real(keys):          # real-valued random keys -> order
    return list(np.argsort(keys, kind='stable'))