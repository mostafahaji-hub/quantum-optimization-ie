p = [2, 3, 4]
d = [4, 7, 5]
w = [1, 3, 3]

def weighted_tardiness(order, p, d, w):
    """Total weighted tardiness of one order sequence."""
    t = 0          # clock: when the current order finishes
    total = 0
    for j in order:
        t = t + p[j]
        late = max(0, t - d[j])
        total = total + w[j] * late
    return total

if __name__ == "__main__":     # runs only when started directly
    print(weighted_tardiness([2, 1, 0], p, d, w))   # J3 J2 J1
    print(weighted_tardiness([0, 1, 2], p, d, w))   # J1 J2 J3
