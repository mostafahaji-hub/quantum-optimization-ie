"""Figures 13.1 - 13.7 (black, greys and white).
Run ex07, ex08, ex10 first (heatmap.npz, trace.txt, angles.json)."""
import json
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from figstyle import plt, bars
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeFez
from machine2 import machine_qubo
from qubo import energy
from ham import qubo_to_pauli
from qaoa import qaoa_circuit
from fastsim import qaoa_probs
from shop9 import setup, describe, FEASIBLE, OPT
from runner import run_counts, to_book

def save(fig, name):
    fig.savefig(f'fig/{name}.png', dpi=150, bbox_inches='tight',
                facecolor='white'); plt.close(fig)

# 13.2 clock hands: the cost layer turns each arrow by -gamma*f(x)
Q, c = machine_qubo(); g = 0.1
S2 = ['00', '10', '01', '11']
F = [energy(Q, [int(b) for b in s], c) for s in S2]
fig, axs = plt.subplots(2, 4, figsize=(9.0, 4.8))
for row, title in enumerate(['Before The Cost Layer',
                             'After The Cost Layer (γ = 0.1)']):
    for col, (s, f) in enumerate(zip(S2, F)):
        ax = axs[row, col]; ax.set_aspect('equal'); ax.axis('off')
        ax.add_patch(Circle((0, 0), 1, fill=False, lw=1.2, ec='0.6'))
        ang = 0 if row == 0 else -g * f
        ax.annotate('', xy=(np.cos(ang), np.sin(ang)), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='-|>', lw=2.4,
                                    color='black'))
        ax.plot([0, 1], [0, 0], color='0.75', lw=1, ls=':')
        lab = f'{s}   f = {f:.0f}'
        if row == 1:
            lab += f'\nTurn {-g * f:+.1f} rad'
        ax.text(0, -1.45, lab, ha='center', va='top', fontsize=10)
        ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.9, 1.25)
    axs[row, 0].text(-1.6, 1.45, title, fontsize=11.5,
                     fontweight='bold')
save(fig, 'fig13_2_arrows')

# 13.1 the QAOA loop: quantum circuit + classical optimizer
fig, ax = plt.subplots(figsize=(9.6, 3.9)); ax.axis('off')
def box(x, y, w, h, txt, fc='white'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, fc=fc, ec='black',
                 lw=2.2, boxstyle='round,pad=0.02,rounding_size=0.12'))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center',
            fontsize=10)
