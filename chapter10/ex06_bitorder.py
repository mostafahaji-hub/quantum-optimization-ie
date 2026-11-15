from qiskit_aer import AerSimulator
from circuits import basis_state
from runner import run_counts, to_book
sim = AerSimulator()
for book in ['10', '01', '110']:       # book order: q0 first
    c = run_counts([basis_state(book)], sim, 100, seed=1)[0]
    q = list(c)[0]
    print(f'book {book:>3} -> Qiskit {q:>3}'
          f' -> to_book {to_book(q):>3}')
