from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def get_gate(mane: str, num_qbits: int, num_ctrls: int = 0, ctrls: str = None):
    qc = QuantumCircuit(num_qbits, name=mane).to_gate()
    if ctrls is not None:
        qc = qc.control(num_ctrls, ctrl_state=ctrls)
    return qc


q = QuantumRegister(6, 'q')
c = ClassicalRegister(3, 'c')
qc = QuantumCircuit(q, c)

qc.append(get_gate('K', 3), [q[0], q[1], q[2]])
qc.append(get_gate('L', 3, 1, "1"), [q[5], q[0], q[1], q[2]])
qc.append(get_gate('L', 2, 1, "1"), [q[4], q[0], q[1]])
qc.cx(q[3], q[0])
qc.swap(q[2], q[5])
qc.swap(q[1], q[4])
qc.swap(q[0], q[3])
qc.cx(q[3], q[0])
qc.append(get_gate('R', 2, 1, "1"), [q[4], q[0], q[1]])
qc.append(get_gate('R', 3, 1, "1"), [q[5], q[0], q[1], q[2]])
qc.append(get_gate('K\^\\dagger', 3), [q[0], q[1], q[2]])
qc.measure(q[0], c[0])
qc.measure(q[1], c[1])
qc.measure(q[2], c[2])

qc.draw('latex_source', filename='example.tex')
