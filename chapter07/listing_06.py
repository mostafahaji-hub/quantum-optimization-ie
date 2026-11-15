# Chapter 7, code listing 6 (in order of appearance)
# This listing is part of algs.py (see listing_04 for the file header); run it via algs.py.
def QTS(seed, iters=300, m=10, dt=np.radians(3), tenure=5):
    rng = np.random.default_rng(seed)
    q = np.full(n * K, np.pi/4); bb, bv = None, 10**9; tabu = {}
    for it in range(iters):
        X = [observe(q, rng) for _ in range(m)]; V = [f_bits(x) for x in X]
        best, worst = X[int(np.argmin(V))], X[int(np.argmax(V))]
        if min(V) < bv: bb, bv = best, min(V)
        for gidx in range(len(q)):
            if tabu.get(gidx, -1) >= it or best[gidx] == worst[gidx]: continue
            q[gidx] += dt if best[gidx] == 1 else -dt      # toward best, away from worst
            tabu[gidx] = it + tenure                        # do not touch again for a while
        q = np.clip(q, 0.02, np.pi/2 - 0.02)
    return bv