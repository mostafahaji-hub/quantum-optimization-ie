import sys
import numpy, scipy, matplotlib
import qiskit, qiskit_aer, qiskit_ibm_runtime

print("python            ", sys.version.split()[0])
print("numpy             ", numpy.__version__)
print("scipy             ", scipy.__version__)
print("matplotlib        ", matplotlib.__version__)
print("qiskit            ", qiskit.__version__)
print("qiskit-aer        ", qiskit_aer.__version__)
print("qiskit-ibm-runtime", qiskit_ibm_runtime.__version__)
