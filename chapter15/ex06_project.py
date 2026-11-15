"""Example 15.12 - first steps of the final project (16 qubits)."""
import numpy as np
from scipy.optimize import minimize
from tsp5 import D, TOURS, length, setup, feasible_mask
from fastsim import qaoa_probs
from common import runs99
L = sorted((length(t), t) for t in TOURS)
print('24 directed tours; shortest:', L[:3])
print('distinct lengths:', sorted({l for l, _ in L}))
Q, c, X, E = setup(lam=10)
feas = feasible_mask(X)
opt = np.isclose(E, L[0][0])
print('strings', len(E), 'feasible', feas.sum(),
      'optimal', opt.sum(),
      'mean (= offset)', round(E.mean(), 2),
      'cheapest infeasible', E[~feas].min())
S = 50                                     # gamma = u / S (Ch. 13)
f = lambda t: qaoa_probs(E, [t[0] / S], [t[1]]) @ E
G = np.linspace(0, 0.1, 21)
B = np.linspace(-np.pi / 2, np.pi / 2, 19)
M = np.array([[f([g * S, b]) for g in G] for b in B])
i, j = np.unravel_index(M.argmin(), M.shape)
print(f'grid best gamma {G[j]:.3f} beta {B[i]:.4f}'
      f' <H> {M[i, j]:.2f}')
r = minimize(f, [G[j] * S, B[i]], method='COBYLA',
             options={'rhobeg': 0.2, 'tol': 1e-4})
P = qaoa_probs(E, [r.x[0] / S], [r.x[1]])
po, pf = P[opt].sum(), P[feas].sum()
print(f'COBYLA gamma {r.x[0] / S:.4f} beta {r.x[1]:.4f} '
      f'<H> {r.fun:.2f} evals {r.nfev}')
print(f'P(opt) {po:.5f} P(feas) {pf:.4f} P(opt|feas) {po / pf:.3f}'
      f' shots99 {runs99(po)}')
print('random 16-bit string shots99', runs99(opt.sum() / 2 ** 16),
      '| random tour shots99', runs99(opt.sum() / 24))
