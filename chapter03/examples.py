"""Chapter 3 - NumPy versions of the worked examples (Examples 3.1 to 3.18)."""
import numpy as np
np.set_printoptions(precision=4, suppress=True)
# Example 3.1
z1, z2 = 3 + 4j, 1 - 2j
print("3.1", z1 + z2, z1 - z2, z1 * z2, np.conj(z1), abs(z1), abs(z1)**2)
# Example 3.2
psi = np.array([0.6, 0.8j]); print("3.2", np.abs(psi)**2, (np.abs(psi)**2).sum())
# Example 3.3
for z in [1 + 1j, -1 + np.sqrt(3)*1j]: print("3.3", abs(z), np.degrees(np.angle(z)))
# Example 3.4
print("3.4", 1j*(2 + 1j), np.degrees(np.angle(1j)), np.exp(1j*np.pi))
# Example 3.5
print("3.5", np.abs(1j*psi)**2)
# Example 3.6
for v in [np.array([1, 1j]), np.array([3, 4j])]:
    n = v/np.linalg.norm(v); print("3.6", n, np.abs(n)**2)
# Example 3.7
plus, minus = np.array([1, 1])/np.sqrt(2), np.array([1, -1])/np.sqrt(2)
psi1 = np.array([0.6, 0.8])
print("3.7", np.vdot(plus, minus), abs(np.vdot(plus, psi1))**2, abs(np.vdot(minus, psi1))**2)
# Example 3.8
psi2 = np.array([0.6, 0.8j]); print("3.8", abs(np.vdot(plus, psi2))**2)
X = np.array([[0, 1], [1, 0]]); Z = np.array([[1, 0], [0, -1]]); H = np.array([[1, 1], [1, -1]])/np.sqrt(2)
k0, k1 = np.array([1, 0]), np.array([0, 1])
# Example 3.9
a = H @ k0; b = Z @ a; c = H @ b
print("3.9", np.abs(a)**2, np.abs(b)**2, np.abs(c)**2)
# Example 3.10
def Ry(t): return np.array([[np.cos(t/2), -np.sin(t/2)], [np.sin(t/2), np.cos(t/2)]])
print("3.10", Ry(np.pi/3) @ k0, (Ry(np.pi/3) @ k0)**2)
# Example 3.11
print("3.11", X @ k0, X @ k1, H @ k0, H @ k1, H @ H @ k0)
# Example 3.12
print("3.12", X @ Z, Z @ X, np.allclose(Z @ X, -X @ Z))
# Example 3.13
A = np.array([[1, 1], [0, 1]]); v = A @ plus
print("3.13", np.allclose(H.conj().T @ H, np.eye(2)), v, np.linalg.norm(v))
# Example 3.14
print("3.14", np.kron(psi1, psi1), np.kron(k0, k1), np.kron(k1, k0))
# Example 3.15
print("3.15", np.kron(H, H) @ np.kron(k0, k0))
# Example 3.16
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
print("3.16", CNOT @ np.kron(H, np.eye(2)) @ np.kron(k0, k0))
# Example 3.17
f = np.array([12, 9, 13, 11, 8, 5]); P = np.array([0.05, 0.10, 0.05, 0.10, 0.20, 0.50])
print("3.17", P @ f, f.mean(), np.ceil(np.log(0.01)/np.log(1 - 0.5)))
# Example 3.18
p = 487/1000; se = np.sqrt(p*(1 - p)/1000); print("3.18", p, se, p - 1.96*se, p + 1.96*se)
