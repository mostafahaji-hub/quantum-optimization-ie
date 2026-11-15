"""Chapter 13 - the small workshop as a 9-qubit problem (Ch. 11)."""
import numpy as np
from shop_pos_qubo import shop_pos_qubo, p, d, wt
from qubo import brute_force
from ham import qubo_to_pauli
from encode import bits_to_order

def setup(lam=20):
    """QUBO, Hamiltonian and the QUBO value of all 512 strings.
    E[k] belongs to the book string format(k, '09b')."""
    Q, c = shop_pos_qubo(lam)
    X, E = brute_force(Q, c)
    return Q, c, qubo_to_pauli(Q, c), E

def tardiness(order):
    """Total weighted tardiness of an order such as [3, 2, 1]."""
    t, total = 0, 0
    for j in order:
        t += p[j - 1]
        total += wt[j - 1] * max(0, t - d[j - 1])
    return total

def describe(book):
    """'J3J2J1 (5)' for a feasible string, else 'infeasible'."""
    order = bits_to_order(book)
    if order is None:
        return 'infeasible'
    name = ''.join(f'J{j}' for j in order)
    return f'{name} ({tardiness(order)})'

BOOK = [format(k, '09b') for k in range(512)]
FEASIBLE = np.array([bits_to_order(s) is not None for s in BOOK])
OPT = BOOK.index('001010100')
