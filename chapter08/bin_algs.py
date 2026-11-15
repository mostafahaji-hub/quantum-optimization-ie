import numpy as np
from qea import observe, rotate
def GA_bin(f, n, budget, seed, pop=20, pm=None):
    """Classic GA on bit strings: tournament, uniform crossover, bit-flip mutation, elitism."""
    rng = np.random.default_rng(seed); pm = pm or 1 / n
    P = rng.integers(0, 2, (pop, n)); F = np.array([f(x) for x in P]); evals = pop
    while evals + pop - 1 <= budget:
        new = [P[F.argmin()].copy()]
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda i: F[i]) for _ in range(2)]
            c = np.where(rng.random(n) < 0.5, P[a], P[b])
            m = rng.random(n) < pm; c[m] = 1 - c[m]
            new.append(c)
        P = np.array(new); F = np.array([f(x) for x in P]); evals += pop - 1
    i = int(F.argmin()); return F[i], P[i]
def QEA_bin(f, n, budget, seed, pop=20, dt=np.radians(3)):
    """QEA of Chapter 6 on a QUBO: one observation per Q-bit chromosome per generation."""
    rng = np.random.default_rng(seed)
    Q = [np.full(n, np.pi/4) for _ in range(pop)]; bb, bv = None, np.inf; evals = 0
    while evals + pop <= budget:
        for i in range(pop):
            x = observe(Q[i], rng); v = f(x); evals += 1
            if v < bv: bb, bv = x, v
            Q[i] = rotate(Q[i], x, bb, dt)
    return bv, bb
def flip_one(x, rng):
    c = x.copy(); k = rng.integers(len(x)); c[k] = 1 - c[k]; return c
def KA_bin(f, n, budget, seed, n_pop=20, pn1=0.2, pn2=0.4, n_swirl=5, move=flip_one):
    """Keshtel Algorithm of Chapter 7 on bit strings; default swirl = flip one bit."""
    rng = np.random.default_rng(seed)
    n1, n2 = max(1, round(pn1 * n_pop)), round(pn2 * n_pop); n3 = n_pop - n1 - n2
    P = [rng.integers(0, 2, n) for _ in range(n_pop)]; F = [f(x) for x in P]; evals = n_pop
    while evals + n1 * n_swirl + n2 + n3 <= budget:
        o = np.argsort(F); P = [P[i] for i in o]; F = [F[i] for i in o]
        lucky, lf = P[:n1], F[:n1]
        for i in range(n1):                                     # 1) swirling: flip one bit
            for s in range(n_swirl):
                c = move(lucky[i], rng)
                fc = f(c); evals += 1
                if fc < lf[i]: lucky[i], lf[i] = c, fc
        mid = []
        for _ in range(n2):                                     # 2) between two lucky ones
            a, b = rng.choice(n1, 2, replace=n1 < 2)
            mid.append(np.where(rng.random(n) < 0.5, lucky[a], lucky[b]))
        new = [rng.integers(0, 2, n) for _ in range(n3)]        # 3) fly to a new lake
        mf = [f(x) for x in mid]; nf = [f(x) for x in new]; evals += n2 + n3
        P, F = lucky + mid + new, lf + mf + nf
    i = int(np.argmin(F)); return F[i], P[i]
def random_bin(f, n, budget, seed):
    rng = np.random.default_rng(seed); best = (np.inf, None)
    for _ in range(budget):
        x = rng.integers(0, 2, n); v = f(x)
        if v < best[0]: best = (v, x)
    return best
