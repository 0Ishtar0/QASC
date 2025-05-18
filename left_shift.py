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


if __name__ == "__main__":
    n = 5
    qc = leftshift(n + 2, list(range(2, n + 1)), controls=[1])
    qc.draw("mpl")
    plt.show()
