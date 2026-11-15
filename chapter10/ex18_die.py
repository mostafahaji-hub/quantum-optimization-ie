from qiskit_aer import AerSimulator
from circuits import die3
from runner import run_counts
orders = ['J1J2J3', 'J1J3J2', 'J2J1J3',
          'J2J3J1', 'J3J1J2', 'J3J2J1']
cost = [12, 9, 13, 11, 8, 5]       # weighted tardiness (Ch. 2)
c = run_counts([die3()], AerSimulator(), 1000, seed=42)[0]
used = total = 0
for s in sorted(c):
    k = int(s, 2)                  # read as a binary number
    if k < 6:
        used += c[s]; total += c[s] * cost[k]
        print(f'{s} -> {k} -> {orders[k]} cost {cost[k]:2d}'
              f' : {c[s]}')
    else:
        print(f'{s} -> {k} -> rejected       : {c[s]}')
print(f'accepted {used}/1000, mean cost {total/used:.2f}')
print(f'optimum J3J2J1 seen {c.get("101", 0)} times')
