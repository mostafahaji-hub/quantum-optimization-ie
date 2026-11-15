"""Chapter 8 answers, part A (hand checks and small QUBOs)."""
import sys, itertools, math; sys.path.insert(0, '../chapter08')
import numpy as np
from qubo import energy, add_linear, add_quad, add_penalty_sum, brute_force, to_ising
from tsp_qubo import tsp_qubo, decode_tour
import shop_pos_qubo as spq
from location_qubo import location_qubo, decode
Q = np.array([[2, 4, 0], [0, -3, -2], [0, 0, 1]], float); X, E = brute_force(Q)
print('8.1', {''.join(map(str, x)): e for x, e in zip(X, E)})
for s in ('0000', '1100', '1111'): print('8.2', s, (sum(map(int, s)) - 2)**2)
def sup(lam, a13=20, k=2):
    Q = np.zeros((3, 3))
    for i, c in enumerate([40, 55, 35]): add_linear(Q, i, c)
    add_quad(Q, 0, 2, a13); add_quad(Q, 1, 2, -10)
    return Q, add_penalty_sum(Q, [0, 1, 2], k, lam)
for lam in (44, 45, 46):
    X, E = brute_force(*sup(lam, 50)); print('8.5 lam', lam, ''.join(map(str, X[np.argmin(E)])), E.min())
Q6, c6 = sup(100, 20, 1); print('8.6 matrix', Q6.tolist(), 'const', c6)
for lam in (34, 35, 36):
    X, E = brute_force(*sup(lam, 20, 1)); print('8.6 lam', lam, ''.join(map(str, X[np.argmin(E)])), E.min())
D = [[0, 5, 12, 4], [5, 0, 7, 4], [12, 7, 0, 10], [4, 4, 10, 0]]
Qt, ct = tsp_qubo(D, 20); print('8.7 row C2 (index 4):', Qt[4].astype(int).tolist(), 'column C2:', Qt[:, 4].astype(int).tolist())
print('8.8', energy(Qt, [1, 0, 0, 1, 0, 0, 0, 0, 1], ct))
D9 = [[0, 5, 3, 4], [5, 0, 7, 4], [3, 7, 0, 10], [4, 4, 10, 0]]
for lam in (2, 3, 4, 5, 6, 8):
    X, E = brute_force(*tsp_qubo(D9, lam)); k = int(np.argmin(E)); t = decode_tour(X[k], 4)
    print('8.9 lam', lam, E[k], t if t else 'infeasible ' + ''.join(map(str, X[k])))
spq.d = [4, 7, 8]; X, E = brute_force(*spq.shop_pos_qubo(20)); k = int(np.argmin(E))
print('8.10 d3=8 optimum', ''.join(map(str, X[k])), E[k]); spq.d = [4, 7, 5]
p, w = [2, 3, 4], [1, 3, 3]; v = lambda j, k: 3*j + k
Q12 = np.zeros((9, 9)); c12 = 0
for j in range(3):
    for k in range(3): add_linear(Q12, v(j, k), w[j]*p[j])
    for k in range(3):
        for i in range(3):
            if i != j:
                for l in range(k): add_quad(Q12, v(i, l), v(j, k), w[j]*p[i])
for j in range(3): c12 += add_penalty_sum(Q12, [v(j, k) for k in range(3)], 1, 100)
for k in range(3): c12 += add_penalty_sum(Q12, [v(j, k) for j in range(3)], 1, 100)
X, E = brute_force(Q12, c12); k = int(np.argmin(E)); M = X[k].reshape(3, 3)
print('8.12 sum wC optimum', ''.join(map(str, X[k])), E[k], 'order', ['J%d' % (np.argmax(M[:, c]) + 1) for c in range(3)])
pp = [6, 8, 9, 6, 3, 6, 7, 2]; print('8.13 hours', sum(47 - x + 1 for x in pp), ' minutes', sum(2820 - 60*x + 1 for x in pp))
f_, c_ = [30, 20, 25], [[4, 9, 12], [10, 5, 9], [13, 8, 3]]
for S in itertools.chain.from_iterable(itertools.combinations(range(3), r) for r in (1, 2, 3)):
    print('8.16', ['W%d' % (i+1) for i in S], sum(f_[i] for i in S) + sum(min(c_[i][j] for i in S) for j in range(3)))
import location_qubo as lq
lq.f = [30, 20, 5]
for lam in (9, 13, 13.1, 14):
    X, E = brute_force(*lq.location_qubo(lam)); k = int(np.argmin(E)); o, s, ok = lq.decode(X[k])
    print('8.18 lam', lam, E[k], o, s, ok)
fl, di = [[10, 12], [4, 8]], [[2, 6], [5, 3]]
for ia in ((0, 1), (1, 0)):
    for ob in ((0, 1), (1, 0)):
        cost = sum(fl[i][j]*di[ia[i]][ob[j]] for i in range(2) for j in range(2))
        print('8.19 T1,T2 at', ['AB'[ia[0]], 'AB'[ia[1]]], 'O1,O2 at', ['CD'[ob[0]], 'CD'[ob[1]]], cost)
h, J, off = to_ising(np.array([[1., -2.], [0, 1.]])); print('8.21 h', h, 'J12', J[0, 1], 'offset', off)
for Q2 in (np.array([[3., -4], [0, 2]]), np.array([[1., 5], [0, -2]])):
    X, E = brute_force(Q2); print('8.22 mean', E.mean(), 'offset', to_ising(Q2)[2])
