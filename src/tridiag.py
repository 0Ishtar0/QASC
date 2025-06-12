import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import RYGate
from qiskit_aer import Aer

from left_shift import leftshift
from right_shift import rightshift


def multi_controlled_ry(theta, control_qubits, target_qubit, control_state):
    """
    Returns a MC-RY gate with specific control state using ancillas if needed
    """
    qc = QuantumCircuit(max(max(control_qubits), target_qubit) + 1)

    # 控制比特倒置以匹配 control_state
    for cbit, state in zip(control_qubits, control_state):
        if state == 0:
            qc.x(cbit)

    ry_gate = RYGate(theta)
    qc.append(ry_gate.control(len(control_qubits)), control_qubits + [target_qubit])

    # 恢复原控制比特状态
    for cbit, state in zip(control_qubits, control_state):
        if state == 0:
            qc.x(cbit)

    return qc.to_gate(label=f'mcry({theta:.2f})')


def tridiag(n, alpha, beta, gamma):
    """
    Constructs a block-encoding circuit of a circulant tridiagonal matrix.
    Returns the full circuit and subcircuits: OA, OC, D.
    """
    assert 0 <= alpha <= 2, "Alpha must be in [0, 2]"
    assert abs(beta) <= 1, "Beta must be in [-1, 1]"
    assert abs(gamma) <= 1, "Gamma must be in [-1, 1]"

    total_qubits = n + 3

    # -------------------- Diffusion Circuit D --------------------
    D = QuantumCircuit(total_qubits, name="D")
    D.h(n + 1)
    D.h(n)

    # -------------------- OA Circuit --------------------
    OA = QuantumCircuit(total_qubits, name="OA")

    theta0 = 2 * np.arccos(alpha - 1)
    theta1 = 2 * np.arccos(beta)
    theta2 = 2 * np.arccos(gamma)

    # 模拟 MCRotationY(control_qubits, target, control_state, angle)
    OA.append(multi_controlled_ry(theta0, [1, 2], 0, [0, 0]), [n + 2, n + 1, n])
    OA.append(multi_controlled_ry(theta1, [1, 2], 0, [0, 1]), [n + 2, n + 1, n])
    OA.append(multi_controlled_ry(theta2, [1, 2], 0, [1, 0]), [n + 2, n + 1, n])

    # 多控制 RY，控制条件是 [0, 1,...,n+1]
    ctrl_condition1 = [0] + [1] * (n + 1)  # [0, 1, 1, ..., 1]
    ctrl_condition2 = [1] + [0] * (n + 1)  # [1, 0, 0, ..., 0]
    ctrl_qubits_full = list(range(1, n + 3))

    lst = list(range(total_qubits))
    lst.reverse()
    OA.append(multi_controlled_ry(np.pi - theta1, ctrl_qubits_full, 0, ctrl_condition1),
              lst)
    OA.append(multi_controlled_ry(np.pi - theta2, ctrl_qubits_full, 0, ctrl_condition2),
              lst)

    # -------------------- OC Circuit --------------------
    OC = QuantumCircuit(n + 2, name="OC")

    OC.append(leftshift(n + 2, list(range(n)), controls=[n]).to_gate(label='L'), list(range(n + 2)))
    OC.append(rightshift(n + 2, list(range(n)), controls=[n + 1]).to_gate(label='R'), list(range(n + 2)))

    # -------------------- Total Circuit --------------------
    circuit = QuantumCircuit(total_qubits, name="MainCircuit")
    circuit.compose(D, inplace=True)
    circuit.compose(OA, inplace=True)
    circuit.compose(OC, qubits=range(1, n + 3), inplace=True)
    circuit.compose(D, inplace=True)

    return circuit, OA, OC, D


if __name__ == "__main__":
    circuit, OA, OC, D = tridiag(n=3, alpha=1, beta=0.4, gamma=0.6)

    # Draw the circuit
    circuit.draw('mpl')
    plt.show()

    backend = Aer.get_backend('unitary_simulator')
    transpiled = transpile(circuit, backend)
    job = backend.run(transpiled)
    result = job.result()
    U = result.get_unitary(circuit)
    np.set_printoptions(threshold=np.inf)
    print(4 * U)
    indices = [i << 3 for i in range(8)]

    A_sub = U[np.ix_(indices, indices)]
    print(A_sub)
