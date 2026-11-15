from truck import w, v, CAP, weight
ratio_order = sorted(range(len(w)), key=lambda i: v[i] / w[i])   # worst ratio first
def repair(x, add=True):
    """Remove worst-ratio items until feasible; optionally add best-ratio items that still fit."""
    x = [int(b) for b in x]
    for i in ratio_order:
        if weight(x) <= CAP: break
        if x[i]: x[i] = 0
    if add:
        for i in reversed(ratio_order):
            if not x[i] and weight(x) + w[i] <= CAP: x[i] = 1
    return x
from truck import weight, value

