from itertools import permutations
from a02_function import weighted_tardiness, p, d, w

costs = {}
for order in permutations([0, 1, 2]):
    name = "".join(f"J{j + 1}" for j in order)
    costs[name] = weighted_tardiness(order, p, d, w)

for name, c in costs.items():
    print(f"{name}: {c:>2}")
best = min(costs, key=costs.get)
print("best:", best, "with cost", costs[best])
