"""Example 13.22 - the role of the penalty weight lambda."""
import numpy as np
from scipy.optimize import minimize
from shop9 import setup, FEASIBLE, OPT
from fastsim import qaoa_probs
from qaoa import interp

def best_qaoa(E, lam, p_max=3):
    """Grid for p = 1, then COBYLA and INTERP up to p_max."""
    S = 2.5 * lam                     # = 50 when lambda = 20
    f = lambda th, p: qaoa_probs(E, th[:p] / S, th[p:]) @ E
    gs = np.linspace(0, 2 / lam, 41)  # = 0..0.1 when lambda = 20
    bs = np.radians(np.arange(-90, 91, 5))
    _, g0, b0 = min((f(np.array([g * S, b]), 1), g, b)
                    for g in gs for b in bs)
    x, out = np.array([g0 * S, b0]), []
    for p in range(1, p_max + 1):
        if p > 1:
            x = np.array(interp(x[:p - 1]) + interp(x[p - 1:]))
        x = minimize(f, x, args=(p,), method='COBYLA',
                     options={'rhobeg': 0.2, 'tol': 1e-4,
                              'maxiter': 3000}).x
        pr = qaoa_probs(E, x[:p] / S, x[p:])
        out.append((pr[OPT], pr[FEASIBLE].sum()))
    return out

if __name__ == '__main__':
    print('lambda  lowest infeasible  below 8   P(opt) p=1  p=3'
          '   P(feasible) p=1  p=3')
    for lam in [3, 5, 10, 20, 40]:
        Q, c, H, E = setup(lam)
        low = E[~FEASIBLE].min()
        below = int((E[~FEASIBLE] < 8).sum())
        (o1, f1), _, (o3, f3) = best_qaoa(E, lam)
        print(f'{lam:6d}  {low:17.0f}  {below:7d}   {o1:10.4f}'
              f'  {o3:.4f}'
              f'   {f1:15.4f}  {f3:.4f}')
