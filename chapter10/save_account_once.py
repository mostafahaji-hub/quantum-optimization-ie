"""Run ONCE on your own (trusted) computer, then delete the key."""
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    token="<paste-your-44-character-API-key>",
    instance="<optional: Open Plan instance name or CRN>",
    set_as_default=True,
    overwrite=True,
)
print('Saved. Test: QiskitRuntimeService().backends()')
