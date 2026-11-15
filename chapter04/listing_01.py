# Chapter 4, code listing 1 (in order of appearance)
# Inline snippet from the text: define CNOT and H first (see Section 3.10 / sim.py).
psi = CNOT @ np.kron(H, np.eye(2)) @ np.array([1, 0, 0, 0])
print(np.round(psi, 3))