# Chapter 4, code listing 8 (in order of appearance)
# Small workshop: p, d, w for J1..J3
p = {'J1': 2, 'J2': 3, 'J3': 4}
d = {'J1': 4, 'J2': 7, 'J3': 5}
w = {'J1': 1, 'J2': 3, 'J3': 3}
def twt(seq):
    t, total = 0, 0
    for j in seq:
        t += p[j]
        total += w[j] * max(0, t - d[j])
    return total
code = {'000': ('J1','J2','J3'), '001': ('J1','J3','J2'),
        '010': ('J2','J1','J3'), '011': ('J2','J3','J1'),
        '100': ('J3','J1','J2'), '101': ('J3','J2','J1')}
from sim import *
from shop import code, twt
n = 3
psi = np.zeros(8); psi[0] = 1
for k in range(n):
    psi = op(H, k, n) @ psi             # uniform superposition
P = probs(psi)
valid = {s: P[s] for s in code}
E_f = sum(P[s] * twt(code[s]) for s in code) / sum(valid.values())
print('P(each code) =', P['000'])
print('P(valid code) =', sum(valid.values()))
print('E[objective | valid] =', round(E_f, 2))
counts = sample(psi, 1000, seed=5)
good = {s: c for s, c in counts.items() if s in code}
avg = sum(c * twt(code[s]) for s, c in good.items()) / sum(good.values())
best = min(good, key=lambda s: twt(code[s]))
print('shots:', counts)
print('valid shots:', sum(good.values()), ' sample average:', round(avg, 2))
print('best seen:', best, code[best], 'objective', twt(code[best]))