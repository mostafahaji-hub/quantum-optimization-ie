import numpy as np
from qubo import to_ising
def sqa_qubo(Q, const, steps, seed, P=8, T=0.5, G0=20.0, G_end=0.05):
    """Simulated quantum annealing (path-integral Monte Carlo) on the Ising form of a QUBO.
    P replicas ('slices') of the spins are coupled; the coupling grows as the transverse field G falls."""
    rng = np.random.default_rng(seed)
    h, J, off = to_ising(Q, const); n = len(h)
    Jsym = J + J.T
    z = rng.choice([-1, 1], size=(P, n))
    beta = 1.0 / T; gamma = (G_end / G0) ** (1 / steps); G = G0
    best_E, best_x = np.inf, None
    for _ in range(steps):
        Jp = -0.5 / beta * np.log(np.tanh(beta * G / P))      # replica coupling (grows as G -> 0)
        k = rng.integers(P); i = rng.integers(n)
        local = h[i] + Jsym[i] @ z[k]                            # problem field on spin i in slice k
        dE = -2 * z[k, i] * local / P                            # problem part, shared by P slices
        dE += 2 * Jp * z[k, i] * (z[(k - 1) % P, i] + z[(k + 1) % P, i])   # keep neighbouring slices alike
        if dE <= 0 or rng.random() < np.exp(-beta * dE):
            z[k, i] *= -1
            x = (1 - z[k]) // 2                                   # book convention: x = (1 - z)/2
            E = float(x @ Q @ x + const)
            if E < best_E: best_E, best_x = E, x.copy()
        G *= gamma
    return best_E, best_x
