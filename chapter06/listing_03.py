# Chapter 6, code listing 3 (in order of appearance)
import numpy as np
from qea import rotate
theta = np.full(8, np.pi/4)
x    = np.array([0, 1, 1, 0, 1, 0, 0, 1])   # an observed solution
best = np.array([0, 0, 1, 1, 0, 1, 0, 0])   # best solution so far
new = rotate(theta, x, best, dtheta=np.radians(9))
print('angle (deg):', np.round(np.degrees(new), 1))
print('P(1)       :', np.round(np.sin(new)**2, 3))