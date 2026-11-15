# Chapter 5, code listing 10 (in order of appearance)
from alg import *
from shop import code, twt
f = lambda s: twt(code[s]) if s in code else None
rng = np.random.default_rng(4)
def measure_once(psi):
    p = np.abs(psi)**2
    i = rng.choice(len(psi), p=p/p.sum())
    return format(i, '03b')
# step 0: one random valid schedule gives the first threshold
s = measure_once(Hn(3) @ np.eye(8)[0])
while f(s) is None:
    s = measure_once(Hn(3) @ np.eye(8)[0])
best, T = s, f(s)
print('start      :', best, code[best], 'T =', T)
fails = 0
for rnd in range(1, 9):
    k = rng.integers(1, 3)                      # 1 or 2 Grover iterations
    psi = grover(lambda x: f(x) is not None and f(x) < T, n=3, k=k)
    s = measure_once(psi)
    ok = f(s) is not None and f(s) < T
    if ok:
        best, T, fails = s, f(s), 0
    else:
        fails += 1
    print(f'round {rnd}, k={k}: measured {s} ->',
          f'better! T = {T}' if ok else 'no improvement')
    if fails == 3:
        break
print('result     :', best, code[best], 'objective', T)