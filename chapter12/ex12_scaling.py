"""Example 12.20 - how Grover scales on the compact encoding
(one marked order); the classical baseline checks all n! orders."""
import numpy as np
from math import factorial, ceil, log2
from grover import best_k, p_success
print(' n        n!  qubits         N   rounds  P(opt)  rounds/n!')
for n in range(3, 11):
    F = factorial(n)
    q = ceil(log2(F))                # compact: about log2(n!)
    N = 2 ** q
    k = best_k(1, N)
    print(f'{n:2d} {F:9,d}  {q:6d} {N:9,d}  {k:7,d}  '
          f'{p_success(1, N, k):.3f}   {k / F:.4f}')
