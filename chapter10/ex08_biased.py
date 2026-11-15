import numpy as np
from qiskit_aer import AerSimulator
from circuits import biased_coin
from runner import run_counts
for p1 in [0.10, 0.25, 0.50]:
    theta = 2 * np.arcsin(np.sqrt(p1))   # P(1)=sin^2(theta/2)
    qc = biased_coin(theta)
    c = run_counts([qc], AerSimulator(), 1000, seed=3)[0]
    print(f'P(1)={p1:.2f} theta={theta:.4f}'
          f' counts={dict(sorted(c.items()))}')
