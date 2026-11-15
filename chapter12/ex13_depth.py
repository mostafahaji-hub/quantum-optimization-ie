"""Example 12.21 - two-qubit gates of ONE Grover round on FakeFez
(one marked string), and of the full search with best k."""
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from grover import grover_circuit, best_k
pm = generate_preset_pass_manager(
    optimization_level=1, backend=FakeFez(), seed_transpiler=0)
print('qubits  2q-gates per round  best k  2q-gates in total')
for n in range(3, 9):
    qc = grover_circuit(['1' * n], n, 1)
    per = pm.run(qc).count_ops().get('cz', 0)
    k = best_k(1, 2 ** n)
    print(f'{n:6d}  {per:18d}  {k:6d}  {per * k:17,d}')
