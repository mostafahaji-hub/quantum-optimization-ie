import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.linewidth': 1.2})
def bars(ax, labels, values, color='0.35', hatch=None, offset=0.0, width=0.6, label=None):
    x = [i + offset for i in range(len(labels))]
    b = ax.bar(x, values, width=width, color=color, edgecolor='black', linewidth=1.2, hatch=hatch, label=label)
    for xi, v in zip(x, values):
        ax.text(xi, v, f'{v}', ha='center', va='bottom', fontsize=9)
    return b
