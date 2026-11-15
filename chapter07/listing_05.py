# Chapter 7, code listing 5 (in order of appearance)
# This listing is part of algs.py (see listing_04 for the file header); run it via algs.py.
def QIGA(seed, pop=20, gens=150, dt=np.radians(3), pc=0.2, pm=0.002):
    rng = np.random.default_rng(seed)
    Q = [np.full(n * K, np.pi/4) for _ in range(pop)]; bb, bv = None, 10**9
    for g in range(gens):
        X = [observe(q, rng) for q in Q]; V = [f_bits(x) for x in X]
        i = int(np.argmin(V))
        if V[i] < bv: bb, bv = X[i], V[i]
        Q = [rotate(q, x, bb, dt) for q, x in zip(Q, X)]
        for a in range(0, pop - 1, 2):                # quantum crossover: swap angle blocks
            if rng.random() < pc:
                cut = rng.integers(1, n) * K
                Q[a][cut:], Q[a+1][cut:] = Q[a+1][cut:].copy(), Q[a][cut:].copy()
        for q in Q:                                   # quantum NOT mutation: theta -> 90 - theta
            m = rng.random(len(q)) < pm; q[m] = np.pi/2 - q[m]
    return bv