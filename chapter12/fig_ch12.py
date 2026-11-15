"""Figures 12.1 - 12.7 (black, greys and white).
Numbered in order of appearance in the chapter."""
import numpy as np
from math import factorial, ceil, log2
from figstyle import plt, bars
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeFez
from grover import oracle, diffuser, grover_circuit, p_success, best_k
from runner import run_counts, to_book
from compact import shop_table
B = [format(i, '03b') for i in range(8)]          # book strings
def save(fig, name):
    fig.savefig(f'fig/{name}.png', dpi=150, bbox_inches='tight',
                facecolor='white'); plt.close(fig)
def amps(qc):
    sv = Statevector(qc).data
    return [sv[int(b[::-1], 2)].real for b in B]

# 12.1 inversion about the mean
qc = QuantumCircuit(3); qc.h(range(3)); a0 = amps(qc)
qc.compose(oracle(['101'], 3), inplace=True); a1 = amps(qc)
qc.compose(diffuser(3), inplace=True); a2 = amps(qc)
fig, axs = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
titles = ['1. After H: All Equal', '2. Oracle Flips 101',
          '3. Diffuser: Reflect About Mean']
for ax, a, t in zip(axs, [a0, a1, a2], titles):
    col = ['0.2' if b == '101' else '0.75' for b in B]
    ax.bar(range(8), a, color=col, edgecolor='black', lw=1.2)
    ax.axhline(0, color='black', lw=1)
    ax.set_xticks(range(8)); ax.set_xticklabels(B, rotation=90)
    ax.set_title(t, fontsize=11)
    if a is a1:
        m = np.mean(a1)
        ax.axhline(m, color='black', ls='--', lw=1.5)
        ax.text(-0.4, 0.62, f'Dashed Line: Mean = {m:.3f}', fontsize=9)
axs[0].set_ylabel('Amplitude'); axs[0].set_ylim(-0.5, 1.0)
for x, v in [(5, a2[5]), (0, a2[0])]:
    axs[2].text(x, v + 0.03, f'{v:.3f}', ha='center', fontsize=9)
save(fig, 'fig12_1_mean')

# 12.2 the circuit (k = 1) with barriers between the blocks
qc = QuantumCircuit(3, 3); qc.h(range(3)); qc.barrier()
qc.compose(oracle(['101'], 3), inplace=True); qc.barrier()
d = diffuser(3); d.global_phase = 0
qc.compose(d, inplace=True); qc.barrier()
qc.measure(range(3), range(3))
style = {'name': 'bw', 'fontsize': 13, 'subfontsize': 9,
         'creglinecolor': '#555555'}
fig = qc.draw('mpl', style=style, scale=0.9, plot_barriers=True)
save(fig, 'fig12_3_circuit')

# 12.3 geometry: every round turns the state by 2*theta
th = np.arcsin(1 / np.sqrt(8))
fig, ax = plt.subplots(figsize=(5.6, 5.0)); ax.set_aspect('equal')
ax.annotate('', xy=(1.15, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='0.4'))
ax.annotate('', xy=(0, 1.15), xytext=(0, 0),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='0.4'))
ax.text(1.17, -0.06, 'Bad\n(7 Strings)', fontsize=10)
ax.text(-0.05, 1.18, 'Good (101)', fontsize=10)
for k, ls in zip(range(4), ['-', '-', '-', '--']):
    ang = (2 * k + 1) * th
    x, y = np.cos(ang), np.sin(ang)
    ax.annotate('', xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', lw=2.2,
                                color='black', ls=ls))
    ax.text(1.08 * x - (0.33 if x < 0 else 0), 1.08 * y,
            f'k={k}  P={np.sin(ang)**2:.3f}', fontsize=9.5)
t = np.linspace(0, np.pi, 100)
ax.plot(np.cos(t), np.sin(t), color='0.7', lw=1)
ax.set_xlim(-1.05, 1.5); ax.set_ylim(-0.15, 1.35); ax.axis('off')
ax.set_title('Each Round Turns The State By 2θ (θ = 20.7°)',
             fontsize=11)
save(fig, 'fig12_2_rotation')

