import numpy as np, time
from scipy.stats import wilcoxon, friedmanchisquare
from sa import sa_qubo
from sqa import sqa_qubo
from tsp8 import D, tour_length
from tsp_qubo import tsp_qubo, decode_tour
from qubo import energy
from bin_algs import KA_bin, GA_bin
Q, c = tsp_qubo(D, 10); f = lambda x: energy(Q, x, c)
def L(x): t = decode_tour(x, 8); return tour_length(t) if t else 60.0    # infeasible counts as 60
algs = {'SA':  lambda s: sa_qubo(Q, c, 20000, s, T0=10, T_end=1.0)[1],     # Taguchi settings
        'SQA': lambda s: sqa_qubo(Q, c, 20000, s, P=8, T=1.0, G0=20)[1],
        'KA':  lambda s: KA_bin(f, 49, 20000, s)[1],
        'GA':  lambda s: GA_bin(f, 49, 20000, s)[1]}
res = {}
for name, run in algs.items():
    t = time.time(); res[name] = [L(run(s)) for s in range(20)]; sec = (time.time() - t) / 20
    hits = sum(v == 25.0 for v in res[name])
    print(f'{name:3s}  mean {np.mean(res[name]):5.2f}  best {min(res[name])}  hit 25.0: {hits:2d}/20  sec/run {sec:.2f}')
print('Wilcoxon SA vs SQA: p =', round(float(wilcoxon(res['SA'], res['SQA']).pvalue), 4))
print('Friedman (4 algorithms): p =', f"{friedmanchisquare(*res.values()).pvalue:.1e}")
