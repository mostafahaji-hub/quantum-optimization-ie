"""Numeric checks for the answers of Chapter 6, part A (Exercises 6.1-6.13)."""
import math, itertools
import numpy as np
from c6_qea import observe, rotate
from c6_truck import w, v, CAP, weight, value
from c6_repair import repair
for p1 in (0.1, 0.3, 0.9):
    th = math.degrees(math.asin(math.sqrt(p1))); print(f'6.1 P={p1}: theta {th:.2f} deg, Ry angle {2*th:.2f} deg')
P1 = [math.sin(math.radians(a))**2 for a in (20, 45, 70, 85)]
pr = {''.join(map(str, x)): math.prod(P1[i] if x[i] else 1-P1[i] for i in range(4)) for x in itertools.product((0, 1), repeat=4)}
print('6.2 P(1):', [round(p, 4) for p in P1], 'max', sorted(pr.items(), key=lambda t: -t[1])[:2], 'min', sorted(pr.items(), key=lambda t: t[1])[:2])
ws, vs, cap = [3, 4, 5], [4, 5, 6], 8
for ang in ((70, 20, 70), (80, 10, 80)):
    q = [math.sin(math.radians(a))**2 for a in ang]; E = 0; P101 = 0
    for x in itertools.product((0, 1), repeat=3):
        p = math.prod(q[i] if x[i] else 1-q[i] for i in range(3))
        if sum(a*b for a, b in zip(ws, x)) <= cap: E += p*sum(a*b for a, b in zip(vs, x))
        if x == (1, 0, 1): P101 = p
    print('6.3 angles', ang, 'P(101)', round(P101, 4), 'E[profit]', round(E, 3))
g = next(g for g in range(30) if math.sin(math.radians(45 + 5*g))**2 > 0.95); print('6.4 generations', g, 'angle', 45 + 5*g)
print('6.4 max P', math.sin(math.pi/2 - 0.02)**2)
order = sorted(range(8), key=lambda i: (-v[i], i)); x = [0]*8
for i in order:
    if weight(x) + w[i] <= CAP: x[i] = 1
print('6.5 by profit', [i+1 for i in range(8) if x[i]], weight(x), value(x), 'RPD %.1f' % (100*(34-value(x))/34))
print('6.6 add=True', repair([1]*8), value(repair([1]*8)), ' add=False', repair([1]*8, add=False), value(repair([1]*8, add=False)))
def qea_truck(seed, pop=10, gens=40, dt=math.radians(4), mode='repair', table=False):
    rng = np.random.default_rng(seed); Q = [np.full(8, np.pi/4) for _ in range(pop)]; best, bv = None, -1e9
    for g in range(gens):
        for k in range(pop):
            x = observe(Q[k], rng)
            if mode == 'repair': x = repair(x, add=False); f = value(x)
            else: f = value(x) - 10*max(0, weight(x) - CAP)
            if f > bv: best, bv = list(x), f
            Q[k] = rotate(Q[k], x, best, dt)
    return value(best) if weight(best) <= CAP else -1
r = [qea_truck(s, mode='penalty') for s in range(20)]; print('6.7 penalty: optimum', r.count(34), 'of 20, mean', np.mean(r))
for pop, gens in ((5, 80), (10, 40), (20, 20)):
    r = [qea_truck(s, pop=pop, gens=gens) for s in range(20)]; print(f'6.8 pop {pop} gens {gens}: optimum {r.count(34)} of 20, mean {np.mean(r):.2f}')
def pbil(seed, gens=400, lam=0.1):
    rng = np.random.default_rng(seed); p = np.full(8, 0.5); best, bv = None, -1
    for g in range(gens):
        x = repair((rng.random(8) < p).astype(int), add=False)
        if value(x) > bv: best, bv = x, value(x)
        p = (1 - lam)*p + lam*np.array(best)
    return bv
r = [pbil(s) for s in range(20)]; print('6.10 PBIL: optimum', r.count(34), 'of 20, mean', np.mean(r))
r = [qea_truck(s, dt=0.01*math.pi) for s in range(20)]; print('6.11 Han-Kim table (0.01 pi, only when x worse): optimum', r.count(34), 'of 20')
k_ = [int('011', 2), int('001', 2), int('000', 2)]; print('6.12 keys', k_, 'order', [j+1 for j in sorted(range(3), key=lambda j: (k_[j], j))])
for k in (2, 3, 5):
    m = 2**k; P = 1 - math.prod(max(0, 1 - i/m) for i in range(8)); print(f'6.13 k={k}: P(tie among 8 keys) = {P:.4f}')
