"""Example 12.16 - lower the threshold until nothing is better."""
import numpy as np
from qiskit_aer import AerSimulator
from compact import shop_table
from grover import grover_circuit
from gas import minimum_search
from runner import run_counts, to_book
tab, sim = shop_table(), AerSimulator()
seeds = iter(range(300, 400))          # a new seed for every shot

def shoot(marked, k):
    qc = grover_circuit(marked, 3, k)
    c = run_counts([qc], sim, shots=1, seed=next(seeds))[0]
    return to_book(next(iter(c)))

rng = np.random.default_rng(5)
best, T, calls, shots = minimum_search(tab, 3, shoot, rng,
                                       log=print)
print(f'result: {best} {tab[best][0]} cost {T}',
      f'| oracle calls {calls}, shots {shots}')
