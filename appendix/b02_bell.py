from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)            # Bell state
qc.measure_all()
sim = AerSimulator(seed_simulator=7)
counts = sim.run(qc, shots=1000).result().get_counts()
print(dict(sorted(counts.items())))
