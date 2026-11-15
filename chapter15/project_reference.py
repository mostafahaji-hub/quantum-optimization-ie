"""Reference numbers for the final project (answers file only)."""
import json
import numpy as np
from scipy.optimize import minimize
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from qubo import energy
from sa import sa_qubo
from bin_algs import random_bin, GA_bin, QEA_bin, KA_bin
from tsp5 import setup, feasible_mask, length
from fastsim import qaoa_probs
from qaoa import interp, qaoa_circuit
from ham import qubo_to_pauli
from runner import run_counts
from mitigate import counts_to_probs
from common import runs99, evals99
Q, c, X, E = setup(lam=10)
feas = feasible_mask(X); best = E[feas].min(); opt = np.isclose(E, best)
f = lambda x: energy(Q, x, c)
import sys
stage = sys.argv[1]
if stage == 'classical':
    algs = {'random': lambda B, s: random_bin(f, 16, B, s)[0],
            'SA': lambda B, s: sa_qubo(Q, c, B, s, T0=10, T_end=1.0)[0],
            'GA': lambda B, s: GA_bin(f, 16, B, s)[0],
            'QEA': lambda B, s: QEA_bin(f, 16, B, s)[0],
            'KA': lambda B, s: KA_bin(f, 16, B, s)[0]}
    BUD, RUNS = [100, 200, 400, 800, 1600], 500
    for name, run in algs.items():
        P = [np.mean([np.isclose(run(B, s), best) for s in range(RUNS)])
             for B in BUD]
        e = [evals99(p, b) for p, b in zip(P, BUD)]
        print(f'{name:6s} P {np.round(P, 3)} best evals99 {min(e)}')
if stage.startswith('p'):
    S = 50
    try:
        angles = {int(k): v for k, v in json.load(open('angles_tsp5.json')).items()}
    except FileNotFoundError:
        angles = {1: ([0.0185], [-0.4890])}
    for p in (int(stage[1]),):
        g0, b0 = angles[p] if p == 1 else (interp(angles[p - 1][0]),
                                            interp(angles[p - 1][1]))
        obj = lambda t: qaoa_probs(E, list(t[:p] / S), list(t[p:])) @ E
        r = minimize(obj, np.r_[np.array(g0) * S, b0], method='COBYLA',
                     options={'rhobeg': 0.2, 'tol': 1e-4, 'maxiter': 2000})
        g, b = list(r.x[:p] / S), list(r.x[p:])
        angles[p] = (g, b)
        P = qaoa_probs(E, g, b)
        print(f'p={p} <H> {r.fun:.2f} P(opt) {P[opt].sum():.4f} '
              f'P(feas) {P[feas].sum():.4f} shots99 {runs99(P[opt].sum())}')
        json.dump(angles, open('angles_tsp5.json', 'w'))
if stage == 'fez':
    angles = {int(k): v for k, v in json.load(open('angles_tsp5.json')).items()}
    H = qubo_to_pauli(Q, c)
    fez = FakeFez()
    pm = generate_preset_pass_manager(optimization_level=1, backend=fez,
                                      seed_transpiler=0)
    isa = pm.run(qaoa_circuit(H, *angles[1], measure=True))
    shots = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    cnt = run_counts([isa], fez, shots, 7)[0]
    Pn = counts_to_probs(cnt, 16)
    print('FakeFez p=1 shots', shots, 'CZ', isa.count_ops()['cz'], 'P(opt)',
          round(Pn[opt].sum(), 4), 'P(feas)', round(Pn[feas].sum(), 4))
