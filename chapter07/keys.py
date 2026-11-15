# Large workshop of Chapter 2 (8 jobs)
p = [6, 8, 9, 6, 3, 6, 7, 2]
d = [16, 29, 14, 17, 23, 39, 17, 23]
w = [1, 1, 2, 3, 2, 2, 4, 1]
def twt(seq):
    t, total = 0, 0
    for j in seq:
        t += p[j]
        total += w[j] * max(0, t - d[j])
    return total
def decode_keys(bits, n_jobs, k=3):
    """k bits per job -> integer key; jobs sorted by key (ties: smaller index first)."""
    keys = [int(''.join(str(b) for b in bits[j*k:(j+1)*k]), 2) for j in range(n_jobs)]
    order = sorted(range(n_jobs), key=lambda j: (keys[j], j))
    return keys, order

