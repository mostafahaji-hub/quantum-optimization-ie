"""Example 12.4 - compact codes, book order and Qiskit order."""
from compact import shop_table, tsp_table
shop, tsp = shop_table(), tsp_table()
print('book  Qiskit  order   cost | tour   length')
for k in range(8):
    b = format(k, '03b')              # book code (q0 leftmost)
    q = b[::-1]                       # what Qiskit prints
    if b in shop:
        (o, c), (t, L) = shop[b], tsp[b]
        print(f' {b}   {q}   {o}  {c:3d}  | {t}  {L:3d}')
    else:
        print(f' {b}   {q}   unused       |')
