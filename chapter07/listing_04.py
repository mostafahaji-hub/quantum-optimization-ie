# Chapter 7, code listing 4 (in order of appearance)
import numpy as np
from qea import observe, rotate
from keys import decode_keys
from prob20 import n, twt, order_from_real
K = 5                                         # Q-bits per job
def f_bits(x): return twt(decode_keys(x, n, K)[1])