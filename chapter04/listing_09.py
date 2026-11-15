# Chapter 4, code listing 9 (in order of appearance)
from sim import *
from shop import code, twt
p_one = [0.8, 0.2, 0.8]                 # desired P(qubit k = 1)
n = 3
psi = np.zeros(8); psi[0] = 1
for k in range(n):
    theta = 2 * np.arcsin(np.sqrt(p_one[k]))
    psi = op(Ry(theta), k, n) @ psi
P = probs(psi)
for s in sorted(P):
    seq = code.get(s, 'invalid')
    f = twt(seq) if s in code else '-'
    print(s, P[s], seq, f)
pv = sum(P[s] for s in code)
E_f = sum(P[s] * twt(code[s]) for s in code) / pv
print('P(valid) =', round(pv, 3), ' E[objective | valid] =', round(E_f, 2))
print('P(optimum 101) =', P['101'])
R = np.ceil(np.log(0.01) / np.log(1 - P['101']))
print('shots for 99% chance to see optimum:', int(R))