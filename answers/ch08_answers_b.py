"""Chapter 8 answers, part B: Exercises 8.20, 8.23, 8.24."""
import sys, itertools, math, time; sys.path.insert(0, '../chapter08')
import numpy as np
from qubo import energy, add_quad, add_penalty_sum, brute_force
from tsp_qubo import tsp_qubo, decode_tour
from tsp8 import D, tour_length
from bin_algs import KA_bin, GA_bin, QEA_bin
t0 = time.time()
r = np.random.default_rng(20); flow = r.integers(0, 12, (3, 3)); dist = r.integers(2, 10, (3, 3))
x = lambda i, k: 3*i + k; y = lambda j, l: 9 + 3*j + l
def cd3(lam):
    Q = np.zeros((18, 18)); c = 0.0
    for i, j, k, l in itertools.product(range(3), repeat=4): add_quad(Q, x(i, k), y(j, l), flow[i][j]*dist[k][l])
    for v in (x, y):
        for a in range(3):
            c += add_penalty_sum(Q, [v(a, b) for b in range(3)], 1, lam); c += add_penalty_sum(Q, [v(b, a) for b in range(3)], 1, lam)
    return Q, c
best = min(sum(flow[i][j]*dist[pi[i]][pj[j]] for i in range(3) for j in range(3))
           for pi in itertools.permutations(range(3)) for pj in itertools.permutations(range(3)))
for lam in (10, 20, 40, 60, 80, 100):
    X, E = brute_force(*cd3(lam)); k = int(np.argmin(E)); xx = X[k]
    ok = all(xx[0:9].reshape(3, 3).sum(a).tolist() == [1, 1, 1] for a in (0, 1)) and all(xx[9:].reshape(3, 3).sum(a).tolist() == [1, 1, 1] for a in (0, 1))
    print(f'8.20 lam {lam}: min {E[k]:.0f} feasible {ok} (optimum by enumeration {best})')
print('8.20 flow', flow.tolist(), 'dist', dist.tolist())
Q, c = tsp_qubo(D, 20); f = lambda v: energy(Q, v, c)
for name, A in (('KA', KA_bin), ('GA', GA_bin), ('QEA', QEA_bin)):
    L = []
    for s in range(5):
        t = decode_tour(A(f, 49, 100000, s)[1], 8); L.append(tour_length(t) if t else None)
    print(f'8.23 {name} 100000 evals: {L}  ({time.time()-t0:.0f} s)')
def GA_swap(f, n, budget, seed, pop=20, pm=None):
    rng = np.random.default_rng(seed); pm = pm or 1/n
    P = rng.integers(0, 2, (pop, n)); F = np.array([f(v) for v in P]); ev = pop
    while ev + pop - 1 <= budget:
        new = [P[F.argmin()].copy()]
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda i: F[i]) for _ in range(2)]
            ch = np.where(rng.random(n) < 0.5, P[a], P[b])
            if rng.random() < 0.5:
                M = ch.reshape(7, 7).copy(); u, w = rng.choice(7, 2, replace=False); M[[u, w]] = M[[w, u]]; ch = M.ravel()
            else:
                m = rng.random(n) < pm; ch[m] = 1 - ch[m]
            new.append(ch)
        P = np.array(new); F = np.array([f(v) for v in P]); ev += pop - 1
    i = int(F.argmin()); return F[i], P[i]
L = []
for s in range(10):
    t = decode_tour(GA_swap(f, 49, 20000, s)[1], 8); L.append(tour_length(t) if t else None)
print('8.24 GA + swap mutation:', L, 'mean', np.mean([v for v in L if v]), ' optimum hits', L.count(25.0))
for lam in (45, 48, 50, 52, 55):
    X, E = brute_force(*cd3(lam)); k = int(np.argmin(E)); xx = X[k]
    ok = all(xx[0:9].reshape(3, 3).sum(a).tolist() == [1, 1, 1] for a in (0, 1)) and all(xx[9:].reshape(3, 3).sum(a).tolist() == [1, 1, 1] for a in (0, 1))
    print(f'8.20 refine lam {lam}: min {E[k]:.0f} feasible {ok}')
