from qiskit_aer import AerSimulator
from circuits import coin
from runner import run_counts
sim = AerSimulator()                   # ideal, noise-free
for seed in range(1, 6):
    c = run_counts([coin()], sim, shots=1000, seed=seed)[0]
    print(f'seed {seed}: {dict(sorted(c.items()))}')
