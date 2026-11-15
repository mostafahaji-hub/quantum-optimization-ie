"""Chapter 14 - the small TSP as a 9-qubit problem (Ch. 8, 11).
Variables B1 B2 B3 C1 C2 C3 D1 D2 D3 = qubits q0 ... q8."""
import numpy as np
from tsp_qubo import tsp_qubo
from qubo import brute_force
from ham import qubo_to_pauli
from encode import bits_to_tour

D = [[0, 5, 12, 4],          # A
     [5, 0, 7, 4],           # B
     [12, 7, 0, 10],         # C
     [4, 4, 10, 0]]          # D

def setup(lam=20):
    """QUBO, Hamiltonian and the QUBO value of all 512 strings.
    E[k] belongs to the book string format(k, '09b')."""
    Q, c = tsp_qubo(D, lam)
    X, E = brute_force(Q, c)
    return Q, c, qubo_to_pauli(Q, c), E

def length(tour):
    """Length of a closed tour such as 'ABCDA'."""
    idx = ['ABCD'.index(ch) for ch in tour]
    return sum(D[a][b] for a, b in zip(idx, idx[1:]))

def describe(book):
    """'ABCDA (26)' for a feasible string, else 'infeasible'."""
    t = bits_to_tour(book)
    return 'infeasible' if t is None else f'{t} ({length(t)})'

BOOK = [format(k, '09b') for k in range(512)]
FEASIBLE = np.array([bits_to_tour(s) is not None for s in BOOK])
OPT = [BOOK.index('100010001'), BOOK.index('001010100')]
