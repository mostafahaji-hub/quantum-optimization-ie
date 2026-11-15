"""Example 14.20 - readout correction on the FakeFez counts."""
import json
from tsp4 import setup, FEASIBLE, OPT
from fastsim import qaoa_probs
from mitigate import counts_to_probs, flip_rates, readout_correct
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))
data = json.load(open('fez_counts.json'))    # from Example 14.13
print('p  version     P(opt)  P(feas)   <H>')
for p in ['1', '2', '3', '4']:
    d = data[p]
    e01, e10 = flip_rates([d['cal0'], d['cal1']], 9)
    raw = counts_to_probs(d['run'], 9)
    rows = [('ideal', qaoa_probs(E, *angles[p])), ('raw', raw),
            ('corrected', readout_correct(raw, e01, e10))]
    for name, P in rows:
        print(f'{p}  {name:10s}  {P[OPT].sum():.4f}  '
              f'{P[FEASIBLE].sum():.4f}  {P @ E:6.2f}')
