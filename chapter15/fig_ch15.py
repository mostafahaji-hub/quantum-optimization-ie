"""Figures of Chapter 15 (grey scale, English text, dpi 150)."""
import json, re
import numpy as np
from figstyle import plt
from matplotlib.patches import FancyBboxPatch
DPI = 150

# Fig 15.1 - one currency: evaluations for 99 percent (log scale)
h = json.load(open('head_to_head.json'))
LAB = ['Enumerate All Solutions', 'One Simple Rule', 'Best Of All Rules/Starts',
       'Random Order Or Tour', 'Random 9-Bit Strings', 'SA On The QUBO',
       'GA On The QUBO', 'QEA On The QUBO', 'KA On The QUBO',
       'QAOA p=1, Ideal', 'QAOA p=4, Ideal', 'QAOA p=4, FakeFez',
       'Grover, Table Oracle']
fig, axes = plt.subplots(1, 2, figsize=(11, 5.4), sharey=True)
for ax, prob, title in zip(axes, ['shop', 'tsp'],
                           ['Small Workshop', 'Small TSP']):
    vals = [v for _, v in h[prob]][::-1]
    ys = range(len(vals))
    for y, v, name in zip(ys, vals, LAB[::-1]):
        if v == 'never':
            ax.text(1.0, y, 'Never Optimal', va='center', fontsize=9,
                    style='italic')
            continue
        quantum = 'QAOA' in name or 'Grover' in name
        ax.barh(y, v, color='white' if quantum else '0.55',
                edgecolor='black', linewidth=1.2)
        ax.text(v * 1.08, y, str(v), va='center', fontsize=9)
    ax.set_xscale('log'); ax.set_xlim(0.8, 2e4)
    ax.set_title(title); ax.set_xlabel('Evaluations (Or Shots) For 99%')
    ax.set_yticks(list(ys)); ax.set_yticklabels(LAB[::-1], fontsize=9)
fig.text(0.5, 0.005, 'Grey = Classical, White = Quantum. QAOA Bars Exclude '
         'About 1.5 Million Tuning Shots.', ha='center', fontsize=9)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig('fig/fig15_1_currency.png', dpi=DPI); plt.close(fig)

# Fig 15.2 - chance of hitting the optimum vs budget
bt = json.load(open('budget_table.json')); B = [25, 50, 100, 200, 400]
styles = {'random': ('k', ':', 'o'), 'SA': ('k', '-', 's'),
          'GA': ('0.45', '-', '^'), 'QEA': ('0.45', '--', 'v'),
          'KA': ('k', '--', 'D')}
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
for ax, prob, title in zip(axes, ['shop', 'tsp'],
                           ['Small Workshop', 'Small TSP']):
    for a, (c, ls, mk) in styles.items():
        ax.plot(B, bt[f'{prob}/{a}']['P'], color=c, ls=ls, marker=mk,
                mfc='white', lw=1.6, label=a if a != 'random' else 'Random')
    ax.set_xscale('log'); ax.set_xticks(B); ax.set_xticklabels(B)
    ax.set_title(title); ax.set_xlabel('Budget Per Run (Evaluations)')
    ax.grid(alpha=0.3)
axes[0].set_ylabel('Chance One Run Finds The Optimum')
axes[1].legend(frameon=True, edgecolor='black')
fig.tight_layout(); fig.savefig('fig/fig15_2_budget.png', dpi=DPI)
plt.close(fig)

# Fig 15.3 - growth of the QAOA circuit with cities (safe layout)
rows = [l.split() for l in open('outputs/ex05_growth.txt')
        if re.match(r'^\s+\d', l)]
n = [int(r[0]) for r in rows]; cz = [int(r[6]) for r in rows]
ok = [float(r[7]) for r in rows]
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].bar(n, cz, color='0.55', edgecolor='black', linewidth=1.2)
for x, v in zip(n, cz):
    ax[0].text(x, v, str(v), ha='center', va='bottom', fontsize=9)
ax[0].set_xlabel('Cities'); ax[0].set_ylabel('CZ Gates (p = 1)')
ax[0].set_title('Two-Qubit Gates On FakeFez')
ax[1].semilogy(n, ok, 'k-o', mfc='white', lw=1.6)
for x, v in zip(n, ok):
    ax[1].text(x + 0.08, v * 1.6, f'{v:.0e}', fontsize=9)
ax[1].set_xlabel('Cities'); ax[1].set_ylabel('Chance Of No Gate Error')
ax[1].set_title('One Layer, Broken Couplers Avoided')
ax[1].grid(alpha=0.3, which='both')
fig.tight_layout(); fig.savefig('fig/fig15_3_growth.png', dpi=DPI)
plt.close(fig)

# Fig 15.4 - a decision map: which tool when?
fig, ax = plt.subplots(figsize=(10, 6.2)); ax.axis('off')
ax.set_xlim(0, 10); ax.set_ylim(0, 6.4)
def box(x, y, w, hgt, txt, fill='white'):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - hgt / 2), w, hgt,
                 boxstyle='round,pad=0.05,rounding_size=0.15',
                 fc=fill, ec='black', lw=2))
    ax.text(x, y, txt, ha='center', va='center', fontsize=10)
def arrow(x1, y1, x2, y2, txt=''):
    ax.annotate('', (x2, y2), (x1, y1),
                arrowprops=dict(arrowstyle='->', lw=1.6))
    if txt:
        ax.text((x1 + x2) / 2 + 0.1, (y1 + y2) / 2, txt, fontsize=9)
box(5, 5.8, 4.4, 0.7, 'An Industrial Problem', '0.85')
box(5, 4.6, 4.4, 0.7, 'Can We List All Solutions?')
box(1.8, 3.3, 2.8, 0.8, 'Enumerate\n(Exact, Done)')
box(5, 3.3, 3.2, 0.8, 'Is A Good Rule Known?\n(EDD, WSPT, Nearest)')
box(8.3, 3.3, 2.8, 0.8, 'Use The Rule\nAs A Start')
box(5, 1.9, 4.4, 0.8, 'Metaheuristic Or SA\n(Tune Fairly, Test Statistically)')
box(5, 0.6, 6.4, 0.8, 'Quantum (Grover, QAOA, Annealing): Today A '
    'Learning\nAnd Research Tool; Compare In The Same Currency', '0.85')
arrow(5, 5.45, 5, 4.95)
arrow(3.6, 4.4, 2.2, 3.7, 'Yes')
arrow(5, 4.25, 5, 3.7, 'No')
arrow(6.6, 3.3, 6.9, 3.3, 'Yes')
arrow(5, 2.9, 5, 2.3, 'No / Not Enough')
arrow(8.3, 2.9, 7.0, 2.2)
arrow(5, 1.5, 5, 1.0)
fig.savefig('fig/fig15_4_decision.png', dpi=DPI, bbox_inches='tight')
plt.close(fig)
print('figures 15.1-15.4 written')
