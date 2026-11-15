# Chapter 5, code listing 4 (in order of appearance)
from alg import *
def deutsch_jozsa(f, n):
    psi = np.zeros(2**n); psi[0] = 1
    psi = Hn(n) @ phase_oracle(f, n) @ Hn(n) @ psi
    return abs(psi[0])**2                 # P(all zeros)
n = 3
tests = {'always 0'        : lambda s: 0,
         'always 1'        : lambda s: 1,
         'last bit'        : lambda s: int(s[-1]),
         'parity (XOR)'    : lambda s: s.count('1') % 2,
         'first two differ': lambda s: int(s[0] != s[1])}
for name, f in tests.items():
    p = deutsch_jozsa(f, n)
    print(f'{name:17s} P(000) = {p:.2f} ->', 'constant' if p > 0.99 else 'balanced')