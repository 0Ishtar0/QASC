from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import RYGate
from numpy import arccos, allclose
import numpy as np
import matplotlib.pyplot as plt


def realsym2(alpha1, alpha2, shots=1024, draw=False):
    assert abs(alpha1) <= 1, "alpha1 must be in [-1, 1]"
    assert abs(alpha2) <= 1, "alpha2 must be in [-1, 1]"

    # === 目标矩阵 A ===
    A = np.array([[alpha1, alpha2],
                  [alpha2, alpha1]])
    print("Matrix A:")
    print(A)

    # === 角度计算 ===
    phi1 = arccos(alpha1) + arccos(alpha2)
    phi2 = arccos(alpha1) - arccos(alpha2)

    # 电路说明：
    # 量子比特：q0: ancilla 控制 (diffusion)，q1: encoding 控制，q2: data qubit
    qc = QuantumCircuit(3, 1)  # 用一个经典位测量 ancilla qubit

    # === D (Diffusion) 电路 ===
    qc.h(0)

    # === OA 电路 ===
    qc.ry(phi1, 0)
    qc.cx(1, 0)
    qc.ry(phi2, 0)
    qc.cx(1, 0)

    # === OC 电路 ===
    qc.cx(0, 1)

    # === 再来一次 D 电路 ===
    qc.h(0)

    # === 测量 ancilla 是否为 0（成功提取 block-encoding 的分量） ===
    qc.measure(0, 0)

    if draw:
        qc.draw('latex_source', filename='realsym2.tex')

    # === 执行模拟器，检查“成功率” ===
    backend = Aer.get_backend("qasm_simulator")
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=shots)
    counts = job.result().get_counts()

    # === 输出测量结果 ===
    print("Measurement result (on ancilla qubit):")
    print(counts)

    # 可视化
    if draw:
        from qiskit.visualization import plot_histogram
        plot_histogram(counts)
        plt.show()

    return qc, A, phi1, phi2, counts


if __name__ == "__main__":
    qc, A, phi1, phi2, counts = realsym2(0.6, 0.8, draw=True)
