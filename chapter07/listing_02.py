# Chapter 7, code listing 2 (in order of appearance)
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