from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

plot_bloch_vector([0, 0, 1], title="Bloch Sphere")  # Z-axis
plt.show()

print(Aer.backends())
