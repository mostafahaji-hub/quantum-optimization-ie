# Chapter 5, code listing 9 (in order of appearance)
from alg import *
cost = [3, 5, 4, 6]                      # service cost of machines M1..M4
def ok(s):
    x = [int(b) for b in s]
    if sum(x) != 2:          return False   # exactly two machines this shift
    if x[0] and x[1]:        return False   # M1 and M2 share one technician
    return sum(c*v for c, v in zip(cost, x)) <= 9   # budget
good = [s for s in (format(i, '04b') for i in range(16)) if ok(s)]
M, N = len(good), 16
theta = np.arcsin(np.sqrt(M / N))
k = int(np.floor(np.pi / (4 * theta)))
print('good plans:', good, ' M =', M, ' best k =', k)
psi = grover(ok, n=4, k=k)
P = probs(psi)
print('P(good) =', round(sum(P.get(s, 0) for s in good), 3))
print(sample(psi, 1000, seed=2))