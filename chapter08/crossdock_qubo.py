import numpy as np
from qubo import add_quad, add_penalty_sum
flow = [[10, 2],                      # pallets from inbound truck T1, T2 to outbound truck O1, O2
        [4, 8]]
dist = [[2, 6],                       # metres from inbound door A, B to outbound door C, D
        [5, 3]]
x = lambda i, k: 2 * i + k            # x_ik: inbound truck i at inbound door k   -> 0..3
y = lambda j, l: 4 + 2 * j + l        # y_jl: outbound truck j at outbound door l -> 4..7
def crossdock_qubo(lam):
    Q = np.zeros((8, 8)); const = 0.0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    add_quad(Q, x(i, k), y(j, l), flow[i][j] * dist[k][l])   # forklift work
    for v in (x, y):                                                       # two assignment problems
        for a in range(2):
            const += add_penalty_sum(Q, [v(a, b) for b in range(2)], 1, lam)   # every truck one door
            const += add_penalty_sum(Q, [v(b, a) for b in range(2)], 1, lam)   # every door one truck
    return Q, const
