"""Numeric checks for the answers of Chapter 5 (uses alg.py, sim.py, shop.py of Chapter 5)."""
import math, itertools
import numpy as np
from alg import *
from shop import code, twt
th = lambda M, N: math.asin(math.sqrt(M / N))
for N, M in ((16, 1), (64, 4), (1024, 1), (1024, 10)):
    t = th(M, N); k = math.floor(math.pi / (4 * t)); P = math.sin((2*k + 1)*t)**2
    print(f'5.7 N={N} M={M}: theta {math.degrees(t):.2f} deg, k {k}, P {P:.4f}')
f = lambda s: twt(code[s]) if s in code else None
for T in (9, 11, 12):
    M = sum(1 for s in code if f(s) <= T); t = th(M, 8); k = math.floor(math.pi/(4*t))
    psi = grover(lambda x: f(x) is not None and f(x) <= T, 3, k)
    P = sum(abs(psi[int(s, 2)])**2 for s in code if f(s) <= T)
    print(f'5.8 T={T}: M={M} k={k} P={P:.4f}  (k=1: {math.sin(3*t)**2:.4f})')
print('5.9 M=5,N=8: k=1 P', round(math.sin(3*th(5, 8))**2, 4), ' k=0', 5/8)
psi = grover(lambda x: x in ('101', '110', '111'), 3, 1)
print('5.10 P(101)', round(abs(psi[5])**2, 4), ' P(110)+P(111)', round(abs(psi[6])**2 + abs(psi[7])**2, 4))
psi = grover(lambda x: x in ('00', '10'), 2, 1); print('5.11', probs(psi))
def plans(costs, budget):
    n = len(costs); good = []
    for i in range(2**n):
        x = [int(b) for b in format(i, f'0{n}b')]
        if sum(x) == 2 and not (x[0] and x[1]) and sum(c*v for c, v in zip(costs, x)) <= budget:
            good.append(format(i, f'0{n}b'))
    return good
for costs, B in (([3, 5, 4, 6], 8), ([3, 5, 4, 6, 2], 8)):
    g = plans(costs, B); N = 2**len(costs); t = th(len(g), N); k = math.floor(math.pi/(4*t))
    print(f'5.12/13 costs {costs} budget {B}: good {g} M={len(g)} N={N} k={k} P={math.sin((2*k+1)*t)**2:.4f}')
def gas(seed, table, n):
    rng = np.random.default_rng(seed); calls = 0
    def once(psi):
        p = np.abs(psi)**2; return format(rng.choice(len(psi), p=p/p.sum()), f'0{n}b')
    s = once(Hn(n) @ np.eye(2**n)[0])
    while s not in table: s = once(Hn(n) @ np.eye(2**n)[0])
    T = table[s]; fails = 0
    while fails < 3:
        k = int(rng.integers(1, 3)); calls += k
        s = once(grover(lambda x: x in table and table[x] < T, n, k))
        if s in table and table[s] < T: T, fails = table[s], 0
        else: fails += 1
    return T, calls
shop_t = {s: twt(code[s]) for s in code}
res = [gas(s, shop_t, 3) for s in range(20)]
print('5.14 optimum found', sum(T == 5 for T, _ in res), 'of 20; mean oracle calls', np.mean([c for _, c in res]))
tsp_t = {'00': 26, '01': 31, '10': 27}
res = [gas(s, tsp_t, 2) for s in range(20)]
print('5.15 TSP optimum found', sum(T == 26 for T, _ in res), 'of 20; mean calls', np.mean([c for _, c in res]))
for n in (8, 9, 10, 12, 14):
    N = math.factorial(n)
    print(f'5.16 n={n}: classical {N/2*1e-6:.3g} s, Grover {math.pi/4*math.sqrt(N)*1e-3:.3g} s')
for a, N, L in ((2, 15, 16), (2, 21, 64), (14, 15, 16)):
    seq = [pow(a, x, N) for x in range(L)]; r = next(x for x in range(1, L) if seq[x] == 1)
    g = (math.gcd(pow(a, r//2) - 1, N), math.gcd(pow(a, r//2) + 1, N)) if r % 2 == 0 else None
    print(f'5.17/18 a={a} N={N}: seq {seq[:8]} period {r} gcds {g}')
spec = np.abs(np.fft.fft(np.array([pow(2, x, 21) for x in range(64)]) - 8.0))
print('5.17 a=2 N=21 FFT peaks (top 5):', sorted(np.argsort(spec)[-5:]))
t = th(1, 16)
for k in range(4):
    print(f'5.20 k={k}: good {math.sin((2*k+1)*t):.4f}, each other {math.cos((2*k+1)*t)/math.sqrt(15):.4f}')
cost = {(0, 0): 2, (0, 1): 5, (1, 0): 4, (1, 1): 1, (2, 0): 2, (2, 1): 4}   # (worker, shift)
feas = [s for s in (format(i, '03b') for i in range(8)) if s[0] != s[1] and s not in ('000', '111')]
print('5.22 feasible', feas, {s: sum(cost[(w, int(s[w]))] for w in range(3)) for s in feas})
c_, v_ = [4, 3, 5, 2], [7, 4, 8, 3]
port = sorted(((sum(v*b for v, b in zip(v_, x)), sum(c*b for c, b in zip(c_, x)), ''.join(map(str, x)))
               for x in itertools.product((0, 1), repeat=4) if sum(c*b for c, b in zip(c_, x)) <= 9), reverse=True)
print('5.23 best portfolios', port[:4])
