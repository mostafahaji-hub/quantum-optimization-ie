"""Example 14.17 - post-selection: keep only the feasible shots."""
import json
from tsp4 import setup, describe, FEASIBLE, OPT, BOOK
from fastsim import qaoa_probs
from mitigate import counts_to_probs
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))
data = json.load(open('fez_counts.json'))    # from Example 14.13

def keep_feasible(P):
    """Feasible part of a distribution, rescaled to a sum of 1."""
    return P * FEASIBLE / (P * FEASIBLE).sum()

print('p  kept shots  P(opt|feas): ideal noisy'
      '   mean length: ideal noisy')
for p in ['1', '2', '3', '4']:
    I = keep_feasible(qaoa_probs(E, *angles[p]))
    P = counts_to_probs(data[p]['run'], 9)
    kept = round((P * FEASIBLE).sum() * 10000)
    N = keep_feasible(P)
    print(f'{p}  {kept:10d}  {I[OPT].sum():18.3f}'
          f' {N[OPT].sum():5.3f}   {I @ E:17.2f} {N @ E:5.2f}')
P = counts_to_probs(data['4']['run'], 9)
print('p = 4, shots of each tour (out of 10000):')
for k in sorted(range(512), key=lambda k: E[k]):
    if FEASIBLE[k]:
        print(f'  {describe(BOOK[k]):11s} {round(P[k] * 10000):4d}')
