"""Example 13.24 - a first look at noise: QAOA on FakeFez."""
import json
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from shop9 import setup, FEASIBLE, OPT, describe
from qaoa import qaoa_circuit
from fastsim import qaoa_probs
from runner import run_counts, to_book
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))      # written by Ex. 13.19
fez = FakeFez()
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)
print('p  depth  CZ   ideal P(opt) P(feas)'
      '   FakeFez P(opt) P(feas)')
for p in ['1', '2', '3', '4']:
    g, b = angles[p]
    qc = qaoa_circuit(H, g, b, measure=True)
    isa = pm.run(qc)
    cz = isa.count_ops().get('cz', 0)
    pr = qaoa_probs(E, g, b)
    cnt = run_counts([qc], fez, 1000, seed=7)[0]
    opt = cnt.get('001010100', 0) / 1000     # symmetric string
    feas = sum(n for s, n in cnt.items()
               if describe(to_book(s)) != 'infeasible') / 1000
    print(f'{p}  {isa.depth():5d}  {cz:3d}   {pr[OPT]:11.3f} '
          f'{pr[FEASIBLE].sum():7.3f}   {opt:13.3f} {feas:7.3f}')
