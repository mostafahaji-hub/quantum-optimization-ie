import numpy as np
def sa_qubo(Q, const, steps, seed, T0, T_end, x0=None, move=None):
    """Simulated annealing on a QUBO with single-bit flips (or a custom move).
    Geometric cooling from T0 to T_end over `steps` proposals."""
    rng = np.random.default_rng(seed); n = len(Q)
    S = Q + Q.T - np.diag(np.diag(Q))                 # symmetric couplings, diagonal = linear terms
    x = rng.integers(0, 2, n) if x0 is None else np.array(x0)
    E = float(x @ Q @ x + const); best_x, best_E = x.copy(), E
    alpha = (T_end / T0) ** (1 / steps); T = T0
    for _ in range(steps):
        if move is None:                                # flip bit i: exact energy change in O(n)
            i = rng.integers(n)
            dE = (1 - 2 * x[i]) * (S[i] @ x - S[i, i] * x[i] + S[i, i])
            if dE <= 0 or rng.random() < np.exp(-dE / T):
                x[i] = 1 - x[i]; E += dE
        else:
            y = move(x, rng); Ey = float(y @ Q @ y + const); dE = Ey - E
            if dE <= 0 or rng.random() < np.exp(-dE / T):
                x, E = y, Ey
        if E < best_E: best_x, best_E = x.copy(), E
        T *= alpha
    return best_E, best_x
