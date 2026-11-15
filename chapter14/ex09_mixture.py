"""Example 14.15 - a one-number noise model:
noisy = F * ideal + (1 - F) * uniform. Find F three ways."""
import json
from tsp4 import setup, FEASIBLE, OPT
from fastsim import qaoa_probs
from mitigate import counts_to_probs
import numpy as np
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))
data = json.load(open('fez_counts.json'))    # from Example 14.13
uni = {'P(opt)': 2 / 512, 'P(feas)': 6 / 512, '<H>': E.mean()}

def stats(P):
    return {'P(opt)': P[OPT].sum(), 'P(feas)': P[FEASIBLE].sum(),
            '<H>': P @ E}

ones = np.array([format(k, '09b').count('1') for k in range(512)])
print('p   F from P(opt)  F from P(feas)  F from <H>'
      '   mean number of 1s: ideal  noisy')
for p in ['1', '2', '3', '4']:
    ideal = stats(qaoa_probs(E, *angles[p]))
    noisy = stats(counts_to_probs(data[p]['run'], 9))
    F = [(noisy[k] - uni[k]) / (ideal[k] - uni[k]) for k in uni]
    w = [qaoa_probs(E, *angles[p]) @ ones,
         counts_to_probs(data[p]['run'], 9) @ ones]
    print(f'{p}   {F[0]:13.3f}  {F[1]:14.3f}  {F[2]:10.3f}'
          f'   {w[0]:26.2f}  {w[1]:5.2f}')
print('uniform: mean number of 1s = 4.5, <H> = 162.0')
