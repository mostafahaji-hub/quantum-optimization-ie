"""Example 12.18 - Grover on the noisy fake Heron (FakeFez)."""
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from grover import grover_circuit, p_success
from runner import run_counts, to_book
fez = FakeFez()
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)
cases = [('shop k=1', ['101'], 1), ('shop k=2', ['101'], 2),
         ('TSP  k=1', ['000', '101'], 1)]
print('case      depth  2q-gates  ideal  noisy (1000 shots)')
for name, good, k in cases:
    qc = grover_circuit(good, 3, k)
    isa = pm.run(qc)
    two_q = isa.count_ops().get('cz', 0)
    c = run_counts([qc], fez, 1000, seed=7)[0]
    hit = sum(n for s, n in c.items() if to_book(s) in good)
    ideal = p_success(len(good), 8, k)
    print(f'{name}  {isa.depth():5d}  {two_q:8d}  {ideal:.3f}'
          f'  {hit / 1000:.3f}')
