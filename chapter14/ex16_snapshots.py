"""Example 14.23 - the same experiment on four calibration
snapshots of real IBM processors (10000 shots, seed 7)."""
import json
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import (
    FakeFez, FakeMarrakesh, FakeKingston, FakeTorino)
from tsp4 import setup, FEASIBLE, OPT
from qaoa import qaoa_circuit
from runner import run_counts
from mitigate import (counts_to_probs, calibration_for,
                      flip_rates, readout_correct)
Q, c, H, E = setup(lam=20)

def no_error_chance(isa, target):
    """Example 14.12: product of (1 - error) over all gates."""
    prob = 1.0
    for inst in isa.data:
        name = inst.operation.name
        if name != 'barrier':
            qs = tuple(isa.find_bit(q).index for q in inst.qubits)
            prob *= 1 - (target[name][qs].error or 0.0)
    return prob

angles = json.load(open('angles.json'))      # from Example 14.10
print('snapshot   p   CZ  no err read ok P(opt) raw  corr'
      ' P(feas) raw  corr')
for backend in [FakeFez(), FakeMarrakesh(), FakeKingston(),
                FakeTorino()]:
    pm = generate_preset_pass_manager(optimization_level=1,
                                      backend=backend,
                                      seed_transpiler=0)
    circuits, cz, good = [], [], []
    for p in ['1', '2', '3', '4']:
        isa = pm.run(qaoa_circuit(H, *angles[p], measure=True))
        cz.append(isa.count_ops().get('cz', 0))
        good.append(no_error_chance(isa, backend.target))
        circuits += [isa] + list(calibration_for(isa, backend))
    counts = run_counts(circuits, backend, 10000, seed=7)
    for i, p in enumerate(['1', '2', '3', '4']):
        run, zero, one = counts[3 * i: 3 * i + 3]
        e01, e10 = flip_rates([zero, one], 9)
        raw = counts_to_probs(run, 9)
        cor = readout_correct(raw, e01, e10)
        ok = (1 - e01).prod()
        name = backend.name.replace('fake_', '').title()
        print(f'{name:9s}  {p}  {cz[i]:3d}  {good[i]:6.3f}'
              f' {ok:7.3f}  {raw[OPT].sum():8.4f}'
              f' {cor[OPT].sum():.4f}  {raw[FEASIBLE].sum():9.4f}'
              f' {cor[FEASIBLE].sum():.4f}')
