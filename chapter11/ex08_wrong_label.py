import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qubo import to_ising
from shop_pos_qubo import shop_pos_qubo
from ham import qubo_to_pauli, check_hamiltonian
Q, c = shop_pos_qubo(lam=20)
h, J, off = to_ising(Q, c)
n = 9
def label(*idx):        # WRONG: variable i = i-th label char
    return ''.join('Z' if i in idx else 'I' for i in range(n))
terms = [('I' * n, off)] + [(label(i), h[i]) for i in range(n)]
terms += [(label(i, j), J[i, j]) for i in range(n)
          for j in range(i + 1, n) if J[i, j] != 0]
H_bad = SparsePauliOp.from_list(terms)
H_ok = qubo_to_pauli(Q, c)
d_bad = H_bad.to_matrix(sparse=True).diagonal().real
d_ok = H_ok.to_matrix(sparse=True).diagonal().real
print('max error, correct H:', check_hamiltonian(Q, c, H_ok))
print('max error, wrong H  :', check_hamiltonian(Q, c, H_bad))
bad = int((abs(d_bad - d_ok) > 1e-9).sum())
print('strings with a wrong energy:', bad, 'of 512')
print('ground energy, correct vs wrong:', d_ok.min(), d_bad.min())
