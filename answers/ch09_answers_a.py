"""Chapter 9 answers, part A."""
import sys, math, time; sys.path.insert(0, '../chapter09'); sys.path.insert(1, '../chapter08')
import numpy as np
from scipy.stats import wilcoxon, friedmanchisquare
from sa import sa_qubo
from qubo import energy, brute_force
from tsp_qubo import tsp_qubo, decode_tour
from tsp8 import D, tour_length
import shop_pos_qubo as spq
t0 = time.time()
for dE in (1, 5, 20): print('9.1 dE', dE, [round(math.exp(-dE/T), 4) for T in (20, 5, 1)])
alpha = (0.05/10)**(1/20000); print('9.3 alpha', alpha, 'T after 10000', 10*alpha**10000)
Q4 = np.array([[-260., 200, 220], [0, -245, 190], [0, 0, -265]]); S = Q4 + Q4.T - np.diag(np.diag(Q4)); x = np.array([1, 0, 1]); i = 1
print('9.4 dE', (1 - 2*x[i])*(S[i] @ x - S[i, i]*x[i] + S[i, i]))
Dsm = [[0, 5, 12, 4], [5, 0, 7, 4], [12, 7, 0, 10], [4, 4, 10, 0]]
for name, (Q, c), opt in (('shop', spq.shop_pos_qubo(20), 5), ('tsp', tsp_qubo(Dsm, 20), 26)):
    for T0, T1 in ((10, 0.05), (10, 1.0)):
        hits = sum(abs(sa_qubo(Q, c, 500, s, T0=T0, T_end=T1)[0] - opt) < 1e-9 for s in range(20))
        p = hits/20; runs = math.ceil(math.log(0.01)/math.log(1-p)) if 0 < p < 1 else (1 if p == 1 else math.inf)
        print(f'9.5 {name} T0={T0} Tend={T1}: {hits}/20, runs for 99% = {runs}')
Q, c = tsp_qubo(D, 10)
def flip_or_swap(xv, rng):
    if rng.random() < 0.5:
        y = xv.copy(); k = rng.integers(len(xv)); y[k] = 1 - y[k]; return y
    M = xv.reshape(7, 7).copy(); a, b = rng.choice(7, 2, replace=False); M[[a, b]] = M[[b, a]]; return M.ravel()
def L(xv): t = decode_tour(xv, 8); return tour_length(t) if t else 60.0
v = [L(sa_qubo(Q, c, 20000, s, T0=10, T_end=1.0, move=flip_or_swap)[1]) for s in range(20)]
print(f'9.6 SA + swap move: mean {np.mean(v):.2f}, hits {v.count(25.0)}/20  ({time.time()-t0:.0f} s)')
for T in (1, 5, 20):
    v = [L(sa_qubo(Q, c, 20000, s, T0=T, T_end=T)[1]) for s in range(10)]
    print(f'9.7 constant T={T}: mean {np.mean(v):.2f} feasible {sum(x < 60 for x in v)}/10')
for P in (4, 8, 16):
    print('9.8 P', P, [round(-0.5*math.log(math.tanh(G/(P*1.0))), 5) for G in (20, 0.05)])
for p in (0.01, 0.1, 0.9): print('9.10', p, math.ceil(math.log(0.01)/math.log(1-p)))
y = [25.0, 27.8, 26.6, 26.6, 26.4]; print('9.13 S/N', -10*math.log10(np.mean(np.square(y))))
X = [26, 25, 27, 26, 28, 25, 25, 26, 27, 25]; Y = [28, 27, 26, 29, 31, 26, 27, 28, 29, 27]
w = wilcoxon(X, Y); print('9.17 statistic', w.statistic, 'p', round(w.pvalue, 4))
A_, B_, C_ = [26, 25, 27, 26], [28, 27, 26, 29], [30, 29, 31, 28]
ranks = np.array([np.argsort(np.argsort(r)) + 1 for r in zip(A_, B_, C_)]); print('9.18 mean ranks', ranks.mean(axis=0))
print('9.19', 1 - 0.95**10)
