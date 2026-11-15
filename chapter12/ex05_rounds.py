"""Example 12.10 - Grover for the optimal order, k = 0..4."""
from qiskit_aer import AerSimulator
from grover import grover_circuit, p_success
from runner import run_counts, to_book
circs = [grover_circuit(['101'], 3, k) for k in range(5)]
counts = run_counts(circs, AerSimulator(), 1000, seed=12)
print('k  theory  measured (1000 shots)')
for k, c in enumerate(counts):
    book = {to_book(s): n for s, n in c.items()}
    print(f'{k}  {p_success(1, 8, k):.3f}   {book.get("101", 0)}')
