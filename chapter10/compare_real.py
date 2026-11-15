"""Chapter 10 - ideal vs fake backend vs real QPU (Sec. 10.10)."""
import json
from scipy.stats import binomtest
from metrics import probs, tvd, hellinger_fid
ideal = {'prepare 0': {'0': 1.0}, 'prepare 1': {'1': 1.0},
         'coin': {'0': 0.5, '1': 0.5},
         'bell': {'00': 0.5, '11': 0.5}}
fake = {'prepare 0': {'0': 991, '1': 9},      # Example 10.19
        'prepare 1': {'0': 14, '1': 986},
        'coin': {'0': 516, '1': 484},
        'bell': {'00': 496, '01': 15, '10': 13, '11': 476}}
try:
    data = json.load(open('real_counts.json'))
    real = data['counts']
    print('real QPU:', data['backend'], data['date'])
except FileNotFoundError:
    real = None
    print('no real_counts.json: fake backend only')
for name in ideal:
    f_tvd = tvd(ideal[name], probs(fake[name]))
    row = f'{name:10s} fake TVD {f_tvd:.3f}'
    if real:
        p = probs(real[name])
        row += (f' | real TVD {tvd(ideal[name], p):.3f}'
                f' fid {hellinger_fid(ideal[name], p):.3f}')
    print(row)
if real:
    z = real['coin'].get('0', 0)
    pv = binomtest(z, 1000, 0.5).pvalue
    print(f'real coin: {z} zeros, binomial p = {pv:.4f}')
