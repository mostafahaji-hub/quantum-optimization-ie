# Chapter 7, code listing 9 (in order of appearance)
def GA(seed, pop=20, gens=150, pm=0.1):
    rng = np.random.default_rng(seed)
    P = rng.random((pop, n)); F = np.array([twt(order_from_real(x)) for x in P])
    for g in range(gens - 1):
        new = [P[F.argmin()].copy()]                  # elitism
        while len(new) < pop:
            a, b = [min(rng.choice(pop, 2, replace=False), key=lambda i: F[i]) for _ in range(2)]
            mask = rng.random(n) < 0.5                # uniform crossover
            c = np.where(mask, P[a], P[b])
            m = rng.random(n) < pm; c[m] = rng.random(m.sum())   # mutation
            new.append(c)
        P = np.array(new); F = np.array([twt(order_from_real(x)) for x in P])
    return int(F.min())