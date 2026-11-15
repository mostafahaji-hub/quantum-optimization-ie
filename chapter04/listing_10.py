# Chapter 4, code listing 10 (in order of appearance)
from sim import *
tours = {'00': ('A-B-C-D-A', 26), '01': ('A-B-D-C-A', 31),
         '10': ('A-C-B-D-A', 27)}
def run(p_one):
    psi = np.zeros(4); psi[0] = 1
    for k in range(2):
        psi = op(Ry(2*np.arcsin(np.sqrt(p_one[k]))), k, 2) @ psi
    P = probs(psi)
    pv = sum(P.get(s, 0) for s in tours)
    E_len = sum(P.get(s, 0) * tours[s][1] for s in tours) / pv
    return P, round(E_len, 2)
for p_one in ([0.5, 0.5], [0.2, 0.2], [0.05, 0.05]):
    P, E_len = run(p_one)
    print(p_one, P, ' E[length | valid] =', E_len)