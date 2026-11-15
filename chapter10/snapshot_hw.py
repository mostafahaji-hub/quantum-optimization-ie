"""Chapter 10 - the four test circuits of real_hw.py on calibration snapshots of
three more IBM Heron QPUs (Section 10.9). This is a stand-in for a live hardware
run: each result is a simulation with the device's recorded noise, not a run on
the device itself. real_hw.py remains the script for a live run."""
import json
from qiskit_ibm_runtime.fake_provider import FakeMarrakesh, FakeKingston, FakeTorino
from circuits import basis_state, coin, bell
from runner import run_counts

names = ['prepare 0', 'prepare 1', 'coin', 'bell']
qcs = [basis_state('0'), basis_state('1'), coin(), bell()]
data = {}
for Backend in [FakeMarrakesh, FakeKingston, FakeTorino]:
    b = Backend()
    date = b.properties().last_update_date.date().isoformat()
    res = run_counts(qcs, b, shots=1000, seed=2026)
    print(f'{b.name} ({b.num_qubits} qubits, calibration of {date})')
    for n, c in zip(names, res):
        print(f'   {n:10s}: {dict(sorted(c.items()))}')
    data[b.name] = {'date': date, 'counts': dict(zip(names, res))}
with open('snapshot_counts.json', 'w') as f:
    json.dump(data, f, indent=1)
print('saved to snapshot_counts.json')
