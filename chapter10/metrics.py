"""Chapter 10 - comparing two histograms."""
import numpy as np

def probs(counts):
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}

def tvd(p, q):
    """Total variation distance: 0 = same, 1 = disjoint."""
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0) - q.get(k, 0))
                     for k in keys)

def hellinger_fid(p, q):
    """(sum of sqrt(p*q))^2 : 1 = same, 0 = disjoint."""
    keys = set(p) | set(q)
    s = sum(np.sqrt(p.get(k, 0) * q.get(k, 0)) for k in keys)
    return s ** 2
