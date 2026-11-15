import numpy as np
from sa import sa_qubo
from sqa import sqa_qubo
from tsp8 import D, tour_length
from tsp_qubo import tsp_qubo, decode_tour
Q, c = tsp_qubo(D, 20)
def L(x): t = decode_tour(x, 8); return tour_length(t) if t else None
sa  = [L(sa_qubo(Q, c, 20000, s, T0=10, T_end=0.05)[1]) for s in range(10)]
sqa = [L(sqa_qubo(Q, c, 20000, s, P=8, T=1.0, G0=20)[1]) for s in range(10)]
print('SA :', sa, ' mean', round(np.mean(sa), 2))
print('SQA:', sqa, ' mean', round(np.mean(sqa), 2))
