# Small workshop: p, d, w for J1..J3
p = {'J1': 2, 'J2': 3, 'J3': 4}
d = {'J1': 4, 'J2': 7, 'J3': 5}
w = {'J1': 1, 'J2': 3, 'J3': 3}
def twt(seq):
    t, total = 0, 0
    for j in seq:
        t += p[j]
        total += w[j] * max(0, t - d[j])
    return total
code = {'000': ('J1','J2','J3'), '001': ('J1','J3','J2'),
        '010': ('J2','J1','J3'), '011': ('J2','J3','J1'),
        '100': ('J3','J1','J2'), '101': ('J3','J2','J1')}
