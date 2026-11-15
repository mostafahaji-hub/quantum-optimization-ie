"""Example 14.25 - a fair table: how many shots for 99 percent?"""
import numpy as np
from tsp4 import D, length

def shots99(P):
    """Shots so that an optimal tour appears w.p. 0.99."""
    if P >= 1:
        return 1
    return int(np.ceil(np.log(0.01) / np.log(1 - P)))

def nearest_neighbour(start=0):
    """Chapter 2: always go to the closest city not yet visited."""
    tour, left = [start], set(range(4)) - {start}
    while left:
        nxt = min(left, key=lambda j: D[tour[-1]][j])
        tour.append(nxt)
        left.remove(nxt)
    return ''.join('ABCD'[i] for i in tour + [start])

t = nearest_neighbour()
print('nearest neighbour from A:', t, length(t))
methods = [('random 9-bit string (= QAOA with gamma = 0)', 2 / 512),
           ('QAOA p = 1, ideal (Ex. 14.8)', 0.0317),
           ('QAOA p = 4, ideal (Ex. 14.10)', 0.1708),
           ('QAOA p = 4, FakeFez raw (Ex. 14.13)', 0.0367),
           ('random tour (classical, 2 of 6)', 2 / 6),
           ('Grover, compact code, k = 1 (Ch. 12)', 1.0)]
print(f'{"method":44s}  P(opt)  shots99')
for name, P in methods:
    print(f'{name:44s}  {P:.4f}  {shots99(P):7d}')
grid, cobyla, shots = 41 * 37, 27, 1000   # Ex. 14.7 and 14.8
print(f'tuning p = 1 on hardware: ({grid} + {cobyla}) evaluations'
      f' x {shots} shots = {(grid + cobyla) * shots:,} shots')
