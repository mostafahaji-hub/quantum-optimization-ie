import numpy as np
from qubo import add_linear, add_quad, add_penalty_sum
p = [2, 3, 4]; d = [4, 7, 5]; wt = [1, 3, 3]                  # small workshop of Chapter 2
v = lambda j, k: 3 * j + k                                     # index of x(j,k): job j in position k (0-based)
def shop_pos_qubo(lam):
    """Position model (9 variables). Exact only because the workshop has 3 jobs."""
    Q = np.zeros((9, 9)); const = 0.0
    for j in range(3):
        add_linear(Q, v(j, 0), wt[j] * max(0, p[j] - d[j]))           # j first: C = p_j
        add_linear(Q, v(j, 2), wt[j] * max(0, sum(p) - d[j]))         # j last:  C = 9
        for i in range(3):
            if i != j:                                                # i first, j second: C = p_i + p_j
                add_quad(Q, v(i, 0), v(j, 1), wt[j] * max(0, p[i] + p[j] - d[j]))
    for j in range(3): const += add_penalty_sum(Q, [v(j, k) for k in range(3)], 1, lam)   # each job once
    for k in range(3): const += add_penalty_sum(Q, [v(j, k) for j in range(3)], 1, lam)   # each position once
    return Q, const
