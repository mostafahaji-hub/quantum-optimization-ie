# Chapter 5, code listing 11 (in order of appearance)
import numpy as np
for N in [100, 10**4, 10**6, 10**8]:
    theta = np.arcsin(1 / np.sqrt(N))
    k = int(np.floor(np.pi / (4 * theta)))
    print(f'N = {N:>11,}  best k = {k:>6,}  P(success) = {np.sin((2*k+1)*theta)**2:.4f}  classical avg = {N//2:,}')