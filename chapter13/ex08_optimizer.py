"""Example 13.16 - let a classical optimizer tune gamma and beta."""
import numpy as np
from scipy.optimize import minimize
from shop9 import setup
from qaoa import expected_cost
Q, c, H, E = setup(lam=20)
S = 50                      # optimizer turns u = S*gamma, not gamma
trace = []                  # every <H> the optimizer asks for

def cost(theta):            # theta = [u, beta]
    e = expected_cost(H, [theta[0] / S], [theta[1]])
    trace.append(e)
    return e

opts = {'rhobeg': 0.2, 'tol': 1e-4}     # first step, final step
r = minimize(cost, [0.015 * S, -0.4363], method='COBYLA',
             options=opts)
print(f'from the best grid point: gamma = {r.x[0] / S:.4f}, '
      f'beta = {r.x[1]:.4f}, <H> = {r.fun:.2f}, '
      f'evaluations = {r.nfev}')
np.savetxt('trace.txt', trace)
rng = np.random.default_rng(2026)
print('five random starts (gamma, beta):')
for _ in range(5):
    x0 = [rng.uniform(0, 0.1) * S,
          rng.uniform(-np.pi / 2, np.pi / 2)]
    r = minimize(cost, x0, method='COBYLA', options=opts)
    print(f'  ({x0[0] / S:.3f}, {x0[1]:6.3f}) -> '
          f'({r.x[0] / S:.4f}, {r.x[1]:6.3f})  <H> = {r.fun:6.2f}'
          f'  evaluations = {r.nfev}')
