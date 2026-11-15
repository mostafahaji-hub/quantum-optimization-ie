"""Example 13.9 - search a grid of angles for two machines."""
import numpy as np
from machine2 import machine_qubo
from ham import qubo_to_pauli
from qaoa import book_probs, expected_cost
H = qubo_to_pauli(*machine_qubo())
gammas = np.linspace(0, np.pi, 61)        # step pi/60
betas = np.linspace(0, np.pi / 2, 31)     # step pi/60
best = (np.inf, 0, 0)
for g in gammas:
    for b in betas:
        e = expected_cost(H, [g], [b])
        if e < best[0]:
            best = (e, g, b)
e, g, b = best
p = book_probs(H, [g], [b])
print(f'evaluations: {len(gammas) * len(betas)}')
print(f'best grid point: gamma = {g:.4f}, beta = {b:.4f}')
print(f'<f> = {e:.3f}   (uniform start: 10.000)')
print('probabilities:', {s: round(float(p.get(s, 0)), 3)
                         for s in ['00', '10', '01', '11']})
