"""Chapter 12 - answers of Exercises 12.13, 12.14, 12.15, 12.17
(the variants are produced by editing the example files on the fly)."""
import subprocess, sys
def run(src):
    out = subprocess.run([sys.executable, '-c', src], text=True,
                         capture_output=True, check=True).stdout
    print(out.rstrip())
ex10 = open('ex10_repeat.py').read()
print('Ex 12.13: max_fail = 5')
run(ex10.replace('minimum_search(tab, 3, shoot, rng)',
                 'minimum_search(tab, 3, shoot, rng, max_fail=5)'))
for lam in ['1.5', '2']:
    print(f'Ex 12.14: growth factor {lam}')
    gas = open('gas.py').read().replace('1.2 * m', f'{lam} * m')
    run(gas + '\n' + ex10.replace('from gas import minimum_search', ''))
print('Ex 12.15: default_rng(2)')
run(open('ex09_minimum.py').read().replace('default_rng(5)',
                                           'default_rng(2)'))
print('Ex 12.17: optimization_level = 3')
src = open('runner.py').read().replace('optimization_level=1',
                                       'optimization_level=3')
open('runner_l3.py', 'w').write(src)
run(open('ex11_noise.py').read()
    .replace('optimization_level=1', 'optimization_level=3')
    .replace('from runner import', 'from runner_l3 import'))
