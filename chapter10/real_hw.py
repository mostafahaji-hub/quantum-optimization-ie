"""Chapter 10 - four test circuits on a real IBM QPU, one job."""
import json, datetime
from qiskit_ibm_runtime import QiskitRuntimeService
from circuits import basis_state, coin, bell
from runner import run_counts

service = QiskitRuntimeService()     # saved credentials
backend = service.least_busy(operational=True, simulator=False)
print('QPU:', backend.name, '| qubits:', backend.num_qubits)

names = ['prepare 0', 'prepare 1', 'coin', 'bell']
qcs = [basis_state('0'), basis_state('1'), coin(), bell()]
res = run_counts(qcs, backend, shots=1000)  # no seed on QPU
for n, c in zip(names, res):
    print(f'{n:10s}: {dict(sorted(c.items()))}')

data = {'backend': backend.name,
        'date': str(datetime.date.today()),
        'counts': dict(zip(names, res))}
with open('real_counts.json', 'w') as f:
    json.dump(data, f, indent=1)
print('saved to real_counts.json')
