"""Answers for the no-account options of Exercises 12.18 and 13.21 (calibration snapshots)."""
import sys, json, time; import warnings; warnings.filterwarnings('ignore')
t0 = time.time()
sys.path.insert(0, '../chapter12')
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.executor_sampler import Sampler
from qiskit_ibm_runtime.fake_provider import FakeKingston, FakeTorino, FakeMarrakesh
from grover import grover_circuit
def to_book(s): return s[::-1]
def sample(qc, b, lvl, shots=1000, seed=7):
    pm = generate_preset_pass_manager(optimization_level=lvl, backend=b, seed_transpiler=0)
    isa = pm.run(qc); sm = Sampler(mode=b); sm.options.simulator.seed_simulator = seed
    return isa.count_ops().get('cz', 0), sm.run([isa], shots=shots).result()[0].join_data().get_counts()
for B in (FakeKingston(), FakeTorino()):
    for lvl in (1, 3):
        row = []
        for k in (1, 2):
            cz, c = sample(grover_circuit(['101'], 3, k), B, lvl)
            row.append((k, cz, sum(n for s, n in c.items() if to_book(s) == '101')/1000))
        print(f'12.18 {B.name} level {lvl}: (k, CZ, P(101)) {row}  ({time.time()-t0:.0f} s)')
sys.path.pop(0); sys.path.insert(0, '../chapter13')
for m in [k for k in list(sys.modules) if k in ('qaoa', 'runner', 'fastsim', 'shop9', 'encode', 'qubo', 'ham', 'shop_pos_qubo')]: del sys.modules[m]
from shop9 import setup, describe
from qaoa import qaoa_circuit
Q, c, H, E = setup(lam=20)
angles = json.load(open('../chapter13/angles.json'))
g, b_ = angles['1']
for B in (FakeMarrakesh(), FakeTorino()):
    cz, cnt = sample(qaoa_circuit(H, g, b_, measure=True), B, 1)
    opt = cnt.get('001010100', 0)/1000
    feas = sum(n for s, n in cnt.items() if describe(to_book(s)) != 'infeasible')/1000
    print(f'13.21 {B.name}: CZ {cz}, P(opt) {opt:.3f}, P(feasible) {feas:.3f}  ({time.time()-t0:.0f} s)')