# 12.4 success probability against k: theory and simulator
circs = [grover_circuit(['101'], 3, k) for k in range(5)]
cs = run_counts(circs, AerSimulator(), 1000, seed=12)
meas = [sum(n for s, n in c.items() if to_book(s) == '101') / 1000
        for c in cs]
fig, ax = plt.subplots(figsize=(6.6, 3.6))
bars(ax, [str(k) for k in range(5)], [round(m, 3) for m in meas],
     color='0.75', label='Simulator (1000 Shots)')
kk = np.linspace(0, 4, 200)
ax.plot(kk, np.sin((2 * kk + 1) * th) ** 2, 'k-', lw=1.8,
        label='Theory sin²((2k+1)θ)')
ax.axhline(1 / 8, color='black', ls=':', lw=1.5)
ax.text(4.35, 1 / 8 + 0.02, 'Random 1/8', fontsize=9, ha='right')
ax.set_xlabel('Grover Rounds k'); ax.set_ylabel('P(Optimal Order)')
ax.set_ylim(0, 1.3); ax.legend(loc='upper center', fontsize=9, ncol=2)
save(fig, 'fig12_4_rounds')

# 12.5 threshold oracles: probability of a marked string
Ms = range(1, 7)
pk = [p_success(M, 8, best_k(M, 8)) for M in Ms]
fig, ax = plt.subplots(figsize=(6.8, 3.6))
lab = [f'M={M}' for M in Ms]
bars(ax, lab, [round(M / 8, 3) for M in Ms], color='white',
     hatch='//', offset=-0.2, width=0.4, label='No Rounds (M/8)')
bars(ax, lab, [round(p, 3) for p in pk], color='0.45',
     offset=0.2, width=0.4, label='Best k Rounds')
ax.set_xticks(range(6)); ax.set_xticklabels(lab)
for i, M in enumerate(Ms):
    ax.text(i, -0.17, f'k={best_k(M, 8)}', ha='center', fontsize=9)
ax.set_ylim(0, 1.32); ax.set_ylabel('P(Marked String)')
ax.legend(loc='upper center', fontsize=9, ncol=2)
save(fig, 'fig12_5_threshold')

# 12.6 ideal versus noisy (FakeFez), shop, k = 2
tab = shop_table()
qc = grover_circuit(['101'], 3, 2)
ci = run_counts([qc], AerSimulator(), 1000, seed=7)[0]
cn = run_counts([qc], FakeFez(), 1000, seed=7)[0]
gi = [sum(n for s, n in ci.items() if to_book(s) == b) for b in B]
gn = [sum(n for s, n in cn.items() if to_book(s) == b) for b in B]
names = [tab[b][0] if b in tab else 'Unused' for b in B]
fig, ax = plt.subplots(figsize=(8.6, 3.8))
bars(ax, names, gi, color='0.75', offset=-0.2, width=0.4,
     label='Ideal Simulator')
bars(ax, names, gn, color='0.25', offset=0.2, width=0.4,
     label='FakeFez (Noisy)')
ax.set_xticks(range(8)); ax.set_xticklabels(
    [f'{b}\n{nm}' for b, nm in zip(B, names)], fontsize=8.5)
ax.set_ylabel('Shots (Of 1000)'); ax.set_ylim(0, 1100)
ax.legend(fontsize=9)
save(fig, 'fig12_6_noise')

# 12.7 scaling: n! evaluations versus Grover rounds
ns = list(range(3, 11))
F = [factorial(n) for n in ns]
K = [best_k(1, 2 ** ceil(log2(f))) for f in F]
fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.semilogy(ns, F, 'ks-', lw=1.8, ms=7, mfc='white',
            label='Check All Orders (n!)')
ax.semilogy(ns, K, 'ko-', lw=1.8, ms=7, mfc='0.3',
            label='Grover Rounds (Best k)')
ax.set_xlabel('Number Of Orders n'); ax.set_ylabel('Count (Log Scale)')
ax.grid(True, which='major', color='0.85'); ax.legend(fontsize=9)
save(fig, 'fig12_7_scaling')
print('ok')
