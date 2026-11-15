# Chapter 7, code listing 14 (in order of appearance)
import numpy as np, itertools
from emer import route_time, names
from qea import observe, rotate
from keys import decode_keys
from ka_perm import keshtel_perm
from qka3 import quantum_keshtel
sites = list(range(1, 8)); n, K = 7, 3
def exact(tau):
    return min((route_time(p, tau)[0], p) for p in itertools.permutations(sites))
def qea(tau, seed, pop=10, gens=60, dt=np.radians(4)):
    rng = np.random.default_rng(seed)
    Q = [np.full(n * K, np.pi/4) for _ in range(pop)]; bb, bv = None, 1e9
    for g in range(gens):
        for i in range(pop):
            x = observe(Q[i], rng); order = [sites[j] for j in decode_keys(x, n, K)[1]]
            v = route_time(order, tau)[0]
            if v < bv: bb, bv = x, v
            Q[i] = rotate(Q[i], x, bb, dt)
    return bv
def ga(tau, seed, pop=10, gens=60, pm=0.15):
    rng = np.random.default_rng(seed)
    f = lambda x: route_time([sites[j] for j in np.argsort(x, kind='stable')], tau)[0]
    P = rng.random((pop, n)); F = np.array([f(x) for x in P])
    for g in range(gens - 1):
        new = [P[F.argmin()].copy()]
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda i: F[i]) for _ in range(2)]
            c = np.where(rng.random(n) < 0.5, P[a], P[b])
            m = rng.random(n) < pm; c[m] = rng.random(m.sum()); new.append(c)
        P = np.array(new); F = np.array([f(x) for x in P])
    return F.min()
for tau in (0.0, 0.70, 0.80, 0.84):
    opt, perm = exact(tau)
    q = [qea(tau, s) for s in range(20)]; g = [ga(tau, s) for s in range(20)]
    fk = lambda perm: route_time([sites[j] for j in perm], tau)[0]
    k = [keshtel_perm(fk, n, budget=600, n_pop=10, pn1=0.2, pn2=0.4, n_swirl=5, seed=s)[0] for s in range(20)]
    qk = [quantum_keshtel(fk, n, K=3, budget=600, n_pop=10, seed=s)[0] for s in range(20)]
    hits = lambda r: sum(abs(v - opt) < 1e-6 for v in r)
    print(f'tau {tau:.2f}: optimum {opt:5.1f} | KA {hits(k):2d} ({np.mean(k):4.1f})'
          f' | QKA {hits(qk):2d} ({np.mean(qk):4.1f}) | GA {hits(g):2d} ({np.mean(g):4.1f})'
          f' | QEA {hits(q):2d} ({np.mean(q):4.1f})')