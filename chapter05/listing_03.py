# Chapter 5, code listing 3 (in order of appearance)
from sim import *
# Deutsch: oracle U_f |x>|y> = |x>|y XOR f(x)>, one input bit
def U_f(f):
    M = np.zeros((4, 4))
    for x in (0, 1):
        for y in (0, 1):
            M[2*x + (y ^ f(x)), 2*x + y] = 1
    return M
funcs = {'f(x)=0': lambda x: 0, 'f(x)=1': lambda x: 1,
         'f(x)=x': lambda x: x, 'f(x)=NOT x': lambda x: 1 - x}
for name, f in funcs.items():
    psi = np.array([0, 1, 0, 0])                 # |0>|1>
    psi = np.kron(H, H) @ psi                     # H on both
    psi = U_f(f) @ psi                            # one oracle call
    psi = op(H, 0, 2) @ psi                       # H on the first qubit
    p0 = sum(abs(psi[i])**2 for i in (0, 1))     # P(first qubit = 0)
    verdict = 'constant' if p0 > 0.99 else 'balanced'
    print(f'{name:12s} P(q0=0) = {p0:.2f} -> {verdict}')