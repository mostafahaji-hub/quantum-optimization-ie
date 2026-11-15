import numpy as np
from qiskit.quantum_info import Statevector
from ham import qubo_to_pauli
from circuits import basis_state
Q = np.array([[3.0, -4.0], [0.0, 2.0]])   # f = 3x1 + 2x2 - 4x1x2
H = qubo_to_pauli(Q)
print(H)
for book in ['00', '10', '01', '11']:
    qc = basis_state(book).remove_final_measurements(inplace=False)
    e = Statevector(qc).expectation_value(H).real
    x1, x2 = int(book[0]), int(book[1])
    f = 3 * x1 + 2 * x2 - 4 * x1 * x2
    print(f'book {book}: <H> = {e:4.1f}   QUBO f = {f}')
