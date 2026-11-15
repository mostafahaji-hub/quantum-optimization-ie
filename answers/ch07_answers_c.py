"""Chapter 7 answers, part C: Exercises 7.7, 7.16, 7.18, 7.21."""
import sys, math, time, heapq, itertools; sys.path.insert(0, '../chapter07')
import numpy as np
import algs
from algs import keshtel_perm, quantum_keshtel
from emer import route_time, names
t0 = time.time()
E = {(1, 2): (4, .95), (1, 3): (2, .75), (2, 3): (1, .90), (2, 4): (5, .85), (3, 4): (8, .95), (3, 5): (10, .90), (4, 5): (2, .88)}
def dij(tau):
    adj = {}
    for (a, b), (t, r) in E.items():
        if r >= tau: adj.setdefault(a, []).append((b, t, r)); adj.setdefault(b, []).append((a, t, r))
    dist, prev, pq = {1: 0}, {}, [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, t, r in adj.get(u, []):
            if d + t < dist.get(v, 1e9): dist[v], prev[v] = d + t, u; heapq.heappush(pq, (d + t, v))
    path = [5]
    while path[-1] != 1: path.append(prev[path[-1]])
    path = path[::-1]; rel = math.prod(E[tuple(sorted(e))][1] for e in zip(path, path[1:]))
    return dist[5], path, round(rel, 4)
print('7.7 tau 0.8:', dij(0.8), ' no threshold:', dij(0.0))
sites = range(1, 8)
best = min(((t + 100*(1 - rel), t, rel, p) for p in itertools.permutations(sites) for t, rel, _ in [route_time(p, 0.0)]))
print('7.16 min time + 100(1-rel):', round(best[0], 2), 'time', best[1], 'rel', round(best[2], 3), 'order H-' + '-'.join(names[i] for i in best[3]) + '-H')
for tau in (0.70, 0.80, 0.84):
    t, rel, _ = route_time(min(itertools.permutations(sites), key=lambda p: route_time(p, tau)[0]), tau)
    print(f'7.16 threshold {tau}: time {t}, rel {rel:.3f}, combined {t + 100*(1-rel):.2f}')
from c6_shop8 import twt as twt8
grid = []
for pn1 in (0.1, 0.2, 0.3):
    for ns in (2, 5, 10):
        hits = sum(keshtel_perm(twt8, 8, budget=1000, pn1=pn1, n_swirl=ns, seed=s)[0] == 58 for s in range(10))
        grid.append((pn1, ns, hits))
print('7.18 (PN1, NSwirl, hits of 58 in 10 runs, budget 1000):', grid)
r = np.random.default_rng(15); P = r.uniform(0, 100, (15, 2)); Dm = np.round(np.linalg.norm(P[:, None] - P[None], axis=2), 1)
L = lambda order: round(sum(Dm[t[i], t[(i+1) % 15]] for t in [[0] + [c+1 for c in order]] for i in range(15)), 1)
algs.n, algs.twt = 14, L
res = {}
for name, A in [('KA', lambda s: keshtel_perm(L, 14, budget=3000, seed=s)[0]),
                ('QKA', lambda s: quantum_keshtel(L, 14, K=5, budget=3000, seed=s)[0]),
                ('GA', algs.GA), ('QEA', algs.QEA), ('QIGA', algs.QIGA), ('QTS', algs.QTS), ('QPSO', algs.QPSO)]:
    v = [A(s) for s in range(5)]; res[name] = v
    print(f'7.21 TSP15 {name:5s}: mean {np.mean(v):.1f} best {min(v)}  ({time.time()-t0:.0f} s)')
