# Chapter 4, code listing 12 (in order of appearance)
from sim import *
psi = cnot(0, 1, 2) @ op(H, 0, 2) @ np.array([1, 0, 0, 0])
ideal = sample(psi, 1000, seed=9)
rng = np.random.default_rng(11)
noisy = {}
for s, cnt in ideal.items():
    for _ in range(cnt):
        bits = [b if rng.random() > 0.05 else str(1 - int(b)) for b in s]
        key = ''.join(bits)
        noisy[key] = noisy.get(key, 0) + 1
print('ideal:', ideal)
print('noisy:', dict(sorted(noisy.items())))