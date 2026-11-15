"""Example 13.3 - QAOA with one qubit: f(x) = 3x."""
import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qaoa import qaoa_circuit, book_probs, expected_cost
H = SparsePauliOp(['I', 'Z'], [1.5, -1.5])    # f = 1.5 - 1.5 z
print(qaoa_circuit(H, [0.5], [0.3]))
print(' gamma   beta   P(1) circuit  P(1) formula   <f>')
pts = [(0, 0.3), (0.5, 0), (0.5, 0.3), (np.pi / 2, np.pi / 4)]
for g, b in pts:
    p1 = book_probs(H, [g], [b]).get('1', 0.0)
    formula = 0.5 * (1 + np.sin(2 * b) * np.sin(3 * g))
    print(f'{g:6.3f} {b:6.3f}   {p1:10.4f}   {formula:10.4f}'
          f'   {expected_cost(H, [g], [b]):6.3f}')
