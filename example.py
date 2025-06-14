import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

if __name__ == "__main__":
    qc = QuantumCircuit(3,1)
    qc.swap(0,1)
    qc.draw('latex_source', filename='example.tex')

