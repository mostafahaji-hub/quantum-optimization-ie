"""Example 12.2 - amplitudes after H, oracle and diffuser."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from grover import oracle, diffuser

def book_amps(qc):
    """Real amplitudes listed in book order (q0 leftmost)."""
    sv = Statevector(qc).data
    return {format(k, '03b')[::-1]: round(sv[k].real, 4)
            for k in range(8)}

qc = QuantumCircuit(3)
qc.h(range(3))
print('after H       :', book_amps(qc)['101'], book_amps(qc)['000'])
qc.compose(oracle(['101'], 3), inplace=True)
print('after oracle  :', book_amps(qc)['101'], book_amps(qc)['000'])
qc.compose(diffuser(3), inplace=True)
a = book_amps(qc)
print('after diffuser:', a['101'], a['000'])
print('P(101) =', round(a['101'] ** 2, 3))
