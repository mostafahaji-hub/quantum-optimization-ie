"""Numeric checks for the answers of Chapters 1 and 2."""
import math, itertools
h, c, eV = 6.63e-34, 3e8, 1.6e-19
print('--- Chapter 1')
for lam in (550e-9, 300e-9, 700e-9, 450e-9):
    E = h * c / lam
    print(f'1.1 lambda {lam*1e9:.0f} nm: E = {E:.3e} J = {E/eV:.2f} eV')
for metal, W in (('potassium', 2.3), ('zinc', 4.3)):
    for name, lam in (('red', 700e-9), ('blue', 450e-9), ('UV', 300e-9)):
        E = h * c / lam / eV
        print(f'1.2 {metal:9s} {name:4s} E={E:.2f} eV ->', f'KEmax {E-W:.2f} eV' if E > W else 'no electron')
print('1.3', 650e-9*2/(0.125e-3)*1e3, 'mm;', 650e-9*5/0.25e-3*1e3, 'mm; d =', 650e-9*3/0.01*1e3, 'mm')
for a, b in ((0.8, 0.6), (0.5, 0.5), (1/2**0.5, -1/2**0.5), (0.3, 0.4)):
    n2 = a*a + b*b
    print(f'1.4 ({a:.3f},{b:.3f}) sum={n2:.3f} factor={1/math.sqrt(n2):.4f} angle={math.degrees(math.atan2(b, a)):.2f}')
for th in (0, 15, 30, 45, 60, 75, 90):
    t = math.radians(th); print(f'1.6 theta {th:2d}: {0.5*math.cos(t)**2*math.sin(t)**2:.5f}')
print('1.7 four filters:', 0.5*math.cos(math.radians(30))**6)
for N in (2, 3, 10, 100):
    print(f'1.7 N={N} steps:', round(0.5*math.cos(math.pi/(2*N))**(2*N), 4))
wins = 0
for a0, a1, b0, b1 in itertools.product((0, 1), repeat=4):
    w = (a0 == b0) + (a0 == b1) + (a1 == b0) + (a1 != b1)
    wins = max(wins, w)
print('1.8 max classical wins of 4:', wins, ' strategies:', 16)
sd = math.sqrt(400*0.75*0.25); print('1.9 mean 300 sd', round(sd, 3), 'z', round(40/sd, 2), 'quantum mean', 0.854*400)
print('1.11', 0.4*1+0.6*0, 0.4*0.5+0.6*0.5, 0.4*0+0.6*1)
print('1.12 tmax nm', 0.1*math.log2(100), ' P(1 nm, 0.05)', 2**-20)
for E in (1.9, 2.3, 3.1): print('1.13', E, 'eV ->', round(1240/E), 'nm')
print('1.13 constant', h*c/(1.602e-19*1e-9))
print('1.14 sd', math.sqrt(0.25/256), ' N', 0.25/0.01**2)
for n in range(2, 13):
    print(f'1.15 n={n:2d} n!={math.factorial(n):>10,d} tours={math.factorial(n-1)/2:>12,.1f}')
print('1.15 n=12 times: shop', math.factorial(12)*1e-6, 's; TSP', math.factorial(11)/2*1e-6, 's')
for n in range(15, 20): print('1.15 n', n, 'TSP years', math.factorial(n-1)/2*1e-6/3.156e7)
print('1.16 2^300 =', f'{2.0**300:.2e}')
print('--- Chapter 2')
p3, d3, w3 = [2, 3, 4], [4, 7, 5], [1, 3, 3]
def stats(o, p, d, w):
    t = 0; C = {}
    for j in o: t += p[j]; C[j] = t
    return (sum(w[j]*max(0, C[j]-d[j]) for j in o), sum(w[j]*C[j] for j in o),
            max(C[j]-d[j] for j in o), sum(C[j] > d[j] for j in o))
