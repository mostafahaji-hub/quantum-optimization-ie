import numpy as np
from sa import sa_qubo
from tsp8 import D, tour_length
from tsp_qubo import tsp_qubo, decode_tour
A = [5, 10, 20]; B = [0.01, 0.1, 1.0]; C = [10, 15, 20]          # T0, T_end, lambda
L9 = [(0,0,0),(0,1,1),(0,2,2),(1,0,1),(1,1,2),(1,2,0),(2,0,2),(2,1,0),(2,2,1)]
sn = []
for r, (a, b, cc) in enumerate(L9, 1):
    Q, c = tsp_qubo(D, C[cc])
    y = [tour_length(decode_tour(sa_qubo(Q, c, 20000, s, A[a], B[b])[1], 8)) for s in range(5)]
    sn.append(-10 * np.log10(np.mean(np.square(y))))                 # smaller-the-better S/N
    print(f'run {r}: T0={A[a]:2d} T_end={B[b]:4} lam={C[cc]}  y={y}  S/N={sn[-1]:.3f}')
for name, col, lv in [('T0', 0, A), ('T_end', 1, B), ('lam', 2, C)]:
    m = [np.mean([sn[r] for r, row in enumerate(L9) if row[col] == k]) for k in range(3)]
    print(name, "mean S/N by level:", [round(float(v), 3) for v in m], ' best level:', lv[int(np.argmax(m))])
