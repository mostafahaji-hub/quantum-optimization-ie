"""Chapter 10 - small circuits used throughout the chapter."""
from qiskit import QuantumCircuit

def coin():
    """The quantum coin: one Hadamard gate, then measure."""
    qc = QuantumCircuit(1, 1)    # 1 qubit, 1 classical bit
    qc.h(0)                      # Hadamard on qubit 0
    qc.measure(0, 0)             # qubit 0 -> classical bit 0
    return qc

def double_coin():
    """Flip the quantum coin twice (H, H) without looking."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def biased_coin(theta):
    """RY(theta) on |0>: P(1) = sin^2(theta/2)."""
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)
    return qc

def two_coins():
    """Two independent quantum coins."""
    qc = QuantumCircuit(2, 2)
    qc.h([0, 1])
    qc.measure([0, 1], [0, 1])
    return qc

def bell():
    """Two entangled coins: H on q0, then CNOT q0 -> q1."""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc

def ghz(n):
    """n entangled coins: all 0 or all 1."""
    qc = QuantumCircuit(n, n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n), range(n))
    return qc

def basis_state(bits):
    """Prepare a fixed bit string (book order: bits[0] is q0)."""
    n = len(bits)
    qc = QuantumCircuit(n, n)
    for i, b in enumerate(bits):
        if b == '1':
            qc.x(i)
    qc.measure(range(n), range(n))
    return qc

def die3():
    """Three quantum coins = an 8-sided die."""
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
