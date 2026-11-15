"""Chapter 7 answers, part D: Exercise 7.22 (a 12-site emergency network; reference run)."""
import sys, math, time, heapq; sys.path.insert(0, '../chapter07')
import numpy as np
from algs import keshtel_perm, observe, rotate, decode_keys
r = np.random.default_rng(22); N = 13
pts = r.uniform(0, 100, (N, 2)); pts[0] = (50, 50)
T = np.round(np.linalg.norm(pts[:, None] - pts[None], axis=2) / 10, 1)
REL = np.ones((N, N))
for i in range(N):
    for j in range(i + 1, N): REL[i, j] = REL[j, i] = round(r.uniform(0.60, 0.99), 2)
def path(a, b, tau):
    dist, pq = {a: 0.0}, [(0.0, a)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == b: return d
        if d > dist[u]: continue
        for v in range(N):
            if v != u and REL[u, v] >= tau and d + T[u, v] < dist.get(v, 1e9):
                dist[v] = d + T[u, v]; heapq.heappush(pq, (dist[v], v))
    return 1e6
cache = {}
def route(order, tau):
    stops = [0] + [c + 1 for c in order] + [0]; tot = 0.0
    for a, b in zip(stops, stops[1:]):
        key = (a, b, tau)
        if key not in cache: cache[key] = path(a, b, tau)
        tot += cache[key]
    return round(tot, 1)
def qea(f, seed, K=4, pop=10, budget=1500, dt=np.radians(4)):
    rng = np.random.default_rng(seed); Q = [np.full(12*K, np.pi/4) for _ in range(pop)]; bb, bv = None, 1e9
    for g in range(budget // pop):
        for i in range(pop):
            x = observe(Q[i], rng); v = f(decode_keys(x, 12, K)[1])
            if v < bv: bb, bv = x, v
            Q[i] = rotate(Q[i], x, bb, dt)
    return bv
def ga(f, seed, pop=10, budget=1500, pm=0.15):
    rng = np.random.default_rng(seed); P = rng.random((pop, 12)); F = np.array([f(list(np.argsort(x))) for x in P])
    for g in range(budget // pop - 1):
        new = [P[F.argmin()].copy()]
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda i: F[i]) for _ in range(2)]
            c = np.where(rng.random(12) < 0.5, P[a], P[b]); m = rng.random(12) < pm; c[m] = rng.random(m.sum()); new.append(c)
        P = np.array(new); F = np.array([f(list(np.argsort(x))) for x in P])
    return F.min()
t0 = time.time()
for tau in (0.0, 0.80):
    f = lambda o: route(o, tau)
    k = [keshtel_perm(f, 12, budget=1500, n_pop=10, seed=s)[0] for s in range(10)]
    q = [qea(f, s) for s in range(10)]; g = [ga(f, s) for s in range(10)]
    best = min(k + q + g)
    hits = lambda v: sum(abs(x - best) < 1e-6 for x in v)
    print(f'7.22 tau {tau}: best found {best}; KA {hits(k)}/10 mean {np.mean(k):.1f} | QEA {hits(q)}/10 mean {np.mean(q):.1f} | GA {hits(g)}/10 mean {np.mean(g):.1f}  ({time.time()-t0:.0f} s)')
