"""Chapter 7 answers, part A: hand checks and Exercises 7.8, 7.10-7.12."""
import sys, math, time; sys.path.insert(0, '../chapter07')
import numpy as np
import algs
from algs import KA, GA, QEA, QIGA, QTS, QPSO, QKA
for a in (5, 45, 80):
    t = math.radians(a); print(f'7.1 {a} deg -> {90-a} deg: P(1) {math.sin(t)**2:.4f} -> {math.cos(t)**2:.4f}')
print('7.4 jumps', 0.5*0.4*math.log(1/0.9), '->', 0.4 - 0.5*0.4*math.log(1/0.9), 0.4 + 0.5*0.4*math.log(1/0.9))
print('7.6', 0.95**8, 0.8**(1/8))
res = {}
for name, A in [('KA', KA), ('GA', GA), ('QEA', QEA), ('QIGA', QIGA), ('QTS', QTS), ('QPSO', QPSO), ('QKA', QKA)]:
    t0 = time.time(); v = [A(s) for s in range(20)]; res[name] = v
    print(f'7.8 {name:5s} 20 runs: best {min(v)} mean {np.mean(v):.1f} worst {max(v)} ({time.time()-t0:.0f} s)')
for pc in (0.0, 0.2, 0.5, 0.8):
    v = [QIGA(s, pc=pc) for s in range(10)]; print(f'7.10 QIGA pc={pc}: mean {np.mean(v):.1f} best {min(v)}')
for ten in (1, 5, 20):
    v = [QTS(s, tenure=ten) for s in range(10)]; print(f'7.11 QTS tenure={ten}: mean {np.mean(v):.1f} best {min(v)}')
def QPSO_b(seed, b0, b1, M=20, iters=150):
    n, twt, ofr = algs.n, algs.twt, algs.order_from_real
    rng = np.random.default_rng(seed)
    X = rng.random((M, n)); P = X.copy(); PF = np.array([twt(ofr(x)) for x in X])
    for t in range(iters - 1):
        beta = b0 + (b1 - b0) * t / iters
        g = P[PF.argmin()]; mbest = P.mean(axis=0)
        for i in range(M):
            phi = rng.random(n); u = rng.random(n)
            att = phi * P[i] + (1 - phi) * g
            sign = np.where(rng.random(n) < 0.5, 1, -1)
            X[i] = att + sign * beta * np.abs(mbest - X[i]) * np.log(1 / u)
            f = twt(ofr(X[i]))
            if f < PF[i]: P[i], PF[i] = X[i].copy(), f
    return int(PF.min())
for b0, b1 in ((1.0, 0.5), (0.75, 0.75), (1.2, 0.4)):
    v = [QPSO_b(s, b0, b1) for s in range(10)]; print(f'7.12 QPSO beta {b0}->{b1}: mean {np.mean(v):.1f} best {min(v)}')
