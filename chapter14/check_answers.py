"""Chapter 14 - numbers for the self-test and exercise answers."""
import json, math
import numpy as np
from scipy.optimize import minimize
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit_ibm_runtime.executor_sampler import Sampler
from tsp4 import setup, describe, length, BOOK, FEASIBLE, OPT, D
from qubo import energy
from qaoa import qaoa_circuit
from fastsim import qaoa_probs
from encode import bits_to_tour, tour_to_bits
from mitigate import counts_to_probs, flip_rates, readout_correct
Q, c, H, E = setup(lam=20)
ang = json.load(open('angles.json'))
data = json.load(open('fez_counts.json'))
fez = FakeFez()

print('14.1', energy(Q, [0] * 9, c),
      energy(Q, [int(b) for b in '001100010'], c))
print('14.2')
for t in ['ABCDA', 'ADCBA', 'ADBCA', 'ACBDA', 'ACDBA', 'ABDCA']:
    b = tour_to_bits(t[:-1])      # without the final A
    r = describe(b[::-1])
    print('  ', t, length(t), b, '-> reversed', b[::-1], r)
g1 = ang['1'][0][0]
print('14.3', [round(g1 * d, 3) for d in (1, 5, 22, 136)])
print('14.4', [m * (m - 1) * (2 * m - 1) for m in (3, 4, 5, 6)])
for lam in (10, 20, 40):
    Ql, cl, Hl, El = setup(lam)
    print('14.5/6 lam', lam, 'offset', Hl.coeffs[0].real,
          'mean', El.mean(), 'cheapest infeasible', El[~FEASIBLE].min())
r = minimize(lambda t: qaoa_probs(E, [t[0]], [t[1]]) @ E,
             [0.015, -0.4363], method='COBYLA',
             options={'rhobeg': 0.2, 'tol': 1e-4})
print(f'14.7 S=1: gamma {r.x[0]:.4f} beta {r.x[1]:.4f} '
      f'<H> {r.fun:.2f} evals {r.nfev}')
P = qaoa_probs(E, *ang['1'])
print('14.8', [(describe(BOOK[k]), round(P[k], 4))
               for k in np.argsort(E)[:6]],
      'cond', round(P[OPT].sum() / P[FEASIBLE].sum(), 3))
for n in (1000, 10000):
    print('14.9 n', n, round(math.sqrt(0.073 * 0.927 / n), 4))
print('14.10', round(0.997 ** 621, 3), round(0.995 ** 100, 3))
print('14.11', round(0.2 * 0.1708 + 0.8 * 2 / 512, 4))
print('14.12', round((0.30 - 0.01) / 0.95, 5),
      round((0.005 - 0.01) / 0.95, 5))
d = data['1']
e01, e10 = flip_rates([d['cal0'], d['cal1']], 9)
raw = counts_to_probs(d['run'], 9)
A = np.array([[1.0]])
for q in range(9):                     # q0 is the leftmost bit
    A = np.kron(A, np.array([[1 - e01[q], e10[q]],
                             [e01[q], 1 - e10[q]]]))
full = np.linalg.solve(A, raw)
fast = readout_correct(raw, e01, e10)
fc = np.clip(full, 0, None); fc /= fc.sum()
print('14.13 max diff', f'{np.abs(fc - fast).max():.1e}')
print('14.14 negative mass', round(-full[full < 0].sum(), 4),
      'negative entries', int((full < 0).sum()))
print('14.15', [round(1 - counts_to_probs(data[p]['run'], 9)
                      [FEASIBLE].sum(), 4) for p in '1234'])
for s in range(4):
    tour, left = [s], set(range(4)) - {s}
    while left:
        nxt = min(left, key=lambda j: D[tour[-1]][j])
        tour.append(nxt); left.remove(nxt)
    t = ''.join('ABCD'[i] for i in tour + [s])
    print('14.16 start', 'ABCD'[s], t, length(t))
for p in ('2', '3'):
    Pp = qaoa_probs(E, *ang[p])[OPT].sum()
    print('14.17 p', p, round(Pp, 4),
          math.ceil(math.log(0.01) / math.log(1 - Pp)))
qc = qaoa_circuit(H, *ang['1'], measure=True)
for lv in (1, 3):
    pm = generate_preset_pass_manager(optimization_level=lv,
                                      backend=fez, seed_transpiler=0)
    isa = pm.run(qc)
    print('14.18 level', lv, 'depth', isa.depth(), 'CZ',
          isa.count_ops().get('cz'))
Q10, c10, H10, E10 = setup(10)
S = 50
G = np.linspace(0, 0.2, 41); B = np.linspace(-np.pi / 2, np.pi / 2, 37)
M = np.array([[qaoa_probs(E10, [g], [b]) @ E10 for g in G] for b in B])
i, j = np.unravel_index(M.argmin(), M.shape)
r = minimize(lambda t: qaoa_probs(E10, [t[0] / S], [t[1]]) @ E10,
             [G[j] * S, B[i]], method='COBYLA',
             options={'rhobeg': 0.2, 'tol': 1e-4})
P10 = qaoa_probs(E10, [r.x[0] / S], [r.x[1]])
print(f'14.19 lam=10 grid ({G[j]:.3f},{B[i]:.4f}) {M[i, j]:.2f}; '
      f'cobyla gamma {r.x[0] / S:.4f} beta {r.x[1]:.4f} '
      f'<H> {r.fun:.2f} P(opt) {P10[OPT].sum():.4f} '
      f'P(feas) {P10[FEASIBLE].sum():.4f}')
czs = []
for sd in range(10):
    pm = generate_preset_pass_manager(optimization_level=1,
                                      backend=fez, seed_transpiler=sd)
    czs.append(pm.run(qc).count_ops().get('cz'))
print('14.20 CZ for seeds 0..9:', czs, 'min', min(czs), 'max', max(czs))
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)
isa = pm.run(qc)
for dd in (False, True):
    s = Sampler(mode=fez)
    s.options.simulator.seed_simulator = 7
    s.options.dynamical_decoupling.enable = dd
    cnt = s.run([isa], shots=10000).result()[0].join_data().get_counts()
    Pn = counts_to_probs(cnt, 9)
    print('14.22 DD', dd, round(Pn[OPT].sum(), 4),
          round(Pn[FEASIBLE].sum(), 4))
from qiskit_aer.noise import NoiseModel
print('14.22 instructions with noise in the FakeFez model:',
      sorted(NoiseModel.from_backend(fez).noise_instructions))
print('14.16 tie from D: c(D,A) =', D[3][0], ' c(D,B) =', D[3][1],
      ' choosing B gives DBACD', length('DBACD'))
