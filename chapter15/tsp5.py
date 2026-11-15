"""Chapter 15 project - the first 5 cities of the 8-city TSP.
City 0 is the fixed depot. Variable x(i,t), i = 1..4, t = 1..4:
16 qubits, q0 = x(1,1) is the leftmost bit of a book string."""
import math, itertools
import numpy as np
from tsp8 import pts
from tsp_qubo import tsp_qubo, decode_tour
from qubo import brute_force
N = 5
D = [[round(math.dist(a, b), 1) for b in pts[:N]] for a in pts[:N]]

def length(tour):
    """Closed tour length; tour like [0, 2, 4, 3, 1]."""
    return round(sum(D[tour[k]][tour[(k + 1) % N]]
                     for k in range(N)), 1)

def setup(lam=10):
    """QUBO and the value of every one of the 2^16 strings."""
    Q, c = tsp_qubo(D, lam)
    X, E = brute_force(Q, c)
    return Q, c, X, E

def feasible_mask(X):
    return np.array([decode_tour(x, N) is not None for x in X])

TOURS = [[0] + list(p) for p in itertools.permutations(range(1, N))]