def arrow(x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', lw=1.8, color='black'))
box(0.0, 2.0, 1.5, 1.0, 'Start\nH On Every\nQubit')
box(2.0, 2.0, 1.7, 1.0, 'Cost Layer\nexp(-iγH)\nPhase By Cost', '0.85')
box(4.2, 2.0, 1.7, 1.0, 'Mixer Layer\nexp(-iβX)\nOn Every Qubit', '0.85')
box(6.4, 2.0, 1.5, 1.0, 'Measure\nMany Shots')
box(3.0, 0.0, 2.6, 0.9, 'Classical Optimizer\n(Grid, Then COBYLA)')
for x0, x1 in [(1.5, 2.0), (3.7, 4.2), (5.9, 6.4)]:
    arrow(x0, 2.5, x1, 2.5)
ax.add_patch(FancyBboxPatch((1.85, 1.8), 4.2, 1.45, fc='none',
             ec='0.4', lw=1.5, ls='--',
             boxstyle='round,pad=0.02,rounding_size=0.1'))
ax.text(3.95, 3.38, 'Repeat p Times (Layers)', ha='center', fontsize=10)
arrow(7.15, 2.0, 5.6, 0.6)
ax.text(7.1, 1.1, 'Average Cost\n<H>', fontsize=9.5)
arrow(3.6, 0.9, 3.6, 1.78)
ax.text(2.2, 1.25, 'New γ, β', fontsize=9.5)
ax.set_xlim(-0.2, 8.3); ax.set_ylim(-0.2, 3.6)
save(fig, 'fig13_1_loop')

# 13.3 the two-qubit QAOA circuit, p = 1
H2 = qubo_to_pauli(Q, c)
qc = qaoa_circuit(H2, [0.1], [-0.3], measure=True)
style = {'name': 'bw', 'fontsize': 13, 'subfontsize': 9,
         'creglinecolor': '#555555'}
fig = qc.draw('mpl', style=style, scale=0.9, plot_barriers=False)
save(fig, 'fig13_3_circuit')

# 13.4 heat map of <H> for the 9-qubit workshop
z = np.load('heatmap.npz'); M, gg, bb = z['M'], z['g'], z['b']
fig, ax = plt.subplots(figsize=(6.4, 4.4))
im = ax.imshow(M, origin='lower', aspect='auto', cmap='gray',
               extent=[gg[0], gg[-1], bb[0], bb[-1]])
cb = fig.colorbar(im, ax=ax); cb.set_label('Expected Cost <H>')
ax.plot(0.0160, -0.4123, marker='*', ms=16, mfc='white', mec='black')
ax.text(0.019, -0.62, 'Best: <H> = 56.3', fontsize=9.5, color='white')
ax.axhline(0, color='0.6', lw=0.8, ls=':')
ax.set_xlabel('Gamma γ'); ax.set_ylabel('Beta β (Radians)')
ax.set_title('Uniform Start: <H> = 134.5', fontsize=10.5)
save(fig, 'fig13_4_heatmap')

# 13.5 what the optimizer sees (COBYLA from the best grid point)
tr = np.loadtxt('trace.txt')
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(range(1, len(tr) + 1), tr, 'o-', color='0.5', mfc='white',
        mec='black', lw=1.2, ms=5, label='Value Asked For')
ax.plot(range(1, len(tr) + 1), np.minimum.accumulate(tr), 'k-',
        lw=2.2, label='Best So Far')
ax.set_xlabel('Evaluation Number'); ax.set_ylabel('Expected Cost <H>')
ax.legend(fontsize=9); ax.grid(True, color='0.88')
save(fig, 'fig13_5_cobyla')

# 13.6 the ten most frequent strings in 1000 shots (p = 1)
Q9, c9, H9, E9 = setup(20)
qc = qaoa_circuit(H9, [0.0160], [-0.4123], measure=True)
cnt = run_counts([qc], AerSimulator(), 1000, seed=7)[0]
top = sorted(cnt.items(), key=lambda kv: -kv[1])[:10]
labs, vals, cols = [], [], []
for s, n in top:
    bk = to_book(s); dsc = describe(bk)
    name = 'Infeasible' if dsc == 'infeasible' else dsc.split()[0]
    labs.append(f'{bk[:3]} {bk[3:6]} {bk[6:]}\n{name}')
    vals.append(n)
    cols.append('0.15' if bk == '001010100' else
                ('0.6' if dsc != 'infeasible' else 'white'))
fig, ax = plt.subplots(figsize=(9.4, 3.9))
ax.bar(range(10), vals, color=cols, edgecolor='black', lw=1.2)
for i, v in enumerate(vals):
    ax.text(i, v + 0.4, str(v), ha='center', fontsize=9)
ax.set_xticks(range(10)); ax.set_xticklabels(labs, fontsize=7.8)
ax.set_ylabel('Shots (Of 1000)'); ax.set_ylim(0, 34)
ax.set_title('Black: Optimal Order   Grey: Other Orders   '
             'White: Infeasible', fontsize=10)
save(fig, 'fig13_6_top10')

# 13.7 more layers: ideal simulator versus FakeFez
ang = json.load(open('angles.json'))
fez = FakeFez(); io, iff, no, nf = [], [], [], []
for p in ['1', '2', '3', '4']:
    gp, bp = ang[p]
    pr = qaoa_probs(E9, gp, bp)
    io.append(round(pr[OPT], 3)); iff.append(round(pr[FEASIBLE].sum(), 3))
    cn = run_counts([qaoa_circuit(H9, gp, bp, measure=True)], fez,
                    1000, seed=7)[0]
    no.append(cn.get('001010100', 0) / 1000)
    nf.append(sum(n for s, n in cn.items()
                  if describe(to_book(s)) != 'infeasible') / 1000)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.7))
L = ['p=1', 'p=2', 'p=3', 'p=4']
for ax, a, b, t, top_ in [(axs[0], io, no, 'P(Optimal Order)', 0.16),
                          (axs[1], iff, nf, 'P(Feasible)', 0.8)]:
    bars(ax, L, a, color='0.8', offset=-0.2, width=0.4,
         label='Ideal Simulator')
    bars(ax, L, b, color='0.25', offset=0.2, width=0.4,
         label='FakeFez (Noisy)')
    ax.set_xticks(range(4)); ax.set_xticklabels(L)
    ax.set_ylabel(t); ax.set_ylim(0, top_); ax.legend(fontsize=8.5)
save(fig, 'fig13_7_layers')
print('ok')
