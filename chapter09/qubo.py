import itertools
import numpy as np
def energy(Q, x, const=0.0):
    """QUBO value x^T Q x + const (Q upper triangular; linear terms on the diagonal)."""
    x = np.asarray(x)
    return float(x @ Q @ x + const)
def add_linear(Q, i, a):
    Q[i, i] += a
def add_quad(Q, i, j, b):
    if i == j: Q[i, i] += b                      # x_i * x_i = x_i
    else: Q[min(i, j), max(i, j)] += b
def add_penalty_sum(Q, idx, k, lam, coef=None):
    """Add lam * (sum_i a_i x_i - k)^2 ; returns the constant lam * k^2."""
    a = [1] * len(idx) if coef is None else coef
    for u, i in enumerate(idx):
        add_linear(Q, i, lam * (a[u] * a[u] - 2 * k * a[u]))
        for v in range(u + 1, len(idx)):
            add_quad(Q, i, idx[v], 2 * lam * a[u] * a[v])
    return lam * k * k
def brute_force(Q, const=0.0):
    """Evaluate all 2^n bit strings (n up to about 22); returns bits and values."""
    n = len(Q)
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)[::-1]) & 1).astype(np.int8)
    E = np.empty(2 ** n)
    for a in range(0, 2 ** n, 2 ** 18):                       # in chunks, to save memory
        B = X[a:a + 2 ** 18].astype(float)
        E[a:a + 2 ** 18] = ((B @ Q) * B).sum(axis=1) + const
    return X, E
def to_ising(Q, const=0.0):
    """x_i = (1 - z_i)/2  (qubit |0> -> z=+1, |1> -> z=-1).  Returns h, J, offset with
    f = offset + sum_i h_i z_i + sum_{i<j} J_ij z_i z_j."""
    n = len(Q); h = np.zeros(n); J = np.zeros((n, n)); offset = const
    for i in range(n):
        h[i] -= Q[i, i] / 2; offset += Q[i, i] / 2
        for j in range(i + 1, n):
            q = Q[i, j]
            J[i, j] += q / 4; h[i] -= q / 4; h[j] -= q / 4; offset += q / 4
    return h, J, offset
