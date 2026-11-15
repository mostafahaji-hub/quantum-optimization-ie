"""Example 14.19 - how often does each qubit read wrong?"""
import json
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from tsp4 import setup
from qaoa import qaoa_circuit
from mitigate import flip_rates
Q, c, H, E = setup(lam=20)
data = json.load(open('fez_counts.json'))    # from Example 14.13
d = data['1']
print('cal0, 3 most frequent:', sorted(d['cal0'].items(),
      key=lambda kv: -kv[1])[:3])
e01, e10 = flip_rates([d['cal0'], d['cal1']], 9)
fez = FakeFez()                              # same layout as 14.13
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)
angles = json.load(open('angles.json'))
isa = pm.run(qaoa_circuit(H, *angles['1'], measure=True))
lay = isa.layout.final_index_layout()
print('qubit  physical  P(1|0)  P(0|1)  FakeFez table')
for q in range(9):
    tab = fez.target['measure'][(lay[q],)].error
    print(f'q{q}     {lay[q]:8d}  {e01[q]:.4f}  {e10[q]:.4f}'
          f'  {tab:.4f}')
ok = (1 - e01).prod()
print(f'chance that all 9 qubits read right (all |0>): {ok:.3f}')
