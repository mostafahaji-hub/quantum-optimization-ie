"""Chapter 9 answers, part C: Exercises 9.16 and 9.22."""
import sys, math, time, itertools; sys.path.insert(0, '../chapter09'); sys.path.insert(1, '../chapter08'); sys.path.insert(2, '../chapter07')
import numpy as np
from scipy.stats import friedmanchisquare
from ka_perm import keshtel_perm
from prob20 import n as n20, twt as twt20
t0 = time.time()
L9 = [(0,0,0,0),(0,1,1,1),(0,2,2,2),(1,0,1,2),(1,1,2,0),(1,2,0,1),(2,0,2,1),(2,1,0,2),(2,2,1,0)]
lv = {'nPop': [10, 20, 30], 'PN1': [0.1, 0.2, 0.3], 'PN2': [0.2, 0.4, 0.6], 'NSwirl': [2, 5, 10]}
names = list(lv); sn = []
for row in L9:
    pr = {k: lv[k][row[i]] for i, k in enumerate(names)}
    if pr['PN1'] + pr['PN2'] >= 1: pr['PN2'] = 0.6 - 1e-9
    y = [keshtel_perm(twt20, n20, budget=3000, n_pop=pr['nPop'], pn1=pr['PN1'], pn2=pr['PN2'], n_swirl=pr['NSwirl'], seed=s)[0] for s in range(5)]
    sn.append(-10*math.log10(np.mean(np.square(y))))
for i, k in enumerate(names):
    m = [np.mean([sn[r] for r, row in enumerate(L9) if row[i] == j]) for j in range(3)]
    print(f'9.16 {k}: mean S/N by level {[round(x, 3) for x in m]} best {lv[k][int(np.argmax(m))]}')
print(f'9.16 ({time.time()-t0:.0f} s)')
from qubo import add_quad, add_penalty_sum, brute_force, energy
from sa import sa_qubo
from sqa import sqa_qubo
from bin_algs import KA_bin
r = np.random.default_rng(20); flow = r.integers(0, 12, (3, 3)); dist = r.integers(2, 10, (3, 3))
x = lambda i, k: 3*i + k; y_ = lambda j, l: 9 + 3*j + l
Q = np.zeros((18, 18)); c = 0.0
for i, j, k, l in itertools.product(range(3), repeat=4): add_quad(Q, x(i, k), y_(j, l), flow[i][j]*dist[k][l])
for v in (x, y_):
    for a in range(3):
        c += add_penalty_sum(Q, [v(a, b) for b in range(3)], 1, 60); c += add_penalty_sum(Q, [v(b, a) for b in range(3)], 1, 60)
f = lambda xx: energy(Q, xx, c)
res = {'SA': [sa_qubo(Q, c, 5000, s, T0=60, T_end=1.0)[0] for s in range(20)],
       'SQA': [sqa_qubo(Q, c, 5000, s, P=8, T=10.0, G0=60)[0] for s in range(20)],
       'KA': [KA_bin(f, 18, 5000, s)[0] for s in range(20)]}
for k, v in res.items(): print(f'9.22 {k}: mean {np.mean(v):.1f} optimum 170 hits {sum(abs(a - 170) < 1e-9 for a in v)}/20')
print('9.22 Friedman p', friedmanchisquare(*res.values()).pvalue, f'({time.time()-t0:.0f} s)')
