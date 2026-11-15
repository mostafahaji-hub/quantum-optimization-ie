"""Example 13.14 - the (gamma, beta) map for p = 1."""
import numpy as np
from shop9 import setup
from qaoa import expected_cost
Q, c, H, E = setup(lam=20)

def scan(gammas, betas):
    """<H> on a grid; rows = beta, columns = gamma."""
    M = np.array([[expected_cost(H, [g], [b]) for g in gammas]
                  for b in betas])
    i, j = np.unravel_index(M.argmin(), M.shape)
    return M, gammas[j], betas[i], M[i, j]

coarse = scan(np.linspace(0, np.pi, 21),
              np.linspace(-np.pi / 2, np.pi / 2, 19))
fine_g = np.linspace(0, 0.1, 41)            # step 0.0025
fine_b = np.radians(np.arange(-90, 91, 5))  # step 5 degrees
fine = scan(fine_g, fine_b)
for name, (M, g, b, e) in [('coarse 21 x 19', coarse),
                           ('fine   41 x 37', fine)]:
    print(f'{name}: best <H> = {e:6.2f} at gamma = {g:.4f},'
          f' beta = {b:.4f} ({np.degrees(b):.0f} deg)')
M = fine[0]
print(f'fine map: min {M.min():.1f}, max {M.max():.1f}')
np.savez('heatmap.npz', M=M, g=fine_g, b=fine_b)
