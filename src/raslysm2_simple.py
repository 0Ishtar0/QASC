from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import RYGate
from numpy import arccos, allclose
import numpy as np
import matplotlib.pyplot as plt


def realsym2_simple(alpha1, alpha2, shots=10000, draw=False):
    assert abs(alpha1) <= 1, "alpha1 must be in [-1, 1]"
    assert abs(alpha2) <= 1, "alpha2 must be in [-1, 1]"

    # 目标矩阵 A
    A = np.array([[alpha1, alpha2],
                  [alpha2, alpha1]])
    print("Matrix A:")
    print(A)

    phi1 = arccos(alpha1) + arccos(alpha2)
    phi2 = arccos(alpha1) - arccos(alpha2)

    qc = QuantumCircuit(3, 2)
    qc.h(1)
    qc.ry(phi1, 2)
    qc.cx(1, 2)
    qc.ry(phi2, 2)
    qc.cx(1, 2)
    qc.cx(1, 0)
    qc.h(1)

    backend = Aer.get_backend('unitary_simulator')
    transpiled = transpile(qc, backend)
    job = backend.run(transpiled)
    result = job.result()
    U = result.get_unitary(qc)

    return qc, A, U


if __name__ == "__main__":
    qc, A, U = realsym2_simple(0.6, 0.8, draw=True)
    print(f"Matrix U: {U}")
    U_compact = 2 * np.asarray(U)[:2, :2]
    print(f"Matrix U_compact: {U_compact}")
