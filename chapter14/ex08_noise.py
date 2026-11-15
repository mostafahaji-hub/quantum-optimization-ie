"""Example 14.13 - QAOA on FakeFez (10000 shots per circuit).
The counts are saved in fez_counts.json for the later examples."""
import json
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from tsp4 import setup, FEASIBLE, OPT
from qaoa import qaoa_circuit
from fastsim import qaoa_probs
from runner import run_counts
from mitigate import counts_to_probs, calibration_for
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))      # from Example 14.10
fez = FakeFez()
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)
circuits, saved = [], {}
for p in ['1', '2', '3', '4']:
    g, b = angles[p]
    isa = pm.run(qaoa_circuit(H, g, b, measure=True))
    circuits += [isa] + list(calibration_for(isa, fez))
counts = run_counts(circuits, fez, 10000, seed=7)
print('p   ideal: P(opt) P(feas)  <H>    '
      'FakeFez: P(opt) P(feas)  <H>')
for i, p in enumerate(['1', '2', '3', '4']):
    run, zero, one = counts[3 * i: 3 * i + 3]
    saved[p] = {'run': run, 'cal0': zero, 'cal1': one}
    ideal = qaoa_probs(E, *angles[p])
    noisy = counts_to_probs(run, 9)
    i_opt, i_feas = ideal[OPT].sum(), ideal[FEASIBLE].sum()
    n_opt, n_feas = noisy[OPT].sum(), noisy[FEASIBLE].sum()
    print(f'{p}   {i_opt:12.4f} {i_feas:7.4f} {ideal @ E:6.2f}'
          f'   {n_opt:14.4f} {n_feas:7.4f} {noisy @ E:6.2f}')
json.dump(saved, open('fez_counts.json', 'w'))
