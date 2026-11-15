"""Chapter 12 - numerical check of the answers in answers_ch12.md."""
import numpy as np
from math import factorial, log, ceil, log2
from itertools import combinations, product
from qiskit.quantum_info import Operator, Statevector
from grover import oracle, best_k, p_success, grover_circuit
from compact import shop_table, tsp_table
def reflect(a):
    a = np.array(a, float); return 2 * a.mean() - a
# self-test 2 and 3
print('ST2', reflect([.5, .5, -.5, .5]))
print('ST3 deg', round(np.degrees(np.arcsin(.25)), 2), 'k', best_k(1, 16))
# Ex 1: third round
a = np.array([-0.0884] * 7 + [0.9723]); a[7] *= -1; a = reflect(a)
print('Ex1', np.round(a, 4), 'P', round(a[7] ** 2, 3))
# Ex 2
a = np.array([.5, .5, .5, .5]); a[0] *= -1; print('Ex2', reflect(a))
# Ex 3
print('Ex3', [round(p_success(1, 16, k), 3) for k in range(6)])
# Ex 5: oracle for 011 is diagonal with -1 only on 011
U = np.diag(Operator(oracle(['011'], 3)).data).real
print('Ex5', {format(i, '03b'): int(round(U[int(format(i, '03b')[::-1], 2)]))
              for i in range(8)})
# Ex 7
print('Ex7', round(p_success(1, 8, 5), 3), round(p_success(1, 8, 6), 3),
      'angle 13th', round(13 * np.degrees(np.arcsin(8 ** -.5)), 1))
# Ex 8
print('Ex8 M', len([c for _, c in shop_table().values() if c <= 12]),
      round(p_success(5, 8, 0), 3), round(p_success(5, 8, 1), 3))
# Ex 9: 2 qubits, M = 1, N = 4
print('Ex9 k', best_k(1, 4), p_success(1, 4, 1))
# Ex 10: TTS99
r = log(0.01) / log(1 - 0.945); print('Ex10 runs', round(r, 2))
# Ex 11: suppliers, x = (S1, S2, S3), exactly two
f = [40, 55, 35]
def sup(x):
    c = sum(fi * xi for fi, xi in zip(f, x))
    return c + 20 * x[0] * x[2] - 10 * x[1] * x[2]
print('Ex11', {''.join(map(str, x)): sup(x)
               for x in product([0, 1], repeat=3) if sum(x) == 2})
# Ex 12: location subsets
F = [30, 20, 25]; C = [[4, 9, 12], [10, 5, 9], [13, 8, 3]]
loc = {}
for x in product([0, 1], repeat=3):
    o = [i for i in range(3) if x[i]]
    if o:
        loc[''.join(map(str, x))] = (sum(F[i] for i in o) +
            sum(min(C[i][j] for i in o) for j in range(3)))
print('Ex12', loc)
# Ex 16: post-selection on FakeFez counts of Fig. 12.6 (seed 7)
print('Ex16', round(738 / (1000 - 31 - 54), 3))
# Ex 19
print('Ex19 qubits', ceil(log2(24)), 'unused', 2 ** 5 - 24,
      'k', best_k(1, 32), round(p_success(1, 32, 4), 3))
# Ex 20
print('Ex20 M1', best_k(1, 512), round(p_success(1, 512, 17), 4),
      'M6', best_k(6, 512), round(p_success(6, 512, 7), 4))
# Ex 22: expected position of one item in a random order of 6
print('Ex22', sum(range(1, 7)) / 6)
# Ex 23
print('Ex23', round(p_success(2, 8, 2), 3), round(p_success(2, 8, 3), 3))
# Ex 24
d = []
for k in range(5):
    pr = Statevector(grover_circuit(['101'], 3, k, False)).probabilities_dict()
    d.append(abs(pr.get('101', 0) - p_success(1, 8, k)))
print('Ex24 max diff', f'{max(d):.1e}')
