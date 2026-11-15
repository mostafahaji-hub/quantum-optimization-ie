"""Figures 14.1 - 14.7 (black, greys and white).
Run ex03, ex06, ex08, ex15, ex16 first (their files and outputs)."""
import json
import numpy as np
from matplotlib.patches import FancyBboxPatch
from figstyle import plt
from qiskit_aer import AerSimulator
from tsp4 import setup, describe, FEASIBLE, OPT
from qaoa import qaoa_circuit
from fastsim import qaoa_probs
from runner import run_counts, to_book
from mitigate import counts_to_probs, flip_rates, readout_correct

def save(fig, name):
    fig.savefig(f'fig/{name}.png', dpi=150, bbox_inches='tight',
                facecolor='white'); plt.close(fig)

def box(ax, x, y, w, h, txt, fc='white', fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, fc=fc, ec='black',
                 lw=2.2, boxstyle='round,pad=0.02,rounding_size=0.12'))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center',
            fontsize=fs)

def arrow(ax, x0, y0, x1, y1, txt=None):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', lw=1.8, color='black'))
    if txt:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.12, txt,
                ha='center', va='bottom', fontsize=9)

Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))
data = json.load(open('fez_counts.json'))

# 14.1 the path from circuit to report
fig, ax = plt.subplots(figsize=(10.0, 4.2)); ax.axis('off')
box(ax, 0.0, 2.3, 1.6, 1.0, 'QAOA Circuit\n(Tuned On\nSimulator)')
box(ax, 2.1, 2.3, 1.7, 1.0, 'Transpile\nFor The QPU\n(CZ, SX, RZ)', '0.85')
box(ax, 4.3, 3.0, 1.9, 0.8, 'Ideal Simulator\n(No Noise)')
box(ax, 4.3, 2.0, 1.9, 0.8, 'FakeFez\n(Noise Model)', '0.85')
box(ax, 4.3, 1.0, 1.9, 0.8, 'Real IBM QPU\n(Your Account)', '0.65')
box(ax, 6.8, 2.3, 1.4, 1.0, 'Counts\n(Shots)')
box(ax, 6.2, 0.0, 2.6, 0.75, 'Calibration Circuits\nAll 0, All 1', '0.85')
box(ax, 8.8, 2.2, 2.3, 1.2, 'Mitigation\nReadout Correction\nPost-Selection', '0.85', fs=9.5)
box(ax, 8.95, 0.6, 2.0, 0.9, 'Report\nP(opt), P(feas)')
arrow(ax, 1.6, 2.8, 2.1, 2.8); arrow(ax, 3.8, 2.8, 4.3, 3.4)
arrow(ax, 3.8, 2.8, 4.3, 2.4); arrow(ax, 3.8, 2.8, 4.3, 1.4)
for y in [3.4, 2.4, 1.4]:
    arrow(ax, 6.2, y, 6.8, 2.8)
arrow(ax, 8.2, 2.8, 8.8, 2.8); arrow(ax, 7.5, 0.75, 9.0, 2.3)
arrow(ax, 9.95, 2.2, 9.95, 1.5)
ax.set_xlim(-0.1, 11.2); ax.set_ylim(-0.1, 4.0)
save(fig, 'fig14_1_pipeline')

# 14.2 heat map (fine grid of Example 14.7)
z = np.load('heatmap.npz'); G, B, M = z['G'], z['B'], z['M']
fig, ax = plt.subplots(figsize=(6.4, 4.6))
im = ax.imshow(M, origin='lower', aspect='auto', cmap='gray',
               extent=[G[0], G[-1], B[0], B[-1]])
i, j = np.unravel_index(M.argmin(), M.shape)
ax.plot(G[j], B[i], 'o', ms=11, mfc='white', mec='black', mew=2)
ax.plot(0.0144, -0.4264, 'x', ms=11, color='black', mew=2.5)
ax.set_xlabel('γ'); ax.set_ylabel('β (rad)')
ax.set_title('Expected Cost <H> Of The Small TSP (p = 1)')
fig.colorbar(im, ax=ax, label='<H>')
save(fig, 'fig14_2_heatmap')

