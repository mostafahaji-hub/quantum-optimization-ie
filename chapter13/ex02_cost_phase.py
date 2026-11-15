"""Example 13.6 - the cost layer only adds a phase -gamma*f(x)."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from machine2 import machine_qubo
from qubo import energy
from ham import qubo_to_pauli
from qaoa import cost_layer
Q, c = machine_qubo()
H = qubo_to_pauli(Q, c)
print(H)
g = 0.1
qc = QuantumCircuit(2)
cost_layer(qc, H, g)
U = Operator(qc).data
print('book  f(x)  -g*(f-f00)  circuit phase (relative to 00)')
for book in ['00', '10', '01', '11']:
    k = int(book[::-1], 2)               # Qiskit index
    f = energy(Q, [int(b) for b in book], c)
    rel = np.angle(U[k, k] / U[0, 0])
    want = -g * (f - 10) + 0.0          # + 0.0 avoids '-0.00'
    print(f' {book}   {f:4.0f}   {want:8.2f}   {rel:8.2f}')
print('off-diagonal entries all zero:',
      np.allclose(U, np.diag(np.diag(U))))
