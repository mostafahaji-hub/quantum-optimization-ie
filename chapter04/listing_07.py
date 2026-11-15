# Chapter 4, code listing 7 (in order of appearance)
from sim import *
p1 = 0.30                              # want P(Line B) = 0.30
theta = 2 * np.arcsin(np.sqrt(p1))
print('theta (deg):', round(float(np.degrees(theta)), 2))
psi = Ry(theta) @ np.array([1, 0])
print('probabilities:', probs(psi))
print('1000 shots:', sample(psi, 1000, seed=3))