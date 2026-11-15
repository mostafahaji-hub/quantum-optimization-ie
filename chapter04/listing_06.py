# Chapter 4, code listing 6 (in order of appearance)
from sim import *
def bloch(psi):
    a, b = psi
    ph = np.angle(b) - np.angle(a) if abs(a) > 1e-9 else np.angle(b)
    theta = 2 * np.degrees(np.arccos(min(1, abs(a))))
    phi = np.degrees(ph) % 360
    return round(float(theta), 1), round(float(phi), 1)

S = np.array([[1, 0], [0, 1j]])
zero = np.array([1, 0])
print('H|0>    :', bloch(H @ zero))
print('S H|0>  :', bloch(S @ H @ zero))
print('Ry(60)  :', bloch(Ry(np.radians(60)) @ zero))
print('0.6,0.8 :', bloch(np.array([0.6, 0.8])))