# Chapter 6, code listing 11 (in order of appearance)
import numpy as np
from qea import observe, rotate
from keys import decode_keys
from shop8 import twt
def qea_schedule(seed, pop=20, gens=150, dtheta=np.radians(3), k=3, n=8):
    rng = np.random.default_rng(seed)
    Q = [np.full(n * k, np.pi/4) for _ in range(pop)]
    best_bits, best_val = None, 10**9
    for g in range(gens):
        for i in range(pop):
            x = observe(Q[i], rng)
            val = twt(decode_keys(x, n, k)[1])
            if val < best_val:
                best_bits, best_val = x, val
            Q[i] = rotate(Q[i], x, best_bits, dtheta)
    return best_val, decode_keys(best_bits, n, k)[1]
results = []
for s in range(10):
    val, order = qea_schedule(s)
    results.append(val)
    if s == 0:
        print('run 0 best order:', ['J%d' % (j + 1) for j in order], 'TWT', val)
print('10 runs:', results)
print('best', min(results), ' mean', np.mean(results),
      ' mean RPD vs 58: %.1f%%' % (100 * (np.mean(results) - 58) / 58))