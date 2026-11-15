# Chapter 4, code listing 4 (in order of appearance)
import numpy as np
from sim import *   # added so this listing runs on its own
psi = np.zeros(4); psi[0] = 1          # |00>
psi = op(H, 0, 2) @ psi                 # H on q0
psi = cnot(0, 1, 2) @ psi               # CNOT q0 -> q1
print(probs(psi))