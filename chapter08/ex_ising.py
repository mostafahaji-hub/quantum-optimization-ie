import numpy as np
from qubo import to_ising, brute_force
from supplier import supplier_qubo
Q, const = supplier_qubo(100)
h, J, offset = to_ising(Q, const)
print('h =', h, ' J12, J13, J23 =', J[0, 1], J[0, 2], J[1, 2], ' offset =', offset)
Z, I = np.diag([1, -1]), np.eye(2)
def on(M, k):                                     # gate M on qubit k of 3 (Kronecker products, Chapter 3)
    out = np.array([[1.0]])
    for q in range(3): out = np.kron(out, M if q == k else I)
    return out
H = offset * np.eye(8) + sum(h[i] * on(Z, i) for i in range(3))
H += sum(J[i, j] * on(Z, i) @ on(Z, j) for i in range(3) for j in range(i + 1, 3))
print('diagonal of H:', np.diag(H))
print('QUBO values  :', brute_force(Q, const)[1])
print('largest off-diagonal entry:', np.abs(H - np.diag(np.diag(H))).max())
