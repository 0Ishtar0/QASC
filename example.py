import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

if __name__ == "__main__":
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    qc.draw('latex_source', filename='example.tex')
