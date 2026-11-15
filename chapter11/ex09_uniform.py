import numpy as np
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qubo import brute_force, energy
from shop_pos_qubo import shop_pos_qubo
from ham import qubo_to_pauli
from encode import bits_to_order
from uniform import uniform
from runner import run_counts, to_book
Q, c = shop_pos_qubo(lam=20)
H = qubo_to_pauli(Q, c)
sv = Statevector(uniform(9, measure=False))
ev = sv.expectation_value(H).real
print(f'<H> uniform superposition: {ev:.2f}')
print(f'offset (identity term)   : {H.coeffs[0].real:.2f}')
mean512 = brute_force(Q, c)[1].mean()
print(f'mean QUBO of 512 strings : {mean512:.2f}')
counts = run_counts([uniform(9)], AerSimulator(), 1000, seed=7)[0]
E = {s: energy(Q, [int(b) for b in to_book(s)], c) for s in counts}
mean = sum(E[s] * counts[s] for s in counts) / 1000
feas = {s: n for s, n in counts.items()
        if bits_to_order(to_book(s)) is not None}
print(f'1000 shots: mean energy {mean:.1f}, feasible shots'
      f' {sum(feas.values())}, best seen {min(E.values()):.0f}')
for s in sorted(feas, key=lambda s: E[s]):
    print(f'   {to_book(s)} -> {bits_to_order(to_book(s))}'
          f' energy {E[s]:.0f}  ({feas[s]} shots)')
