import matplotlib
matplotlib.use("Agg")                  # draw to a file, no window
import matplotlib.pyplot as plt

names = ["J1J2J3", "J1J3J2", "J2J1J3", "J2J3J1", "J3J1J2", "J3J2J1"]
costs = [12, 9, 13, 11, 8, 5]
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(names, costs, color="0.6", edgecolor="black")
ax.set_ylabel("Weighted Tardiness")
plt.tight_layout()
plt.savefig("six_orders.png", dpi=150)
print("saved six_orders.png")
