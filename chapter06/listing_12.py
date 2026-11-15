# Chapter 6, code listing 12 (in order of appearance)
import math
# Large TSP of Chapter 2 (8 cities)
pts = [(6, 6), (0, 4), (8, 7), (6, 4), (7, 5), (9, 3), (8, 2), (4, 2)]
D = [[round(math.dist(a, b), 1) for b in pts] for a in pts]
def tour_length(tour):
    return round(sum(D[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour))), 1)
import numpy as np
from qea import observe, rotate
from keys import decode_keys
from tsp8 import tour_length
def qea_tsp(seed, pop=20, gens=150, dtheta=np.radians(3), k=3):
    rng = np.random.default_rng(seed)
    n = 7                                     # cities 2..8; city 1 is the depot
    Q = [np.full(n * k, np.pi/4) for _ in range(pop)]
    best_bits, best_len = None, 1e9
    for g in range(gens):
        for i in range(pop):
            x = observe(Q[i], rng)
            tour = [0] + [c + 1 for c in decode_keys(x, n, k)[1]]
            L = tour_length(tour)
            if L < best_len:
                best_bits, best_len, best_tour = x, L, tour
            Q[i] = rotate(Q[i], x, best_bits, dtheta)
    return best_len, best_tour
res = []
for s in range(10):
    L, tour = qea_tsp(s)
    res.append(L)
    if s == 0:
        print('run 0 tour:', [c + 1 for c in tour], 'length', L)
print('10 runs:', res)
print('best', min(res), ' mean', round(np.mean(res), 2), ' (nearest neighbour 28.3, optimum 25.0)')