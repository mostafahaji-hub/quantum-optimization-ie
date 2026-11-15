# Chapter 6, code listing 7 (in order of appearance)
import numpy as np
from qea import observe, rotate
from repair import repair
from truck import value, weight
rng = np.random.default_rng(1)
n, pop, gens, dtheta = 8, 10, 40, np.radians(4)
Q = [np.full(n, np.pi/4) for _ in range(pop)]      # 10 Q-bit chromosomes
best, best_val = None, -1
for g in range(1, gens + 1):
    for k in range(pop):
        x = repair(observe(Q[k], rng), add=False)   # observe + repair
        if value(x) > best_val:
            best, best_val = x, value(x)
        Q[k] = rotate(Q[k], x, best, dtheta)           # turn toward the best
    if g in (1, 2, 5, 10, 20, 40):
        p1 = np.mean([np.sin(q)**2 for q in Q], axis=0)
        print(f'gen {g:2d}  best profit {best_val}  P(1) per item {np.round(p1, 2)}')
print('best load:', best, ' weight', weight(best), ' profit', best_val)