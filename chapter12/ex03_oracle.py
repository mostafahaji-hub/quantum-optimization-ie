"""Example 12.6 - the oracle that marks 101 is a sign table."""
import numpy as np
from qiskit.quantum_info import Operator
from grover import oracle
qc = oracle(['101'], 3)
print(qc.draw(output='text'))
U = Operator(qc).data
print('diagonal only:', np.allclose(U, np.diag(np.diag(U))))
for i in range(8):
    book = format(i, '03b')            # book string (q0 left)
    k = int(book[::-1], 2)             # Qiskit index (q0 = LSB)
    print(book, int(round(U[k, k].real)))
