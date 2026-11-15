"""Chapter 15 - second, independent check (no book modules)."""
import itertools, math
import numpy as np
def twt(order, p, d, w):
    t = tot = 0
    for j in order:
        t += p[j]; tot += w[j] * max(0, t - d[j])
    return tot
p, d, w = [2, 3, 4], [4, 7, 5], [1, 3, 3]
print('small shop all orders', sorted((twt(o, p, d, w), o) for o in itertools.permutations(range(3))))
print('LPT small', twt([2, 1, 0], p, d, w))
p8 = [6, 8, 9, 6, 3, 6, 7, 2]; d8 = [16, 29, 14, 17, 23, 39, 17, 23]; w8 = [1, 1, 2, 3, 2, 2, 4, 1]
for name, key in [('SPT', lambda j: (p8[j], j)), ('EDD', lambda j: (d8[j], j)),
                  ('WSPT', lambda j: (-w8[j] / p8[j], j)), ('LPT', lambda j: (-p8[j], j))]:
    o = sorted(range(8), key=key); print('8-job', name, twt(o, p8, d8, w8))
pts = [(6, 6), (0, 4), (8, 7), (6, 4), (7, 5), (9, 3), (8, 2), (4, 2)]
def dist(n): return [[round(math.hypot(a[0]-b[0], a[1]-b[1]), 1) for b in pts[:n]] for a in pts[:n]]
def tlen(t, D): return round(sum(D[t[k]][t[(k+1) % len(t)]] for k in range(len(t))), 1)
def nn(D, s):
    t = [s]
    while len(t) < len(D):
        r = [j for j in range(len(D)) if j not in t]
        t.append(min(r, key=lambda j: (D[t[-1]][j], j)))
    return t
D8 = dist(8); print('8-city NN all starts', [tlen(nn(D8, s), D8) for s in range(8)])
print('8-city optimum (enumeration)', min(tlen((0,) + q, D8) for q in itertools.permutations(range(1, 8))))
D5 = dist(5); print('project NN', [tlen(nn(D5, s), D5) for s in range(5)])
tours = sorted((tlen((0,) + q, D5), q) for q in itertools.permutations(range(1, 5)))
print('project tours: best', tours[:2], 'longest', tours[-1][0])
lam = 10; m = 4
X = ((np.arange(2 ** 16)[:, None] >> np.arange(16)[::-1]) & 1).reshape(-1, m, m)  # row city, col step
pen = ((X.sum(2) - 1) ** 2).sum(1) + ((X.sum(1) - 1) ** 2).sum(1)
dd = sum(D5[0][i+1] * X[:, i, 0] + D5[i+1][0] * X[:, i, m-1] for i in range(m))
for i in range(m):
    for j in range(m):
        if i != j:
            for t in range(m - 1): dd = dd + D5[i+1][j+1] * X[:, i, t] * X[:, j, t+1]
E = dd + lam * pen
feas = pen == 0
print('project mean', round(E.mean(), 3), 'feasible', feas.sum(), 'opt', round(E[feas].min(), 1),
      'n opt', int(np.isclose(E, E[feas].min()).sum()), 'cheapest infeasible', round(E[~feas].min(), 1))
def zz(m):
    v = lambda i, t: i * m + t; S = set()
    for i in range(m):
        for a, b in itertools.combinations(range(m), 2): S.add((v(i, a), v(i, b))); S.add((v(a, i), v(b, i)))
    for t in range(m - 1):
        for i in range(m):
            for j in range(m):
                if i != j: S.add(tuple(sorted((v(i, t), v(j, t + 1)))))
    return len(S)
print('ZZ 8 and 10 cities', zz(7), zz(9))
print('feasible share 8 cities', math.factorial(7) / 2 ** 49)
N = 2 ** 16; th = math.asin(1 / math.sqrt(N)); print('Grover rounds', round(math.pi / (4 * th) - 0.5), 'success', round(math.sin((2 * 201 + 1) * th) ** 2, 4))
r99 = lambda P: math.ceil(math.log(0.01) / math.log(1 - P))
print('runs99', [r99(x) for x in (0.5, 0.1, 0.01, 1/3, 0.0317, 0.2, 0.0016, 2/24)])
print('random exact shop/tsp best evals99', min(B * r99(1 - (511/512) ** B) for B in (25, 50, 100, 200, 400)),
      min(B * r99(1 - (510/512) ** B) for B in (25, 50, 100, 200, 400)))
