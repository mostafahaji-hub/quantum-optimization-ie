"""Example 14.23 - QAOA for the small TSP on a real IBM QPU.
One job: 4 QAOA circuits (p = 1..4) + 2 calibration circuits
for each. Run it ONCE with your own account (Chapter 10)."""
import json, datetime
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler
from tsp4 import setup
from qaoa import qaoa_circuit
from mitigate import calibration_for

SHOTS = 10000                        # same as Example 14.13
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))      # from Example 14.10
service = QiskitRuntimeService()     # saved credentials
backend = service.least_busy(operational=True, simulator=False)
print('QPU:', backend.name, '| qubits:', backend.num_qubits)
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=backend,
                                  seed_transpiler=0)
circuits = []
for p in ['1', '2', '3', '4']:
    isa = pm.run(qaoa_circuit(H, *angles[p], measure=True))
    print(f'p = {p}: depth {isa.depth()}, '
          f'CZ {isa.count_ops().get("cz", 0)}')
    circuits += [isa] + list(calibration_for(isa, backend))
job = Sampler(mode=backend).run(circuits, shots=SHOTS)
print('job id:', job.job_id(), '(see the Workloads page)')
counts = [r.join_data().get_counts() for r in job.result()]
saved = {'backend': backend.name,
         'date': str(datetime.date.today())}
for i, p in enumerate(['1', '2', '3', '4']):
    run, zero, one = counts[3 * i: 3 * i + 3]
    saved[p] = {'run': run, 'cal0': zero, 'cal1': one}
json.dump(saved, open('real_counts.json', 'w'))
print('saved to real_counts.json')
