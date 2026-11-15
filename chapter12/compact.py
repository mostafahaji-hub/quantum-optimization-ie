"""Chapter 12 - compact 3-qubit codes for the two signature
problems. Book order: the leftmost bit of a code is qubit q0.
The code of an order is its index (0..5) written in binary."""
from itertools import permutations

p, d, w = [2, 3, 4], [4, 7, 5], [1, 3, 3]   # small shop (Ch. 2)
dist = {'AB': 5, 'AC': 12, 'AD': 4,          # small TSP (Ch. 2)
        'BC': 7, 'BD': 4, 'CD': 10}

def twt(order):
    """Total weighted tardiness; order = jobs, e.g. (3, 2, 1)."""
    t = total = 0
    for j in order:
        t += p[j - 1]
        total += w[j - 1] * max(0, t - d[j - 1])
    return total

def tour_length(tour):
    """tour like 'ABCDA'."""
    return sum(dist[''.join(sorted(tour[i:i + 2]))]
               for i in range(len(tour) - 1))

def shop_table():
    """book code -> (order name, cost); 6 codes are used."""
    tab = {}
    for k, o in enumerate(permutations([1, 2, 3])):
        name = ''.join(f'J{j}' for j in o)
        tab[format(k, '03b')] = (name, twt(o))
    return tab

def tsp_table():
    """book code -> (tour, length) for the 6 directed tours."""
    tab = {}
    for k, o in enumerate(permutations('BCD')):
        tour = 'A' + ''.join(o) + 'A'
        tab[format(k, '03b')] = (tour, tour_length(tour))
    return tab

def marked_by_threshold(table, T):
    """All used codes whose cost is <= T (unused codes: never)."""
    return [s for s, (_, c) in table.items() if c <= T]
