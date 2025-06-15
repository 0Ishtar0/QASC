import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from typing import List


def leftshift(n: int,
              targets: List[int] = None,
              controls: List[int] = None,
              control_states: List[int] = None) -> QuantumCircuit:
    """
    Constructs a left shift quantum circuit on target qubits, optionally controlled.

    Args:
        n (int): Total number of qubits.
        targets (list[int], optional): Qubit indices to shift. Defaults to all [0..n-1].
        controls (list[int], optional): Control qubit indices. Defaults to [].
        control_states (list[int], optional): Control states (0 or 1). Defaults to [1]*len(controls).

    Returns:
        QuantumCircuit: The constructed circuit.
    """
    if targets is None:
        targets = list(range(n))
    if controls is None:
        controls = []
    if control_states is None:
        control_states = [1] * len(controls)

    assert n > 0
    assert all(0 <= t < n for t in targets), "Invalid target indices!"
    assert all(0 <= c < n for c in controls), "Invalid control indices!"
    assert set(targets).isdisjoint(controls), "Targets and controls must be disjoint."
    assert len(controls) == len(control_states), "Control states mismatch"

    qc = QuantumCircuit(n)

    # Core loop: shift "left" via multi-controlled X gates
    for i in range(1, len(targets)):
        curr_controls = controls + targets[i:]
        curr_ctrl_state = ''.join([str(b) for b in control_states + [1] * (len(targets) - i)])
        target_qubit = targets[i - 1]

        # Controlled X
        if len(curr_controls) == 0:
            qc.x(target_qubit)
        elif len(curr_controls) == 1:
            if curr_ctrl_state == '1':
                qc.cx(curr_controls[0], target_qubit)
            else:
                qc.x(curr_controls[0])
                qc.cx(curr_controls[0], target_qubit)
                qc.x(curr_controls[0])
        else:
            gate = MCXGate(len(curr_controls), ctrl_state=curr_ctrl_state)
            qc.append(gate, curr_controls + [target_qubit])

    # X on last target if no controls
    if len(controls) == 0:
        qc.x(targets[-1])
    else:
        gate = MCXGate(len(controls), ctrl_state=''.join(str(b) for b in control_states))
        qc.append(gate, controls + [targets[-1]])

    return qc


def rightshift(n, targets=None, controls=None, control_states=None):
    """
    Constructs an n-qubit quantum circuit that performs a right-shift
    on the specified target qubits, optionally controlled by control qubits.

    Parameters:
        n (int): total number of qubits
        targets (list): indices of target qubits to shift (default: 0 to n-1)
        controls (list): indices of control qubits (default: empty list)
        control_states (list): acceptable control states (default: all 1s)

    Returns:
        QuantumCircuit: the constructed right shift circuit
    """
    # Default arguments
    if targets is None:
        targets = list(range(n))
    if controls is None:
        controls = []
    if control_states is None:
        control_states = [1] * len(controls)

    # --- Input validation ---
    assert n > 0
    assert all(0 <= t < n for t in targets), "Invalid target qubit index"
    assert all(0 <= c < n for c in controls), "Invalid control qubit index"
    assert set(targets).isdisjoint(set(controls)), "Targets and controls must be disjoint"
    assert len(controls) == len(control_states), "Mismatch in controls and controlStates lengths"

    # --- Build Circuit ---
    qc = QuantumCircuit(n)

    for i in range(1, len(targets)):
        # current control qubits and state
        ctrl = controls + targets[i:]
        ctrlStates = [0] * (len(targets) - i) + control_states
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
        ctrl_state_str = ''.join(str(b) for b in control_states)
        final_gate = MCXGate(len(controls), ctrl_state=ctrl_state_str)
        qc.append(final_gate, controls + [targets[-1]])

    return qc


if __name__ == "__main__":
    n = 5
    qc = leftshift(n, list(range(n)))
    qc.draw("mpl")
    plt.show()
