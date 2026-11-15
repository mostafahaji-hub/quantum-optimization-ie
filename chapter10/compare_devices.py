"""Chapter 10 - ideal vs four calibration snapshots (Sec. 10.10)."""
import json
from scipy.stats import binomtest
from metrics import probs, tvd
ideal = {'prepare 0': {'0': 1.0}, 'prepare 1': {'1': 1.0},
         'coin': {'0': 0.5, '1': 0.5},
         'bell': {'00': 0.5, '11': 0.5}}
fez = {'prepare 0': {'0': 991, '1': 9},          # Example 10.19
       'prepare 1': {'0': 14, '1': 986},
       'coin': {'0': 516, '1': 484},
       'bell': {'00': 496, '01': 15, '10': 13, '11': 476}}
devices = {'fake_fez': {'date': '2025-02-26', 'counts': fez}}
devices.update(json.load(open('snapshot_counts.json')))  # from snapshot_hw.py
short = [d.replace('fake_', '') for d in devices]
print('TVD from ideal ' + ''.join(f'{s:>11s}' for s in short))
for name in ideal:
    row = [tvd(ideal[name], probs(d['counts'][name])) for d in devices.values()]
    print(f'{name:14s} ' + ''.join(f'{v:11.3f}' for v in row))
pv = [binomtest(d['counts']['coin'].get('0', 0), 1000, 0.5).pvalue
      for d in devices.values()]
print(f'{"coin p-value":14s} ' + ''.join(f'{v:11.3f}' for v in pv))
