"""Chapter 13 - numerical check of the answers in answers_ch13.md."""
import json, warnings; warnings.filterwarnings('ignore')
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Operator, Statevector
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from qubo import to_ising, energy, brute_force
from machine2 import machine_qubo
from supplier import supplier_qubo
from ham import qubo_to_pauli
from qaoa import qaoa_circuit, book_probs, expected_cost, interp
from fastsim import qaoa_probs
from shop9 import setup, describe, FEASIBLE, OPT, BOOK
from runner import run_counts, to_book
pr = lambda *a: print(*a)
# ST / Ex1: f = 2x, P(1) = (1 + sin2b sin2g)/2
H1 = SparsePauliOp(['I', 'Z'], [1.0, -1.0])
for g, b in [(np.pi / 4, -np.pi / 4), (3 * np.pi / 4, np.pi / 4), (0.3, 0.2)]:
    pr('Ex1', round(g, 4), round(b, 4), round(book_probs(H1, [g], [b]).get('1', 0), 4),
       round(0.5 * (1 + np.sin(2 * b) * np.sin(2 * g)), 4))
# Ex2: f = 3x at gamma = pi/6, beta = -pi/4
H3 = SparsePauliOp(['I', 'Z'], [1.5, -1.5])
pr('Ex2', round(book_probs(H3, [np.pi / 6], [-np.pi / 4]).get('1', 0), 6))
# Ex3: machine phases at gamma = 0.2
Q, c = machine_qubo()
pr('Ex3', {s: round(-0.2 * energy(Q, [int(t) for t in s], c), 2) for s in ['00', '10', '01', '11']})
# Ex4: machine with lambda = 6
h, J, off = to_ising(*machine_qubo(6))
pr('Ex4 h', h, 'J', J[0, 1], 'off', off,
   {s: energy(*machine_qubo(6)[:1], [int(t) for t in s], machine_qubo(6)[1]) for s in ['00', '10', '01', '11']})
# Ex5: RZZ(theta) diagonal
qc = QuantumCircuit(2); qc.rzz(1.0, 0, 1)
pr('Ex5', np.round(np.angle(np.diag(Operator(qc).data)), 3), np.allclose(Operator(qc).data, np.diag(np.diag(Operator(qc).data))))
# Ex6: mixer beta = pi/2 on |00>
qc = QuantumCircuit(2); qc.rx(np.pi, 0); qc.rx(np.pi, 1)
pr('Ex6', {to_book(k): round(v, 3) for k, v in Statevector(qc).probabilities_dict().items()})
# Ex7: two machines, COBYLA from the grid point of Ex. 13.9
H2 = qubo_to_pauli(Q, c)
r = minimize(lambda t: expected_cost(H2, [t[0]], [t[1]]), [1.8326, 0.7330], method='COBYLA',
             options={'rhobeg': 0.05, 'tol': 1e-6})
p2 = book_probs(H2, [r.x[0]], [r.x[1]])
pr('Ex7', np.round(r.x, 4), round(r.fun, 4), round(p2.get('10', 0), 4))
X2, E2 = brute_force(Q, c)
best = min((qaoa_probs(E2, [g], [b]) @ E2, g, b) for g in np.linspace(0, np.pi, 61)
           for b in np.linspace(-np.pi / 2, np.pi / 2, 61))
pr('Ex7 full beta range grid', [round(float(v), 4) for v in best])
# Ex8: gate count for p = 3
pr('Ex8', dict(qaoa_circuit(setup(20)[2], [0.1] * 3, [0.1] * 3).count_ops()))
# Ex9: uniform mean = offset for several lambda
for lam in [5, 10, 20]:
    Qs, cs, Hs, Es = setup(lam); pr('Ex9', lam, Es.mean(), to_ising(Qs, cs)[2])
# Ex10: shots for standard error 0.5
pr('Ex10', np.ceil(1000 * (1.30 / 0.5) ** 2))
# Ex11: beta and beta + pi give the same state
Q9, c9, H9, E9 = setup(20)
pa, pb = qaoa_probs(E9, [0.0385], [2.069]), qaoa_probs(E9, [0.0385], [2.069 - np.pi])
pr('Ex11', np.abs(pa - pb).max(), round(pa @ E9, 2))
# Ex12: COBYLA without scaling (S = 1)
r = minimize(lambda t: qaoa_probs(E9, [t[0]], [t[1]]) @ E9, [0.015, -0.4363], method='COBYLA',
             options={'rhobeg': 0.2, 'tol': 1e-4})
