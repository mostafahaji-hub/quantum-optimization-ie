from sim import *
def Hn(n):
    """H on every one of n qubits."""
    M = H
    for _ in range(n - 1):
        M = np.kron(M, H)
    return M
def phase_oracle(f, n):
    """Diagonal matrix with (-1)^f(x) for every bit string x."""
    return np.diag([(-1)**f(format(i, f'0{n}b')) for i in range(2**n)])
def diffusion(n):
    """Reflection about the uniform superposition: 2|s><s| - I."""
    N = 2**n
    s = np.ones(N) / np.sqrt(N)
    return 2 * np.outer(s, s) - np.eye(N)
def grover(marked, n, k):
    """k Grover iterations; marked(x) is True for good strings."""
    O = phase_oracle(lambda x: int(marked(x)), n)
    psi = Hn(n) @ np.eye(2**n)[0]
    for _ in range(k):
        psi = diffusion(n) @ (O @ psi)
    return psi