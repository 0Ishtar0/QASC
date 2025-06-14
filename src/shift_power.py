from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import matplotlib.pyplot as plt

q = QuantumRegister(6, "wq")
qc = QuantumCircuit(q)

l3 = QuantumCircuit(3, name='L3').to_gate()
c_l3 = l3.control(1, ctrl_state='1')
qc.append(c_l3, [q[5], q[0], q[1], q[2]])
l2 = QuantumCircuit(2, name='L2').to_gate()
c_l2 = l2.control(1, ctrl_state='1')
qc.append(c_l2, [q[4], q[0], q[1]])
qc.cx(q[3], q[0])

qc.draw('latex_source', filename='example.tex')
# qc.draw('mpl')
# plt.show()