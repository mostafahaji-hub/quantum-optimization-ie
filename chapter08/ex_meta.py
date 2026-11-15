import numpy as np
from tsp8 import D, tour_length
from tsp_qubo import tsp_qubo, decode_tour
from qubo import energy
from bin_algs import KA_bin, GA_bin, QEA_bin, random_bin
for lam in [5, 10, 20, 50, 200]:
    Q, const = tsp_qubo(D, lam)                     # 49 variables
    f = lambda x: energy(Q, x, const)
    for name, A in [('KA', KA_bin), ('GA', GA_bin), ('QEA', QEA_bin), ('Random', random_bin)]:
        lens = []
        for s in range(10):
            val, x = A(f, 49, 20000, s)
            t = decode_tour(x, 8)
            if t: lens.append(tour_length(t))
        txt = f'best {min(lens):4.1f}  mean {np.mean(lens):4.1f}' if lens else '-'
        print(f'lam {lam:3d}  {name:6s} feasible {len(lens):2d}/10  {txt}')
