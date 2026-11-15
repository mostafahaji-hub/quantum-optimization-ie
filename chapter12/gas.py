"""Chapter 12 - minimum finding by lowering the threshold
(the idea of Duerr and Hoyer; also called Grover adaptive search).
shoot(marked, k) runs k Grover rounds once and returns one
book-order string."""
import numpy as np

def minimum_search(table, n, shoot, rng, max_fail=3, log=None):
    N = 2 ** n
    calls = shots = 0
    s = shoot([], 0); shots += 1          # k = 0: a random string
    while s not in table:                 # unused code: try again
        s = shoot([], 0); shots += 1
    best, T = s, table[s][1]
    if log: log(f'start : {s} {table[s][0]}  T = {T}')
    m, fails = 1.0, 0
    while fails < max_fail:
        k = int(rng.integers(0, int(np.ceil(m))))   # 0..ceil(m)-1
        good = [x for x, (_, c) in table.items() if c < T]
        s = shoot(good, k); shots += 1; calls += k
        if s in table and table[s][1] < T:
            best, T, m, fails = s, table[s][1], 1.0, 0
            msg = f'better! T = {T}'
        else:
            m, fails = min(1.2 * m, np.sqrt(N)), fails + 1
            msg = 'no improvement'
        if log: log(f'k = {k}: measured {s} -> {msg}')
    return best, T, calls, shots
