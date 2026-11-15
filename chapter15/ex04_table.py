"""Example 15.6 - the head-to-head table in one currency:
evaluations (= shots) for a 99 percent chance to see the optimum."""
import json
from common import runs99, evals99
bt = json.load(open('budget_table.json'))
B = [25, 50, 100, 200, 400]

def best_classical(key):
    e = bt[key]['e99']
    return min(e)

rows = {'shop': [], 'tsp': []}
for prob, n_perm, n_opt in [('shop', 6, 1), ('tsp', 6, 2)]:
    r = rows[prob]
    r.append(('enumerate all orders/tours', n_perm))
    r.append(('simple rule (EDD/WSPT or NN)', 'never'))
    r.append(('best of all rules / all starts',
              'never' if prob == 'shop' else 4))
    r.append(('random order/tour', runs99(n_opt / n_perm)))
    for a in ['random', 'SA', 'GA', 'QEA', 'KA']:
        r.append((f'{a} on the 9-bit QUBO',
                  best_classical(f'{prob}/{a}')))
fixed = {'shop': [('QAOA p=1 ideal (Ch. 13)', 0.0216),
                  ('QAOA p=4 ideal (Ch. 13)', 0.1213),
                  ('QAOA p=4 FakeFez (Ch. 13)', 0.032),
                  ('Grover k=2, table oracle (Ch. 12)', 0.948)],
         'tsp':  [('QAOA p=1 ideal (Ch. 14)', 0.0317),
                  ('QAOA p=4 ideal (Ch. 14)', 0.1708),
                  ('QAOA p=4 FakeFez (Ch. 14)', 0.0367),
                  ('Grover k=1, table oracle (Ch. 12)', 1.0)]}
for prob in rows:
    for name, P in fixed[prob]:
        rows[prob].append((name, runs99(P)))
    print(f'--- {prob} (shots or evaluations for 99 percent)')
    for name, v in rows[prob]:
        print(f'  {name:36s} {v}')
print('extra cost of QAOA, tuning p=1 on hardware:',
      'shop ~1.55 million shots (Ch. 13), tsp 1,544,000 (Ch. 14)')
json.dump(rows, open('head_to_head.json', 'w'), indent=1)
