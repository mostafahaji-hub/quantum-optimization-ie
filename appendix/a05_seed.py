import numpy as np

rng = np.random.default_rng(2026)     # fixed seed
print(rng.integers(0, 2, size=9))      # a random 9-bit string
print(rng.permutation(3))              # a random order of 3 jobs
rng = np.random.default_rng(2026)     # same seed again
print(rng.integers(0, 2, size=9))      # exactly the same bits
