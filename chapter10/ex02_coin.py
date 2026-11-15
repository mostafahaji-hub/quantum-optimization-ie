from qiskit.quantum_info import Statevector
from circuits import coin
qc = coin()
print(qc.draw())                       # text drawing
qc0 = qc.remove_final_measurements(inplace=False)
sv = Statevector(qc0)
print('amplitudes   :', sv.data.round(4))
prob = {str(k): round(float(v), 4)
        for k, v in sv.probabilities_dict().items()}
print('probabilities:', prob)
