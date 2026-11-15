# Chapter 5, code listing 5 (in order of appearance)
from alg import *
s = '1011'                                # hidden pattern
f = lambda x: sum(int(a) * int(b) for a, b in zip(s, x)) % 2
n = len(s)
psi = np.zeros(2**n); psi[0] = 1
psi = Hn(n) @ phase_oracle(f, n) @ Hn(n) @ psi
print(probs(psi))