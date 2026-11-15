"""Example 15.10 - QAOA (p = 1) for the TSP as cities grow.
Cities: the first n points of the 8-city TSP (Ch. 2, 8, 9)."""
import math
from qiskit.transpiler import generate_preset_pass_manager, Target
from qiskit_ibm_runtime.fake_provider import FakeFez
from tsp8 import pts
from tsp_qubo import tsp_qubo
from ham import qubo_to_pauli
from qaoa import qaoa_circuit
fez = FakeFez()
t = fez.target
broken = {qs for qs, pr in t['cz'].items() if pr.error == 1.0}
print('couplers marked broken (error = 1):',
      sorted(q for q in broken if q[0] < q[1]))

def without(target, bad):
    """Copy of the target without the cz couplers in `bad`."""
    new = Target(num_qubits=target.num_qubits, dt=target.dt)
    for name in target.operation_names:
        op, props = target.operation_from_name(name), target[name]
        if isinstance(op, type) or props == {None: None}:
            new.add_instruction(op, name=name)  # e.g. if_else
            continue
        if name == 'cz':
            props = {q: p for q, p in props.items() if q not in bad}
        new.add_instruction(op, dict(props), name=name)
    return new

plain = generate_preset_pass_manager(optimization_level=1,
                                     backend=fez, seed_transpiler=0)
safe = generate_preset_pass_manager(optimization_level=1,
                                    target=without(t, broken),
                                    seed_transpiler=0)

def no_error_chance(isa):
    """Product of (1 - error) over all gates (Example 14.12)."""
    prob = 1.0
    for inst in isa.data:
        name = inst.operation.name
        if name == 'barrier':
            continue
        qs = tuple(isa.find_bit(q).index for q in inst.qubits)
        prob *= 1 - (t[name][qs].error or 0.0)
    return prob

print('cities qubits  ZZ    CZ   no error | CZ safe  no error safe')
for n in range(4, 9):
    D = [[round(math.dist(a, b), 1) for b in pts[:n]]
         for a in pts[:n]]
    H = qubo_to_pauli(*tsp_qubo(D, lam=10))
    zz = sum(1 for lab, _, _ in H.to_sparse_list() if lab == 'ZZ')
    qc = qaoa_circuit(H, [0.01], [-0.4], measure=True)
    a, b = plain.run(qc), safe.run(qc)
    ca, cb = a.count_ops()['cz'], b.count_ops()['cz']
    print(f'{n:6d} {(n - 1) ** 2:6d} {zz:4d} {ca:5d}'
          f'   {no_error_chance(a):.1e} | {cb:5d}'
          f'    {no_error_chance(b):.1e}')
