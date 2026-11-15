import numpy as np
from qubo import add_linear, add_quad, add_penalty_sum
p = [2, 3, 4]; d = [4, 7, 5]; wt = [1, 3, 3]; H = sum(p)       # small workshop, horizon 9
VARS = [(j, t) for j in range(3) for t in range(H - p[j] + 1)]  # x(j,t): job j starts at t
def shop_qubo(lam):
    idx = {jt: k for k, jt in enumerate(VARS)}
    Q = np.zeros((len(VARS), len(VARS))); const = 0.0
    for (j, t), k in idx.items():
        add_linear(Q, k, wt[j] * max(0, t + p[j] - d[j]))          # weighted tardiness if j starts at t
    for j in range(3):                                              # every job starts exactly once
        const += add_penalty_sum(Q, [idx[(jj, t)] for (jj, t) in VARS if jj == j], 1, lam)
    for (j, t), k in idx.items():                                   # no two jobs on the machine together
        for (jj, tt), kk in idx.items():
            if j < jj and t < tt + p[jj] and tt < t + p[j]:
                add_quad(Q, k, kk, lam)
    return Q, const
def decode_schedule(x):
    starts = {}
    for b, (j, t) in zip(x, VARS):
        if b: starts.setdefault(j, []).append(t)
    if sorted(starts) != [0, 1, 2] or any(len(s) != 1 for s in starts.values()): return None
    order = sorted(range(3), key=lambda j: starts[j][0])
    return order, {j: starts[j][0] for j in range(3)}
