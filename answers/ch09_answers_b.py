"""Chapter 9 answers, part B: Exercises 9.9, 9.14, 9.15."""
import sys, math, time; sys.path.insert(0, '../chapter09'); sys.path.insert(1, '../chapter08')
import numpy as np
from scipy.stats import wilcoxon
from sa import sa_qubo
import sqa as SQ
from qubo import to_ising, energy
from tsp_qubo import tsp_qubo, decode_tour
from tsp8 import D, tour_length
t0 = time.time()
def L(x): t = decode_tour(x, 8); return tour_length(t) if t else 60.0
Q, c = tsp_qubo(D, 10)
def sqa_nospring(Q, const, steps, seed, P=8, T=1.0):
    rng = np.random.default_rng(seed); h, J, off = to_ising(Q, const); n = len(h); Jsym = J + J.T
    z = rng.choice([-1, 1], size=(P, n)); beta = 1/T; best_E, best_x = np.inf, None
    for _ in range(steps):
        k = rng.integers(P); i = rng.integers(n)
        dE = -2*z[k, i]*(h[i] + Jsym[i] @ z[k])/P
        if dE <= 0 or rng.random() < np.exp(-beta*dE):
            z[k, i] *= -1; x = (1 - z[k])//2; E = float(x @ Q @ x + const)
            if E < best_E: best_E, best_x = E, x.copy()
    return best_E, best_x
v = [L(sqa_nospring(Q, c, 20000, s)[1]) for s in range(10)]
print(f'9.9 SQA without springs: mean {np.mean(v):.2f} (with springs 27.72)  ({time.time()-t0:.0f} s)')
a = [L(sa_qubo(Q, c, 20000, s, T0=10, T_end=1.0)[1]) for s in range(30)]
b = [L(sa_qubo(*tsp_qubo(D, 20), 20000, s, T0=20, T_end=0.05)[1]) for s in range(30)]
print(f'9.14 Taguchi (10, 1.0, 10): mean {np.mean(a):.2f}; guess (20, 0.05, 20): mean {np.mean(b):.2f}; Wilcoxon p = {wilcoxon(a, b).pvalue:.4f}  ({time.time()-t0:.0f} s)')
Ps, Ts, Gs = [4, 8, 16], [0.5, 1.0, 2.0], [5.0, 20.0, 50.0]
L9 = [(0,0,0),(0,1,1),(0,2,2),(1,0,1),(1,1,2),(1,2,0),(2,0,2),(2,1,0),(2,2,1)]
sn = []
for row in L9:
    y = [L(SQ.sqa_qubo(Q, c, 20000, s, P=Ps[row[0]], T=Ts[row[1]], G0=Gs[row[2]])[1]) for s in range(5)]
    sn.append(-10*math.log10(np.mean(np.square(y))))
best = []
for col, lv in ((0, Ps), (1, Ts), (2, Gs)):
    m = [np.mean([sn[r] for r, row in enumerate(L9) if row[col] == k]) for k in range(3)]; best.append(lv[int(np.argmax(m))])
    print('9.15 main effects', [round(x, 3) for x in m], 'best', lv[int(np.argmax(m))])
q = [L(SQ.sqa_qubo(Q, c, 20000, s, P=best[0], T=best[1], G0=best[2])[1]) for s in range(20)]
sa20 = [L(sa_qubo(Q, c, 20000, s, T0=10, T_end=1.0)[1]) for s in range(20)]
print(f'9.15 tuned SQA {best}: mean {np.mean(q):.2f} hits {q.count(25.0)}/20; SA mean {np.mean(sa20):.2f} hits {sa20.count(25.0)}/20; Wilcoxon p = {wilcoxon(sa20, q).pvalue:.4f}  ({time.time()-t0:.0f} s)')
