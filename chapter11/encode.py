"""Chapter 11 - job orders and tours <-> 9-bit strings.
Book order: the leftmost character is variable 0 = qubit q0."""
import numpy as np

def order_to_bits(order):
    """order = jobs by position, e.g. [3, 2, 1] for J3J2J1.
    x(j,k) = job j in position k has index 3*(j-1)+(k-1)."""
    n = len(order)
    M = np.zeros((n, n), dtype=int)   # rows jobs, cols positions
    for k, j in enumerate(order):
        M[j - 1, k] = 1
    return ''.join(map(str, M.flatten()))

def bits_to_order(bits):
    """Inverse of order_to_bits; None if not a permutation."""
    n = int(round(len(bits) ** 0.5))
    M = np.array([int(b) for b in bits]).reshape(n, n)
    if (M.sum(0) != 1).any() or (M.sum(1) != 1).any():
        return None
    return [int(np.argmax(M[:, k])) + 1 for k in range(n)]

def tour_to_bits(tour, cities='ABCD'):
    """tour like 'ABCD' (depot A first). x(i,t) = city i at step t,
    in the order B1 B2 B3 C1 C2 C3 D1 D2 D3."""
    m = len(cities) - 1
    M = np.zeros((m, m), dtype=int)   # rows cities, cols steps
    for t, c in enumerate(tour[1:]):
        M[cities.index(c) - 1, t] = 1
    return ''.join(map(str, M.flatten()))

def bits_to_tour(bits, cities='ABCD'):
    order = bits_to_order(bits)         # the same matrix test
    if order is None:
        return None
    return cities[0] + ''.join(cities[i] for i in order) + cities[0]
