from itertools import permutations
from encode import tour_to_bits, bits_to_tour
D = {'AB': 5, 'AC': 12, 'AD': 4, 'BC': 7, 'BD': 4, 'CD': 10}
dist = lambda a, b: D[''.join(sorted(a + b))]
for p in permutations('BCD'):
    tour = 'A' + ''.join(p)
    L = sum(dist(tour[i], (tour + 'A')[i + 1]) for i in range(4))
    b = tour_to_bits(tour)
    print(f'{"-".join(tour)}-A  {b[:3]} {b[3:6]} {b[6:]}'
          f'  back {bits_to_tour(b)}  length {L}')
