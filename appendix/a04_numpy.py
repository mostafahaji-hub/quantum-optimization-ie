import numpy as np

# Two-machine toy QUBO of Chapter 13:
# f = 4 x0 + 6 x1 + 10 (x0 + x1 - 1)^2 = x^T Q x + 10
Q = np.array([[-6, 20],
              [ 0, -4]])
for x0 in (0, 1):
    for x1 in (0, 1):
        x = np.array([x0, x1])
        print(x0, x1, "->", x @ Q @ x + 10)
