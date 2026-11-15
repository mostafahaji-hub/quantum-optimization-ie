# Chapter 4, code listing 5 (in order of appearance)
from sim import *
psi = np.zeros(4); psi[0] = 1
psi = cnot(0, 1, 2) @ op(H, 0, 2) @ psi
print(sample(psi, 1000))