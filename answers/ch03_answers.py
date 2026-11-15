"""Numeric checks for the answers of Chapter 3."""
import numpy as np
np.set_printoptions(precision=4, suppress=True)
z1, z2 = 2 - 1j, -1 + 3j
print('3.1', z1 + z2, z1 * z2, np.conj(z2), abs(z2)**2, z1 / z2)
print('3.2', [1j**k for k in range(2, 6)], 1j**100)
for z in (-2, 3j, 1 - 1j, -np.sqrt(3) - 1j):
    print('3.3', z, round(abs(z), 4), round(np.degrees(np.angle(z)), 2))
print('3.4', (1 + 1j)**8, np.exp(1j*np.pi/4)**2)
for v in (np.array([1, 2]), np.array([1 + 1j, 1 - 1j]), np.array([2j, -1])):
    n = v / np.linalg.norm(v); print('3.5', n, np.abs(n)**2)
plus, minus = np.array([1, 1])/np.sqrt(2), np.array([1, -1])/np.sqrt(2)
for psi in (np.array([1, 0]), np.array([0, 1]), np.array([1, 1j])/np.sqrt(2)):
    print('3.7', abs(np.vdot(plus, psi))**2, abs(np.vdot(minus, psi))**2)
X = np.array([[0, 1], [1, 0]]); Z = np.diag([1, -1]); H = np.array([[1, 1], [1, -1]])/np.sqrt(2)
print('3.8', Z @ plus, H @ Z @ H)
Y = np.array([[0, -1j], [1j, 0]]); S = np.diag([1, 1j]); A = np.ones((2, 2))/2
t = 0.3; Rt = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
for name, U in (('Y', Y), ('S', S), ('A', A), ('R', Rt)):
    print('3.9', name, np.allclose(U.conj().T @ U, np.eye(2)))
k0, k1 = np.array([1, 0]), np.array([0, 1])
print('3.10', np.kron(plus, k0), np.kron(k0, plus), np.kron(np.kron(k1, k1), k0))
I = np.eye(2); s01 = np.kron(k0, k1)
print('3.11', np.kron(X, I) @ s01, np.kron(I, X) @ s01)
psi3 = np.kron(np.kron(H, H), H) @ np.eye(8)[0]; print('3.12', psi3, 1/512)
P = [0.6, 0.1, 0.3]; L = [26, 31, 27]
print('3.13', np.dot(P, L), np.mean(L), int(np.ceil(np.log(0.01)/np.log(0.4))))
print('3.14', 0.2*0.8/0.01**2, 4*0.2*0.8/0.01**2)
for p1 in (0.1, 0.5, 0.9): print('3.16', p1, round(np.degrees(2*np.arcsin(np.sqrt(p1))), 2))
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
for s in (np.kron(k0, k1), np.kron(k1, k0)):
    print('3.17', CNOT @ np.kron(H, I) @ s)
phi = np.array([1, 1j])/np.sqrt(2); Sd = np.diag([1, -1j])
print('3.18', np.abs(phi)**2, np.abs(H @ phi)**2, np.abs(H @ Sd @ phi)**2)
rng = np.random.default_rng(1)
psi = np.kron(H, H) @ np.eye(4)[0]
counts = np.bincount(rng.choice(4, size=1000, p=np.abs(psi)**2), minlength=4)
print('3.15', [np.allclose(U.conj().T @ U, I) for U in (X, Z, H)], psi, counts)
print('3.19 wrong *:', H * np.array([1, 0]))
