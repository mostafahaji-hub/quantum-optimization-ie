import numpy as np
def observe(theta, rng):
    """One observation of a Q-bit chromosome: bit i is 1 with prob sin^2(theta_i)."""
    return (rng.random(len(theta)) < np.sin(theta)**2).astype(int)
def rotate(theta, x, best, dtheta):
    """Turn every Q-bit a little toward the bit of the best solution."""
    theta = theta.copy()
    for i in range(len(theta)):
        if x[i] != best[i]:
            theta[i] += dtheta if best[i] == 1 else -dtheta
    return np.clip(theta, 0.02, np.pi/2 - 0.02)
