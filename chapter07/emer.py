import numpy as np, heapq, math
# A simplified emergency network: hospital H (node 0) and 7 incident sites A..G
names = ['H', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
pts = [(50, 50), (20, 80), (35, 20), (80, 85), (85, 30), (10, 40), (60, 10), (65, 65)]
N = len(pts)
T = [[round(math.dist(a, b) / 10, 1) for b in pts] for a in pts]   # travel time (minutes)
r = np.random.default_rng(7)
REL = np.ones((N, N))
for i in range(N):
    for j in range(i + 1, N):
        REL[i, j] = REL[j, i] = round(r.uniform(0.60, 0.99), 2)          # arc reliability
def reliable_path(a, b, tau):
    """Fastest path from a to b using only arcs with reliability >= tau (Dijkstra)."""
    dist, prev = {a: 0.0}, {}
    pq = [(0.0, a)]
    while pq:
        dcur, u = heapq.heappop(pq)
        if u == b: break
        if dcur > dist[u]: continue
        for v in range(N):
            if v != u and REL[u, v] >= tau:
                nd = dcur + T[u][v]
                if nd < dist.get(v, 1e9):
                    dist[v], prev[v] = nd, u; heapq.heappush(pq, (nd, v))
    if b not in dist: return None, None
    path = [b]
    while path[-1] != a: path.append(prev[path[-1]])
    return dist[b], path[::-1]
def route_time(order, tau):
    """Visit the sites in 'order' starting and ending at H; repair each leg with reliable paths."""
    stops = [0] + list(order) + [0]
    total, rel, legs = 0.0, 1.0, []
    for a, b in zip(stops[:-1], stops[1:]):
        t, path = reliable_path(a, b, tau)
        if t is None: return 1e6, 0.0, None
        total += t; legs.append(path)
        for u, v in zip(path[:-1], path[1:]): rel *= REL[u, v]
    return round(total, 1), rel, legs