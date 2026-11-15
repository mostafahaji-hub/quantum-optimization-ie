"""Example 15.3 - simple rules (Chapter 2) on all four problems."""
import shop8, tsp8
from shop9 import tardiness           # small workshop, jobs 1..3
from tsp4 import D as D4, length

def rule(jobs, key):
    """Sort the jobs by a key: the whole 'algorithm' is one sort."""
    return sorted(jobs, key=key)

p3, d3, w3 = [2, 3, 4], [4, 7, 5], [1, 3, 3]
J = [1, 2, 3]
small = {'SPT': rule(J, lambda j: p3[j - 1]),
         'EDD': rule(J, lambda j: d3[j - 1]),
         'WSPT': rule(J, lambda j: -w3[j - 1] / p3[j - 1])}
for name, order in small.items():
    print(f'small shop {name:4s}', order, tardiness(order))
J8 = range(8)
big = {'SPT': rule(J8, lambda j: shop8.p[j]),
       'EDD': rule(J8, lambda j: shop8.d[j]),
       'WSPT': rule(J8, lambda j: -shop8.w[j] / shop8.p[j])}
for name, order in big.items():
    print(f'8-job shop {name:4s}', [j + 1 for j in order],
          shop8.twt(order))

def nearest(D, start):
    """Nearest neighbour; ties go to the smaller city index."""
    tour, left = [start], set(range(len(D))) - {start}
    while left:
        nxt = min(sorted(left), key=lambda j: D[tour[-1]][j])
        tour.append(nxt)
        left.remove(nxt)
    return tour

t = nearest(D4, 0)
s = ''.join('ABCD'[i] for i in t) + 'A'
print('small TSP nearest neighbour from A:', s, length(s))
lens = [tsp8.tour_length(nearest(tsp8.D, s)) for s in range(8)]
print('8-city TSP nearest neighbour from city 0:', lens[0])
print('8-city TSP best of 8 starts:', min(lens), 'all:', lens)
