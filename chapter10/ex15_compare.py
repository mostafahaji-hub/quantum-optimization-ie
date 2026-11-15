from qiskit.quantum_info import hellinger_fidelity
from metrics import probs, tvd, hellinger_fid
ideal = {'00': 0.5, '11': 0.5}
hand = {'00': 480, '11': 470, '01': 30, '10': 20}  # Ex. 10.22
fake = {'00': 496, '01': 15, '10': 13, '11': 476}  # Ex. 10.19
for name, c in [('hand', hand), ('FakeFez', fake)]:
    p = probs(c)
    print(f'{name:8s} TVD {tvd(ideal, p):.4f}'
          f'  fidelity {hellinger_fid(ideal, p):.4f}'
          f'  (qiskit {hellinger_fidelity(ideal, c):.4f})')
