"""Chapter 14 - two simple error-mitigation tools.
1) post-selection: keep only the feasible shots;
2) readout correction: undo measurement bit flips, qubit by
   qubit, with a 2x2 'confusion' matrix for every qubit."""
import numpy as np
from qiskit import QuantumCircuit, transpile
from runner import to_book

def counts_to_probs(counts, n):
    """Qiskit counts -> vector of 2^n frequencies (book index)."""
    P = np.zeros(2 ** n)
    total = sum(counts.values())
    for s, k in counts.items():
        P[int(to_book(s), 2)] += k / total
    return P

def calibration_circuits(n):
    """Two circuits: all qubits |0>, and all qubits |1>."""
    zero = QuantumCircuit(n)
    one = QuantumCircuit(n)
    one.x(range(n))
    zero.measure_all()
    one.measure_all()
    return [zero, one]

def calibration_for(isa, backend):
    """The two calibration circuits, measured on exactly the
    physical qubits where `isa` measures its qubits."""
    n = isa.layout._input_qubit_count
    lay = isa.layout.final_index_layout()
    return transpile(calibration_circuits(n), backend=backend,
                     initial_layout=lay, optimization_level=0)

def flip_rates(cal_counts, n):
    """From the two calibration runs, for every qubit q:
    e01[q] = P(read 1 | prepared 0), e10[q] = P(read 0 | 1)."""
    p0 = counts_to_probs(cal_counts[0], n)
    p1 = counts_to_probs(cal_counts[1], n)
    bits = (np.arange(2 ** n)[:, None] >> np.arange(n)[::-1]) & 1
    e01 = p0 @ bits             # how often bit q came out 1
    e10 = p1 @ (1 - bits)       # how often bit q came out 0
    return e01, e10

def readout_correct(P, e01, e10):
    """Apply the inverse confusion matrix of every qubit,
    then clip negative values and rescale to a sum of 1."""
    n = len(e01)
    t = P.reshape([2] * n)             # axis q = qubit q
    for q in range(n):
        A = np.array([[1 - e01[q], e10[q]],
                      [e01[q], 1 - e10[q]]])
        t = np.moveaxis(np.tensordot(np.linalg.inv(A), t,
                                     axes=([1], [q])), 0, q)
    P = np.clip(t.reshape(-1), 0, None)
    return P / P.sum()
