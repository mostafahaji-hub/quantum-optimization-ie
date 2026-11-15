# Chapter 6, code listing 6 (in order of appearance)
import numpy as np
# tiny truck: 3 shipments, capacity 8 tons
w, v, CAP = [3, 4, 5], [4, 5, 6], 8
ratio_order = sorted(range(3), key=lambda i: v[i] / w[i])     # worst ratio first
def repair(x):
    x = list(x)
    for i in ratio_order:
        if sum(wi for wi, b in zip(w, x) if b) <= CAP: break
        if x[i]: x[i] = 0
    return x
value = lambda x: sum(vi for vi, b in zip(v, x) if b)
# the random numbers are written down so you can follow by hand
R = {1: {'A': [0.30, 0.62, 0.71], 'B': [0.12, 0.40, 0.25]},
     2: {'A': [0.20, 0.90, 0.35], 'B': [0.55, 0.30, 0.80]}}
theta = {'A': np.radians([45, 45, 45]), 'B': np.radians([45, 45, 45])}
best, best_val, dt = None, -1, np.radians(10)
for g in (1, 2):
    obs = {}
    for c in ('A', 'B'):
        P1 = np.sin(theta[c])**2
        raw = [int(r < p) for r, p in zip(R[g][c], P1)]
        x = repair(raw)
        obs[c] = x
        print(f'gen {g} {c}: P(1) {np.round(P1, 3)}  raw {raw} -> repaired {x}  value {value(x)}')
        if value(x) > best_val:
            best, best_val = x, value(x)
    print(f'gen {g} best so far: {best}  value {best_val}')
    for c in ('A', 'B'):
        for i in range(3):
            if obs[c][i] != best[i]:
                theta[c][i] += dt if best[i] == 1 else -dt
        print(f'   after rotation {c}: angles {np.round(np.degrees(theta[c])).astype(int)}')