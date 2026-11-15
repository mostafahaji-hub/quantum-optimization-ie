"""Example 13.23 - how many shots to see the optimum?"""
import numpy as np

def shots99(P):
    """Shots so that the optimum appears at least once w.p. 0.99."""
    return int(np.ceil(np.log(0.01) / np.log(1 - P)))

methods = [('random 9-bit string (= QAOA with gamma = 0)', 1 / 512),
           ('QAOA p = 1 (Ex. 13.17)', 0.0216),
           ('QAOA p = 4 (Ex. 13.19)', 0.1213),
           ('random order of the 3 jobs (classical)', 1 / 6),
           ('Grover, compact code, k = 2 (Ch. 12)', 0.945)]
print(f'{"method":45s}  P(opt)  shots99')
for name, P in methods:
    print(f'{name:45s}  {P:.4f}  {shots99(P):7d}')
grid, cobyla, shots = 41 * 37, 35, 1000  # Ex. 13.14, 13.16
print(f'tuning p = 1 on hardware: ({grid} + {cobyla}) evaluations'
      f' x {shots} shots = {(grid + cobyla) * shots:,} shots')
