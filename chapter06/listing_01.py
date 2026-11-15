# Chapter 6, code listing 1 (in order of appearance)
import numpy as np
theta = np.radians(30)                 # Q-bit angle
alpha, beta = np.cos(theta), np.sin(theta)
print('alpha =', round(alpha, 3), ' beta =', round(beta, 3))
print('P(1) =', round(beta**2, 3))
rng = np.random.default_rng(1)
bits = (rng.random(1000) < beta**2).astype(int)   # 1000 observations
print('ones observed:', bits.sum(), 'of 1000')