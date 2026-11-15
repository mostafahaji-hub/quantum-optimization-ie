# Truck loading: 8 shipments, capacity 20 tons
w = [7, 9, 9, 6, 8, 5, 9, 2]          # weight (tons)
v = [9, 13, 14, 7, 6, 13, 6, 3]       # profit (thousand $)
CAP = 20
def weight(x): return sum(wi for wi, b in zip(w, x) if b)
def value(x):  return sum(vi for vi, b in zip(v, x) if b)
