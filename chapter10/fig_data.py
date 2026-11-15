"""Figures 10.1, 10.3, 10.4, 10.8, 10.9, 10.10 (all numbers come from the example scripts)."""
import numpy as np
from figstyle import plt, bars
from matplotlib.patches import FancyBboxPatch
from qiskit_aer import AerSimulator
from circuits import coin
from runner import run_counts

# --- Figure 10.1: the workflow of the chapter
fig, ax = plt.subplots(figsize=(9.5, 3.0)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 3)
boxes = [(0.1, 'Write The\nCircuit\n(Qiskit)', 'white'), (2.1, 'Ideal\nSimulator\n(Aer)', '0.9'),
         (4.1, 'Translate\nFor Hardware\n(Transpile)', 'white'), (6.1, 'IBM QPU\nOr Fake\nBackend', '0.75'),
         (8.1, 'Counts And\nHistogram', 'white')]
for x, t, c in boxes:
    ax.add_patch(FancyBboxPatch((x, 0.8), 1.7, 1.4, boxstyle='round,pad=0.05,rounding_size=0.2',
                                fc=c, ec='black', lw=2.2))
    ax.text(x + 0.85, 1.5, t, ha='center', va='center', fontsize=10.5)
for x in [1.8, 3.8, 5.8, 7.8]:
    ax.annotate('', xy=(x + 0.3, 1.5), xytext=(x, 1.5), arrowprops=dict(arrowstyle='-|>', lw=2, color='black'))
ax.text(7.0, 0.35, 'Queue + Noise', ha='center', fontsize=10, style='italic')
ax.text(3.0, 0.35, 'Exact, Free, Instant', ha='center', fontsize=10, style='italic')
fig.savefig('../fig/fig10_1_workflow.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# --- Figure 10.3: histogram of 1000 shots of the coin (seed 1 of Example 10.4)
c = run_counts([coin()], AerSimulator(), shots=1000, seed=1)[0]
fig, ax = plt.subplots(figsize=(4.8, 3.2))
bars(ax, ['0', '1'], [c.get('0', 0), c.get('1', 0)])
ax.axhline(500, color='black', ls='--', lw=1); ax.text(1.35, 505, 'Ideal 500', fontsize=9, ha='right', va='bottom')
ax.set_xticks([0, 1], ['0', '1']); ax.set_ylim(0, 620)
ax.set_xlabel('Measured Bit'); ax.set_ylabel('Counts'); ax.set_title('Quantum Coin, 1000 Shots')
fig.savefig('../fig/fig10_3_coin_hist.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# --- Figure 10.4: fraction of zeros versus number of shots
shots = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
frac = [run_counts([coin()], AerSimulator(), shots=n, seed=3)[0].get('0', 0) / n for n in shots]
n = np.logspace(1, 4, 200); band = 2 * np.sqrt(0.25 / n)
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.fill_between(n, 0.5 - band, 0.5 + band, color='0.85', label='Ideal ± 2 Std. Dev.')
ax.plot(shots, frac, 'o-', color='black', lw=1.5, label='Simulated Fraction Of 0')
ax.axhline(0.5, color='black', ls='--', lw=1)
ax.set_xscale('log'); ax.set_ylim(0.15, 0.85); ax.set_xlabel('Number Of Shots'); ax.set_ylabel('Fraction Of 0')
ax.legend(frameon=True, edgecolor='black', fontsize=9); ax.set_title('More Shots, Smaller Statistical Error')
fig.savefig('../fig/fig10_4_shots.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
print('fig 10.4 data:', list(zip(shots, [round(f, 3) for f in frac])))

# --- Figure 10.8: Bell state, ideal vs FakeFez (numbers of Examples 10.9 and 10.12)
ideal = {'00': 492, '01': 0, '10': 0, '11': 508}
fake = {'00': 496, '01': 15, '10': 13, '11': 476}
lab = ['00', '01', '10', '11']
fig, ax = plt.subplots(figsize=(6.2, 3.4))
bars(ax, lab, [ideal[k] for k in lab], color='white', offset=-0.2, width=0.4, label='Ideal Simulator')
bars(ax, lab, [fake[k] for k in lab], color='0.45', offset=0.2, width=0.4, label='Fake IBM Backend (Noisy)')
ax.set_xticks(range(4), lab); ax.set_ylim(0, 600); ax.set_xlabel('Measured String (Qiskit Order)'); ax.set_ylabel('Counts')
ax.legend(edgecolor='black', fontsize=9); ax.set_title('Two Entangled Coins, 1000 Shots')
fig.savefig('../fig/fig10_8_bell_noise.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# --- Figure 10.9: GHZ success vs size (numbers of Example 10.13)
sizes = [2, 4, 6, 8, 10, 12]; good = [0.967, 0.942, 0.928, 0.869, 0.857, 0.849]
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.plot(sizes, good, 's-', color='black', lw=1.8, ms=7, mfc='0.6', label='Fake IBM Backend')
ax.axhline(1.0, color='black', ls='--', lw=1, label='Ideal (Always 1)')
ax.set_ylim(0.75, 1.03); ax.set_xticks(sizes); ax.set_xlabel('Number Of Entangled Coins (Qubits)')
ax.set_ylabel('Fraction All-0 Or All-1'); ax.legend(edgecolor='black', fontsize=9, loc='lower left')
ax.set_title('Bigger Circuits, More Noise')
fig.savefig('../fig/fig10_9_ghz.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# --- Figure 10.10: the 8-sided die (numbers of Example 10.18)
lab = ['000', '001', '010', '011', '100', '101', '110', '111']
val = [107, 137, 136, 121, 123, 127, 115, 134]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
for i, (l, v) in enumerate(zip(lab, val)):
    ax.bar(i, v, color='white' if i >= 6 else ('0.25' if i == 5 else '0.6'), edgecolor='black', lw=1.2,
           hatch='//' if i >= 6 else None)
    ax.text(i, v + 2, str(v), ha='center', fontsize=9)
names = ['J1J2J3', 'J1J3J2', 'J2J1J3', 'J2J3J1', 'J3J1J2', 'J3J2J1\n(Optimum)', 'Rejected', 'Rejected']
ax.set_xticks(range(8), [f'{l}\n{n}' for l, n in zip(lab, names)], fontsize=8.5)
ax.set_ylim(0, 165); ax.set_ylabel('Counts'); ax.set_title('Three Quantum Coins As A Random Job-Order Picker')
fig.savefig('../fig/fig10_10_die.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
print('ok')
