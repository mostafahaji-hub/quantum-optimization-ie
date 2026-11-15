from qiskit_ibm_runtime.fake_provider import FakeFez
from circuits import ghz
from runner import run_counts
sizes = [2, 4, 6, 8, 10, 12]
res = run_counts([ghz(n) for n in sizes], FakeFez(),
                 shots=2000, seed=2026)
for n, c in zip(sizes, res):
    good = c.get('0' * n, 0) + c.get('1' * n, 0)
    print(f'n = {n:2d}: correct {good:4d}/2000 = {good/2000:.3f}'
          f'   distinct strings: {len(c)}')
