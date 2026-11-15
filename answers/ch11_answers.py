"""Chapter 11 answers."""
import sys, time, itertools, math; sys.path.insert(0, '../chapter11'); sys.path.insert(1, '../chapter10'); sys.path.insert(2, '../chapter08')
import warnings; warnings.filterwarnings('ignore')
import numpy as np
from encode import order_to_bits, bits_to_order, bits_to_tour
from qubo import energy, brute_force
from shop_pos_qubo import shop_pos_qubo
from tsp_qubo import tsp_qubo
from ham import qubo_to_pauli, check_hamiltonian, diag_energy
t0 = time.time()
b = order_to_bits([2, 4, 1, 3]); print('11.4 book', b, 'Qiskit', b[::-1])
t = time.time(); ok = sum(bits_to_order(format(k, '016b')) is not None for k in range(2**16))
print('11.6 4 jobs feasible', ok, f'time {time.time()-t:.2f} s, 25 bits about {512*(time.time()-t):.0f} s')
Q, c = shop_pos_qubo(20); Q0, c0 = shop_pos_qubo(0)
x = [int(ch) for ch in '100100001']; print('11.7 QUBO', energy(Q, x, c), 'cost', energy(Q0, x, c0))
X, E = brute_force(Q, c); feas = np.array([bits_to_order(''.join(map(str, r))) is not None for r in X])
for k in np.argsort(np.where(feas, np.inf, E), kind='stable')[:5]:
    s = ''.join(map(str, X[k])); print('11.8', s, E[k], 'cost', energy(Q0, X[k], c0))
for lam in (2, 100):
    Ql, cl = shop_pos_qubo(lam); Xl, El = brute_force(Ql, cl)
    fl = np.array([bits_to_order(''.join(map(str, r))) is not None for r in Xl])
    print('11.9 lam', lam, 'min feasible', El[fl].min(), 'min infeasible', El[~fl].min())
H = qubo_to_pauli(Q, c); lab = dict(zip(H.paulis.to_labels(), H.coeffs.real))
print('11.13 J07 label', 'IZIIIIIIZ'[::-1], lab.get('IZIIIIIIZ', lab.get('IZIIIIIIZ'[::-1])))
print('11.13 search', {l: v for l, v in lab.items() if l.count('Z') == 2 and l[8] == 'Z' and l[1] == 'Z'})
from qiskit.quantum_info import Statevector
from circuits import basis_state
rng = np.random.default_rng(16); diffs = []
for _ in range(20):
    s = ''.join(map(str, rng.integers(0, 2, 9)))
    sv = Statevector(basis_state(s).remove_final_measurements(inplace=False)).expectation_value(H).real
    diffs.append(abs(sv - diag_energy(H, s)))
print('11.16 max difference over 20 strings', max(diffs))
print('11.15 P(pass with 20 random strings)', (48/512)**20)
D = [[0, 5, 12, 4], [5, 0, 7, 4], [12, 7, 0, 10], [4, 4, 10, 0]]
from qiskit_aer import AerSimulator
from uniform import uniform
from runner import run_counts, to_book
cnt = run_counts([uniform(9)], AerSimulator(), 1000, seed=7)[0]
tours = {s: n for s, n in cnt.items() if bits_to_tour(to_book(s))}
lens = {'ABCDA': 26, 'ADCBA': 26, 'ACBDA': 27, 'ADBCA': 27, 'ABDCA': 31, 'ACDBA': 31}
seen = [(bits_to_tour(to_book(s)), n) for s, n in tours.items()]
print('11.17 feasible shots', sum(tours.values()), seen, 'mean length', round(sum(lens[t]*n for t, n in seen)/max(1, sum(n for _, n in seen)), 2))
from qiskit_ibm_runtime.fake_provider import FakeFez
cf = run_counts([uniform(9)], FakeFez(), 1000, seed=7)[0]
Ev = sum(energy(Q, [int(ch) for ch in to_book(s)], c)*n for s, n in cf.items())/1000
print('11.18 FakeFez uniform: mean energy', round(Ev, 1), 'feasible shots', sum(n for s, n in cf.items() if bits_to_order(to_book(s))), f'({time.time()-t0:.0f} s)')
vals = [12, 9, 13, 11, 8, 5, 20, 20]
coef = {}
for S in itertools.chain.from_iterable(itertools.combinations(range(3), r) for r in range(4)):
    a = sum((-1)**(len(S) - len(T)) * vals[sum(4 >> i for i in T)] for r in range(len(S) + 1) for T in itertools.combinations(S, r))
    if abs(a) > 1e-9: coef[S] = a
print('11.19 multilinear coefficients (code bit 0 = leftmost):', coef)
sys.path.insert(0, '../chapter08')
from location_qubo import location_qubo
from truck_qubo import truck_qubo
Ql, cl = location_qubo(20); Hl = qubo_to_pauli(Ql, cl); t = time.time()
print('11.20 location: qubits', Hl.num_qubits, 'terms', len(Hl), 'max error', check_hamiltonian(Ql, cl, Hl), f'{time.time()-t:.1f} s')
Qt, ct = truck_qubo(10); Ht = qubo_to_pauli(Qt, ct); t = time.time()
print('11.21 truck: qubits', Ht.num_qubits, 'terms', len(Ht), 'max error', check_hamiltonian(Qt, ct, Ht), f'{time.time()-t:.1f} s')
Qd, cd = tsp_qubo(D, 20); Qd = Qd.copy(); Qd[6, 6] += 0.5   # D at step 1 costs 0.5 more
Xd, Ed = brute_force(Qd, cd); o = np.argsort(Ed, kind='stable')[:3]
print('11.22', [(''.join(map(str, Xd[k])), Ed[k], bits_to_tour(''.join(map(str, Xd[k])))) for k in o])
