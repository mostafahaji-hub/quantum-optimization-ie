from qiskit_aer import AerSimulator
from circuits import basis_state
from runner import run_counts, to_book
from encode import order_to_bits, bits_to_order
cost = {(1, 2, 3): 12, (1, 3, 2): 9, (2, 1, 3): 13,
        (2, 3, 1): 11, (3, 1, 2): 8, (3, 2, 1): 5}
for order in [(3, 2, 1), (3, 1, 2)]:
    book = order_to_bits(order)
    qc = basis_state(book)
    c = run_counts([qc], AerSimulator(), 10, seed=1)[0]
    q = list(c)[0]
    wrong, right = bits_to_order(q), bits_to_order(to_book(q))
    print(f'prepared {book} | Qiskit prints {q}')
    print(f'   read directly: {wrong} cost {cost[tuple(wrong)]}'
          f' | with to_book: {right} cost {cost[tuple(right)]}')
