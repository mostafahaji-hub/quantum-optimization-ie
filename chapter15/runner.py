"""Chapter 10 - run circuits on any 'mode': ideal simulator,
noisy fake IBM backend, or a real IBM QPU."""
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.executor_sampler import Sampler

def run_counts(circuits, backend, shots=1000, seed=None):
    """Transpile for `backend`, sample, return a list of counts."""
    pm = generate_preset_pass_manager(
        optimization_level=1, backend=backend, seed_transpiler=0)
    isa = pm.run(list(circuits))
    sampler = Sampler(mode=backend)
    if seed is not None:              # only simulators use a seed
        sampler.options.simulator.seed_simulator = seed
    result = sampler.run(isa, shots=shots).result()
    return [pub.join_data().get_counts() for pub in result]

def to_book(bitstring):
    """Qiskit prints q0 on the RIGHT; the book puts q0 LEFT."""
    return bitstring[::-1]
