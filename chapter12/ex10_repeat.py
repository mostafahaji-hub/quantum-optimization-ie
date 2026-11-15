"""Example 12.17 - 1000 repetitions of the threshold search,
compared with random guessing that uses the same shots."""
import numpy as np
from functools import lru_cache
from qiskit.quantum_info import Statevector
from compact import shop_table, tsp_table
from grover import grover_circuit
from gas import minimum_search

@lru_cache(maxsize=None)
def probs(marked, k):
    """Ideal probabilities of the 8 book strings (no sampling)."""
    p = Statevector(grover_circuit(list(marked), 3, k, False))
    d = p.probabilities_dict()
    return [d.get(format(i, '03b')[::-1], 0.0) for i in range(8)]

rng = np.random.default_rng(2026)
def shoot(marked, k):
    i = rng.choice(8, p=probs(tuple(sorted(marked)), k))
    return format(i, '03b')

for name, tab in [('shop', shop_table()), ('TSP ', tsp_table())]:
    opt = min(c for _, c in tab.values())
    found = calls = shots = rand = 0
    for run in range(1000):
        b, T, c, s = minimum_search(tab, 3, shoot, rng)
        found += T == opt; calls += c; shots += s
        guess = rng.choice(8, size=s)    # same shots, no Grover
        rand += any(format(g, '03b') in tab and
                    tab[format(g, '03b')][1] == opt for g in guess)
    print(f'{name}: optimum found {found / 10:.1f}%,',
          f'random guessing {rand / 10:.1f}%')
    print(f'      mean oracle calls {calls / 1000:.2f},',
          f'mean shots {shots / 1000:.2f}')
