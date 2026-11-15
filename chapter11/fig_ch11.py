"""Figures 11.1 - 11.5."""
import numpy as np
from math import factorial
from figstyle import plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from qubo import brute_force, energy
from shop_pos_qubo import shop_pos_qubo
from encode import bits_to_order
from qiskit_aer import AerSimulator
from uniform import uniform
from runner import run_counts, to_book

def box(ax, x, y, w, h, txt, fc='white', fs=11, lw=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, fc=fc, ec='black', lw=lw,
                 boxstyle='round,pad=0.02,rounding_size=0.08'))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center', fontsize=fs)

# 11.1 permutation matrix -> bit string (J3 J2 J1)
fig, ax = plt.subplots(figsize=(8.6, 3.6)); ax.axis('off')
ax.set_xlim(0, 13); ax.set_ylim(0.2, 5.2)
M = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
for j in range(3):
    ax.text(0.45, 3.9 - j, f'J{j+1}', ha='center', va='center', fontsize=11)
    for k in range(3):
        box(ax, 0.9 + k, 3.45 - j, 0.9, 0.9, str(M[j][k]),
            fc='0.3' if M[j][k] else 'white', fs=12)
        if M[j][k]:
            ax.texts[-1].set_color('white')
for k in range(3):
    ax.text(1.35 + k, 4.65, f'Pos {k+1}', ha='center', fontsize=10)
ax.annotate('', xy=(5.0, 3.0), xytext=(4.1, 3.0),
            arrowprops=dict(arrowstyle='-|>', lw=2, color='black'))
ax.text(4.55, 3.35, 'Read Row\nBy Row', ha='center', fontsize=9)
names = ['x11', 'x12', 'x13', 'x21', 'x22', 'x23', 'x31', 'x32', 'x33']
bits = '001010100'
for i in range(9):
    x = 5.2 + i * 0.85
    box(ax, x, 2.55, 0.75, 0.9, bits[i], fc='0.3' if bits[i] == '1' else 'white', fs=12)
    if bits[i] == '1':
        ax.texts[-1].set_color('white')
    ax.text(x + 0.375, 3.7, names[i], ha='center', fontsize=9)
    ax.text(x + 0.375, 2.2, f'q{i}', ha='center', fontsize=9)
ax.text(8.95, 1.35, 'Book Order: q0 Is The Leftmost Bit', ha='center', fontsize=10, style='italic')
ax.text(2.35, 0.75, 'Order J3 J2 J1\n(Rows: Jobs, Columns: Positions)', ha='center', fontsize=9.5)
fig.savefig('../fig/fig11_1_matrix.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# 11.2 book order vs Qiskit order (J3 J1 J2)
fig, ax = plt.subplots(figsize=(8.6, 3.0)); ax.axis('off')
ax.set_xlim(0, 10.5); ax.set_ylim(0, 3.6)
book = '010001100'
for i in range(9):
    x = 1.6 + i * 0.95
    box(ax, x, 2.3, 0.8, 0.8, book[i], fc='0.8' if i == 0 else 'white')
    ax.text(x + 0.4, 3.25, f'q{i}', ha='center', fontsize=9)
    j = 8 - i                                   # Qiskit prints q8 ... q0
    box(ax, x, 0.5, 0.8, 0.8, book[j], fc='0.8' if j == 0 else 'white')
    ax.text(x + 0.4, 0.15, f'q{j}', ha='center', fontsize=9)
ax.text(0.75, 2.7, 'Book', ha='center', fontsize=11, weight='bold')
ax.text(0.75, 0.9, 'Qiskit\nPrints', ha='center', fontsize=11, weight='bold')
ax.annotate('', xy=(1.6 + 8 * 0.95 + 0.4, 1.35), xytext=(2.0, 2.25),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='0.3'))
ax.text(6.0, 1.75, 'Same Qubits, Reversed Text', ha='center', fontsize=9.5, style='italic',
        bbox=dict(fc='white', ec='none'))
fig.savefig('../fig/fig11_2_order.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# 11.3 feasible fraction
ms = [3, 4, 5, 6, 7, 8]
frac = [factorial(m) / 2 ** (m * m) for m in ms]
fig, ax = plt.subplots(figsize=(6.0, 3.4))
ax.bar(range(len(ms)), frac, color='0.5', edgecolor='black', lw=1.2)
ax.set_yscale('log'); ax.set_xticks(range(len(ms)), [f'{m} Jobs\n{m*m} Qubits' for m in ms], fontsize=9)
for i, f in enumerate(frac):
    ax.text(i, f * 1.6, f'{f:.0e}', ha='center', fontsize=8.5)
ax.set_ylabel('Fraction Of Feasible Strings'); ax.set_ylim(1e-17, 1)
ax.set_title('Feasible Strings Become Needles In A Haystack')
fig.savefig('../fig/fig11_3_feasible.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)

# 11.4 energy landscape of the 512 strings
Q, c = shop_pos_qubo(lam=20)
X, E = brute_force(Q, c)
ok = np.array([bits_to_order(''.join(map(str, x))) is not None for x in X])
idx = np.argsort(E, kind='stable')
fig, ax = plt.subplots(figsize=(6.4, 3.5))
r = np.arange(512)
ax.scatter(r[~ok[idx]], E[idx][~ok[idx]], s=6, color='0.65', label='Infeasible (506)')
ax.scatter(r[ok[idx]], E[idx][ok[idx]], s=40, color='black', marker='D', label='Feasible Orders (6)')
ax.axhline(c + 0 if False else E.mean(), color='black', ls='--', lw=1)
ax.text(330, E.mean() + 12, f'Mean = {E.mean():.1f}', fontsize=9)
ax.set_xlabel('Rank Of String (Cheapest First)'); ax.set_ylabel('QUBO Value (Lambda = 20)')
ax.legend(edgecolor='black', fontsize=9, loc='upper left'); ax.set_title('All 512 Strings Of The Small Workshop')
fig.savefig('../fig/fig11_4_landscape.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
print('energy range', E.min(), E.max(), 'mean', E.mean())

# 11.5 energies of 1000 uniform samples
counts = run_counts([uniform(9)], AerSimulator(), 1000, seed=7)[0]
vals = []
for s, n in counts.items():
    vals += [energy(Q, [int(b) for b in to_book(s)], c)] * n
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.hist(vals, bins=np.arange(0, 541, 20), color='0.6', edgecolor='black')
ax.axvline(134.5, color='black', ls='--', lw=1.5); ax.text(140, ax.get_ylim()[1] * 0.9, 'Offset = 134.5', fontsize=9)
ax.axvline(5, color='black', lw=2.5); ax.text(14, ax.get_ylim()[1] * 0.55, 'Optimum = 5', fontsize=9)
ax.set_xlabel('QUBO Value Of The Sampled String'); ax.set_ylabel('Shots')
ax.set_title('Uniform Superposition, 1000 Shots, 9 Qubits')
fig.savefig('../fig/fig11_5_uniform.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close(fig)
print('sample mean', np.mean(vals), 'max', max(vals))
