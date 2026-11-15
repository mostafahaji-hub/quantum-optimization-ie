"""Example 14.22 - one report for any counts file: raw results,
readout correction and post-selection, next to the ideal ones.
Usage: python ex13_report.py fez_counts.json
   or: python ex13_report.py real_counts.json"""
import sys, json
from tsp4 import setup, FEASIBLE, OPT
from fastsim import qaoa_probs
from mitigate import counts_to_probs, flip_rates, readout_correct
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))
name = sys.argv[1] if len(sys.argv) > 1 else 'fez_counts.json'
data = json.load(open(name))
print('file:', name, '| backend:', data.get('backend', 'FakeFez'))
print('p  version     P(opt)  P(feas)  P(opt|feas)  feas. length')
for p in ['1', '2', '3', '4']:
    d = data[p]
    e01, e10 = flip_rates([d['cal0'], d['cal1']], 9)
    raw = counts_to_probs(d['run'], 9)
    for tag, P in [('ideal', qaoa_probs(E, *angles[p])),
                   ('raw', raw),
                   ('corrected', readout_correct(raw, e01, e10))]:
        pf = P[FEASIBLE].sum()
        mean_len = (P * FEASIBLE) @ E / pf
        print(f'{p}  {tag:10s}  {P[OPT].sum():.4f}  {pf:.4f}'
              f'  {P[OPT].sum() / pf:11.3f}  {mean_len:12.2f}')
