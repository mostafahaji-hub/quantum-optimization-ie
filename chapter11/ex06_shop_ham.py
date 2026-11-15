import numpy as np
from shop_pos_qubo import shop_pos_qubo
from ham import qubo_to_pauli, check_hamiltonian
from encode import bits_to_order
Q, c = shop_pos_qubo(lam=20)
H = qubo_to_pauli(Q, c)
print('qubits:', H.num_qubits, '  Pauli terms:', len(H))
for label, coef in list(zip(H.paulis.to_labels(), H.coeffs))[:4]:
    print(f'   {label}  {coef.real:7.2f}')
print('max |<x|H|x> - QUBO| over 512 strings:',
      check_hamiltonian(Q, c, H))
d = H.to_matrix(sparse=True).diagonal().real
k = int(np.argmin(d))
q_str = format(k, '09b')                  # what Qiskit would print
book = q_str[::-1]
print(f'ground state: Qiskit {q_str} -> book {book}'
      f' -> order {bits_to_order(book)}, energy {d[k]:.0f}')
