"""Chapter 10 - same four circuits on two snapshots, but let the transpiler
choose the qubits from the calibration data (optimization_level=3)."""
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.executor_sampler import Sampler
from qiskit_ibm_runtime.fake_provider import FakeKingston, FakeTorino
from circuits import basis_state, coin, bell
from metrics import probs, tvd
ideal = [{'0': 1.0}, {'1': 1.0}, {'0': 0.5, '1': 0.5}, {'00': 0.5, '11': 0.5}]
qcs = [basis_state('0'), basis_state('1'), coin(), bell()]
for B in [FakeKingston, FakeTorino]:
    b = B()
    pm = generate_preset_pass_manager(optimization_level=3, backend=b, seed_transpiler=0)
    isa = pm.run(qcs)
    sampler = Sampler(mode=b); sampler.options.simulator.seed_simulator = 2026
    res = [p.join_data().get_counts() for p in sampler.run(isa, shots=1000).result()]
    d = [round(tvd(i, probs(c)), 3) for i, c in zip(ideal, res)]
    print(f'{b.name:14s} qubits {isa[3].layout.final_index_layout()}  TVD {d}')
