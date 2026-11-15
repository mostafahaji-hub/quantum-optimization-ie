"""Chapter 13 - QAOA built gate by gate from a Hamiltonian.
Variable i of the QUBO acts on qubit i (Chapter 11)."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from runner import to_book

def cost_layer(qc, H, gamma):
    """Append exp(-i*gamma*H). H has only I, Z and ZZ terms.
    The constant (I) term is a global phase, so it is skipped."""
    for pauli, idx, coef in H.to_sparse_list():
        if pauli == 'Z':
            qc.rz(2 * gamma * coef.real, idx[0])
        elif pauli == 'ZZ':
            qc.rzz(2 * gamma * coef.real, idx[0], idx[1])

def mixer_layer(qc, beta):
    """Append exp(-i*beta*X) on every qubit."""
    for q in range(qc.num_qubits):
        qc.rx(2 * beta, q)

def qaoa_circuit(H, gammas, betas, measure=False):
    """H layer, then p pairs (cost, mixer); p = len(gammas)."""
    qc = QuantumCircuit(H.num_qubits)
    qc.h(range(H.num_qubits))
    for g, b in zip(gammas, betas):
        cost_layer(qc, H, g)
        mixer_layer(qc, b)
    if measure:
        qc.measure_all()
    return qc

def expected_cost(H, gammas, betas):
    """Exact <H> from the state vector (no shots)."""
    sv = Statevector(qaoa_circuit(H, gammas, betas))
    return sv.expectation_value(H).real

def book_probs(H, gammas, betas):
    """Exact probability of every string, in BOOK order."""
    sv = Statevector(qaoa_circuit(H, gammas, betas))
    return {to_book(s): p for s, p in
            sv.probabilities_dict().items()}

def interp(v):
    """Zhou et al. (2020): p good angles -> p + 1 start angles."""
    q = len(v)
    w = [0.0] + list(v) + [0.0]
    return [i / q * w[i] + (q - i) / q * w[i + 1]
            for i in range(q + 1)]
