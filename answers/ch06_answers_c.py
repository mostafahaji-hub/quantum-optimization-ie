"""Chapter 6 answers, part C: Exercises 6.21-6.23 (example data)."""
import math, itertools
import numpy as np
from c6_qea import observe, rotate
from c6_keys import decode_keys
def qea_bits(f, n, seed, pop=10, gens=100, dt=math.radians(4), maximize=True):
    rng = np.random.default_rng(seed); Q = [np.full(n, np.pi/4) for _ in range(pop)]; bb, bv = None, None
    for g in range(gens):
        for i in range(pop):
            x = observe(Q[i], rng); val = f(x)
            if bv is None or (val > bv if maximize else val < bv): bb, bv = x, val
            Q[i] = rotate(Q[i], x, bb, dt)
    return bv, bb, Q
# 6.21 two-dimensional knapsack: 10 projects, capital and workforce
r = np.random.default_rng(21); cap = r.integers(10, 40, 10); lab = r.integers(1, 8, 10); prof = r.integers(15, 60, 10)
CAPB, LABB = int(0.4*cap.sum()), int(0.4*lab.sum())
ratio = prof / (cap/CAPB + lab/LABB)
def rep(x):
    x = list(x)
    for i in np.argsort(ratio):
        if np.dot(cap, x) <= CAPB and np.dot(lab, x) <= LABB: break
        x[i] = 0
    return x
f = lambda x: int(np.dot(prof, rep(x)))
g = [0]*10
for i in np.argsort(-ratio):
    if np.dot(cap, g) + cap[i] <= CAPB and np.dot(lab, g) + lab[i] <= LABB: g[i] = 1
best = max(int(np.dot(prof, x)) for x in itertools.product((0, 1), repeat=10) if np.dot(cap, x) <= CAPB and np.dot(lab, x) <= LABB)
q = [qea_bits(f, 10, s)[0] for s in range(10)]
print(f'6.21 budgets ({CAPB},{LABB}): optimum {best}, greedy {int(np.dot(prof, g))}, QEA mean {np.mean(q):.1f}, hits {q.count(best)}/10')
# 6.22 two identical machines, 10 jobs, makespan
r = np.random.default_rng(22); pj = r.integers(2, 20, 10)
def makespan(x):
    loads = [0, 0]
    for j in range(10): loads[x[4*j]] += pj[j]
    return max(loads)
lpt = [0, 0]
for j in sorted(range(10), key=lambda j: -pj[j]): lpt[lpt.index(min(lpt))] += pj[j]
lb = math.ceil(pj.sum()/2)
best = min(max(sum(pj[j] for j in range(10) if m[j] == 0), sum(pj[j] for j in range(10) if m[j] == 1)) for m in itertools.product((0, 1), repeat=10))
q = [qea_bits(makespan, 40, s, maximize=False)[0] for s in range(10)]
print(f'6.22 p={list(pj)}: LPT {max(lpt)}, optimum {best} (lower bound {lb}), QEA mean {np.mean(q):.1f} best {min(q)}')
# 6.23 the final truck chromosome as an Ry circuit
from c6_truck import w, v, CAP, weight, value
from c6_repair import repair
def obj(x): return value(repair(x, add=False))
_, _, Q = qea_bits(obj, 8, 1, pop=10, gens=40)
theta = Q[0]
from sim import op, Ry, probs
psi = np.zeros(256); psi[0] = 1
for k in range(8): psi = op(Ry(2*theta[k]), k, 8) @ psi
rng = np.random.default_rng(5); p = np.abs(psi)**2
quantum = rng.choice(256, size=1000, p=p/p.sum())
classic = [int(''.join(map(str, observe(theta, rng))), 2) for _ in range(1000)]
top = np.argsort(-p)[:3]
print('6.23 angles (deg):', np.round(np.degrees(theta), 1))
for i in top:
    print(f'6.23 string {i:08b}: exact {p[i]:.3f}, circuit samples {np.mean(quantum == i):.3f}, classical observations {np.mean(np.array(classic) == i):.3f}')
