import numpy as np
from qubo import energy
from shop_pos_qubo import shop_pos_qubo
from encode import bits_to_order
lam = 20
Q, c = shop_pos_qubo(lam)
Q0, c0 = shop_pos_qubo(0)                # cost part only
for b in ['001010100', '000010100', '011010100', '000000000']:
    x = [int(ch) for ch in b]
    total, cost = energy(Q, x, c), energy(Q0, x, c0)
    print(f'{b}: QUBO {total:5.0f} = cost {cost:3.0f}'
          f' + penalty {total - cost:4.0f}'
          f'  order {bits_to_order(b)}')
