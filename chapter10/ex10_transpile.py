from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from circuits import coin, bell
backend = FakeFez()          # snapshot of a 156-qubit Heron QPU
native = {'cz', 'rz', 'sx', 'x', 'id', 'measure'}
print('native:', sorted(set(backend.operation_names) & native))
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=0)
for name, qc in [('coin', coin()), ('bell', bell())]:
    isa = pm.run(qc)
    print(f'{name} before: {dict(qc.count_ops())}')
    print(f'{name} after : {dict(isa.count_ops())}'
          f'  depth {isa.depth()}')
    print('   physical qubits:', isa.layout.final_index_layout())
print(pm.run(coin()).draw(idle_wires=False))