# 14.3 the ten most frequent strings (Example 14.9)
qc = qaoa_circuit(H, [0.0144], [-0.4264], measure=True)
counts = run_counts([qc], AerSimulator(), 1000, seed=7)[0]
top = sorted(counts.items(), key=lambda kv: -kv[1])[:10]
fig, ax = plt.subplots(figsize=(9.0, 4.0))
for r, (s, n) in enumerate(top):
    d = describe(to_book(s))
    ax.bar(r, n, color='black' if d != 'infeasible' else '0.8',
           edgecolor='black', lw=1.2)
    ax.text(r, n + 0.4, str(n), ha='center', fontsize=9)
lab = [f'{to_book(s)}\n' + ('Infeasible' if describe(to_book(s))
       == 'infeasible' else describe(to_book(s))) for s, _ in top]
ax.set_xticks(range(10)); ax.set_xticklabels(lab, fontsize=7.5)
ax.set_ylabel('Shots (Of 1000)')
ax.set_title('Ten Most Frequent Strings, p = 1 (Black = A Real Tour)')
save(fig, 'fig14_3_top10')

# 14.4 layers: ideal versus FakeFez
ps = ['1', '2', '3', '4']
ideal = [qaoa_probs(E, *angles[p]) for p in ps]
noisy = [counts_to_probs(data[p]['run'], 9) for p in ps]
fig, axs = plt.subplots(1, 3, figsize=(11.0, 3.6))
for ax, (title, f) in zip(axs, [
        ('P(Optimal Tour)', lambda P: P[OPT].sum()),
        ('P(Feasible)', lambda P: P[FEASIBLE].sum()),
        ('Expected Cost <H>', lambda P: P @ E)]):
    x = np.arange(1, 5)
    ax.bar(x - 0.18, [f(P) for P in ideal], 0.36, color='0.8',
           edgecolor='black', lw=1.2, label='Ideal')
    ax.bar(x + 0.18, [f(P) for P in noisy], 0.36, color='0.25',
           edgecolor='black', lw=1.2, label='FakeFez')
    ax.set_xticks(x); ax.set_xlabel('Layers p'); ax.set_title(title)
axs[0].legend(frameon=True, edgecolor='black')
fig.tight_layout(); save(fig, 'fig14_4_layers')

# 14.5 readout errors of one qubit
fig, ax = plt.subplots(figsize=(7.2, 3.4)); ax.axis('off')
box(ax, 0.0, 2.0, 1.6, 0.9, 'Qubit Was |0⟩'); box(ax, 0.0, 0.0, 1.6, 0.9, 'Qubit Was |1⟩')
box(ax, 4.6, 2.0, 1.6, 0.9, 'We Read 0', '0.85')
box(ax, 4.6, 0.0, 1.6, 0.9, 'We Read 1', '0.85')
arrow(ax, 1.6, 2.45, 4.6, 2.45, '1 - e01')
arrow(ax, 1.6, 0.45, 4.6, 0.45, '1 - e10')
arrow(ax, 1.6, 2.2, 4.6, 0.7)
arrow(ax, 1.6, 0.7, 4.6, 2.2)
ax.text(2.45, 1.95, 'e01', fontsize=10, ha='left')
ax.text(1.75, 0.95, 'e10', fontsize=10, ha='left')
ax.set_xlim(-0.1, 6.3); ax.set_ylim(-0.1, 3.0)
save(fig, 'fig14_5_readout')

# 14.6 how much do the two mitigation tools bring back?
fig, axs = plt.subplots(1, 2, figsize=(10.0, 3.7))
corr = []
for p in ps:
    d = data[p]
    e01, e10 = flip_rates([d['cal0'], d['cal1']], 9)
    corr.append(readout_correct(counts_to_probs(d['run'], 9), e01, e10))
