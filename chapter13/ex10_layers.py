"""Example 13.19 - more layers: p = 1, 2, 3, 4."""
import json
import numpy as np
from scipy.optimize import minimize
from shop9 import setup, FEASIBLE, OPT
from fastsim import qaoa_probs
from qaoa import expected_cost, interp
Q, c, H, E = setup(lam=20)
S = 50

def mean_cost(theta, p):        # theta = [u_1..u_p, beta_1..beta_p]
    return qaoa_probs(E, theta[:p] / S, theta[p:]) @ E

opts = {'rhobeg': 0.2, 'tol': 1e-4, 'maxiter': 3000}
x = np.array([0.0160 * S, -0.4123])          # p = 1 from Ex. 13.16
best = {}                                    # saved for Ex. 13.24
print('p  evals   <H>    check   P(opt)  P(feasible)')
for p in range(1, 5):
    if p > 1:
        x = np.array(interp(x[:p - 1]) + interp(x[p - 1:]))
    r = minimize(mean_cost, x, args=(p,), method='COBYLA',
                 options=opts)
    x = r.x
    g, b = x[:p] / S, x[p:]
    pr = qaoa_probs(E, g, b)
    e = expected_cost(H, g, b)              # check with Qiskit
    print(f'{p}  {r.nfev:5d}  {r.fun:6.2f}  {e:6.2f}'
          f'  {pr[OPT]:.4f}  {pr[FEASIBLE].sum():.4f}')
    print('   gamma:', np.round(g, 4), ' beta:', np.round(b, 3))
    best[p] = [list(g), list(b)]
json.dump(best, open('angles.json', 'w'))
