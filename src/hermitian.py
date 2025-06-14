from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import matplotlib.pyplot as plt

# 创建量子寄存器
q = QuantumRegister(4, 'q')
c = ClassicalRegister(3, 'c')  # 控制寄存器
qc = QuantumCircuit(q, c)

d_s = QuantumCircuit(1, name='D\\_s').to_gate()
qc.append(d_s, [q[2]])
o_a = QuantumCircuit(3, name='O\\_A').to_gate()
qc.append(o_a, [q[1], q[2], q[3]])
o_c = QuantumCircuit(2, name='O\\_C').to_gate()
qc.append(o_c, [q[2], q[3]])
qc.swap(0, 1)
swap = QuantumCircuit(2, name='SWAP').to_gate()
qc.append(swap, [q[2], q[3]])
qc.append(o_c, [q[2], q[3]])
qc.append(o_a, [q[1], q[2], q[3]])
qc.append(d_s, [q[2]])
qc.measure([0, 1, 2], [0, 1, 2])

qc.draw('latex_source', filename='example.tex')
plt.show()
