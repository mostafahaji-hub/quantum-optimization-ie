"""Numeric checks for the answers of Chapter 4 (uses sim.py and shop.py of Chapter 4)."""
import math, itertools
import numpy as np
from sim import *
from shop import code, twt
np.set_printoptions(precision=4, suppress=True)
S = np.diag([1, 1j]); k0 = np.array([1, 0])
print('4.1', (H @ Z @ H @ k0).round(4), (H @ S @ H @ k0).round(4), (H @ Z @ H @ X @ k0).round(4))
def bloch(psi):
    a, b = psi; th = 2*np.degrees(np.arccos(min(1, abs(a))))
    ph = (np.degrees(np.angle(b) - np.angle(a)) % 360) if abs(b) > 1e-9 else 0
    return round(float(th), 1), round(float(ph), 1)
for psi in ([np.sqrt(3)/2, 0.5], [1/np.sqrt(2), -1j/np.sqrt(2)], [0.5, np.sqrt(3)/2*np.exp(1j*np.pi/4)]):
    print('4.3', bloch(np.array(psi)))
plus = np.array([1, 1])/np.sqrt(2); minus = np.array([1, -1])/np.sqrt(2); pi_ = np.array([1, 1j])/np.sqrt(2)
print('4.4', bloch(X @ plus), bloch(Z @ k0), bloch(H @ pi_), bloch(S @ minus))
st = S @ Ry(np.radians(120)) @ k0; print('4.5', bloch(st), abs(st[0])**2)
v = np.array([0.6, 0.8]); print('4.6', v**2, np.abs(H @ v)**2)
for b in ('00', '01', '10', '11'):
    psi = np.zeros(4); psi[int(b, 2)] = 1
    print('4.7', b, (cnot(0, 1, 2) @ op(H, 0, 2) @ psi).round(4))
for n in (4, 8, 20):
    F = math.factorial(n); k = math.ceil(math.log2(F))
    print(f'4.13 n={n}: position {n*n}, index {k}, unused {100*(2**k-F)/2**k:.1f}%')
A = 0.999**80*0.99**10; B = 0.999**20*0.99**30; e = 1 - 0.999**3
print('4.15', round(A, 3), round(B, 3), 'tie e =', round(e, 5))
for N in (100, 1000, 10000):
    dev = []
    for seed in range(5):
        c = sample(cnot(0, 1, 2) @ op(H, 0, 2) @ np.array([1, 0, 0, 0]), N, seed=seed)
        dev.append(abs(c.get('00', 0) - N/2))
    print(f'4.18 N={N}: mean |dev| {np.mean(dev):.1f}  sd theory {math.sqrt(N*0.25):.1f}')
def chrom(p1):
    psi = np.zeros(8); psi[0] = 1
    for k in range(3): psi = op(Ry(2*np.arcsin(np.sqrt(p1[k]))), k, 3) @ psi
    P = probs(psi); pv = sum(P.get(s, 0) for s in code)
    return P, pv, (sum(P.get(s, 0)*twt(code[s]) for s in code)/pv if pv > 1e-12 else float('nan'))
for p1 in ([0.9, 0.1, 0.9], [0.95, 0.05, 0.95], [0.0, 1.0, 0.0]):
    P, pv, E = chrom(p1); print('4.19/20', p1, 'P(101)', P.get('101', 0), 'P(invalid)', round(1-pv, 4), 'E', round(E, 3))
best = max(((chrom(p)[2], p) for p in itertools.product(np.linspace(0, 1, 11), repeat=3) if chrom(p)[1] > 1e-9), key=lambda t: t[0])
print('4.20 worst E on grid', best)
for p in (0.05, 0.09, 0.0909, 0.1, 0.2, 0.5): print('4.21', p, round((26 + 32*p)/(1 + p), 4))
def cost(x, lam):
    x1, x2, x3 = x
    return 40*x1 + 55*x2 + 35*x3 + 20*x1*x3 - 10*x2*x3 + lam*(x1 + x2 + x3 - 2)**2
for lam in (10, 45, 46):
    tab = {''.join(map(str, x)): cost(x, lam) for x in itertools.product((0, 1), repeat=3)}
    print('4.22 lam', lam, tab, 'min', min(tab, key=tab.get))
for e in (0.01, 0.05, 0.10, 0.20): print('4.24', e, 2*e*(1-e))
print('4.25', 1 - (0.95**4 + 0.05**4))
D = {'AB': 5, 'AC': 12, 'AD': 4, 'BC': 7, 'BD': 4, 'CD': 10}; dist = lambda a, b: D[''.join(sorted(a+b))]
valid = {}
for bits in itertools.product('01', repeat=9):
    M = np.array(bits, int).reshape(3, 3)
    if (M.sum(0) == 1).all() and (M.sum(1) == 1).all():
        tour = 'A' + ''.join('BCD'[np.argmax(M[:, t])] for t in range(3)) + 'A'
        L = sum(dist(tour[i], tour[i+1]) for i in range(4)); valid[''.join(bits)] = (tour, L)
print('4.27', len(valid), valid)
times = {'00': 32, '01': 27, '10': 41, '11': 35}
def route(p1):
    psi = np.zeros(4); psi[0] = 1
    for k in range(2): psi = op(Ry(2*np.arcsin(np.sqrt(p1[k]))), k, 2) @ psi
    P = probs(psi); return sum(P.get(s, 0)*times[s] for s in times), P
for p1 in ([0.5, 0.5], [0.2, 0.8], [0.05, 0.95]):
    E, P = route(p1); print('4.29', p1, round(E, 3), P)
s_, f_ = [3, 4, 2], [6, 5, 4]
mc = {''.join(map(str, x)): sum(x[i]*s_[i] + (1-x[i])*f_[i] for i in range(3)) + 50*(sum(x) == 3)
      for x in itertools.product((0, 1), repeat=3)}
print('4.30', mc, 'uniform E', np.mean(list(mc.values())), 'opt', min(mc, key=mc.get))
for p1 in ([0.9, 0.1, 0.9], [0.85, 0.15, 0.85]):
    print('4.30 chromosome', p1, round(p1[0]*(1-p1[1])*p1[2], 4))
