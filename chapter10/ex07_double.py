from qiskit_aer import AerSimulator
from qiskit.quantum_info import Operator
from circuits import double_coin
from runner import run_counts
qc = double_coin()
print(qc.draw())
U = Operator(qc.remove_final_measurements(inplace=False))
print('matrix of H*H:\n', U.data.real.round(4))
print(run_counts([qc], AerSimulator(), 1000, seed=7)[0])
