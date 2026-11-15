# Chapter 4, code listing 2 (in order of appearance)
import itertools
from shop import twt
def decode(bits):
    """9 bits x11..x33 -> job sequence, or None if infeasible."""
    x = [[int(bits[3*j + k]) for k in range(3)] for j in range(3)]
    rows_ok = all(sum(r) == 1 for r in x)
    cols_ok = all(sum(x[j][k] for j in range(3)) == 1 for k in range(3))
    if not (rows_ok and cols_ok):
        return None
    pos = {k: f'J{j+1}' for j in range(3) for k in range(3) if x[j][k]}
    return tuple(pos[k] for k in range(3))
for b in ['001010100', '100001010', '101000010']:
    seq = decode(b)
    print(b, seq, twt(seq) if seq else 'infeasible')
feasible = [b for b in (''.join(t) for t in itertools.product('01', repeat=9))
            if decode(b)]
print('feasible strings:', len(feasible), 'of', 2**9)