"""Chapter 15 - numbers for the self-test and exercise answers."""
import math, time
import numpy as np
import shop8, tsp8
from shop9 import tardiness, setup as shop_setup
from tsp4 import setup as tsp_setup
from sa import sa_qubo
from common import runs99, evals99
from tsp5 import setup as p_setup, feasible_mask, D as D5
print('15.1', [runs99(P) for P in (0.5, 0.1, 0.01)], runs99(1), runs99(0))
p3, d3, w3 = [2, 3, 4], [4, 7, 5], [1, 3, 3]
lpt = sorted([1, 2, 3], key=lambda j: -p3[j - 1])
print('15.3 LPT small', lpt, tardiness(lpt))
lpt8 = sorted(range(8), key=lambda j: -shop8.p[j])
print('15.3 LPT 8-job', [j + 1 for j in lpt8], shop8.twt(lpt8))
P = 1 - (511 / 512) ** 50
print('15.4', round(P, 4), runs99(P), evals99(P, 50))
Q, c, H, E = shop_setup(20)
for T0, Te in ((10, 1.0), (50, 5.0), (100, 10.0)):
    Ps = [np.mean([sa_qubo(Q, c, B, s, T0=T0, T_end=Te)[0] == 5
                   for s in range(1000)]) for B in (25, 100, 400)]
    e = [evals99(p, B) for p, B in zip(Ps, (25, 100, 400))]
    print('15.5 SA shop T0', T0, 'T_end', Te, 'P', np.round(Ps, 3),
          'best evals99', min(e))
print('15.6 KA first generation needs', 20 + 4 * 5 + 8 + 8)
print('15.7', round(math.sqrt(0.374 * 0.626 / 2000), 4),
      round(math.sqrt(0.264 * 0.736 / 2000), 4))
print('15.8', 1544000 / 400, 1544000 / 6)
print('15.9', f'{math.factorial(7) / 2 ** 49:.2e}',
      f'{1e4 * math.factorial(7) / 2 ** 49:.1e}')
print('15.10', [m * (m - 1) * (2 * m - 1) for m in (7, 9)])
print('15.11', f'{0.997 ** 4104:.1e}', f'{0.997 ** 4041:.1e}')
th = math.asin(1 / 256)
print('15.12 Grover rounds', math.floor(math.pi / (4 * th) + 1e-9),
      'classical average', (2 ** 16 + 1) / 2)
L = [tsp8.tour_length(t) for t in [[3, 0, 2, 4, 5, 6, 7, 1]]]
o = sorted(range(8), key=lambda j: (-shop8.w[j] / shop8.p[j], j))
o2 = o.copy(); i, j = o2.index(3), o2.index(7); o2[i], o2[j] = o2[j], o2[i]
print('15.14 WSPT', [k + 1 for k in o], shop8.twt(o), 'swap J4/J8',
      [k + 1 for k in o2], shop8.twt(o2))
Qp, cp, X, Ep = p_setup(10)
feas = feasible_mask(X)
k = int(np.argmin(np.where(feas, np.inf, Ep)))
print('15.15 feasible', feas.sum(), 'max distance', max(map(max, D5)),
      'longest tour', Ep[feas].max(), 'cheapest infeasible', Ep[k],
      'string', ''.join(map(str, X[k])))
print('15.17', round(0.0016 / 0.0171, 3), round(2 / 24, 3))
print('15.18', round(2859 / 53, 1), round(764 / 53, 1))
print('15.19', round(math.sqrt(0.008 * 0.992 / 2000), 4),
      f'{math.factorial(4) / 2 ** 16:.2e}')
Q4, c4, H4, E4 = tsp_setup(20)
t = time.time()
for s in range(2000):
    sa_qubo(Q4, c4, 25, s, T0=10, T_end=1.0)
print('15.20 SA small TSP, B=25: ms per run (this machine)',
      round((time.time() - t) / 2000 * 1000, 3))
se = math.sqrt(0.374 * 0.626 / 2000 + 0.383 * 0.617 / 2000)
print('15.7 difference', round(0.383 - 0.374, 3), 'se of difference',
      round(se, 4), 'z', round(0.009 / se, 2))
from tsp5 import length as len5
def nearest(D, start):
    tour, left = [start], set(range(len(D))) - {start}
    while left:
        nxt = min(sorted(left), key=lambda j: D[tour[-1]][j])
        tour.append(nxt); left.remove(nxt)
    return tour
print('15.16', [(s, nearest(D5, s), len5(nearest(D5, s)))
                for s in range(5)])
print('15.7 se for 0.600:', round(math.sqrt(0.6 * 0.4 / 2000), 4))
