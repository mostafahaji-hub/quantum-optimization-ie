"""Figures 10.2, 10.6, 10.7: circuit drawings in black and white."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from circuits import coin, bell, double_coin
style = {'name': 'bw', 'fontsize': 14, 'subfontsize': 10, 'creglinecolor': '#555555'}
for name, qc in [('fig10_2_coin', coin()), ('fig10_5_double', double_coin()), ('fig10_6_bell', bell())]:
    fig = qc.draw('mpl', style=style, scale=1.1)
    fig.savefig(f'../fig/{name}.png', dpi=150, bbox_inches='tight', facecolor='white')
pm = generate_preset_pass_manager(optimization_level=1, backend=FakeFez(), seed_transpiler=0)
fig = pm.run(bell()).draw('mpl', style=style, idle_wires=False, scale=1.0)
fig.savefig('../fig/fig10_7_bell_isa.png', dpi=150, bbox_inches='tight', facecolor='white')
print('ok')
