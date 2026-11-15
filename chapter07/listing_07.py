# Chapter 7, code listing 7 (in order of appearance)
# This listing is part of algs.py (see listing_04 for the file header); run it via algs.py.
def QPSO(seed, M=20, iters=150):
    rng = np.random.default_rng(seed)
    X = rng.random((M, n)); P = X.copy(); PF = np.array([twt(order_from_real(x)) for x in X])
    for t in range(iters - 1):
        beta = 1.0 - 0.5 * t / iters                  # contraction-expansion coefficient
        g = P[PF.argmin()]; mbest = P.mean(axis=0)
        for i in range(M):
            phi = rng.random(n); u = rng.random(n)
            attractor = phi * P[i] + (1 - phi) * g
            sign = np.where(rng.random(n) < 0.5, 1, -1)
            X[i] = attractor + sign * beta * np.abs(mbest - X[i]) * np.log(1 / u)
            f = twt(order_from_real(X[i]))
            if f < PF[i]: P[i], PF[i] = X[i].copy(), f
    return int(PF.min())