"""Example 12.8 - the diffuser circuit equals 2|s><s| - I."""
import numpy as np
from qiskit.quantum_info import Operator
from grover import diffuser
for n in [1, 2, 3]:
    N = 2 ** n
    s = np.ones(N) / np.sqrt(N)        # uniform superposition
    R = 2 * np.outer(s, s) - np.eye(N)
    U = Operator(diffuser(n)).data
    print(f'n = {n}: max |U - (2ss - I)| =',
          f'{np.abs(U - R).max():.1e}')
print(np.round(Operator(diffuser(1)).data.real, 3))
