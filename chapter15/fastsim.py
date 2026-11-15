"""Chapter 13 - a tiny QAOA simulator with NumPy only.
It works because the cost layer is diagonal: string x just
gets the phase exp(-i*gamma*f(x)). E[k] = f(book string k)."""
import numpy as np

def mixer(psi, beta, n):
    """exp(-i*beta*X) on each of the n qubits."""
    c, s = np.cos(beta), -1j * np.sin(beta)
    t = psi.reshape([2] * n)            # axis a = qubit q_a
    for a in range(n):
        t0, t1 = np.take(t, 0, axis=a), np.take(t, 1, axis=a)
        t = np.stack([c * t0 + s * t1, s * t0 + c * t1], axis=a)
    return t.reshape(-1)

def qaoa_probs(E, gammas, betas):
    """Probabilities of all strings (index = book string)."""
    n = int(np.log2(len(E)))
    psi = np.ones(2 ** n, dtype=complex) / np.sqrt(2 ** n)
    for g, b in zip(gammas, betas):
        psi = mixer(psi * np.exp(-1j * g * E), b, n)
    return np.abs(psi) ** 2
