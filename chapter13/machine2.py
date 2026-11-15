"""Chapter 13 - two machines, choose exactly one:
f = 4 x0 + 6 x1 + 10 (x0 + x1 - 1)^2   (x0 = machine M1)."""
import numpy as np
from qubo import add_linear, add_penalty_sum

def machine_qubo(lam=10):
    Q = np.zeros((2, 2))
    add_linear(Q, 0, 4)
    add_linear(Q, 1, 6)
    const = add_penalty_sum(Q, [0, 1], 1, lam)
    return Q, const
