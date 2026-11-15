from math import factorial
from encode import bits_to_order
n = 9
ok = [format(k, '09b') for k in range(2 ** n)
      if bits_to_order(format(k, '09b')) is not None]
print(f'feasible strings: {len(ok)} of {2**n}'
      f' = {100*len(ok)/2**n:.2f}%')
for m in [3, 4, 5, 6, 8]:
    frac = factorial(m) / 2 ** (m * m)
    print(f'{m} jobs: {m*m:2d} qubits, {factorial(m):6d} feasible'
          f' of 2^{m*m}, fraction {frac:.1e}')
