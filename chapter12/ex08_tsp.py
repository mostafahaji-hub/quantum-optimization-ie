"""Example 12.15 - Grover for the small TSP (6 directed tours)."""
from qiskit_aer import AerSimulator
from compact import tsp_table, marked_by_threshold
from grover import grover_circuit, best_k, p_success
from runner import run_counts, to_book
tab = tsp_table()
good = marked_by_threshold(tab, 26)        # the two optimal codes
k = best_k(len(good), 8)
print('marked:', [(s, tab[s][0]) for s in good], ' k =', k,
      ' theory =', round(p_success(len(good), 8, k), 3))
c = run_counts([grover_circuit(good, 3, k)],
               AerSimulator(), 1000, seed=26)[0]
for q, n in sorted(c.items()):
    b = to_book(q)
    print(f'Qiskit {q} -> book {b} -> {tab[b][0]}'
          f' length {tab[b][1]} : {n}')
