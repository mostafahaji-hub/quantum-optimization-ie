"""Chapter 11 - QUBO -> Ising -> Qiskit Hamiltonian."""
import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qubo import to_ising, energy

def qubo_to_pauli(Q, const=0.0):
    """Variable i acts on qubit i (by index, never by label)."""
    h, J, offset = to_ising(Q, const)
    n = len(Q)
    terms = [('', [], offset)]
    terms += [('Z', [i], h[i]) for i in range(n) if h[i] != 0]
    terms += [('ZZ', [i, j], J[i, j]) for i in range(n)
              for j in range(i + 1, n) if J[i, j] != 0]
    return SparsePauliOp.from_sparse_list(terms, num_qubits=n)

def diag_energy(H, book_bits):
    """<x|H|x> for a book-order string: Qiskit index = reversed."""
    k = int(book_bits[::-1], 2)      # q0 = least significant
    return H.to_matrix(sparse=True)[k, k].real

def check_hamiltonian(Q, const, H):
    """Compare H with the QUBO on all 2^n strings (max error)."""
    n = len(Q)
    d = H.to_matrix(sparse=True).diagonal().real
    worst = 0.0
    for k in range(2 ** n):
        book = format(k, f'0{n}b')[::-1]   # index -> book string
        x = [int(c) for c in book]
        worst = max(worst, abs(d[k] - energy(Q, x, const)))
    return worst
