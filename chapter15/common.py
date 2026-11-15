"""Chapter 15 - one currency for every method."""
import math

def runs99(P):
    """Independent runs so that at least one hits w.p. 0.99."""
    if P >= 1:
        return 1
    if P <= 0:
        return math.inf
    return math.ceil(math.log(0.01) / math.log(1 - P))

def evals99(P, budget):
    """Total evaluations (or shots) for 99 percent:
    runs99 restarts, each with `budget` evaluations."""
    return budget * runs99(P)
