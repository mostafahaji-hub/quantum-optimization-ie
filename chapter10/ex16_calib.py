from qiskit_ibm_runtime.fake_provider import FakeFez
b = FakeFez()                # calibration snapshot in Qiskit
t, q = b.target, 0
p = b.qubit_properties(q)
print(f'T1 = {p.t1*1e6:.1f} us,  T2 = {p.t2*1e6:.1f} us')
for gate, qubits in [('sx', (0,)), ('cz', (0, 1)),
                     ('measure', (0,))]:
    if qubits not in t[gate]:
        qubits = qubits[::-1]
    ip = t[gate][qubits]
    print(f'{gate:7s} {str(qubits):6s} error {ip.error:.5f}'
          f'  duration {ip.duration*1e9:5.0f} ns')
nb = {b2 if a == q else a for (a, b2) in t['cz'] if q in (a, b2)}
print('neighbours of qubit 0:', sorted(nb))
