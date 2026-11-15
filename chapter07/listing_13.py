# Chapter 7, code listing 13 (in order of appearance)
import itertools
from emer import route_time, names
sites = range(1, 8)
for tau in (0.0, 0.84):
    t, p = min((route_time(q, tau)[0], q) for q in itertools.permutations(sites))
    t, rel, legs = route_time(p, tau)
    print(f'tau {tau:.2f}: visit order H-' + '-'.join(names[i] for i in p) + '-H',
          f' time {t}  route reliability {rel:.3f}')
    print('   legs:', ['-'.join(names[i] for i in leg) for leg in legs])