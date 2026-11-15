"""Chapter 12 - Grover search built from Qiskit gates.
Marked strings are written in BOOK order (q0 = leftmost)."""
import numpy as np
from qiskit import QuantumCircuit

def mcz(qc, qubits):
    """Z on the last qubit, controlled by all the others:
    flips the sign of |11...1> only."""
    *controls, target = qubits
    qc.h(target)
    qc.mcx(controls, target)
    qc.h(target)

def oracle(marked, n):
    """Phase oracle: multiply every marked string by -1."""
    qc = QuantumCircuit(n, name='Oracle')
    for s in marked:
        zeros = [i for i, b in enumerate(s) if b == '0']
        if zeros:
            qc.x(zeros)        # turn the marked string into 11...1
        mcz(qc, list(range(n)))
        if zeros:
            qc.x(zeros)        # undo
    return qc

def diffuser(n):
    """Reflection about the uniform superposition 2|s><s| - I."""
    qc = QuantumCircuit(n, name='Diffuser')
    qc.h(range(n))
    qc.x(range(n))
    mcz(qc, list(range(n)))    # -1 on |00...0> after the X gates
    qc.x(range(n))
    qc.h(range(n))
    qc.global_phase = np.pi    # exact sign (invisible in counts)
    return qc

def grover_circuit(marked, n, k, measure=True):
    """H on all qubits, then k rounds of (oracle, diffuser)."""
    qc = QuantumCircuit(n, n) if measure else QuantumCircuit(n)
    qc.h(range(n))
    O, D = oracle(marked, n), diffuser(n)
    for _ in range(k):
        qc.compose(O, inplace=True)
        qc.compose(D, inplace=True)
    if measure:
        qc.measure(range(n), range(n))
    return qc

def best_k(M, N):
    """Number of rounds that brings the state closest to |good>."""
    theta = np.arcsin(np.sqrt(M / N))
    x = np.pi / (4 * theta)
    return int(np.floor(x + 1e-9))   # 1e-9: guard against rounding

def p_success(M, N, k):
    """Probability of measuring a marked string after k rounds."""
    theta = np.arcsin(np.sqrt(M / N))
    return float(np.sin((2 * k + 1) * theta) ** 2)
