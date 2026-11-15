# Chapter 5, code listing 12 (in order of appearance)
import numpy as np
from math import gcd
N, a = 15, 7
seq = [pow(a, x, N) for x in range(16)]
print('7^x mod 15 :', seq)
# Fourier transform of the sequence (what the QFT does, in spirit)
spec = np.abs(np.fft.fft(np.array(seq) - np.mean(seq)))
peaks = [k for k in range(16) if spec[k] > 1e-6]
print('frequency peaks at k =', peaks)
r = 16 // peaks[0]                 # spacing of peaks -> period
print('period r =', r)
print('factors  :', gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N))