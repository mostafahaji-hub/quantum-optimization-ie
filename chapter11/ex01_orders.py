from itertools import permutations
from encode import order_to_bits, bits_to_order
cost = {(1, 2, 3): 12, (1, 3, 2): 9, (2, 1, 3): 13,
        (2, 3, 1): 11, (3, 1, 2): 8, (3, 2, 1): 5}
for order in permutations([1, 2, 3]):
    b = order_to_bits(order)
    back = bits_to_order(b)
    name = ''.join(f'J{j}' for j in order)
    print(f'{name}  {b[:3]} {b[3:6]} {b[6:]}  back {back}'
          f'  cost {cost[order]}')
