from qiskit_aer import AerSimulator
from circuits import two_coins, bell
from runner import run_counts
print(bell().draw())
c2, cb = run_counts([two_coins(), bell()], AerSimulator(),
                    shots=1000, seed=5)
print('independent:', dict(sorted(c2.items())))
print('entangled  :', dict(sorted(cb.items())))
