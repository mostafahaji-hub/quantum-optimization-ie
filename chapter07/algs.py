import numpy as np
from qea import observe, rotate
from keys import decode_keys
from prob20 import n, twt, order_from_real
K = 5                                         # Q-bits per job
def f_bits(x): return twt(decode_keys(x, n, K)[1])

import numpy as np
def swirl_move(perm, rng):
    """A small move around a solution: swap two jobs or move one job to a new place."""
    p = list(perm)
    i, j = rng.choice(len(p), 2, replace=False)
    if rng.random() < 0.5:
        p[i], p[j] = p[j], p[i]                  # swap
    else:
        job = p.pop(i); p.insert(j, job)         # insertion
    return p
def between(p1, p2, rng):
    """A solution 'between' two lucky ones: order crossover (OX)."""
    n = len(p1); a, b = sorted(rng.choice(n, 2, replace=False))
    child = [None] * n; child[a:b] = p1[a:b]
    rest = [j for j in p2 if j not in child[a:b]]
    k = 0
    for i in range(n):
        if child[i] is None: child[i] = rest[k]; k += 1
    return child
def keshtel_perm(f, n, budget=3000, n_pop=20, pn1=0.2, pn2=0.4, n_swirl=5, seed=0):
    """Keshtel Algorithm for permutation problems; f(perm) is minimized."""
    rng = np.random.default_rng(seed)
    n1, n2 = max(1, round(pn1 * n_pop)), round(pn2 * n_pop); n3 = n_pop - n1 - n2
    P = [list(rng.permutation(n)) for _ in range(n_pop)]; F = [f(p) for p in P]; evals = n_pop
    while evals < budget:
        order = np.argsort(F); P = [P[i] for i in order]; F = [F[i] for i in order]
        lucky, lucky_f = P[:n1], F[:n1]
        for i in range(n1):                                   # 1) swirling (intensification)
            for s in range(n_swirl):
                c = swirl_move(lucky[i], rng); fc = f(c); evals += 1
                if fc < lucky_f[i]: lucky[i], lucky_f[i] = c, fc
        mid = [between(*[lucky[k] for k in rng.choice(n1, 2, replace=n1 < 2)], rng) for _ in range(n2)]
        mid_f = [f(p) for p in mid]; evals += n2                # 2) between two lucky ones
        new = [list(rng.permutation(n)) for _ in range(n3)]
        new_f = [f(p) for p in new]; evals += n3                # 3) fly to a new lake
        P, F = lucky + mid + new, lucky_f + mid_f + new_f
    i = int(np.argmin(F)); return F[i], P[i]

def QIGA(seed, pop=20, gens=150, dt=np.radians(3), pc=0.2, pm=0.002):
    rng = np.random.default_rng(seed)
    Q = [np.full(n * K, np.pi/4) for _ in range(pop)]; bb, bv = None, 10**9
    for g in range(gens):
        X = [observe(q, rng) for q in Q]; V = [f_bits(x) for x in X]
        i = int(np.argmin(V))
        if V[i] < bv: bb, bv = X[i], V[i]
        Q = [rotate(q, x, bb, dt) for q, x in zip(Q, X)]
        for a in range(0, pop - 1, 2):                # quantum crossover: swap angle blocks
            if rng.random() < pc:
                cut = rng.integers(1, n) * K
                Q[a][cut:], Q[a+1][cut:] = Q[a+1][cut:].copy(), Q[a][cut:].copy()
        for q in Q:                                   # quantum NOT mutation: theta -> 90 - theta
            m = rng.random(len(q)) < pm; q[m] = np.pi/2 - q[m]
    return bv

def QTS(seed, iters=300, m=10, dt=np.radians(3), tenure=5):
    rng = np.random.default_rng(seed)
    q = np.full(n * K, np.pi/4); bb, bv = None, 10**9; tabu = {}
    for it in range(iters):
        X = [observe(q, rng) for _ in range(m)]; V = [f_bits(x) for x in X]
        best, worst = X[int(np.argmin(V))], X[int(np.argmax(V))]
        if min(V) < bv: bb, bv = best, min(V)
        for gidx in range(len(q)):
            if tabu.get(gidx, -1) >= it or best[gidx] == worst[gidx]: continue
            q[gidx] += dt if best[gidx] == 1 else -dt      # toward best, away from worst
            tabu[gidx] = it + tenure                        # do not touch again for a while
        q = np.clip(q, 0.02, np.pi/2 - 0.02)
    return bv

