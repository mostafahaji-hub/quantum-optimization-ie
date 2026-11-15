"""Example 14.9 - 1000 shots: the 10 most frequent strings."""
from qiskit_aer import AerSimulator
from tsp4 import setup, describe, FEASIBLE, OPT
from qaoa import qaoa_circuit
from runner import run_counts, to_book
Q, c, H, E = setup(lam=20)
g, b = [0.0144], [-0.4264]                 # from Example 14.8
qc = qaoa_circuit(H, g, b, measure=True)
counts = run_counts([qc], AerSimulator(), 1000, seed=7)[0]
top = sorted(counts.items(), key=lambda kv: -kv[1])[:10]
print('rank  Qiskit     book       QUBO  shots  meaning')
for r, (s, n) in enumerate(top, 1):
    book = to_book(s)
    print(f'{r:4d}  {s}  {book}  {E[int(book, 2)]:5.0f}  {n:5d}'
          f'  {describe(book)}')
feas = sum(n for s, n in counts.items()
           if FEASIBLE[int(to_book(s), 2)])
best = sum(counts.get(format(k, '09b')[::-1], 0) for k in OPT)
print(f'feasible shots: {feas} of 1000; optimal tour: {best}')
print(f'different strings seen: {len(counts)}')
