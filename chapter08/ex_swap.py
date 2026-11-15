import numpy as np
from tsp8 import D, tour_length
from tsp_qubo import tsp_qubo, decode_tour
from qubo import energy
from bin_algs import KA_bin
def flip_or_swap(x, rng):
    """Half the time flip one bit; half the time swap the steps of two cities (4 bits)."""
    if rng.random() < 0.5:
        c = x.copy(); k = rng.integers(len(x)); c[k] = 1 - c[k]; return c
    M = x.reshape(7, 7).copy(); a, b = rng.choice(7, 2, replace=False)
    M[[a, b]] = M[[b, a]]; return M.ravel()
Q, const = tsp_qubo(D, 20); f = lambda x: energy(Q, x, const)
lens = [tour_length(decode_tour(KA_bin(f, 49, 20000, s, move=flip_or_swap)[1], 8)) for s in range(10)]
print('KA + swap move:', lens)
print(f'mean {np.mean(lens):.2f}   RPD of mean {100 * (np.mean(lens) - 25.0) / 25.0:.1f}%   optimum 25.0 found in {lens.count(25.0)} of 10')
