"""Example 14.2 - the 512 strings of the small TSP, cheapest first."""
import numpy as np
from tsp4 import setup, describe, BOOK, FEASIBLE
Q, c, H, E = setup(lam=20)
print('Pauli terms:', len(H), '  offset:', H.coeffs[0].real)
print('mean of all 512 QUBO values:', E.mean())
print('feasible strings:', FEASIBLE.sum(), ' of', len(E))
for k in np.argsort(E, kind='stable')[:8]:
    print(f'{BOOK[k]}  {E[k]:5.0f}  {describe(BOOK[k])}')
print('cheapest infeasible:', E[~FEASIBLE].min(),
      '  most expensive string:', E.max())
