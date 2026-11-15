"""Example 13.11 - the 9-qubit QAOA circuit of the workshop."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import Statevector
from shop9 import setup, BOOK
from qaoa import qaoa_circuit, book_probs
from fastsim import qaoa_probs
Q, c, H, E = setup(lam=20)
g, b = [0.02], [-0.4]
qc = qaoa_circuit(H, g, b)
print('gates:', dict(qc.count_ops()), '  depth:', qc.depth())
# check 1: Qiskit's own QAOA circuit (parameters: beta, gamma)
ref = QAOAAnsatz(H, reps=1)
ref = ref.assign_parameters(dict(zip(ref.parameters, b + g)))
same = Statevector(ref).equiv(Statevector(qc))
print('same state as QAOAAnsatz (up to global phase):', same)
# check 2: our NumPy simulator of fastsim.py
pq = book_probs(H, g, b)
pn = qaoa_probs(E, g, b)
diff = max(abs(pq.get(s, 0) - pn[k]) for k, s in enumerate(BOOK))
print(f'largest probability difference vs fastsim: {diff:.1e}')
