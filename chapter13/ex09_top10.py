"""Example 13.17 - 1000 shots: the 10 most frequent strings."""
from qiskit_aer import AerSimulator
from shop9 import setup, describe, FEASIBLE, OPT
from qaoa import qaoa_circuit
from fastsim import qaoa_probs
from runner import run_counts, to_book
Q, c, H, E = setup(lam=20)
g, b = [0.0160], [-0.4123]                 # from Example 13.16
pr = qaoa_probs(E, g, b)
print(f'exact: P(optimum) = {pr[OPT]:.4f}, '
      f'P(feasible) = {pr[FEASIBLE].sum():.4f}')
qc = qaoa_circuit(H, g, b, measure=True)
counts = run_counts([qc], AerSimulator(), 1000, seed=7)[0]
top = sorted(counts.items(), key=lambda kv: -kv[1])[:10]
print('rank  Qiskit     book       QUBO  shots  meaning')
for r, (s, n) in enumerate(top, 1):
    book = to_book(s)
    print(f'{r:4d}  {s}  {book}  {E[int(book, 2)]:5.0f}  {n:5d}'
          f'  {describe(book)}')
feas = sum(n for s, n in counts.items() if describe(to_book(s))
           != 'infeasible')
print(f'feasible shots: {feas} of 1000; infeasible: {1000 - feas}')
print(f'different strings seen: {len(counts)}')
