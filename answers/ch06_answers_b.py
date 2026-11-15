"""Numeric checks for the answers of Chapter 6, part B (Exercises 6.9, 6.14-6.18, 6.21-6.23)."""
import math, itertools
import numpy as np
from c6_qea import observe, rotate
from c6_keys import decode_keys
import c6_shop8 as shop8
def qea_bits(f, n, seed, pop=20, gens=150, dt=math.radians(3), maximize=False):
    rng = np.random.default_rng(seed); Q = [np.full(n, np.pi/4) for _ in range(pop)]; bb, bv = None, None
    for g in range(gens):
        for i in range(pop):
            x = observe(Q[i], rng); val = f(x)
            if bv is None or (val > bv if maximize else val < bv): bb, bv = x, val
            Q[i] = rotate(Q[i], x, bb, dt)
    return bv, bb
# 6.9: a 20-shipment truck
r = np.random.default_rng(7); W = r.integers(2, 15, 20); V = r.integers(3, 25, 20); C = int(0.4*W.sum())
def rep(x):
    x = list(x); order = sorted(range(20), key=lambda i: V[i]/W[i])
    for i in order:
        if np.dot(W, x) <= C: break
        x[i] = 0
    return x
f20 = lambda x: int(np.dot(V, rep(x)))
g = [0]*20
for i in sorted(range(20), key=lambda i: -V[i]/W[i]):
    if np.dot(W, g) + W[i] <= C: g[i] = 1
X = ((np.arange(2**20)[:, None] >> np.arange(20)[::-1]) & 1)
ok = X @ W <= C; best = int((X[ok] @ V).max())
q = [qea_bits(f20, 20, s, pop=10, gens=100, dt=math.radians(4), maximize=True)[0] for s in range(10)]
print(f'6.9 capacity {C}: optimum {best} (2^20 enumeration), greedy {int(np.dot(V, g))}, QEA best {max(q)} mean {np.mean(q):.1f}, optimum hits {q.count(best)}/10')
# 6.14 genes per job on the large workshop
for k in (2, 3, 5):
    res = [qea_bits(lambda x: shop8.twt(decode_keys(x, 8, k)[1]), 8*k, s)[0] for s in range(10)]
    print(f'6.14 k={k}: runs {res} mean {np.mean(res):.1f}')
# 6.15 largest key first
def dec_desc(x, k=3):
    keys = [int(''.join(map(str, x[j*k:(j+1)*k])), 2) for j in range(8)]
    return sorted(range(8), key=lambda j: (-keys[j], j))
res = [qea_bits(lambda x: shop8.twt(dec_desc(x)), 24, s)[0] for s in range(10)]
print('6.15 descending keys: runs', res, 'mean', np.mean(res))
# 6.16 / 6.17: 20-job workshop
r = np.random.default_rng(2026); n = 20
p = r.integers(2, 10, n); wt = r.integers(1, 5, n); d = (r.uniform(0.2, 0.8, n) * p.sum()).astype(int)
def twt20(seq):
    t = tot = 0
    for j in seq: t += p[j]; tot += wt[j]*max(0, t - d[j])
    return int(tot)
for budget, gens in ((1000, 50), (10000, 500)):
    q = [qea_bits(lambda x: twt20(decode_keys(x, n, 5)[1]), 100, s, gens=gens)[0] for s in range(10)]
    rs = []
    for s in range(10):
        rg = np.random.default_rng(s); rs.append(min(twt20(rg.permutation(n)) for _ in range(budget)))
    print(f'6.16 budget {budget}: QEA mean {np.mean(q):.1f} best {min(q)}; random mean {np.mean(rs):.1f} best {min(rs)}')
imp = []
for s in range(10):
    v0, bits = qea_bits(lambda x: twt20(decode_keys(x, n, 5)[1]), 100, s)
    seq = decode_keys(bits, n, 5)[1]; cur = twt20(seq); better = True
    while better:
        better = False
        for i in range(n - 1):
            t = seq[:]; t[i], t[i+1] = t[i+1], t[i]
            if twt20(t) < cur: seq, cur, better = t, twt20(t), True
    imp.append((v0, cur))
print('6.17 QEA -> +adjacent swaps:', imp, 'mean', np.mean([a for a, _ in imp]), '->', np.mean([b for _, b in imp]))
# 6.18 TSP with 15 random cities
r = np.random.default_rng(15); P = r.uniform(0, 100, (15, 2))
Dm = np.round(np.linalg.norm(P[:, None] - P[None], axis=2), 1)
Lt = lambda t: round(sum(Dm[t[i], t[(i+1) % 15]] for i in range(15)), 1)
t = [0]
while len(t) < 15: t.append(min((j for j in range(15) if j not in t), key=lambda j: (Dm[t[-1], j], j)))
nn = Lt(t); imp2 = True
while imp2:
    imp2 = False
    for i in range(1, 14):
        for k in range(i+1, 15):
            u = t[:i] + t[i:k+1][::-1] + t[k+1:]
            if Lt(u) < Lt(t) - 1e-9: t, imp2 = u, True
q = [qea_bits(lambda x: Lt([0] + [c+1 for c in decode_keys(x, 14, 3)[1]]), 42, s)[0] for s in range(10)]
print(f'6.18 15 cities: NN {nn}, NN+2opt {Lt(t)}, QEA best {min(q)} mean {np.mean(q):.1f}')
