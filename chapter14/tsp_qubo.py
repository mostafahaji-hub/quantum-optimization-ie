import numpy as np
from qubo import add_linear, add_quad, add_penalty_sum
def tsp_qubo(D, lam):
    """Position model, city 0 is the fixed depot. Variable x(i,t): city i (1..n-1) at step t (1..n-1)."""
    n = len(D); m = n - 1
    v = lambda i, t: (i - 1) * m + (t - 1)          # index of x(i,t)
    Q = np.zeros((m * m, m * m)); const = 0.0
    for i in range(1, n):
        add_linear(Q, v(i, 1), D[0][i])             # depot -> first city
        add_linear(Q, v(i, m), D[i][0])             # last city -> depot
        for j in range(1, n):
            if i != j:
                for t in range(1, m):
                    add_quad(Q, v(i, t), v(j, t + 1), D[i][j])   # i at t, j at t+1
    for i in range(1, n):                           # every city exactly once
        const += add_penalty_sum(Q, [v(i, t) for t in range(1, m + 1)], 1, lam)
    for t in range(1, m + 1):                       # every step exactly one city
        const += add_penalty_sum(Q, [v(i, t) for i in range(1, n)], 1, lam)
    return Q, const
def decode_tour(x, n):
    """Bits -> tour, or None if the bits are not a permutation matrix."""
    m = n - 1; M = np.asarray(x).reshape(m, m)
    if not (M.sum(0) == 1).all() or not (M.sum(1) == 1).all(): return None
    return [0] + [int(np.argmax(M[:, t])) + 1 for t in range(m)]
