import math
# Large TSP of Chapter 2 (8 cities)
pts = [(6, 6), (0, 4), (8, 7), (6, 4), (7, 5), (9, 3), (8, 2), (4, 2)]
D = [[round(math.dist(a, b), 1) for b in pts] for a in pts]
def tour_length(tour):
    return round(sum(D[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour))), 1)
import numpy as np
from c6_qea import observe, rotate
from c6_keys import decode_keys

