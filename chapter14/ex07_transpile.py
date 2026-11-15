"""Example 14.12 - the TSP circuits after translation for FakeFez,
and a quick 'chance that no gate makes an error' estimate."""
import json
import numpy as np
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from tsp4 import setup
from qaoa import qaoa_circuit
Q, c, H, E = setup(lam=20)
angles = json.load(open('angles.json'))      # from Example 14.10
fez = FakeFez()
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=fez, seed_transpiler=0)

def no_error_chance(isa, target):
    """Product of (1 - error) over all gates and measurements."""
    prob = 1.0
    for inst in isa.data:
        name = inst.operation.name
        if name == 'barrier':
            continue
        qs = tuple(isa.find_bit(q).index for q in inst.qubits)
        err = target[name][qs].error or 0.0
        prob *= 1 - err
    return prob

print('p  depth   CZ  SX  chance of no error')
for p in ['1', '2', '3', '4']:
    g, b = angles[p]
    isa = pm.run(qaoa_circuit(H, g, b, measure=True))
    ops = isa.count_ops()
    ok = no_error_chance(isa, fez.target)
    print(f'{p}  {isa.depth():5d}  {ops.get("cz", 0):3d}'
          f' {ops.get("sx", 0):3d}  {ok:.3f}')
