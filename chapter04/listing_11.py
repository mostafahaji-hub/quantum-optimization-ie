# Chapter 4, code listing 11 (in order of appearance)
from sim import *
import itertools
c = [40, 55, 35]                         # cost of suppliers S1, S2, S3
lam = 100                                # penalty if not exactly 2 chosen
def cost(x):
    x1, x2, x3 = x
    f = c[0]*x1 + c[1]*x2 + c[2]*x3
    f += 20*x1*x3                        # S1 and S3 share a congested port
    f -= 10*x2*x3                        # S2 and S3 share one truck
    f += lam * (x1 + x2 + x3 - 2)**2     # exactly two suppliers
    return f
strings = [''.join(b) for b in itertools.product('01', repeat=3)]
F = np.array([cost([int(ch) for ch in s]) for s in strings])
for s, f in zip(strings, F):
    print(s, f)
C = np.diag(F)                           # cost as a diagonal matrix
psi_u = np.ones(8) / np.sqrt(8)          # H on all three qubits
print('uniform  E =', round(psi_u @ C @ psi_u, 2))
psi = np.zeros(8); psi[0] = 1
for k, p1 in enumerate([0.1, 0.9, 0.9]):
    psi = op(Ry(2*np.arcsin(np.sqrt(p1))), k, 3) @ psi
print('biased   E =', round(psi @ C @ psi, 2), ' P(011) =', round(abs(psi[3])**2, 3))