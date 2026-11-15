import numpy as np
from sa import sa_qubo
from tsp8 import D, tour_length
from tsp_qubo import tsp_qubo, decode_tour
for lam in [10, 20, 50, 200]:
    Q, c = tsp_qubo(D, lam)
    L = [decode_tour(sa_qubo(Q, c, 20000, s, T0=10, T_end=0.05)[1], 8) for s in range(10)]
    lens = [tour_length(t) for t in L if t]
    print(f'lam {lam:3d}: feasible {len(lens)}/10  mean tour {np.mean(lens):.2f}  best {min(lens)}')
