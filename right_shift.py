from matplotlib import pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from typing import List

from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate


def rightshift(n, targets=None, controls=None, controlStates=None):
    """
    Constructs an n-qubit quantum circuit that performs a right-shift
    on the specified target qubits, optionally controlled by control qubits.

    Parameters:
        n (int): total number of qubits
        targets (list): indices of target qubits to shift (default: 0 to n-1)
        controls (list): indices of control qubits (default: empty list)
        controlStates (list): acceptable control states (default: all 1s)

    Returns:
        QuantumCircuit: the constructed right shift circuit
    """
    # Default arguments
    if targets is None:
        targets = list(range(n))
    if controls is None:
        controls = []
    if controlStates is None:
        controlStates = [1] * len(controls)

    # --- Input validation ---
    assert n > 0
    assert all(0 <= t < n for t in targets), "Invalid target qubit index"
    assert all(0 <= c < n for c in controls), "Invalid control qubit index"
    assert set(targets).isdisjoint(set(controls)), "Targets and controls must be disjoint"
    assert len(controls) == len(controlStates), "Mismatch in controls and controlStates lengths"

    # --- Build Circuit ---
    qc = QuantumCircuit(n)

    for i in range(1, len(targets)):
        # current control qubits and state
        ctrl = controls + targets[i:]
        ctrlStates = controlStates + [0] * (len(targets) - i)
        ctrl_state_str = ''.join(str(b) for b in ctrlStates)
        target = targets[i - 1]

        if len(ctrl) == 0:
            qc.x(target)
        elif len(ctrl) == 1:
            if ctrl_state_str == '0':
                qc.cx(ctrl[0], target, ctrl_state=ctrl_state_str)
            else:  # ctrl_state == '1'
                qc.x(ctrl[0])
                qc.cx(ctrl[0], target, ctrl_state=ctrl_state_str)
                qc.x(ctrl[0])
        else:
            gate = MCXGate(len(ctrl), ctrl_state=ctrl_state_str)
            qc.append(gate, ctrl + [target])

    # Final controlled X (edge case)
    if len(controls) == 0:
        qc.x(targets[-1])
    else:
        ctrl_state_str = ''.join(str(b) for b in controlStates)
        final_gate = MCXGate(len(controls), ctrl_state=ctrl_state_str)
        qc.append(final_gate, controls + [targets[-1]])

    return qc


if __name__ == "__main__":
    n = 5
    targets = []
    controls = []
    control_states = []

    qc = rightshift(n)
    qc.draw("mpl")
    plt.show()
