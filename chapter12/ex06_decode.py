"""Example 12.11 - decode the k = 2 histogram into job orders."""
from qiskit_aer import AerSimulator
from compact import shop_table
from grover import grover_circuit
from runner import run_counts, to_book
tab = shop_table()
c = run_counts([grover_circuit(['101'], 3, 2)],
               AerSimulator(), 1000, seed=12)[0]
print('Qiskit  book  order   cost  shots')
for q, n in sorted(c.items(), key=lambda t: -t[1]):
    b = to_book(q)                     # reverse: q0 to the left
    o, cost = tab.get(b, ('unused', '-'))
    print(f' {q}    {b}   {o:7s} {cost!s:>4}  {n}')
