# Chapter 4, code listing 13 (in order of appearance)
from sim import *
print(np.round(H @ Z @ H, 3) + 0)
S = np.array([[1, 0], [0, 1j]])
print(np.round(H @ S @ H @ np.array([1, 0]), 3))