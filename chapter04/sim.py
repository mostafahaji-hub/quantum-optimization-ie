import numpy as np
I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

def op(gate, k, n):
    """Gate on qubit k of n qubits (q0 = leftmost)."""
    mats = [gate if i == k else I for i in range(n)]
    M = mats[0]
    for m in mats[1:]:
        M = np.kron(M, m)
    return M

def cnot(c, t, n):
    """CNOT with control c and target t on n qubits."""
    N = 2**n
    M = np.zeros((N, N))
    for i in range(N):
        bits = list(format(i, f'0{n}b'))
        if bits[c] == '1':
            bits[t] = '0' if bits[t] == '1' else '1'
        M[int(''.join(bits), 2), i] = 1
    return M

def probs(psi):
    n = int(np.log2(len(psi)))
    return {format(i, f'0{n}b'): round(float(abs(a)**2), 4)
            for i, a in enumerate(psi) if abs(a) > 1e-9}

def Ry(theta):
    c, s = np.cos(theta/2), np.sin(theta/2)
    return np.array([[c, -s], [s, c]])

def sample(psi, shots, seed=1):
    n = int(np.log2(len(psi)))
    p = np.abs(psi)**2
    rng = np.random.default_rng(seed)
    out = rng.choice(len(psi), size=shots, p=p/p.sum())
    keys, cnt = np.unique(out, return_counts=True)
    return {format(k, f'0{n}b'): int(c) for k, c in zip(keys, cnt)}