x = np.arange(1, 5)
for k, (lab, Ps, fc) in enumerate([('Ideal', ideal, '0.85'),
                                   ('Raw FakeFez', noisy, '0.25'),
                                   ('Readout Corrected', corr, '0.55')]):
    axs[0].bar(x + (k - 1) * 0.26, [P[FEASIBLE].sum() for P in Ps],
               0.26, color=fc, edgecolor='black', lw=1.2, label=lab)
    axs[1].bar(x + (k - 1) * 0.26,
               [P[OPT].sum() / P[FEASIBLE].sum() for P in Ps],
               0.26, color=fc, edgecolor='black', lw=1.2, label=lab)
axs[0].set_title('P(Feasible)')
axs[1].set_title('P(Optimal | Feasible) After Post-Selection')
axs[1].axhline(1 / 3, color='black', ls='--', lw=1.2)
axs[1].text(0.6, 0.43, 'Dashed Line: Random Tour (1/3)', ha='left', fontsize=9)
axs[1].set_ylim(0, 0.47)
for ax in axs:
    ax.set_xticks(x); ax.set_xlabel('Layers p')
axs[0].legend(frameon=True, edgecolor='black', fontsize=9)
fig.tight_layout(); save(fig, 'fig14_6_mitigation')

# 14.7 four processor snapshots (Example 14.23)
rows = [l.split() for l in open('outputs/ex16_snapshots.txt')][1:]
fig, axs = plt.subplots(1, 2, figsize=(10.0, 3.8))
styles = {'Fez': ('o', 'white'), 'Marrakesh': ('s', '0.7'),
          'Kingston': ('^', 'black'), 'Torino': ('D', '0.4')}
x = np.arange(1, 5)
axs[0].plot(x, [P[FEASIBLE].sum() for P in ideal], '--', color='black',
            lw=1.5, label='Ideal')
axs[1].plot(x, [P[OPT].sum() for P in ideal], '--', color='black',
            lw=1.5, label='Ideal')
for name, (mk, fc) in styles.items():
    r = [row for row in rows if row[0] == name]
    lab = 'Fake' + name
    axs[0].plot(x, [float(v[7]) for v in r], marker=mk, mfc=fc,
                color='black', lw=1.6, ms=8, mew=1.5, label=lab)
    axs[1].plot(x, [float(v[5]) for v in r], marker=mk, mfc=fc,
                color='black', lw=1.6, ms=8, mew=1.5, label=lab)
axs[0].set_title('P(Feasible), Raw'); axs[1].set_title('P(Optimal Tour), Raw')
for ax in axs:
    ax.set_xticks(x); ax.set_xlabel('Layers p')
axs[0].legend(frameon=True, edgecolor='black', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig14_7_snapshots')

# 14.8 growth (Example 14.26)
rows = [l.split() for l in open('outputs/ex15_growth.txt')][1:]
n = [int(r[0]) for r in rows]; cz = [int(r[3]) for r in rows]
share = [float(r[5]) for r in rows]
fig, axs = plt.subplots(1, 2, figsize=(10.0, 3.6))
axs[0].plot(n, cz, 'o-', color='black', lw=2, ms=8, mfc='white', mew=2)
for a, b in zip(n, cz):
    axs[0].text(a, b + 60, str(b), ha='center', fontsize=9)
axs[0].set_title('CZ Gates In One Layer (FakeFez)'); axs[0].set_ylim(0, 2600)
axs[1].semilogy(n, share, 's-', color='black', lw=2, ms=8,
                mfc='0.7', mew=2)
axs[1].set_title('Share Of Feasible Strings')
for ax in axs:
    ax.set_xticks(n); ax.set_xlabel('Number Of Cities')
fig.tight_layout(); save(fig, 'fig14_8_growth')
print('figures saved')
