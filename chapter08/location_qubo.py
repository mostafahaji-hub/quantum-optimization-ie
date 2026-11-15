import numpy as np
from qubo import add_linear, add_quad, add_penalty_sum
f = [30, 20, 25]                                  # fixed cost of opening warehouse W1, W2, W3
c = [[4, 9, 12],                                  # c[i][j]: cost of serving customer j from warehouse i
     [10, 5, 9],
     [13, 8, 3]]
y = lambda i: i                                   # y_i: warehouse i open           -> indices 0..2
x = lambda i, j: 3 + 3 * i + j                    # x_ij: customer j served by i    -> indices 3..11
def location_qubo(lam):
    Q = np.zeros((12, 12)); const = 0.0
    for i in range(3):
        add_linear(Q, y(i), f[i])
        for j in range(3):
            add_linear(Q, x(i, j), c[i][j])
            add_linear(Q, x(i, j), lam); add_quad(Q, x(i, j), y(i), -lam)   # x_ij <= y_i : lam*(x - x*y)
    for j in range(3):                                                       # every customer served once
        const += add_penalty_sum(Q, [x(i, j) for i in range(3)], 1, lam)
    return Q, const
def decode(b):
    opened = [i + 1 for i in range(3) if b[y(i)]]
    serve = {j + 1: [i + 1 for i in range(3) if b[x(i, j)]] for j in range(3)}
    ok = all(len(s) == 1 and s[0] in opened for s in serve.values())
    return opened, serve, ok
