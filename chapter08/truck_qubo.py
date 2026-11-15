import numpy as np
from qubo import add_linear, add_penalty_sum
w = [7, 9, 9, 6, 8, 5, 9, 2]; v = [9, 13, 14, 7, 6, 13, 6, 3]; CAP = 20
SLACK = [1, 2, 4, 8, 5]                        # slack bits: any value 0..20
def truck_qubo(lam):
    n = len(w) + len(SLACK)
    Q = np.zeros((n, n))
    for i in range(len(w)): add_linear(Q, i, -v[i])          # maximize profit = minimize -profit
    const = add_penalty_sum(Q, list(range(n)), CAP, lam, coef=w + SLACK)
    return Q, const
