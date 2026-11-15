"""Example 14.5 - the QAOA circuit of the TSP and its <H> at 0."""
from tsp4 import setup
from qaoa import qaoa_circuit, expected_cost
Q, c, H, E = setup(lam=20)
qc = qaoa_circuit(H, [0.02], [-0.4])
print('gates:', dict(qc.count_ops()), '  total:', qc.size(),
      '  depth:', qc.depth())
e0 = expected_cost(H, [0], [0])
e1 = expected_cost(H, [0.02], [-0.4])
print('<H> at gamma = beta = 0:', round(e0, 4))
print('<H> at (0.02, -0.4):', round(e1, 4))
