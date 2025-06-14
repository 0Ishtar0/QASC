from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate, IGate, MCXGate

q = QuantumRegister(5, 'q')
qc = QuantumCircuit(q)

r_1 = QuantumCircuit(1, name='R\\_y(-\\theta\\_1)').to_gate()
qc.append(r_1, [q[4]])

r_2 = QuantumCircuit(1, name='R\\_y(-\\theta\\_2)').to_gate()
c_r_2 = r_2.control(1, ctrl_state='1')
qc.append(c_r_2, [q[4], q[3]])

qc.cx(q[0], q[2])
qc.cx(q[0], q[1])

qc.append(MCXGate(2, ctrl_state="11"), [q[4], q[3], q[0]])

qc.draw('latex_source', filename='example.tex')
