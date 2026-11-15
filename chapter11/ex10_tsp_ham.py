import numpy as np
from tsp_qubo import tsp_qubo
from ham import qubo_to_pauli, check_hamiltonian
from encode import bits_to_tour
D = [[0, 5, 12, 4], [5, 0, 7, 4], [12, 7, 0, 10], [4, 4, 10, 0]]
Q, c = tsp_qubo(D, lam=20)
H = qubo_to_pauli(Q, c)
print('Pauli terms:', len(H), '  offset:', H.coeffs[0].real)
print('max error over 512 strings:', check_hamiltonian(Q, c, H))
d = H.to_matrix(sparse=True).diagonal().real
for k in np.argsort(d, kind='stable')[:7]:
    q = format(int(k), '09b')             # Qiskit's string
    t = bits_to_tour(q[::-1])
    print(f'Qiskit {q} -> book {q[::-1]} -> {t or "infeasible"}'
          f'  energy {d[k]:.0f}')
