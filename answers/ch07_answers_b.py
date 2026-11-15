"""Chapter 7 answers, part B: Exercises 7.9, 7.13, 7.14, 7.15."""
import sys, math, time; sys.path.insert(0, '../chapter07')
import numpy as np
import algs
from algs import GA, QEA, QIGA, QTS, QPSO, keshtel_perm, quantum_keshtel, perm_to_bits, swirl_move, between
from algs import observe, rotate, decode_keys
from prob20 import n, twt
t0 = time.time()
big = {'KA': lambda s: int(keshtel_perm(twt, n, budget=10000, seed=s)[0]),
       'QKA': lambda s: int(quantum_keshtel(twt, n, K=5, budget=10000, seed=s)[0]),
       'GA': lambda s: GA(s, gens=500), 'QEA': lambda s: QEA(s, gens=500),
       'QIGA': lambda s: QIGA(s, gens=500), 'QTS': lambda s: QTS(s, iters=1000), 'QPSO': lambda s: QPSO(s, iters=500)}
for name, A in big.items():
    v = [A(s) for s in range(5)]; print(f'7.9 {name:5s} 10000 evals, 5 runs: mean {np.mean(v):.1f} best {min(v)}  ({time.time()-t0:.0f} s)')
def qka_mid_map(f, n, K=5, budget=3000, n_pop=20, pn1=0.2, pn2=0.4, n_swirl=5, dt=np.radians(3), seed=0):
    rng = np.random.default_rng(seed)
    n1, n2 = max(1, round(pn1*n_pop)), round(pn2*n_pop); n3 = n_pop - n1 - n2
    q = np.full(n*K, np.pi/4); P = [list(rng.permutation(n)) for _ in range(n_pop)]; F = [f(p) for p in P]; evals = n_pop
    while evals < budget:
        o = np.argsort(F); P = [P[i] for i in o]; F = [F[i] for i in o]; lucky, lf = P[:n1], F[:n1]
        for i in range(n1):
            for s in range(n_swirl):
                c = swirl_move(lucky[i], rng); fc = f(c); evals += 1
                if fc < lf[i]: lucky[i], lf[i] = c, fc
        best = lucky[int(np.argmin(lf))]; new = []
        for _ in range(n2 + n3):                       # middle AND new lake from the map
            x = observe(q, rng); new.append(decode_keys(x, n, K)[1]); q = rotate(q, x, perm_to_bits(best, n, K), dt)
        nf = [f(p) for p in new]; evals += n2 + n3
        P, F = lucky + new, lf + nf
    return min(F)
v = [qka_mid_map(twt, n, seed=s) for s in range(10)]; print(f'7.13 map also for the middle group: mean {np.mean(v):.1f} best {min(v)} worst {max(v)}')
algs.K = 8
v = [QEA(s) for s in range(10)]; print(f'7.14 QEA with 8 genes per key: mean {np.mean(v):.1f} best {min(v)}')
algs.K = 5
def local(order, rng, f, k=5):
    cur = f(order); evals = 0
    for _ in range(k):
        c = swirl_move(order, rng); fc = f(c); evals += 1
        if fc < cur: order, cur = c, fc
    return order, cur, evals
def GA_mem(seed, pop=20, budget=3000, pm=0.1):
    rng = np.random.default_rng(seed); ofr = algs.order_from_real
    Pp = rng.random((pop, n)); F = np.array([twt(ofr(x)) for x in Pp]); ev = pop
    while ev + pop + 4 <= budget:
        i = int(F.argmin()); o, fo, e = local(list(ofr(Pp[i])), rng, twt); ev += e
        keys = np.empty(n); keys[o] = (np.arange(n) + 0.5)/n; Pp[i], F[i] = keys, fo
        new = [Pp[F.argmin()].copy()]
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda j: F[j]) for _ in range(2)]
            c = np.where(rng.random(n) < 0.5, Pp[a], Pp[b]); m = rng.random(n) < pm; c[m] = rng.random(m.sum()); new.append(c)
        Pp = np.array(new); F = np.array([twt(ofr(x)) for x in Pp]); ev += pop - 1
    return int(F.min())
def QEA_mem(seed, pop=20, budget=3000, dt=np.radians(3), K=5):
    rng = np.random.default_rng(seed); Q = [np.full(n*K, np.pi/4) for _ in range(pop)]; bb, bv, bo = None, 10**9, None; ev = 0
    while ev + pop + 5 <= budget:
        for i in range(pop):
            x = observe(Q[i], rng); o = decode_keys(x, n, K)[1]; v = twt(o); ev += 1
            if v < bv: bb, bv, bo = x, v, o
        o, fo, e = local(list(bo), rng, twt); ev += e
        if fo < bv: bv, bo, bb = fo, o, perm_to_bits(o, n, K)
        Q = [rotate(q, observe(q, rng), bb, dt) for q in Q]
    return int(bv)
v = [GA_mem(s) for s in range(10)]; print(f'7.15 GA + local search (3000 evals): mean {np.mean(v):.1f} best {min(v)}')
v = [QEA_mem(s) for s in range(10)]; print(f'7.15 QEA + local search (3000 evals): mean {np.mean(v):.1f} best {min(v)}  ({time.time()-t0:.0f} s)')
