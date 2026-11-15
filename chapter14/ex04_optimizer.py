"""Example 14.8 - COBYLA tunes gamma and beta (p = 1)."""
import numpy as np
from scipy.optimize import minimize
from tsp4 import setup, OPT, FEASIBLE
from fastsim import qaoa_probs
Q, c, H, E = setup(lam=20)
S = 50                       # the optimizer turns u = S * gamma

def cost(theta):             # theta = [u, beta]
    return qaoa_probs(E, [theta[0] / S], [theta[1]]) @ E

r = minimize(cost, [0.015 * S, -0.4363], method='COBYLA',
             options={'rhobeg': 0.2, 'tol': 1e-4})
g, b = r.x[0] / S, r.x[1]
P = qaoa_probs(E, [g], [b])
print(f'gamma = {g:.4f}, beta = {b:.4f}, <H> = {r.fun:.2f}, '
      f'evaluations = {r.nfev}')
print(f'P(optimal tour) = {P[OPT].sum():.4f}, '
      f'P(feasible) = {P[FEASIBLE].sum():.4f}')
cond = P[OPT].sum() / P[FEASIBLE].sum()
print(f'P(optimal | feasible) = {cond:.3f}')
