"""Example 14.26 - how fast does the TSP circuit grow?
Cities: the first n points of the 8-city TSP of Chapter 8."""
import math
import numpy as np
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from tsp_qubo import tsp_qubo
from ham import qubo_to_pauli
from qaoa import qaoa_circuit
pts = [(6, 6), (0, 4), (8, 7), (6, 4),
       (7, 5), (9, 3), (8, 2), (4, 2)]
fez = FakeFez()
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)
print('cities qubits  ZZ terms  CZ (p=1)  depth  feasible share')
for n in range(4, 8):
    D = [[round(math.dist(a, b), 1) for b in pts[:n]]
         for a in pts[:n]]
    H = qubo_to_pauli(*tsp_qubo(D, lam=10))
    zz = sum(1 for lab, _, _ in H.to_sparse_list() if lab == 'ZZ')
    isa = pm.run(qaoa_circuit(H, [0.01], [-0.4], measure=True))
    m = n - 1
    share = math.factorial(m) / 2 ** (m * m)
    print(f'{n:6d} {m * m:6d}  {zz:8d}  {isa.count_ops()["cz"]:8d}'
          f'  {isa.depth():5d}  {share:.2e}')