pr('Ex12', np.round(r.x, 4), round(r.fun, 2), r.nfev)
# Ex13: misreading ranks 5-7
for s in ['100001010', '100010001', '010100001']:
    pr('Ex13', s, 'right:', describe(to_book(s)), ' misread:', describe(s))
# Ex14: exact probability of each feasible order at p = 1
pp = qaoa_probs(E9, [0.0160], [-0.4123])
for k in np.where(FEASIBLE)[0]:
    pr('Ex14', BOOK[k], describe(BOOK[k]), round(pp[k], 4), round(pp[k] / pp[FEASIBLE].sum(), 3))
# Ex15: INTERP from p = 2 to p = 3
ang = json.load(open('angles.json'))
g2, b2 = ang['2']
pr('Ex15', np.round(interp(g2), 4), np.round(interp(b2), 4))
# Ex16: lambda = 3, infeasible strings with value 6 (below 8)
Q3, c3, H3_, E3 = setup(3)
pr('Ex16', [(BOOK[k], E3[k]) for k in np.argsort(E3) if not FEASIBLE[k] and E3[k] < 8])
# Ex17: shots99 for p = 2, 3
s99 = lambda P: int(np.ceil(np.log(0.01) / np.log(1 - P)))
pr('Ex17', s99(0.0612), s99(0.0897))
# Ex18: first-order formula
h9, J9, off9 = to_ising(Q9, c9)
for b in [-0.3, -0.6, 0.3]:
    g = 1e-6
    pr('Ex18', b, round((qaoa_probs(E9, [g], [b]) @ E9 - off9) / g, 1),
       round(2 * np.sin(2 * b) * (h9 ** 2).sum() + 2 * np.sin(4 * b) * (J9 ** 2).sum(), 1))
pr('Ex18 sums', (h9 ** 2).sum(), (J9 ** 2).sum())
# Ex19: annealing-like linear schedule, p = 4, no optimizer
for D in [0.02, 0.04, 0.06, 0.08]:   # gamma_max; beta from -0.5 to 0
    p = 4; t = (np.arange(1, p + 1) - 0.5) / p
    gs, bs = D * t, -0.5 * (1 - t)
    q = qaoa_probs(E9, gs, bs)
    pr('Ex19', D, np.round(gs, 4), np.round(bs, 4), round(q @ E9, 2), round(q[OPT], 4), round(q[FEASIBLE].sum(), 4))
# Ex20: optimization level 3 on FakeFez, p = 1
fez = FakeFez()
qc = qaoa_circuit(H9, [0.0160], [-0.4123], measure=True)
for lvl in [1, 3]:
    pm = generate_preset_pass_manager(optimization_level=lvl, backend=fez, seed_transpiler=0)
    isa = pm.run(qc)
    pr('Ex20', lvl, isa.depth(), isa.count_ops().get('cz', 0))
# Ex22: supplier problem (Ch. 4), lambda = 100, p = 1
Qs, cs = supplier_qubo(100); Hs = qubo_to_pauli(Qs, cs); Xs, Es = brute_force(Qs, cs)
pr('Ex22 values', {''.join(map(str, x)): e for x, e in zip(Xs, Es)}, 'mean', Es.mean())
best = min((qaoa_probs(Es, [g], [b]) @ Es, g, b) for g in np.linspace(0, 0.05, 101)
           for b in np.radians(np.arange(-90, 91, 2)))
r = minimize(lambda t: qaoa_probs(Es, [t[0] / 200], [t[1]]) @ Es, [best[1] * 200, best[2]],
             method='COBYLA', options={'rhobeg': 0.2, 'tol': 1e-4})
qs = qaoa_probs(Es, [r.x[0] / 200], [r.x[1]])
pr('Ex22 grid', [round(float(v), 4) for v in best], 'cobyla', round(r.x[0] / 200, 5), round(r.x[1], 4),
   round(r.fun, 2), 'P(011)', round(qs[int('011', 2)], 4),
   'P(feasible)', round(sum(qs[int(s, 2)] for s in ['110', '101', '011']), 4))
pr('Ex22 check', round(expected_cost(Hs, [r.x[0] / 200], [r.x[1]]), 2))
