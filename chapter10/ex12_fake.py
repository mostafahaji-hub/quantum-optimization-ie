from qiskit_ibm_runtime.fake_provider import FakeFez
from circuits import basis_state, coin, bell
from runner import run_counts
backend = FakeFez()          # real calibration data, on a laptop
names = ['prepare 0', 'prepare 1', 'coin', 'bell']
qcs = [basis_state('0'), basis_state('1'), coin(), bell()]
res = run_counts(qcs, backend, shots=1000, seed=2026)
for n, c in zip(names, res):
    print(f'{n:10s}: {dict(sorted(c.items()))}')
