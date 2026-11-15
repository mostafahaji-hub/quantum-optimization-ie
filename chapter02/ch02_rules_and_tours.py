"""Chapter 2 - the two signature problems: rules, enumeration, nearest neighbour, 2-opt.
Reproduces Examples 2.3, 2.4, 2.6-2.8 and the subtour of Exercise 2.17."""
import itertools, math

# ---- small workshop (Example 2.3) and large workshop (Example 2.4) ----
def twt(order, p, d, w):
    t = total = 0
    for j in order:
        t += p[j]
        total += w[j] * max(0, t - d[j])
    return total

p3, d3, w3 = [2, 3, 4], [4, 7, 5], [1, 3, 3]
for o in itertools.permutations(range(3)):
    print('small workshop', ''.join(f'J{j+1}' for j in o), twt(o, p3, d3, w3))

p = [6, 8, 9, 6, 3, 6, 7, 2]; d = [16, 29, 14, 17, 23, 39, 17, 23]; w = [1, 1, 2, 3, 2, 2, 4, 1]
rules = {'SPT': lambda j: (p[j], j), 'EDD': lambda j: (d[j], j), 'WSPT': lambda j: (p[j] / w[j], j)}
for name, key in rules.items():
    o = sorted(range(8), key=key)
    print(f'{name:4s}', [j + 1 for j in o], twt(o, p, d, w))
best = min(itertools.permutations(range(8)), key=lambda o: twt(o, p, d, w))
print('optimum', [j + 1 for j in best], twt(best, p, d, w))

# ---- large TSP (Example 2.8) ----
pts = [(6, 6), (0, 4), (8, 7), (6, 4), (7, 5), (9, 3), (8, 2), (4, 2)]
D = [[round(math.dist(a, b), 1) for b in pts] for a in pts]
L = lambda t: round(sum(D[t[i]][t[(i + 1) % 8]] for i in range(8)), 1)
tour = [0]
while len(tour) < 8:
    c = tour[-1]
    tour.append(min((j for j in range(8) if j not in tour), key=lambda j: (D[c][j], j)))
print('nearest neighbour', [c + 1 for c in tour], L(tour))
improved = True
while improved:                      # first-improvement 2-opt
    improved = False
    for i in range(1, 7):
        for k in range(i + 1, 8):
            new = tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]
            if L(new) < L(tour) - 1e-9:
                tour, improved = new, True
print('after 2-opt', [c + 1 for c in tour], L(tour))
opt = min(L([0] + list(q)) for q in itertools.permutations(range(1, 8)))
print('optimum by enumeration of 2520 tours:', opt)
print('two subtours 1-3-5-1 + 2-4-6-7-8-2:',
      round(D[0][2] + D[2][4] + D[4][0] + D[1][3] + D[3][5] + D[5][6] + D[6][7] + D[7][1], 1))
