"""Example 12.13 - threshold oracles 'cost <= T' for the shop."""
from qiskit_aer import AerSimulator
from compact import shop_table, marked_by_threshold
from grover import grover_circuit, best_k, p_success
from runner import run_counts, to_book
tab = shop_table()
print(' T  M  k  theory  measured  marked orders')
for T in [13, 11, 9, 8, 5, 4]:
    good = marked_by_threshold(tab, T)
    M = len(good)
    k = best_k(M, 8) if M > 0 else 1
    c = run_counts([grover_circuit(good, 3, k)],
                   AerSimulator(), 1000, seed=T)[0]
    hit = sum(n for s, n in c.items() if to_book(s) in good)
    names = ' '.join(tab[s][0] for s in good) or '(none)'
    if M == 6:
        names = '(all six orders)'
    th = p_success(M, 8, k) if M > 0 else 0.0
    print(f'{T:2d}  {M}  {k}  {th:.3f}   {hit:4d}     {names}')
