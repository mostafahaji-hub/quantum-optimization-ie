import numpy as np
from qubo import add_linear, add_quad, add_penalty_sum, brute_force
def supplier_qubo(lam):
    Q = np.zeros((3, 3))
    for i, c in enumerate([40, 55, 35]): add_linear(Q, i, c)
    add_quad(Q, 0, 2, 20); add_quad(Q, 1, 2, -10)
    const = add_penalty_sum(Q, [0, 1, 2], 2, lam)
    return Q, const