for o in itertools.permutations(range(3)):
    print('2.1', ''.join(f'J{j+1}' for j in o), 'TWT, wC, Lmax, nTardy =', stats(o, p3, d3, w3))
for w1 in (1, 2, 3, 4, 5, 6):
    w = [w1, 3, 3]; best = min(itertools.permutations(range(3)), key=lambda o: (stats(o, p3, d3, w)[0], o))
    vals = sorted((stats(o, p3, d3, w)[0], ''.join(f'J{j+1}' for j in o)) for o in itertools.permutations(range(3)))
    print('2.2 w1 =', w1, vals[:3])
p = [6, 8, 9, 6, 3, 6, 7, 2]; d = [16, 29, 14, 17, 23, 39, 17, 23]; w = [1, 1, 2, 3, 2, 2, 4, 1]
ms3 = sorted(range(3), key=lambda j: (d3[j]-p3[j], j)); print('2.3 small MS', [j+1 for j in ms3], stats(ms3, p3, d3, w3)[0])
ms8 = sorted(range(8), key=lambda j: (d[j]-p[j], j)); v = stats(ms8, p, d, w)[0]; print('2.3 large MS', [j+1 for j in ms8], v, 'RPD', round(100*(v-58)/58, 1))
wspt = sorted(range(8), key=lambda j: (p[j]/w[j], j))
nb = []
for i in range(7):
    o = wspt[:]; o[i], o[i+1] = o[i+1], o[i]; nb.append((stats(o, p, d, w)[0], i, [j+1 for j in o]))
for x in sorted(nb): print('2.4 swap', x)
D4 = {'AB': 5, 'AC': 12, 'AD': 4, 'BC': 7, 'BD': 4, 'CD': 10}
dist = lambda a, b: D4[''.join(sorted(a+b))]
def nn(start):
    t = [start]; left = set('ABCD') - {start}
    while left:
        nx = min(sorted(left), key=lambda x: dist(t[-1], x)); t.append(nx); left.remove(nx)
    return ''.join(t), sum(dist(t[i], t[(i+1) % 4]) for i in range(4))
for s in 'ABCD': print('2.5 NN from', s, nn(s))
tour = 'ADBC'
for i in range(4):
    for k in range(i+2, 4 + (i > 0)):
        if (k - i) % 4 < 2: continue
        new = tour[:i+1] + tour[i+1:k+1][::-1] + tour[k+1:]
        L = sum(dist(new[q], new[(q+1) % 4]) for q in range(4))
        print('2.6 reverse', tour[i+1:k+1], '->', new, L)
print('2.8 n^3:', 40*1e6**(1/3), ' 2^n:', 40 + math.log2(1e6))
fr = [2, 6, 3, 4, 7, 0, 1, 5]; print('2.10 friend', stats(fr, p, d, w)[0])
for n in (12, 16, 20):
    N = math.factorial(n-1)/2
    print(f'2.11 n={n}: enum {N/2*1e-6:.3g} s, Grover {math.pi/4*math.sqrt(N)*1e-3:.3g} s, HK {n*n*2**n*1e-6:.3g} s')
for P, tau in ((0.5, 20), (0.05, 2), (0.99, 100)):
    R = math.ceil(math.log(0.01)/math.log(1-P)); print('2.12', P, tau, R, R*tau, 'ms')
print('2.12 tie p >=', 1 - math.exp(math.log(0.01)/70))
lo, hi, qs = 0, 258, []
while lo < hi:
    mid = (lo+hi)//2; ans = 58 <= mid; qs.append((mid, 'yes' if ans else 'no'))
    hi, lo = (mid, lo) if ans else (hi, mid+1)
print('2.19', len(qs), qs, 'value', lo)
for n in (8, 12, 20):
    N = math.factorial(n); print(f'2.20 n={n}: N={N:.3e} classical {N/2:.3e} Grover {math.pi/4*math.sqrt(N):.3e}')
