from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError
from circuits import basis_state, coin
from runner import run_counts
e = 0.05                     # 5% chance to read the wrong bit
noise = NoiseModel()
noise.add_all_qubit_readout_error(
    ReadoutError([[1 - e, e], [e, 1 - e]]))
sim = AerSimulator(noise_model=noise)
names = ['prepare 0', 'prepare 1', 'coin']
qcs = [basis_state('0'), basis_state('1'), coin()]
for n, c in zip(names, run_counts(qcs, sim, 1000, seed=11)):
    print(f'{n:10s}: {dict(sorted(c.items()))}')
