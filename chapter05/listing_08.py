# Chapter 5, code listing 8 (in order of appearance)
from alg import *
tours = {'00': 26, '01': 31, '10': 27}                # '11' is unused
marked = lambda s: s in tours and tours[s] <= 26
for k in range(3):
    print('iterations', k, probs(grover(marked, n=2, k=k)))