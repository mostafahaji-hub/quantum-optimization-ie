# Chapter 7, code listing 12 (in order of appearance)
import numpy as np
from emer import REL, N, names
for tau in (0.0, 0.70, 0.80, 0.84):
    usable = sum(1 for i in range(N) for j in range(i + 1, N) if REL[i, j] >= tau)
    print(f'threshold {tau:.2f}: usable arcs {usable} of {N*(N-1)//2}')
print('reliability of arcs from H:', {names[j]: float(REL[0, j]) for j in range(1, N)})