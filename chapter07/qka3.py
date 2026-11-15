import numpy as np
from qea import observe, rotate
from keys import decode_keys
from ka_perm import swirl_move, between
def perm_to_bits(perm, n, K):
    """Write an order back as Q-bit keys: the job in place k gets a key that grows with k."""
    bits = np.zeros(n * K, dtype=int); top = 2**K - 1
    for k, job in enumerate(perm):
        key = round(k * top / (n - 1))
        bits[job*K:(job+1)*K] = [int(b) for b in format(key, f'0{K}b')]
    return bits
def quantum_keshtel(f, n, K=5, budget=3000, n_pop=20, pn1=0.2, pn2=0.4, n_swirl=5, dt=np.radians(3), seed=0):
    """Quantum Keshtel: classical Keshtel, but the 'new lake' keshtels are observed from a
    Q-bit chromosome that keeps learning where the lucky keshtels live."""
    rng = np.random.default_rng(seed)
    n1, n2 = max(1, round(pn1 * n_pop)), round(pn2 * n_pop); n3 = n_pop - n1 - n2
    q = np.full(n * K, np.pi/4)                                   # the 'map' of good lakes
    P = [list(rng.permutation(n)) for _ in range(n_pop)]; F = [f(p) for p in P]; evals = n_pop
    while evals < budget:
        order = np.argsort(F); P = [P[i] for i in order]; F = [F[i] for i in order]
        lucky, lucky_f = P[:n1], F[:n1]
        for i in range(n1):                                       # 1) swirling (as in Keshtel)
            for s in range(n_swirl):
                c = swirl_move(lucky[i], rng); fc = f(c); evals += 1
                if fc < lucky_f[i]: lucky[i], lucky_f[i] = c, fc
        mid = [between(*[lucky[k] for k in rng.choice(n1, 2, replace=n1 < 2)], rng) for _ in range(n2)]
        mid_f = [f(p) for p in mid]; evals += n2                  # 2) between two lucky ones
        best = lucky[int(np.argmin(lucky_f))]                     # 3) new lake, chosen by the Q-bit map
        new = []
        for _ in range(n3):
            x = observe(q, rng); new.append(decode_keys(x, n, K)[1])
            q = rotate(q, x, perm_to_bits(best, n, K), dt)
        new_f = [f(p) for p in new]; evals += n3
        P, F = lucky + mid + new, lucky_f + mid_f + new_f
    i = int(np.argmin(F)); return F[i], P[i]
