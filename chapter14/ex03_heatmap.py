"""Example 14.7 - the gamma-beta landscape of the TSP, coarse and fine."""
import numpy as np
from tsp4 import setup
from fastsim import qaoa_probs
Q, c, H, E = setup(lam=20)

def grid(gs, bs):
    """<H> for every (beta, gamma): rows beta, columns gamma."""
    return np.array([[qaoa_probs(E, [g], [b]) @ E for g in gs]
                     for b in bs])

for name, gs, bs in [
        ('coarse 21 x 19', np.linspace(0, np.pi, 21),
         np.linspace(-np.pi / 2, np.pi / 2, 19)),
        ('fine 41 x 37', np.linspace(0, 0.1, 41),
         np.linspace(-np.pi / 2, np.pi / 2, 37))]:
    M = grid(gs, bs)
    i, j = np.unravel_index(M.argmin(), M.shape)
    print(f'{name}: best gamma = {gs[j]:.4f}, beta = {bs[i]:.4f},'
          f' <H> = {M[i, j]:.2f}')
np.savez('heatmap.npz', G=gs, B=bs, M=M)      # fine grid, for Fig.
