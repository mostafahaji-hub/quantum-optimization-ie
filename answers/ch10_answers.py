"""Chapter 10 answers (Qiskit 2.5.2, Aer 0.17.2, runtime 0.50.0)."""
import sys, math, time, json; sys.path.insert(0, '../chapter10')
import warnings; warnings.filterwarnings('ignore')
import numpy as np
from scipy.stats import chisquare
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez, FakeTorino, FakeBrisbane
from circuits import coin, bell, ghz, basis_state, biased_coin, die3
from runner import run_counts, to_book
from metrics import probs, tvd, hellinger_fid
t0 = time.time(); sim = AerSimulator()
out = [run_counts([coin()], sim, 1000, seed=s)[0].get('0', 0) for s in range(1, 201)]
print('10.4 outside 468..532:', sum(not (468 <= z <= 532) for z in out), 'of 200')
for b in ('1011', '0001', '1100'): print('10.5', b, '->', b[::-1])
qc = QuantumCircuit(1, 1); qc.h(0); qc.z(0); qc.h(0); qc.measure(0, 0); print('10.7', run_counts([qc], sim, 1000, seed=7)[0])
th = 2*math.asin(math.sqrt(0.08)); c = run_counts([biased_coin(th)], sim, 500, seed=8)[0]
print('10.8 theta', round(th, 4), 'rad', round(math.degrees(th), 2), 'deg; 500 shots', c)
qc = QuantumCircuit(2, 2); qc.h(0); qc.cx(0, 1); qc.x(1); qc.measure([0, 1], [0, 1])
c = run_counts([qc], sim, 1000, seed=10)[0]; print('10.10 Qiskit', c, 'book', {to_book(k): v for k, v in c.items()})
fez = FakeFez()
c3 = run_counts([ghz(3)], fez, 1000, seed=2026)[0]; print('10.11 GHZ3 FakeFez correct', (c3.get('000', 0) + c3.get('111', 0))/1000, f'({time.time()-t0:.0f} s)')
for lvl in range(4):
    pm = generate_preset_pass_manager(optimization_level=lvl, backend=fez, seed_transpiler=0); isa = pm.run(ghz(8))
    print('10.12 level', lvl, 'cz', isa.count_ops().get('cz', 0), 'depth', isa.depth())
qc = QuantumCircuit(3); qc.cx(0, 2)
for lay in ([0, 1, 2], None):
    pm = generate_preset_pass_manager(optimization_level=1, backend=fez, seed_transpiler=0, initial_layout=lay)
    isa = pm.run(qc); print('10.13 layout', lay, 'ops', dict(isa.count_ops()), 'qubits', isa.layout.final_index_layout()[:3])
sx = np.array([[1+1j, 1-1j], [1-1j, 1+1j]])/2; print('10.14 sx*sx', np.round(sx @ sx, 6).real.tolist())
qx = QuantumCircuit(1, 1); qx.x(0); qx.measure(0, 0)
print('10.14 transpiled X', dict(generate_preset_pass_manager(optimization_level=1, backend=fez, seed_transpiler=0).run(qx).count_ops()))
nm = NoiseModel(); nm.add_all_qubit_readout_error(ReadoutError([[0.98, 0.02], [0.06, 0.94]]))
ns = AerSimulator(noise_model=nm); r = run_counts([basis_state('0'), basis_state('1'), coin()], ns, 1000, seed=11)
print('10.15', r)
M = np.array([[0.98, 0.06], [0.02, 0.94]]); q = np.array([r[1].get('0', 0), r[1].get('1', 0)])/1000
print('10.16 corrected prepare-1', np.linalg.solve(M, q).round(4), ' if observed (0.05, 0.95):', np.linalg.solve(M, [0.05, 0.95]).round(4))
for B in (fez, FakeTorino()):
    ro = sorted((B.target['measure'][(q_,)].error, q_) for q_ in range(B.num_qubits) if (q_,) in B.target['measure'] and B.target['measure'][(q_,)].error is not None)
    best, worst = ro[0][1], ro[-1][1]
    res = []
    for q_ in (best, worst):
        pm = generate_preset_pass_manager(optimization_level=1, backend=B, seed_transpiler=0, initial_layout=[q_])
        from qiskit_ibm_runtime.executor_sampler import Sampler
        smp = Sampler(mode=B); smp.options.simulator.seed_simulator = 2026
        cc = smp.run([pm.run(basis_state('1'))], shots=1000).result()[0].join_data().get_counts()
        res.append((q_, round(B.target['measure'][(q_,)].error, 4), cc.get('1', 0)))
    print(f'10.17 {B.name}: best 3 {[(round(e,4), q_) for e, q_ in ro[:3]]}, worst 3 {[(round(e,4), q_) for e, q_ in ro[-3:]]}; prepare 1 on best/worst: {res}  ({time.time()-t0:.0f} s)')
br = FakeBrisbane(); names = ['prepare 0', 'prepare 1', 'coin', 'bell']
rb = run_counts([basis_state('0'), basis_state('1'), coin(), bell()], br, 1000, seed=2026)
ideal = [{'0': 1.0}, {'1': 1.0}, {'0': .5, '1': .5}, {'00': .5, '11': .5}]
print('10.18 FakeBrisbane', br.properties().last_update_date.date(), [(n, round(tvd(i, probs(c)), 3)) for n, i, c in zip(names, ideal, rb)], f'({time.time()-t0:.0f} s)')
cnt = {'00': 470, '01': 40, '10': 35, '11': 455}
print('10.19 TVD', round(tvd({'00': .5, '11': .5}, probs(cnt)), 4), 'fidelity', round(hellinger_fid({'00': .5, '11': .5}, probs(cnt)), 4))
for N in (100, 1000, 10000):
    t = [tvd({'00': .5, '11': .5}, probs(run_counts([bell()], sim, N, seed=s)[0])) for s in range(20)]
    print(f'10.20 N={N}: mean TVD {np.mean(t):.4f} (theory {0.399/math.sqrt(N):.4f})')
c = run_counts([die3()], sim, 8000, seed=21)[0]; faces = [c.get(format(k, '03b'), 0) for k in range(6)]
print('10.21 accepted', sum(faces), faces, 'chi-square p', round(chisquare(faces).pvalue, 3))
q2 = QuantumCircuit(2, 2); q2.h([0, 1]); q2.measure([0, 1], [0, 1]); c = run_counts([q2], sim, 1000, seed=22)[0]
L = {'00': 26, '01': 31, '10': 27}; acc = {k: v for k, v in c.items() if k in L}
print('10.22', c, 'accepted mean length', round(sum(L[k]*v for k, v in acc.items())/sum(acc.values()), 2))
print(f'done ({time.time()-t0:.0f} s)')