def QPSO(seed, M=20, iters=150):
    rng = np.random.default_rng(seed)
    X = rng.random((M, n)); P = X.copy(); PF = np.array([twt(order_from_real(x)) for x in X])
    for t in range(iters - 1):
        beta = 1.0 - 0.5 * t / iters                  # contraction-expansion coefficient
        g = P[PF.argmin()]; mbest = P.mean(axis=0)
        for i in range(M):
            phi = rng.random(n); u = rng.random(n)
            attractor = phi * P[i] + (1 - phi) * g
            sign = np.where(rng.random(n) < 0.5, 1, -1)
            X[i] = attractor + sign * beta * np.abs(mbest - X[i]) * np.log(1 / u)
            f = twt(order_from_real(X[i]))
            if f < PF[i]: P[i], PF[i] = X[i].copy(), f
    return int(PF.min())

import numpy as np
from qea import observe, rotate
from keys import decode_keys
from ka_perm import swirl_move, between
def perm_to_bits(perm, n, K):
    """Write an order back as Q-bit keys: the job in place k gets a key that grows with k."""
    bits = np.zeros(n * K, dtype=int); top = 2**K - 1
    for k, job in enumerate(perm):
        key = round(k * top / (n - 1))
        bits[job*K:(job+1)*K] = [int(b) for b in format(key, f'0{K}b')]
    return bits
def quantum_keshtel(f, n, K=5, budget=3000, n_pop=20, pn1=0.2, pn2=0.4, n_swirl=5, dt=np.radians(3), seed=0):
    """Quantum Keshtel: classical Keshtel, but the 'new lake' keshtels are observed from a
    Q-bit chromosome that keeps learning where the lucky keshtels live."""
    rng = np.random.default_rng(seed)
    n1, n2 = max(1, round(pn1 * n_pop)), round(pn2 * n_pop); n3 = n_pop - n1 - n2
    q = np.full(n * K, np.pi/4)                                   # the 'map' of good lakes
    P = [list(rng.permutation(n)) for _ in range(n_pop)]; F = [f(p) for p in P]; evals = n_pop
    while evals < budget:
        order = np.argsort(F); P = [P[i] for i in order]; F = [F[i] for i in order]
        lucky, lucky_f = P[:n1], F[:n1]
        for i in range(n1):                                       # 1) swirling (as in Keshtel)
            for s in range(n_swirl):
                c = swirl_move(lucky[i], rng); fc = f(c); evals += 1
                if fc < lucky_f[i]: lucky[i], lucky_f[i] = c, fc
        mid = [between(*[lucky[k] for k in rng.choice(n1, 2, replace=n1 < 2)], rng) for _ in range(n2)]
        mid_f = [f(p) for p in mid]; evals += n2                  # 2) between two lucky ones
        best = lucky[int(np.argmin(lucky_f))]                     # 3) new lake, chosen by the Q-bit map
        new = []
        for _ in range(n3):
            x = observe(q, rng); new.append(decode_keys(x, n, K)[1])
            q = rotate(q, x, perm_to_bits(best, n, K), dt)
        new_f = [f(p) for p in new]; evals += n3
        P, F = lucky + mid + new, lucky_f + mid_f + new_f
    i = int(np.argmin(F)); return F[i], P[i]

def GA(seed, pop=20, gens=150, pm=0.1):
    rng = np.random.default_rng(seed)
    P = rng.random((pop, n)); F = np.array([twt(order_from_real(x)) for x in P])
    for g in range(gens - 1):
        new = [P[F.argmin()].copy()]                  # elitism
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda i: F[i]) for _ in range(2)]
            mask = rng.random(n) < 0.5                # uniform crossover
            c = np.where(mask, P[a], P[b])
            m = rng.random(n) < pm; c[m] = rng.random(m.sum())   # mutation
            new.append(c)
        P = np.array(new); F = np.array([twt(order_from_real(x)) for x in P])
    return int(F.min())

# ---- Wrappers used by the comparison experiment of Section 7.7 (same budget: 3000 evaluations) ----
def KA(seed):  return int(keshtel_perm(twt, n, budget=3000, seed=seed)[0])
def QKA(seed): return int(quantum_keshtel(twt, n, K=K, budget=3000, seed=seed)[0])
def QEA(seed, pop=20, gens=150, dt=np.radians(3)):
    """QEA of Chapter 6 with random-key decoding (K Q-bits per job)."""
    rng = np.random.default_rng(seed)
    Qs = [np.full(n * K, np.pi / 4) for _ in range(pop)]; best, bv = None, np.inf
    for g in range(gens):
        for i in range(pop):
            x = observe(Qs[i], rng); v = f_bits(x)
            if v < bv: best, bv = x, v
            Qs[i] = rotate(Qs[i], x, best, dt)
    return int(bv)
