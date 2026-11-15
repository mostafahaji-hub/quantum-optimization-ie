"""Figure 10.11 - the four test circuits on four calibration snapshots."""
import json
import numpy as np
from figstyle import plt
fez = {'prepare 0': {'0': 991, '1': 9}, 'prepare 1': {'0': 14, '1': 986},
       'coin': {'0': 516, '1': 484}, 'bell': {'00': 496, '01': 15, '10': 13, '11': 476}}
dev = {'Fez': fez}
for k, v in json.load(open('snapshot_counts.json')).items():
    dev[k.replace('fake_', '').capitalize()] = v['counts']
ideal = {'prepare 0': {'0': 1000}, 'prepare 1': {'1': 1000},
         'coin': {'0': 500, '1': 500}, 'bell': {'00': 500, '11': 500}}
titles = {'prepare 0': 'Prepare 0', 'prepare 1': 'Prepare 1', 'coin': 'Coin', 'bell': 'Bell'}
shades = ['white', '0.75', '0.45', '0.15']; hatches = [None, None, '//', None]
fig, axs = plt.subplots(2, 2, figsize=(9, 6.2))
for ax, name in zip(axs.ravel(), ['prepare 0', 'prepare 1', 'coin', 'bell']):
    keys = ['0', '1'] if name != 'bell' else ['00', '01', '10', '11']
    w = 0.8 / len(dev); x = np.arange(len(keys))
    for i, (dname, c) in enumerate(dev.items()):
        ax.bar(x - 0.4 + w * (i + 0.5), [c[name].get(k, 0) for k in keys], width=w,
               color=shades[i], edgecolor='black', linewidth=1, hatch=hatches[i], label=dname)
    for j, k in enumerate(keys):
        v = ideal[name].get(k, 0)
        ax.plot([j - 0.42, j + 0.42], [v, v], 'k--', lw=1.2)
    ax.set_xticks(x); ax.set_xticklabels(keys); ax.set_ylim(0, 1100)
    ax.set_title(titles[name]); ax.set_ylabel('Counts (1000 Shots)')
axs[0, 0].legend(frameon=False, fontsize=9, loc='upper right')
fig.text(0.5, 0.005, 'Dashed Lines: Ideal Counts.  Bars: Calibration Snapshots, Optimization Level 1 (Physical Qubits 0 and 1).',
         ha='center', fontsize=9)
plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig('fig/fig10_11_snapshots.png', dpi=150)
print('saved')
