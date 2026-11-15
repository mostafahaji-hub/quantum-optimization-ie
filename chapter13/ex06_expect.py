"""Example 13.13 - expected cost: exact and from 1000 shots."""
import numpy as np
from qiskit_aer import AerSimulator
from shop9 import setup
from qaoa import qaoa_circuit, expected_cost
from fastsim import qaoa_probs
from runner import run_counts, to_book
Q, c, H, E = setup(lam=20)
print(f'gamma = beta = 0 : <H> = {expected_cost(H, [0], [0]):.2f}')
g, b = [0.02], [-0.4]
print(f'exact (Statevector): {expected_cost(H, g, b):.2f}')
print(f'exact (fastsim)    : {qaoa_probs(E, g, b) @ E:.2f}')
qc = qaoa_circuit(H, g, b, measure=True)
counts = run_counts([qc], AerSimulator(), 1000, seed=7)[0]
vals = []                                   # one value per shot
for s, n in counts.items():
    vals += [E[int(to_book(s), 2)]] * n
vals = np.array(vals)
se = vals.std(ddof=1) / np.sqrt(len(vals))  # standard error
print(f'1000 shots: mean = {vals.mean():.2f}, '
      f'standard error = {se:.2f}')
