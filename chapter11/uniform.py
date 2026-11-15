"""Chapter 11 - uniform superposition: H on every qubit."""
from qiskit import QuantumCircuit

def uniform(n, measure=True):
    qc = QuantumCircuit(n, n if measure else 0)
    qc.h(range(n))
    if measure:
        qc.measure(range(n), range(n))
    return qc
