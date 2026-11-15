"""Example 13.8 - one layer alone changes nothing we can see."""
from machine2 import machine_qubo
from ham import qubo_to_pauli
from qaoa import book_probs, expected_cost
H = qubo_to_pauli(*machine_qubo())
print('gamma  beta   P(00)  P(10)  P(01)  P(11)   <f>')
for g, b in [(0.0, 0.4), (0.6, 0.0), (0.6, 0.4)]:
    p = book_probs(H, [g], [b])
    row = '  '.join(f'{p.get(s, 0):.3f}' for s in
                    ['00', '10', '01', '11'])
    e = expected_cost(H, [g], [b])
    print(f'{g:4.1f}  {b:4.1f}   {row}  {e:5.2f}')
